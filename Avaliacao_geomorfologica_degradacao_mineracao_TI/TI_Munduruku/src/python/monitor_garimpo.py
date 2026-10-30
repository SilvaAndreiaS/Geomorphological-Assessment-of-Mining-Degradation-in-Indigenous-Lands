# -* coding: utf-8 -*-
# Avaliação geomorfológica da degradação causada pela mineração em terras indígenas

def calculate_ndvi(nir, red):
    den = nir + red
    return (nir - red) / den if den != 0 else 0.0

def calculate_mndwi(green, swir):
    den = green + swir
    return (green - swir) / den if den != 0 else 0.0

def calculate_bsi(swir, red, nir, blue):
    num = (swir + red) - (nir + blue)
    den = (swir + red) + (nir + blue)
    return num / den if den != 0 else 0.0
