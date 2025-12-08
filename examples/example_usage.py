#!/usr/bin/env python3
"""
Exemplo de Uso do Sistema de Detecção de Garimpo

Este script demonstra como usar os principais módulos do sistema.
"""

import sys
from pathlib import Path
import numpy as np

# Adiciona src ao path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from utils.config_loader import ConfigLoader
from classification.hybrid_classifier import HybridClassifier, SpectralIndices
from detection.mining_scar_detector import MiningScarDetector
from monitoring.change_detection import ChangeDetector
from visualization.visualizer import ResultsVisualizer


def example_spectral_indices():
    """Exemplo de cálculo de índices espectrais"""
    print("=" * 60)
    print("Exemplo 1: Cálculo de Índices Espectrais")
    print("=" * 60)
    
    # Cria dados sintéticos para demonstração
    red_band = np.random.rand(100, 100) * 0.3  # Baixa reflectância
    nir_band = np.random.rand(100, 100) * 0.7  # Alta reflectância (vegetação)
    green_band = np.random.rand(100, 100) * 0.4
    swir_band = np.random.rand(100, 100) * 0.5
    blue_band = np.random.rand(100, 100) * 0.3
    
    # Calcula índices
    indices = SpectralIndices()
    
    ndvi = indices.calculate_ndvi(nir_band, red_band)
    ndwi = indices.calculate_ndwi(green_band, nir_band)
    ndmi = indices.calculate_ndmi(nir_band, swir_band)
    bsi = indices.calculate_bsi(blue_band, red_band, nir_band, swir_band)
    
    print(f"\nNDVI (Vegetação):")
    print(f"  Mínimo: {np.min(ndvi):.3f}")
    print(f"  Máximo: {np.max(ndvi):.3f}")
    print(f"  Média: {np.mean(ndvi):.3f}")
    
    print(f"\nNDWI (Água):")
    print(f"  Mínimo: {np.min(ndwi):.3f}")
    print(f"  Máximo: {np.max(ndwi):.3f}")
    print(f"  Média: {np.mean(ndwi):.3f}")
    
    print(f"\nNDMI (Mineração):")
    print(f"  Mínimo: {np.min(ndmi):.3f}")
    print(f"  Máximo: {np.max(ndmi):.3f}")
    print(f"  Média: {np.mean(ndmi):.3f}")
    
    print(f"\nBSI (Solo Exposto):")
    print(f"  Mínimo: {np.min(bsi):.3f}")
    print(f"  Máximo: {np.max(bsi):.3f}")
    print(f"  Média: {np.mean(bsi):.3f}")


def example_classification():
    """Exemplo de classificação híbrida"""
    print("\n" + "=" * 60)
    print("Exemplo 2: Classificação Híbrida")
    print("=" * 60)
    
    # Carrega configuração
    config_loader = ConfigLoader()
    config = config_loader.config
    
    # Inicializa classificador
    classifier = HybridClassifier(config)
    
    # Cria dados sintéticos para demonstração
    # Simula imagem com 5 bandas, 200x200 pixels
    image_data = np.random.rand(5, 200, 200).astype(np.float32)
    
    # Cria dados de treinamento sintéticos
    n_samples = 1000
    n_features = 9  # 5 bandas + 4 índices
    X_train = np.random.rand(n_samples, n_features)
    y_train = np.random.randint(0, 5, n_samples)  # 5 classes
    
    print("\nTreinando modelos...")
    classifier.train_hybrid_model(X_train, y_train)
    
    print("\nExtraindo features da imagem...")
    band_mapping = {
        'blue': 0, 'green': 1, 'red': 2, 'nir': 3, 'swir': 4
    }
    features = classifier.extract_features(image_data, band_mapping)
    
    print(f"Features extraídas: {features.shape}")
    
    print("\nFazendo predição ensemble...")
    classification = classifier.ensemble_prediction(features)
    classification = classification.reshape(200, 200)
    
    print(f"Classificação gerada: {classification.shape}")
    print(f"Classes encontradas: {np.unique(classification)}")


