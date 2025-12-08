"""
Detector de cicatrizes de garimpo ilegal
"""

import numpy as np
from typing import Dict, List, Tuple, Optional
from scipy import ndimage
from skimage import measure, morphology
from skimage.filters import threshold_otsu
import cv2


class MiningScarDetector:
    """Classe para detecção de cicatrizes de garimpo"""
    
    def __init__(self, config: Dict):
        """
        Inicializa o detector de cicatrizes de garimpo
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.detection_config = config.get('detection', {}).get('mining_scars', {})
    
    def detect_mining_scars(
        self, 
        classification_map: np.ndarray,
        mining_classes: Optional[List[int]] = None
    ) -> Tuple[np.ndarray, List[Dict]]:
        """
        Detecta cicatrizes de garimpo no mapa de classificação
        
        Args:
            classification_map: Mapa de classificação
            mining_classes: Lista de classes que representam garimpo
            
        Returns:
            Tupla (mapa_binário, lista_de_objetos)
        """
        if mining_classes is None:
            # Usa classes padrão de garimpo
            mining_classes = [0, 1]  # garimpo_ativo, garimpo_abandonado
        
        # Cria máscara binária de áreas de garimpo
        binary_mask = np.isin(classification_map, mining_classes)
        
        # Remove pequenas áreas e ruído
        binary_mask = self.remove_small_objects(binary_mask)
        
        # Detecta objetos individuais
        labeled_map = measure.label(binary_mask, connectivity=2)
        mining_objects = self.extract_mining_objects(labeled_map, classification_map)
        
        return binary_mask, mining_objects
    
    def remove_small_objects(
        self, 
        binary_mask: np.ndarray,
        min_size: Optional[int] = None
    ) -> np.ndarray:
        """
        Remove objetos pequenos da máscara binária
        
        Args:
            binary_mask: Máscara binária
            min_size: Tamanho mínimo em pixels
            
        Returns:
            Máscara filtrada
        """
        if min_size is None:
            # Calcula min_size baseado na configuração
            min_area_m2 = self.detection_config.get('morphology', {}).get('min_area', 100)
            # Assume resolução de 10m (ajustar conforme necessário)
            resolution = self.config.get('output', {}).get('output_resolution', 10)
            min_size = int(min_area_m2 / (resolution ** 2))
        
        cleaned = morphology.remove_small_objects(binary_mask, min_size=min_size)
        return cleaned
    
    def extract_mining_objects(
        self, 
        labeled_map: np.ndarray,
        classification_map: np.ndarray
    ) -> List[Dict]:
        """
        Extrai características de cada objeto de garimpo detectado
        
        Args:
            labeled_map: Mapa com objetos rotulados
            classification_map: Mapa de classificação original
            
        Returns:
            Lista de dicionários com características dos objetos
        """
        mining_objects = []
        
        # Propriedades regionais
        regions = measure.regionprops(labeled_map)
        
        for region in regions:
            # Calcula características morfológicas
            area = region.area
            perimeter = region.perimeter
            
            # Compacidade (quanto mais próximo de 1, mais circular)
            if perimeter > 0:
                compactness = (4 * np.pi * area) / (perimeter ** 2)
            else:
                compactness = 0
            
            # Extrai bounding box
            minr, minc, maxr, maxc = region.bbox
            
            # Centroide
            centroid = region.centroid
            
            # Cria objeto com informações
            mining_obj = {
                'id': region.label,
                'area_pixels': area,
                'perimeter': perimeter,
                'compactness': compactness,
                'centroid': centroid,
                'bbox': (minr, minc, maxr, maxc),
                'eccentricity': region.eccentricity,
                'solidity': region.solidity,
                'extent': region.extent
            }
            
            mining_objects.append(mining_obj)
        
        return mining_objects
    
    def filter_by_morphology(
        self, 
        mining_objects: List[Dict],
        min_area_m2: Optional[float] = None,
        max_area_m2: Optional[float] = None
    ) -> List[Dict]:
        """
        Filtra objetos baseado em características morfológicas
        
        Args:
            mining_objects: Lista de objetos detectados
            min_area_m2: Área mínima em m²
            max_area_m2: Área máxima em m²
            
        Returns:
            Lista filtrada de objetos
        """
        morphology_config = self.detection_config.get('morphology', {})
        
        if min_area_m2 is None:
            min_area_m2 = morphology_config.get('min_area', 100)
        
        if max_area_m2 is None:
            max_area_m2 = morphology_config.get('max_area', 1000000)
        
        # Converte área de pixels para m²
        resolution = self.config.get('output', {}).get('output_resolution', 10)
        pixel_area = resolution ** 2
        
        filtered_objects = []
        for obj in mining_objects:
            area_m2 = obj['area_pixels'] * pixel_area
            
            if min_area_m2 <= area_m2 <= max_area_m2:
                obj['area_m2'] = area_m2
                obj['area_hectares'] = area_m2 / 10000
                filtered_objects.append(obj)
        
        return filtered_objects
    
    def calculate_spatial_context(
        self, 
        mining_objects: List[Dict],
        rivers_layer: Optional[np.ndarray] = None,
        roads_layer: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Calcula contexto espacial dos objetos (proximidade a rios, estradas, etc.)
        
        Args:
            mining_objects: Lista de objetos detectados
            rivers_layer: Camada de rios (opcional)
            roads_layer: Camada de estradas (opcional)
            
        Returns:
            Lista de objetos com informações de contexto espacial
        """
        distance_threshold = self.detection_config.get('spatial_context', {}).get('distance_threshold', 500)
        resolution = self.config.get('output', {}).get('output_resolution', 10)
        distance_threshold_pixels = distance_threshold / resolution
        
        for obj in mining_objects:
            centroid = obj['centroid']
            
            # Calcula distância a rios se disponível
            if rivers_layer is not None:
                dist_to_river = self._calculate_distance_to_feature(
                    centroid, rivers_layer
                )
                obj['distance_to_river_m'] = dist_to_river * resolution
                obj['near_river'] = dist_to_river <= distance_threshold_pixels
            
            # Calcula distância a estradas se disponível
            if roads_layer is not None:
                dist_to_road = self._calculate_distance_to_feature(
                    centroid, roads_layer
                )
                obj['distance_to_road_m'] = dist_to_road * resolution
                obj['near_road'] = dist_to_road <= distance_threshold_pixels
        
        return mining_objects
    
    def _calculate_distance_to_feature(
        self, 
        point: Tuple[float, float], 
        feature_layer: np.ndarray
    ) -> float:
        """
        Calcula distância euclidiana de um ponto à feature mais próxima
        
        Args:
            point: Coordenadas do ponto (row, col)
            feature_layer: Camada binária com features
            
        Returns:
            Distância em pixels
        """
        # Calcula mapa de distâncias
        distance_map = ndimage.distance_transform_edt(~feature_layer)
        
        # Obtém distância no ponto especificado
        row, col = int(point[0]), int(point[1])
        distance = distance_map[row, col]
        
        return distance
    
    def segment_active_vs_abandoned(
        self, 
        mining_objects: List[Dict],
        temporal_data: Optional[np.ndarray] = None
    ) -> List[Dict]:
        """
        Segmenta áreas de garimpo em ativas vs abandonadas
        
        Args:
            mining_objects: Lista de objetos detectados
            temporal_data: Dados temporais para análise de atividade
            
        Returns:
            Lista de objetos com classificação de atividade
        """
        for obj in mining_objects:
            # Simplificação: classificação baseada em características
            # Em produção, usaria análise temporal mais sofisticada
            
            if temporal_data is not None:
                # Analisa mudanças recentes
                obj['status'] = 'garimpo_ativo' if self._is_active(obj, temporal_data) else 'garimpo_abandonado'
            else:
                # Usa heurística baseada em compacidade e outras features
                # Garimpos ativos tendem a ter formas mais irregulares
                if obj['compactness'] < 0.4:
                    obj['status'] = 'garimpo_ativo'
                else:
                    obj['status'] = 'garimpo_abandonado'
        
        return mining_objects
    
    def _is_active(
        self, 
        mining_obj: Dict, 
        temporal_data: np.ndarray
    ) -> bool:
        """
        Determina se um objeto de garimpo está ativo
        
        Args:
            mining_obj: Objeto de garimpo
            temporal_data: Dados temporais
            
        Returns:
            True se ativo, False caso contrário
        """
        # Placeholder para análise temporal mais sofisticada
        # Em produção, analisaria mudanças espectrais recentes
        return True
    
    def generate_detection_report(
        self, 
        mining_objects: List[Dict]
    ) -> Dict:
        """
        Gera relatório de detecção
        
        Args:
            mining_objects: Lista de objetos detectados
            
        Returns:
            Dicionário com estatísticas de detecção
        """
        if not mining_objects:
            return {
                'total_objects': 0,
                'total_area_m2': 0,
                'total_area_hectares': 0,
                'active_count': 0,
                'abandoned_count': 0
            }
        
        total_area_m2 = sum(obj.get('area_m2', 0) for obj in mining_objects)
        active_count = sum(1 for obj in mining_objects if obj.get('status') == 'garimpo_ativo')
        abandoned_count = sum(1 for obj in mining_objects if obj.get('status') == 'garimpo_abandonado')
        
        report = {
            'total_objects': len(mining_objects),
            'total_area_m2': total_area_m2,
            'total_area_hectares': total_area_m2 / 10000,
            'active_count': active_count,
            'abandoned_count': abandoned_count,
            'average_area_m2': total_area_m2 / len(mining_objects) if mining_objects else 0,
            'objects': mining_objects
        }
        
        return report
