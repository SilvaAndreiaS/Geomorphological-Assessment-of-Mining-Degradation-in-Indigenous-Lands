# -*- coding: utf-8 -*-
# Avaliação geomorfológica da degradação causada pela mineração em terras indígenas
# Referência Técnica: A12297 - LOMAS (TI Munduruku / Bacia do Rio Cabitutu)

from dataclasses import dataclass, field
from typing import List, Dict, Tuple
import heapq


# 1. Funções de Índices Espectrais (Sentinel-2 MSI)
def calculate_ndvi(nir: float, red: float) -> float:
    """(B8 - B4) / (B8 + B4) -> Supressão vegetal e corte raso."""
    den = nir + red
    return (nir - red) / den if den != 0 else 0.0


def calculate_mndwi(green: float, swir: float) -> float:
    """(B3 - B11) / (B3 + B11) -> Cavas inundadas e alteração hídrica."""
    den = green + swir
    return (green - swir) / den if den != 0 else 0.0


def calculate_bsi(swir: float, red: float, nir: float, blue: float) -> float:
    """[(B11 + B4) - (B8 + B2)] / [(B11 + B4) + (B8 + B2)] -> Lomas de rejeito e solo exposto."""
    num = (swir + red) - (nir + blue)
    den = (swir + red) + (nir + blue)
    return num / den if den != 0 else 0.0


# 2. Equação da Matriz de Vulnerabilidade e Risco Normalizado
def calculate_normalized_risk(
    dist_garimpo_norm: float,
    area_devastada_norm: float,
    impacto_hidrico_norm: float
) -> float:
    """
    Risco = (DistanciaGarimpo_norm * 0.40) + (AreaDevastada_norm * 0.35) + (ImpactoHidrico_norm * 0.25)
    """
    risco = (
        (dist_garimpo_norm * 0.40) +
        (area_devastada_norm * 0.35) +
        (impacto_hidrico_norm * 0.25)
    )
    return round(min(max(risco, 0.0), 1.0), 4)


# 3. Classificador Geomorfológico de Cicatrizes (Cavas vs. Lomas de Rejeito)
def classify_geomorphological_feature(ndvi: float, mndwi: float, bsi: float) -> str:
    if mndwi > 0.15 and ndvi < 0.20:
        return "CAVA_INUNDADA_MERCURIO"
    elif bsi > 0.12 and ndvi < 0.25:
        return "LOMA_REJEITO_SOLO_EXPOSTO"
    elif ndvi < 0.38 and bsi > 0.02:
        return "SUPRESSAO_VEGETAL_CORTE_RASO"
    return "COBERTURA_FLORESTAL_ESTAVEL"