def example_detection():
    """Exemplo de detecção de cicatrizes"""
    print("\n" + "=" * 60)
    print("Exemplo 3: Detecção de Cicatrizes de Garimpo")
    print("=" * 60)
    
    # Carrega configuração
    config_loader = ConfigLoader()
    config = config_loader.config
    
    # Inicializa detector
    detector = MiningScarDetector(config)
    
    # Cria mapa de classificação sintético
    classification_map = np.zeros((300, 300), dtype=int)
    
    # Adiciona algumas áreas de garimpo sintéticas
    classification_map[50:80, 50:90] = 0  # Garimpo ativo
    classification_map[120:150, 120:180] = 1  # Garimpo abandonado
    classification_map[200:240, 200:250] = 0  # Garimpo ativo
    
    print("\nDetectando cicatrizes...")
    binary_mask, mining_objects = detector.detect_mining_scars(
        classification_map,
        mining_classes=[0, 1]
    )
    
    print(f"\nTotal de objetos detectados: {len(mining_objects)}")
    
    # Filtra por morfologia
    filtered_objects = detector.filter_by_morphology(mining_objects)
    print(f"Objetos após filtro morfológico: {len(filtered_objects)}")
    
    # Segmenta ativos vs abandonados
    segmented_objects = detector.segment_active_vs_abandoned(filtered_objects)
    
    # Gera relatório
    report = detector.generate_detection_report(segmented_objects)
    
    print(f"\n--- RELATÓRIO DE DETECÇÃO ---")
    print(f"Total de objetos: {report['total_objects']}")
    print(f"Área total: {report['total_area_hectares']:.2f} hectares")
    print(f"Garimpos ativos: {report['active_count']}")
    print(f"Garimpos abandonados: {report['abandoned_count']}")
    print(f"Área média: {report['average_area_m2']:.2f} m²")


def example_change_detection():
    """Exemplo de detecção de mudanças"""
    print("\n" + "=" * 60)
    print("Exemplo 4: Detecção de Mudanças Temporais")
    print("=" * 60)
    
    # Carrega configuração
    config_loader = ConfigLoader()
    config = config_loader.config
    
    # Inicializa detector de mudanças
    change_detector = ChangeDetector(config)
    
    # Cria classificações sintéticas para dois períodos
    baseline = np.zeros((200, 200), dtype=int)
    baseline[50:80, 50:80] = 0  # Garimpo na linha de base
    
    comparison = baseline.copy()
    comparison[80:110, 50:80] = 0  # Expansão
    comparison[50:80, 80:110] = 1  # Nova área
    comparison[120:150, 120:150] = 0  # Novo garimpo
    
    print("\nDetectando mudanças...")
    change_types, stats = change_detector.classify_change_types(
        baseline,
        comparison,
        mining_classes=[0, 1]
    )
    
    print(f"\n--- ESTATÍSTICAS DE MUDANÇA ---")
    print(f"Nova área: {stats['new_mining_area_hectares']:.2f} hectares")
    print(f"Expansão: {stats['expansion_area_hectares']:.2f} hectares")
    print(f"Retração: {stats['retraction_area_hectares']:.2f} hectares")
    print(f"Área estável: {stats['stable_mining_area_hectares']:.2f} hectares")
    print(f"Mudança líquida: {stats['net_change_hectares']:.2f} hectares")
    
    # Gera alerta se necessário
    alert = change_detector.generate_alert(stats)
    if alert:
        print(f"\n⚠ ALERTA GERADO!")
        print(f"Tipo: {alert['alert_type']}")
        print(f"Severidade: {alert['severity']}")
        print(f"Mensagem: {alert['message']}")
    else:
        print(f"\nNenhum alerta gerado (mudanças abaixo do threshold)")


def example_temporal_analysis():
    """Exemplo de análise temporal"""
    print("\n" + "=" * 60)
    print("Exemplo 5: Análise Temporal de Série")
    print("=" * 60)
    
    # Carrega configuração
    config_loader = ConfigLoader()
    config = config_loader.config
    
    # Inicializa detector de mudanças
    change_detector = ChangeDetector(config)
    
    # Cria série temporal sintética
    time_series = []
    dates = ['2020', '2021', '2022', '2023', '2024']
    
    for i, date in enumerate(dates):
        # Simula crescimento de garimpo ao longo do tempo
        classification = np.zeros((200, 200), dtype=int)
        size = 30 + i * 15  # Crescimento progressivo
        classification[50:50+size, 50:50+size] = 0  # Garimpo crescente
        time_series.append((date, classification))
    
    print("\nAnalisando série temporal...")
    temporal_stats = change_detector.temporal_analysis(
        time_series,
        mining_classes=[0, 1]
    )
    
    print(f"\n--- ANÁLISE TEMPORAL ---")
    for date, area, change in zip(
        temporal_stats['dates'],
        temporal_stats['total_mining_area_hectares'],
        temporal_stats['change_from_previous']
    ):
        print(f"{date}: {area:.2f} ha (mudança: {change['percent']:+.1f}%)")
    
    print(f"\nTendência geral: {temporal_stats.get('trend', 'N/A')}")


def main():
    """Executa todos os exemplos"""
    print("\n")
    print("╔" + "═" * 58 + "╗")
    print("║  EXEMPLOS DE USO - SISTEMA DE DETECÇÃO DE GARIMPO      ║")
    print("╚" + "═" * 58 + "╝")
    
    try:
        example_spectral_indices()
        example_classification()
        example_detection()
        example_change_detection()
        example_temporal_analysis()
        
        print("\n" + "=" * 60)
        print("Todos os exemplos executados com sucesso!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Erro ao executar exemplos: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
