"""
Módulo para aquisição de dados de satélite
Suporta Sentinel-2, Landsat-8 e outras fontes
"""

import numpy as np
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Tuple, Optional
import rasterio
from rasterio.warp import calculate_default_transform, reproject, Resampling


class SatelliteDataAcquisition:
    """Classe para aquisição e gerenciamento de dados de satélite"""
    
    def __init__(self, config: Dict):
        """
        Inicializa o módulo de aquisição de dados
        
        Args:
            config: Dicionário de configuração do projeto
        """
        self.config = config
        self.study_area = config.get('study_area', {})
        self.satellite_config = config.get('satellite_data', {})
    
    def get_bounding_box(self) -> Tuple[float, float, float, float]:
        """
        Retorna a bounding box da área de estudo
        
        Returns:
            Tupla (min_lon, min_lat, max_lon, max_lat)
        """
        bbox = self.study_area.get('bounding_box', {})
        return (
            bbox.get('min_lon', -58.5),
            bbox.get('min_lat', -8.0),
            bbox.get('max_lon', -56.5),
            bbox.get('max_lat', -6.0)
        )
    
    def validate_cloud_coverage(self, metadata: Dict) -> bool:
        """
        Valida se a cobertura de nuvens está dentro do limite aceitável
        
        Args:
            metadata: Metadados da imagem contendo cloud_coverage
            
        Returns:
            True se a imagem é aceitável, False caso contrário
        """
        cloud_coverage = metadata.get('cloud_coverage', 100)
        max_cloud = self.satellite_config.get('cloud_coverage_max', 20)
        return cloud_coverage <= max_cloud
    
    def search_sentinel2_data(
        self, 
        start_date: str, 
        end_date: str,
        max_cloud_coverage: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca dados do Sentinel-2 para a área de estudo
        
        Args:
            start_date: Data inicial (formato: YYYY-MM-DD)
            end_date: Data final (formato: YYYY-MM-DD)
            max_cloud_coverage: Cobertura máxima de nuvens (%)
            
        Returns:
            Lista de metadados das imagens encontradas
        """
        bbox = self.get_bounding_box()
        
        if max_cloud_coverage is None:
            max_cloud_coverage = self.satellite_config.get('cloud_coverage_max', 20)
        
        # Placeholder para integração com API real (SentinelSat, Google Earth Engine, etc.)
        # Em produção, aqui seria feita a busca real nos servidores de dados
        results = []
        
        # Exemplo de estrutura de resultado
        example_result = {
            'id': 'S2A_MSIL2A_20240101T000000',
            'date': start_date,
            'satellite': 'Sentinel-2',
            'cloud_coverage': 15.5,
            'bbox': bbox,
            'bands': ['B02', 'B03', 'B04', 'B08', 'B11', 'B12'],
            'resolution': 10
        }
        
        return results
    
    def search_landsat8_data(
        self, 
        start_date: str, 
        end_date: str,
        max_cloud_coverage: Optional[int] = None
    ) -> List[Dict]:
        """
        Busca dados do Landsat-8 para a área de estudo
        
        Args:
            start_date: Data inicial (formato: YYYY-MM-DD)
            end_date: Data final (formato: YYYY-MM-DD)
            max_cloud_coverage: Cobertura máxima de nuvens (%)
            
        Returns:
            Lista de metadados das imagens encontradas
        """
        bbox = self.get_bounding_box()
        
        if max_cloud_coverage is None:
            max_cloud_coverage = self.satellite_config.get('cloud_coverage_max', 20)
        
        # Placeholder para integração com API real
        results = []
        
        return results
    
    def load_satellite_image(self, image_path: str) -> Tuple[np.ndarray, Dict]:
        """
        Carrega uma imagem de satélite do disco
        
        Args:
            image_path: Caminho para o arquivo da imagem
            
        Returns:
            Tupla (array_dados, metadados)
        """
        with rasterio.open(image_path) as src:
            # Lê todas as bandas
            data = src.read()
            
            # Obtém metadados
            metadata = {
                'crs': src.crs,
                'transform': src.transform,
                'bounds': src.bounds,
                'width': src.width,
                'height': src.height,
                'count': src.count,
                'dtype': src.dtypes[0]
            }
        
        return data, metadata
    
    def reproject_image(
        self, 
        data: np.ndarray, 
        src_crs: str, 
        dst_crs: str,
        src_transform,
        width: int,
        height: int
    ) -> Tuple[np.ndarray, any]:
        """
        Reprojeta imagem para um sistema de coordenadas diferente
        
        Args:
            data: Array de dados da imagem
            src_crs: Sistema de coordenadas de origem
            dst_crs: Sistema de coordenadas de destino
            src_transform: Transformação da imagem de origem
            width: Largura da imagem
            height: Altura da imagem
            
        Returns:
            Tupla (dados_reprojetados, nova_transformação)
        """
        # Obtém bounds da imagem de origem
        from rasterio.transform import array_bounds
        bounds = array_bounds(height, width, src_transform)
        
        # Calcula a transformação para o novo CRS
        dst_transform, dst_width, dst_height = calculate_default_transform(
            src_crs, dst_crs, width, height, *bounds
        )
        
        # Cria array de destino
        dst_data = np.empty((data.shape[0], dst_height, dst_width), dtype=data.dtype)
        
        # Reprojeta cada banda
        for i in range(data.shape[0]):
            reproject(
                source=data[i],
                destination=dst_data[i],
                src_transform=src_transform,
                src_crs=src_crs,
                dst_transform=dst_transform,
                dst_crs=dst_crs,
                resampling=Resampling.bilinear
            )
        
        return dst_data, dst_transform
    
    def download_image(self, image_id: str, output_path: str) -> bool:
        """
        Baixa uma imagem de satélite
        
        Args:
            image_id: ID da imagem a ser baixada
            output_path: Caminho para salvar a imagem
            
        Returns:
            True se o download foi bem sucedido, False caso contrário
        """
        # Placeholder para implementação de download real
        # Em produção, aqui seria feita a conexão com a API e download
        print(f"Baixando imagem {image_id} para {output_path}")
        return True
    
    def get_available_bands(self, satellite: str) -> List[str]:
        """
        Retorna as bandas disponíveis para um satélite específico
        
        Args:
            satellite: Nome do satélite (ex: 'Sentinel-2', 'Landsat-8')
            
        Returns:
            Lista de nomes de bandas
        """
        sources = self.satellite_config.get('sources', [])
        
        for source in sources:
            if source.get('name') == satellite:
                return source.get('bands', [])
        
        return []
