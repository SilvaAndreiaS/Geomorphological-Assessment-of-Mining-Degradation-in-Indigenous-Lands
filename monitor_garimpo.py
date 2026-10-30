# -* coding: utf-8 -*-
"""
Mapeamento Híbrido de Risco e Cicatrizes de Garimpo — TI Munduruku
Módulo de Sensoriamento Remoto e Processamento de Imagens
"""

import numpy as np

def calculate_ndvi(nir, red):
    """Calcula o Índice de Vegetação por Diferença Normalizada (NDVI)"""
    denominator = nir + red
    if denominator == 0:
        return 0.0
    return (nir - red) / denominator

def calculate_mndwi(green, swir):
    """Calcula o Índice de Água por Diferença Normalizada Modificado (MNDWI)"""
    denominator = green + swir
    if denominator == 0:
        return 0.0
    return (green - swir) / denominator

def calculate_bsi(swir, red, nir, blue):
    """Calcula o Índice de Solo Exposto (BSI)"""
    num = (swir + red) - (nir + blue)
    den = (swir + red) + (nir + blue)
    if den == 0:
        return 0.0
    return num / den

class GarimpoMonitor:
    def __init__(self, area_total_ha=7000.0):
        self.area_total_ha = area_total_ha
        self.models = ["RandomForestClassifier", "UNet_Segmentation"]

    def process_hybrid_fusion(self, optical_bands, sar_backscatter):
        """
        Simula a fusão de dados ópticos (Sentinel-2) com SAR (Sentinel-1)
        """
        ndvi = calculate_ndvi(optical_bands.get('B8', 0), optical_bands.get('B4', 0))
        mndwi = calculate_mndwi(optical_bands.get('B3', 0), optical_bands.get('B11', 0))
        bsi = calculate_bsi(optical_bands.get('B11', 0), optical_bands.get('B4', 0),
                            optical_bands.get('B8', 0), optical_bands.get('B2', 0))
        
        # Lógica heurística simplificada de classificação
        is_garimpo = (bsi > 0.1) and (mndwi > -0.2 or mndwi < -0.6) and (ndvi < 0.3)
        
        return {
            "ndvi": ndvi,
            "mndwi": mndwi,
            "bsi": bsi,
            "is_garimpo_candidate": is_garimpo,
            "sar_coherence_check": sar_backscatter.get('coherence', 0) < 0.4
        }

if __name__ == "__main__":
    print("Mapeamento Híbrido TI Munduruku — Teste do Módulo Python")
    sample_optical = {'B2': 0.05, 'B3': 0.08, 'B4': 0.12, 'B8': 0.25, 'B11': 0.35}
    sample_sar = {'VV': -12.5, 'VH': -18.2, 'coherence': 0.32}
    
    monitor = GarimpoMonitor()
    res = monitor.process_hybrid_fusion(sample_optical, sample_sar)
    print("Resultado do Processamento Amostral:", res)
