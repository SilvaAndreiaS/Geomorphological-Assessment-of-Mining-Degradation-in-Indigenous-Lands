"""
Módulo de pré-processamento de imagens de satélite
Inclui correção atmosférica, normalização, remoção de nuvens, etc.
"""

import numpy as np
from typing import Tuple, Dict, Optional
from scipy import ndimage
import cv2


class ImagePreprocessor:
    """Classe para pré-processamento de imagens de satélite"""
    
    def __init__(self, config: Dict):
        """
        Inicializa o pré-processador de imagens
        
        Args:
            config: Dicionário de configuração do projeto
        """
        self.config = config
        self.preprocessing_config = config.get('preprocessing', {})
    
    def atmospheric_correction(
        self, 
        data: np.ndarray, 
        method: str = 'DOS'
    ) -> np.ndarray:
        """
        Aplica correção atmosférica na imagem
        
        Args:
            data: Array de dados da imagem (shape: [bands, height, width])
            method: Método de correção ('DOS', 'TOA', etc.)
            
        Returns:
            Imagem corrigida
        """
        if not self.preprocessing_config.get('atmospheric_correction', True):
            return data
        
        corrected = data.copy().astype(np.float32)
        
        if method == 'DOS':  # Dark Object Subtraction
            # Simples correção DOS
            for i in range(corrected.shape[0]):
                band = corrected[i]
                # Encontra o valor mínimo (dark object)
                dark_value = np.percentile(band[band > 0], 1)
                # Subtrai o valor escuro
                corrected[i] = np.maximum(band - dark_value, 0)
        
        return corrected
    
    def radiometric_normalization(
        self, 
        data: np.ndarray
    ) -> np.ndarray:
        """
        Normaliza valores radiométricos da imagem
        
        Args:
            data: Array de dados da imagem
            
        Returns:
            Imagem normalizada
        """
        if not self.preprocessing_config.get('radiometric_normalization', True):
            return data
        
        normalized = data.copy().astype(np.float32)
        
        # Normaliza cada banda para o intervalo [0, 1]
        for i in range(normalized.shape[0]):
            band = normalized[i]
            min_val = np.percentile(band, 2)
            max_val = np.percentile(band, 98)
            
            if max_val > min_val:
                normalized[i] = (band - min_val) / (max_val - min_val)
                normalized[i] = np.clip(normalized[i], 0, 1)
        
        return normalized
    
    def topographic_correction(
        self, 
        data: np.ndarray, 
        dem: Optional[np.ndarray] = None,
        sun_elevation: float = 45.0,
        sun_azimuth: float = 135.0
    ) -> np.ndarray:
        """
        Aplica correção topográfica (C-correction ou cosine correction)
        
        Args:
            data: Array de dados da imagem
            dem: Modelo Digital de Elevação (opcional)
            sun_elevation: Elevação solar em graus
            sun_azimuth: Azimute solar em graus
            
        Returns:
            Imagem corrigida
        """
        if not self.preprocessing_config.get('topographic_correction', True):
            return data
        
        # Se não houver DEM, retorna a imagem sem correção
        if dem is None:
            return data
        
        corrected = data.copy().astype(np.float32)
        
        # Converte ângulos para radianos
        sun_elev_rad = np.radians(sun_elevation)
        sun_azim_rad = np.radians(sun_azimuth)
        
        # Calcula a inclinação e aspecto do terreno
        slope, aspect = self._calculate_slope_aspect(dem)
        
        # Calcula o ângulo de incidência solar
        cos_i = (np.cos(slope) * np.sin(sun_elev_rad) +
                 np.sin(slope) * np.cos(sun_elev_rad) *
                 np.cos(sun_azim_rad - aspect))
        
        # Aplica C-correction
        for i in range(corrected.shape[0]):
            band = corrected[i]
            # C-correction: reflectância_corrigida = reflectância * (cos(θz) / cos(i))
            correction_factor = np.sin(sun_elev_rad) / (cos_i + 0.01)  # +0.01 para evitar divisão por zero
            corrected[i] = band * correction_factor
            corrected[i] = np.clip(corrected[i], 0, np.max(band))
        
        return corrected
    
    def _calculate_slope_aspect(
        self, 
        dem: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcula inclinação e aspecto a partir do DEM
        
        Args:
            dem: Modelo Digital de Elevação
            
        Returns:
            Tupla (inclinação, aspecto) em radianos
        """
        # Calcula gradientes
        dx = ndimage.sobel(dem, axis=1)
        dy = ndimage.sobel(dem, axis=0)
        
        # Calcula inclinação
        slope = np.arctan(np.sqrt(dx**2 + dy**2))
        
        # Calcula aspecto
        aspect = np.arctan2(-dy, dx)
        aspect = np.where(aspect < 0, 2 * np.pi + aspect, aspect)
        
        return slope, aspect
    
    def cloud_shadow_removal(
        self, 
        data: np.ndarray,
        cloud_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Remove nuvens e sombras da imagem
        
        Args:
            data: Array de dados da imagem
            cloud_mask: Máscara de nuvens (opcional)
            
        Returns:
            Imagem com nuvens/sombras removidas
        """
        if not self.preprocessing_config.get('cloud_shadow_removal', True):
            return data
        
        cleaned = data.copy()
        
        if cloud_mask is None:
            # Gera máscara de nuvens automaticamente
            cloud_mask = self._detect_clouds(data)
        
        # Gera máscara de sombras
        shadow_mask = self._detect_shadows(data, cloud_mask)
        
        # Combina máscaras
        combined_mask = np.logical_or(cloud_mask, shadow_mask)
        
        # Interpola valores nas áreas mascaradas
        for i in range(cleaned.shape[0]):
            band = cleaned[i]
            if np.any(combined_mask):
                # Interpolação simples usando inpainting
                band_uint8 = (band * 255).astype(np.uint8)
                mask_uint8 = combined_mask.astype(np.uint8) * 255
                inpainted = cv2.inpaint(band_uint8, mask_uint8, 3, cv2.INPAINT_TELEA)
                cleaned[i] = inpainted.astype(np.float32) / 255.0
        
        return cleaned
    
    def _detect_clouds(self, data: np.ndarray) -> np.ndarray:
        """
        Detecta nuvens na imagem usando análise espectral
        
        Args:
            data: Array de dados da imagem
            
        Returns:
            Máscara binária de nuvens
        """
        # Assume que as primeiras bandas são visíveis/NIR
        # Nuvens geralmente têm alta reflectância em todas as bandas
        
        if data.shape[0] >= 3:
            # Média das bandas visíveis
            visible_mean = np.mean(data[:3], axis=0)
            
            # Threshold para detecção de nuvens
            cloud_threshold = np.percentile(visible_mean, 95)
            cloud_mask = visible_mean > cloud_threshold
        else:
            cloud_mask = np.zeros(data.shape[1:], dtype=bool)
        
        return cloud_mask
    
    def _detect_shadows(
        self, 
        data: np.ndarray, 
        cloud_mask: np.ndarray
    ) -> np.ndarray:
        """
        Detecta sombras de nuvens na imagem
        
        Args:
            data: Array de dados da imagem
            cloud_mask: Máscara de nuvens
            
        Returns:
            Máscara binária de sombras
        """
        if data.shape[0] >= 3:
            # Sombras têm baixa reflectância
            visible_mean = np.mean(data[:3], axis=0)
            
            # Threshold para detecção de sombras
            shadow_threshold = np.percentile(visible_mean, 10)
            shadow_mask = visible_mean < shadow_threshold
            
            # Remove sombras que não estão próximas de nuvens
            # (implementação simplificada)
            shadow_mask = np.logical_and(shadow_mask, ~cloud_mask)
        else:
            shadow_mask = np.zeros(data.shape[1:], dtype=bool)
        
        return shadow_mask
    
    def temporal_compositing(
        self, 
        image_stack: np.ndarray,
        method: str = 'median'
    ) -> np.ndarray:
        """
        Cria mosaico temporal de múltiplas imagens
        
        Args:
            image_stack: Array de imagens (shape: [n_images, bands, height, width])
            method: Método de composição ('median', 'mean', 'max', 'min')
            
        Returns:
            Imagem composta
        """
        compositing_config = self.preprocessing_config.get('temporal_compositing', {})
        method = compositing_config.get('method', method)
        
        if method == 'median':
            composite = np.median(image_stack, axis=0)
        elif method == 'mean':
            composite = np.mean(image_stack, axis=0)
        elif method == 'max':
            composite = np.max(image_stack, axis=0)
        elif method == 'min':
            composite = np.min(image_stack, axis=0)
        else:
            raise ValueError(f"Método desconhecido: {method}")
        
        return composite
    
    def apply_full_preprocessing(
        self, 
        data: np.ndarray,
        dem: Optional[np.ndarray] = None,
        cloud_mask: Optional[np.ndarray] = None
    ) -> np.ndarray:
        """
        Aplica o pipeline completo de pré-processamento
        
        Args:
            data: Array de dados da imagem
            dem: Modelo Digital de Elevação (opcional)
            cloud_mask: Máscara de nuvens (opcional)
            
        Returns:
            Imagem pré-processada
        """
        print("Aplicando correção atmosférica...")
        data = self.atmospheric_correction(data)
        
        print("Aplicando normalização radiométrica...")
        data = self.radiometric_normalization(data)
        
        if dem is not None:
            print("Aplicando correção topográfica...")
            data = self.topographic_correction(data, dem)
        
        print("Removendo nuvens e sombras...")
        data = self.cloud_shadow_removal(data, cloud_mask)
        
        print("Pré-processamento concluído!")
        return data
