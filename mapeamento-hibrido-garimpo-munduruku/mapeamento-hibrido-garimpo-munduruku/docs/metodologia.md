# Metodologia Detalhada

## Etapa 1 — Aquisição de dados
Seleção de imagens de satélite de fontes apropriadas (Landsat, Sentinel-2), considerando cobertura de nuvens e resolução espacial.

## Etapa 2 — Pré-processamento
Correção atmosférica, máscaras de nuvens, recorte da área de estudo e padronização espacial.

## Etapa 3 — Extração de características
Cálculo de índices espectrais (NDVI, NDWI, NDBI) para diferenciar solo exposto, vegetação e água.

## Etapa 4 — Classificação híbrida
Combinação de regras espectrais, classificadores supervisionados (Random Forest) e análise temporal.

## Etapa 5 — Análise de risco espacial
Cruzamento com hidrografia e limites territoriais.

## Etapa 6 — Validação
Uso de matriz de confusão, F1-score e precisão global com amostras de referência.
