#!/usr/bin/env python3
"""
Pipeline Principal de Processamento Híbrido de Imagens de Sensoriamento Remoto
para Mapeamento de Garimpo Ilegal na Terra Indígena Munduruku

Este script orquestra todo o processo de:
1. Aquisição de dados de satélite
2. Pré-processamento de imagens
3. Classificação híbrida (métodos tradicionais + ML)
4. Detecção de cicatrizes de garimpo
5. Monitoramento de mudanças temporais
6. Visualização e geração de relatórios
"""

import sys
import argparse
from pathlib import Path
import numpy as np
from typing import Optional

# Adiciona o diretório src ao path
sys.path.insert(0, str(Path(__file__).parent / "src"))

from utils.config_loader import ConfigLoader
from data_acquisition.satellite_data import SatelliteDataAcquisition
from preprocessing.image_preprocessing import ImagePreprocessor
from classification.hybrid_classifier import HybridClassifier
from detection.mining_scar_detector import MiningScarDetector
from monitoring.change_detection import ChangeDetector
from visualization.visualizer import ResultsVisualizer


class MiningDetectionPipeline:
    """Pipeline principal de detecção de garimpo"""
    
    def __init__(self, config_path: Optional[str] = None):
        """
        Inicializa o pipeline
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        print("=" * 80)
        print("PIPELINE DE DETECÇÃO DE GARIMPO ILEGAL")
        print("Terra Indígena Munduruku - Bacia do Rio Tapajós, Pará")
        print("=" * 80)
        print()
        
        # Carrega configuração
        self.config_loader = ConfigLoader(config_path)
        self.config = self.config_loader.config
        
        # Inicializa módulos
        print("Inicializando módulos...")
        self.data_acquisition = SatelliteDataAcquisition(self.config)
        self.preprocessor = ImagePreprocessor(self.config)
        self.classifier = HybridClassifier(self.config)
        self.detector = MiningScarDetector(self.config)
        self.change_detector = ChangeDetector(self.config)
        self.visualizer = ResultsVisualizer(self.config)
        
        print("✓ Pipeline inicializado com sucesso!\n")
    
    def run_classification_pipeline(
        self, 
        image_data: np.ndarray,
        dem: Optional[np.ndarray] = None,
        training_data: Optional[tuple] = None
    ) -> dict:
        """
        Executa pipeline de classificação
        
        Args:
            image_data: Dados da imagem
            dem: Modelo Digital de Elevação (opcional)
            training_data: Dados de treinamento (opcional)
            
        Returns:
            Dicionário com resultados
        """
        print("\n" + "=" * 80)
        print("FASE 1: PRÉ-PROCESSAMENTO")
        print("=" * 80)
        
        # Pré-processamento
        preprocessed_data = self.preprocessor.apply_full_preprocessing(
            image_data, 
            dem=dem
        )
        
        print("\n" + "=" * 80)
        print("FASE 2: CLASSIFICAÇÃO HÍBRIDA")
        print("=" * 80)
        
        # Mapeamento de bandas (exemplo para Sentinel-2)
        band_mapping = {
            'blue': 0,
            'green': 1,
            'red': 2,
            'nir': 3,
            'swir': 4 if preprocessed_data.shape[0] > 4 else 3
        }
        
        # Classificação
        classification = self.classifier.classify(
            preprocessed_data,
            training_data=training_data,
            band_mapping=band_mapping
        )
        
        results = {
            'preprocessed_data': preprocessed_data,
            'classification': classification,
            'band_mapping': band_mapping
        }
        
        return results
    
    def run_detection_pipeline(
        self, 
        classification: np.ndarray,
        mining_classes: Optional[list] = None
    ) -> dict:
        """
        Executa pipeline de detecção de cicatrizes
        
        Args:
            classification: Mapa de classificação
            mining_classes: Classes que representam garimpo
            
        Returns:
            Dicionário com resultados de detecção
        """
        print("\n" + "=" * 80)
        print("FASE 3: DETECÇÃO DE CICATRIZES DE GARIMPO")
        print("=" * 80)
        
        # Detecta cicatrizes
        binary_mask, mining_objects = self.detector.detect_mining_scars(
            classification, 
            mining_classes
        )
        
        # Filtra por morfologia
        filtered_objects = self.detector.filter_by_morphology(mining_objects)
        
        # Segmenta ativos vs abandonados
        segmented_objects = self.detector.segment_active_vs_abandoned(filtered_objects)
        
        # Gera relatório
        detection_report = self.detector.generate_detection_report(segmented_objects)
        
        print(f"\n✓ Detecção concluída!")
        print(f"  Total de objetos: {detection_report['total_objects']}")
        print(f"  Área total: {detection_report['total_area_hectares']:.2f} hectares")
        print(f"  Ativos: {detection_report['active_count']}")
        print(f"  Abandonados: {detection_report['abandoned_count']}")
        
        results = {
            'binary_mask': binary_mask,
            'mining_objects': segmented_objects,
            'detection_report': detection_report
        }
        
        return results
    
    def run_monitoring_pipeline(
        self, 
        baseline_classification: np.ndarray,
        comparison_classification: np.ndarray
    ) -> dict:
        """
        Executa pipeline de monitoramento de mudanças
        
        Args:
            baseline_classification: Classificação de linha de base
            comparison_classification: Classificação de comparação
            
        Returns:
            Dicionário com resultados de monitoramento
        """
        print("\n" + "=" * 80)
        print("FASE 4: MONITORAMENTO DE MUDANÇAS")
        print("=" * 80)
        
        # Detecta mudanças
        change_map = self.change_detector.detect_changes(
            baseline_classification,
            comparison_classification
        )
        
        # Classifica tipos de mudança
        change_types, change_stats = self.change_detector.classify_change_types(
            baseline_classification,
            comparison_classification
        )
        
        # Gera alertas
        alert = self.change_detector.generate_alert(change_stats)
        
        print(f"\n✓ Monitoramento concluído!")
        print(f"  Nova área: {change_stats['new_mining_area_hectares']:.2f} hectares")
        print(f"  Expansão: {change_stats['expansion_area_hectares']:.2f} hectares")
        print(f"  Retração: {change_stats['retraction_area_hectares']:.2f} hectares")
        print(f"  Mudança líquida: {change_stats['net_change_hectares']:.2f} hectares")
        
        if alert:
            print(f"\n⚠ ALERTA GERADO!")
            print(f"  Tipo: {alert['alert_type']}")
            print(f"  Severidade: {alert['severity']}")
            print(f"  Mensagem: {alert['message']}")
        
        results = {
            'change_map': change_map,
            'change_types': change_types,
            'change_stats': change_stats,
            'alert': alert
        }
        
        return results
    
    def run_visualization_pipeline(
        self, 
        classification: np.ndarray,
        detection_report: dict,
        change_results: Optional[dict] = None,
        output_dir: str = "results"
    ):
        """
        Executa pipeline de visualização
        
        Args:
            classification: Mapa de classificação
            detection_report: Relatório de detecção
            change_results: Resultados de mudanças (opcional)
            output_dir: Diretório de saída
        """
        print("\n" + "=" * 80)
        print("FASE 5: VISUALIZAÇÃO E RELATÓRIOS")
        print("=" * 80)
        
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        
        # Visualiza mapa de classificação
        print("\nGerando mapa de classificação...")
        self.visualizer.plot_classification_map(
            classification,
            title="Mapa de Classificação - Terra Indígena Munduruku",
            save_path=str(output_path / "classification_map.png")
        )
        
        # Gera dashboard de estatísticas
        print("Gerando dashboard de estatísticas...")
        change_stats = change_results.get('change_stats') if change_results else None
        self.visualizer.plot_statistics_dashboard(
            detection_report,
            change_stats=change_stats,
            save_path=str(output_path / "statistics_dashboard.png")
        )
        
        # Gera mapa de mudanças se disponível
        if change_results:
            print("Gerando mapa de mudanças...")
            self.visualizer.plot_change_map(
                change_results['change_types'],
                title="Mapa de Mudanças Temporais",
                save_path=str(output_path / "change_map.png")
            )
        
        # Gera relatório em texto
        print("Gerando relatório textual...")
        temporal_analysis = None  # Pode ser adicionado se disponível
        self.visualizer.generate_report(
            detection_report,
            temporal_analysis=temporal_analysis,
            change_stats=change_stats,
            output_dir=output_dir
        )
        
        print(f"\n✓ Visualização concluída! Resultados salvos em: {output_dir}")
    
    def run_full_pipeline(
        self, 
        image_data: np.ndarray,
        baseline_image: Optional[np.ndarray] = None,
        dem: Optional[np.ndarray] = None,
        training_data: Optional[tuple] = None,
        output_dir: str = "results"
    ) -> dict:
        """
        Executa pipeline completo
        
        Args:
            image_data: Dados da imagem atual
            baseline_image: Imagem de linha de base para monitoramento (opcional)
            dem: Modelo Digital de Elevação (opcional)
            training_data: Dados de treinamento (opcional)
            output_dir: Diretório de saída
            
        Returns:
            Dicionário com todos os resultados
        """
        print("\nIniciando pipeline completo...")
        
        # 1. Classificação
        classification_results = self.run_classification_pipeline(
            image_data, 
            dem=dem,
            training_data=training_data
        )
        
        # 2. Detecção
        detection_results = self.run_detection_pipeline(
            classification_results['classification']
        )
        
        # 3. Monitoramento (se imagem de linha de base estiver disponível)
        monitoring_results = None
        if baseline_image is not None:
            # Classifica imagem de linha de base
            baseline_classification = self.run_classification_pipeline(
                baseline_image,
                dem=dem,
                training_data=training_data
            )['classification']
            
            monitoring_results = self.run_monitoring_pipeline(
                baseline_classification,
                classification_results['classification']
            )
        
        # 4. Visualização
        self.run_visualization_pipeline(
            classification_results['classification'],
            detection_results['detection_report'],
            change_results=monitoring_results,
            output_dir=output_dir
        )
        
        print("\n" + "=" * 80)
        print("PIPELINE CONCLUÍDO COM SUCESSO!")
        print("=" * 80)
        
        # Retorna todos os resultados
        all_results = {
            'classification': classification_results,
            'detection': detection_results,
            'monitoring': monitoring_results,
            'output_dir': output_dir
        }
        
        return all_results


def main():
    """Função principal"""
    parser = argparse.ArgumentParser(
        description='Pipeline de Detecção de Garimpo Ilegal - Terra Indígena Munduruku'
    )
    
    parser.add_argument(
        '--config',
        type=str,
        default=None,
        help='Caminho para arquivo de configuração YAML'
    )
    
    parser.add_argument(
        '--image',
        type=str,
        help='Caminho para imagem de entrada'
    )
    
    parser.add_argument(
        '--baseline',
        type=str,
        default=None,
        help='Caminho para imagem de linha de base (opcional)'
    )
    
    parser.add_argument(
        '--output',
        type=str,
        default='results',
        help='Diretório de saída'
    )
    
    parser.add_argument(
        '--demo',
        action='store_true',
        help='Executa em modo demonstração com dados sintéticos'
    )
    
    args = parser.parse_args()
    
    # Inicializa pipeline
    pipeline = MiningDetectionPipeline(args.config)
    
    if args.demo:
        print("\n⚠ Modo demonstração: usando dados sintéticos")
        print("Para uso em produção, forneça imagens reais com --image\n")
        
        # Cria dados sintéticos para demonstração
        image_data = np.random.rand(5, 512, 512).astype(np.float32)
        baseline_image = np.random.rand(5, 512, 512).astype(np.float32)
        
        # Executa pipeline
        results = pipeline.run_full_pipeline(
            image_data,
            baseline_image=baseline_image,
            output_dir=args.output
        )
        
    elif args.image:
        # Carrega imagem real
        print(f"Carregando imagem: {args.image}")
        # Aqui seria implementada a leitura de imagem real
        # image_data, metadata = pipeline.data_acquisition.load_satellite_image(args.image)
        
        print("⚠ Implementação de leitura de imagem real pendente")
        print("Use --demo para executar com dados sintéticos")
        
    else:
        parser.print_help()
        print("\n⚠ Forneça uma imagem com --image ou use --demo para demonstração")


if __name__ == "__main__":
    main()
