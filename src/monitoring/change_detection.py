"""
Módulo de detecção de mudanças temporais
Monitora expansão/retração de áreas de garimpo
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from datetime import datetime
from scipy import ndimage


class ChangeDetector:
    """Classe para detecção de mudanças temporais"""
    
    def __init__(self, config: Dict):
        """
        Inicializa o detector de mudanças
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.monitoring_config = config.get('monitoring', {})
        self.change_detection_config = self.monitoring_config.get('change_detection', {})
    
    def detect_changes(
        self, 
        baseline_image: np.ndarray,
        comparison_image: np.ndarray,
        method: str = 'spectral_difference'
    ) -> np.ndarray:
        """
        Detecta mudanças entre duas imagens
        
        Args:
            baseline_image: Imagem de referência (linha de base)
            comparison_image: Imagem de comparação
            method: Método de detecção de mudanças
            
        Returns:
            Mapa de mudanças
        """
        if method == 'spectral_difference':
            change_map = self._spectral_difference(baseline_image, comparison_image)
        elif method == 'change_vector_analysis':
            change_map = self._change_vector_analysis(baseline_image, comparison_image)
        elif method == 'image_differencing':
            change_map = self._image_differencing(baseline_image, comparison_image)
        else:
            raise ValueError(f"Método desconhecido: {method}")
        
        return change_map
    
    def _spectral_difference(
        self, 
        baseline: np.ndarray, 
        comparison: np.ndarray
    ) -> np.ndarray:
        """
        Detecta mudanças usando diferença espectral
        
        Args:
            baseline: Imagem de linha de base
            comparison: Imagem de comparação
            
        Returns:
            Mapa de mudanças
        """
        # Calcula diferença absoluta para cada banda
        diff = np.abs(comparison - baseline)
        
        # Calcula magnitude da mudança
        change_magnitude = np.linalg.norm(diff, axis=0)
        
        # Normaliza
        if np.max(change_magnitude) > 0:
            change_magnitude = change_magnitude / np.max(change_magnitude)
        
        return change_magnitude
    
    def _change_vector_analysis(
        self, 
        baseline: np.ndarray, 
        comparison: np.ndarray
    ) -> np.ndarray:
        """
        Detecta mudanças usando análise de vetor de mudança (CVA)
        
        Args:
            baseline: Imagem de linha de base
            comparison: Imagem de comparação
            
        Returns:
            Mapa de mudanças
        """
        # Calcula vetor de mudança
        change_vector = comparison - baseline
        
        # Calcula magnitude e direção do vetor
        magnitude = np.linalg.norm(change_vector, axis=0)
        
        # Normaliza
        if np.max(magnitude) > 0:
            magnitude = magnitude / np.max(magnitude)
        
        return magnitude
    
    def _image_differencing(
        self, 
        baseline: np.ndarray, 
        comparison: np.ndarray
    ) -> np.ndarray:
        """
        Detecta mudanças usando diferenciação de imagens simples
        
        Args:
            baseline: Imagem de linha de base
            comparison: Imagem de comparação
            
        Returns:
            Mapa de mudanças
        """
        # Calcula média das bandas
        baseline_mean = np.mean(baseline, axis=0)
        comparison_mean = np.mean(comparison, axis=0)
        
        # Calcula diferença
        diff = np.abs(comparison_mean - baseline_mean)
        
        # Normaliza
        if np.max(diff) > 0:
            diff = diff / np.max(diff)
        
        return diff
    
    def threshold_changes(
        self, 
        change_map: np.ndarray,
        threshold: Optional[float] = None
    ) -> np.ndarray:
        """
        Aplica threshold para identificar mudanças significativas
        
        Args:
            change_map: Mapa de mudanças contínuo
            threshold: Threshold de mudança (0-1)
            
        Returns:
            Mapa binário de mudanças
        """
        if threshold is None:
            threshold = self.change_detection_config.get('change_threshold', 0.15)
        
        binary_change = change_map > threshold
        return binary_change
    
    def classify_change_types(
        self, 
        baseline_classification: np.ndarray,
        comparison_classification: np.ndarray,
        mining_classes: Optional[List[int]] = None
    ) -> Tuple[np.ndarray, Dict]:
        """
        Classifica tipos de mudança (nova área, expansão, retração, recuperação)
        
        Args:
            baseline_classification: Classificação da linha de base
            comparison_classification: Classificação de comparação
            mining_classes: Classes que representam garimpo
            
        Returns:
            Tupla (mapa_tipos_mudança, estatísticas)
        """
        if mining_classes is None:
            mining_classes = [0, 1]  # garimpo_ativo, garimpo_abandonado
        
        # Cria máscaras binárias de garimpo
        baseline_mining = np.isin(baseline_classification, mining_classes)
        comparison_mining = np.isin(comparison_classification, mining_classes)
        
        # Classifica tipos de mudança
        change_types = np.zeros_like(baseline_classification, dtype=np.int8)
        
        # 1: Nova área de garimpo
        new_mining = np.logical_and(~baseline_mining, comparison_mining)
        change_types[new_mining] = 1
        
        # 2: Expansão de garimpo (adjacente a área existente)
        expansion = self._detect_expansion(baseline_mining, new_mining)
        change_types[expansion] = 2
        
        # 3: Retração de garimpo
        retraction = np.logical_and(baseline_mining, ~comparison_mining)
        change_types[retraction] = 3
        
        # 4: Área de garimpo estável (sem mudança)
        stable_mining = np.logical_and(baseline_mining, comparison_mining)
        change_types[stable_mining] = 4
        
        # Calcula estatísticas
        resolution = self.config.get('output', {}).get('output_resolution', 10)
        pixel_area = resolution ** 2
        
        stats = {
            'new_mining_area_m2': np.sum(new_mining) * pixel_area,
            'expansion_area_m2': np.sum(expansion) * pixel_area,
            'retraction_area_m2': np.sum(retraction) * pixel_area,
            'stable_mining_area_m2': np.sum(stable_mining) * pixel_area,
            'new_mining_area_hectares': np.sum(new_mining) * pixel_area / 10000,
            'expansion_area_hectares': np.sum(expansion) * pixel_area / 10000,
            'retraction_area_hectares': np.sum(retraction) * pixel_area / 10000,
            'stable_mining_area_hectares': np.sum(stable_mining) * pixel_area / 10000,
            'net_change_m2': (np.sum(new_mining) - np.sum(retraction)) * pixel_area,
            'net_change_hectares': (np.sum(new_mining) - np.sum(retraction)) * pixel_area / 10000
        }
        
        return change_types, stats
    
    def _detect_expansion(
        self, 
        baseline_mining: np.ndarray,
        new_mining: np.ndarray
    ) -> np.ndarray:
        """
        Detecta expansão de áreas de garimpo (novas áreas adjacentes)
        
        Args:
            baseline_mining: Máscara de garimpo da linha de base
            new_mining: Máscara de novas áreas de garimpo
            
        Returns:
            Máscara de áreas de expansão
        """
        # Dilata área de garimpo da linha de base
        dilated_baseline = ndimage.binary_dilation(baseline_mining, iterations=2)
        
        # Expansão são novas áreas que estão adjacentes às áreas existentes
        expansion = np.logical_and(new_mining, dilated_baseline)
        
        return expansion
    
    def temporal_analysis(
        self, 
        time_series: List[Tuple[str, np.ndarray]],
        mining_classes: Optional[List[int]] = None
    ) -> Dict:
        """
        Análise temporal de série de imagens
        
        Args:
            time_series: Lista de tuplas (data, classificação)
            mining_classes: Classes que representam garimpo
            
        Returns:
            Dicionário com análise temporal
        """
        if mining_classes is None:
            mining_classes = [0, 1]
        
        resolution = self.config.get('output', {}).get('output_resolution', 10)
        pixel_area = resolution ** 2
        
        temporal_stats = {
            'dates': [],
            'total_mining_area_m2': [],
            'total_mining_area_hectares': [],
            'change_from_previous': []
        }
        
        previous_area = 0
        
        for date, classification in time_series:
            # Calcula área de garimpo
            mining_mask = np.isin(classification, mining_classes)
            mining_area_pixels = np.sum(mining_mask)
            mining_area_m2 = mining_area_pixels * pixel_area
            mining_area_hectares = mining_area_m2 / 10000
            
            temporal_stats['dates'].append(date)
            temporal_stats['total_mining_area_m2'].append(mining_area_m2)
            temporal_stats['total_mining_area_hectares'].append(mining_area_hectares)
            
            # Calcula mudança em relação ao período anterior
            if previous_area > 0:
                change = mining_area_m2 - previous_area
                change_percent = (change / previous_area) * 100
                temporal_stats['change_from_previous'].append({
                    'absolute': change,
                    'percent': change_percent
                })
            else:
                temporal_stats['change_from_previous'].append({
                    'absolute': 0,
                    'percent': 0
                })
            
            previous_area = mining_area_m2
        
        # Calcula tendência geral
        if len(temporal_stats['total_mining_area_m2']) > 1:
            trend = self._calculate_trend(temporal_stats['total_mining_area_m2'])
            temporal_stats['trend'] = trend
        
        return temporal_stats
    
    def _calculate_trend(self, values: List[float]) -> str:
        """
        Calcula tendência dos valores ao longo do tempo
        
        Args:
            values: Lista de valores temporais
            
        Returns:
            String descrevendo a tendência ('increasing', 'decreasing', 'stable')
        """
        if len(values) < 2:
            return 'insufficient_data'
        
        # Regressão linear simples
        x = np.arange(len(values))
        slope = np.polyfit(x, values, 1)[0]
        
        # Define threshold para considerar mudança significativa
        threshold = np.mean(values) * 0.05  # 5% da média
        
        if slope > threshold:
            return 'increasing'
        elif slope < -threshold:
            return 'decreasing'
        else:
            return 'stable'
    
    def generate_alert(
        self, 
        change_stats: Dict
    ) -> Optional[Dict]:
        """
        Gera alerta se mudanças significativas forem detectadas
        
        Args:
            change_stats: Estatísticas de mudança
            
        Returns:
            Dicionário com alerta ou None
        """
        alerts_config = self.monitoring_config.get('alerts', {})
        
        if not alerts_config.get('generate_alerts', True):
            return None
        
        alert_threshold = alerts_config.get('alert_threshold', 1000)  # m²
        
        new_mining_area = change_stats.get('new_mining_area_m2', 0)
        
        if new_mining_area > alert_threshold:
            alert = {
                'timestamp': datetime.now().isoformat(),
                'alert_type': 'new_mining_activity',
                'severity': 'high' if new_mining_area > alert_threshold * 5 else 'medium',
                'area_m2': new_mining_area,
                'area_hectares': new_mining_area / 10000,
                'message': f'Nova atividade de garimpo detectada: {new_mining_area:.2f} m² ({new_mining_area/10000:.2f} hectares)',
                'recommendation': 'Verificação in loco recomendada'
            }
            
            return alert
        
        return None
    
    def compare_multi_temporal(
        self, 
        baseline_year: str,
        comparison_periods: List[str],
        classifications: Dict[str, np.ndarray]
    ) -> Dict:
        """
        Compara múltiplos períodos temporais com uma linha de base
        
        Args:
            baseline_year: Ano de linha de base
            comparison_periods: Lista de períodos de comparação
            classifications: Dicionário {período: classificação}
            
        Returns:
            Dicionário com análises comparativas
        """
        baseline_classification = classifications.get(baseline_year)
        
        if baseline_classification is None:
            raise ValueError(f"Classificação de linha de base não encontrada: {baseline_year}")
        
        multi_temporal_analysis = {
            'baseline_year': baseline_year,
            'comparisons': []
        }
        
        for period in comparison_periods:
            if period in classifications:
                comparison_classification = classifications[period]
                
                # Detecta mudanças
                change_map = self.detect_changes(
                    baseline_classification, 
                    comparison_classification
                )
                
                # Classifica tipos de mudança
                change_types, stats = self.classify_change_types(
                    baseline_classification,
                    comparison_classification
                )
                
                # Gera alerta se necessário
                alert = self.generate_alert(stats)
                
                comparison_result = {
                    'period': period,
                    'change_map': change_map,
                    'change_types': change_types,
                    'statistics': stats,
                    'alert': alert
                }
                
                multi_temporal_analysis['comparisons'].append(comparison_result)
        
        return multi_temporal_analysis
