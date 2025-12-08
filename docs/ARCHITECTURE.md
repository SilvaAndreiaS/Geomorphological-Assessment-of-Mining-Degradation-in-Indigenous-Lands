# Arquitetura do Sistema

## Visão Geral

Este documento descreve a arquitetura do Sistema de Detecção de Garimpo Ilegal para a Terra Indígena Munduruku.

## Componentes Principais

### 1. Módulo de Aquisição de Dados (`src/data_acquisition/`)

**Arquivo**: `satellite_data.py`

**Responsabilidades**:
- Busca e download de imagens de satélite (Sentinel-2, Landsat-8)
- Validação de cobertura de nuvens
- Carregamento de imagens do disco
- Reprojeção para diferentes sistemas de coordenadas
- Gerenciamento de metadados

**Principais Classes**:
- `SatelliteDataAcquisition`: Gerencia todas as operações de aquisição de dados

**Métodos Principais**:
- `search_sentinel2_data()`: Busca imagens Sentinel-2
- `search_landsat8_data()`: Busca imagens Landsat-8
- `load_satellite_image()`: Carrega imagens do disco
- `reproject_image()`: Reprojeta imagens

### 2. Módulo de Pré-processamento (`src/preprocessing/`)

**Arquivo**: `image_preprocessing.py`

**Responsabilidades**:
- Correção atmosférica (DOS, TOA)
- Normalização radiométrica
- Correção topográfica
- Remoção de nuvens e sombras
- Composição temporal de imagens

**Principais Classes**:
- `ImagePreprocessor`: Aplica todas as técnicas de pré-processamento

**Métodos Principais**:
- `atmospheric_correction()`: Correção atmosférica
- `radiometric_normalization()`: Normalização radiométrica
- `topographic_correction()`: Correção topográfica
- `cloud_shadow_removal()`: Remove nuvens e sombras
- `temporal_compositing()`: Cria mosaicos temporais
- `apply_full_preprocessing()`: Pipeline completo

### 3. Módulo de Classificação Híbrida (`src/classification/`)

**Arquivo**: `hybrid_classifier.py`

**Responsabilidades**:
- Cálculo de índices espectrais
- Classificação por métodos tradicionais
- Classificação por Machine Learning
- Ensemble de múltiplos classificadores
- Avaliação de desempenho

**Principais Classes**:
- `SpectralIndices`: Calcula índices espectrais (NDVI, NDWI, NDMI, BSI)
- `TraditionalClassifier`: Métodos tradicionais (K-means, Maximum Likelihood, SAM)
- `MachineLearningClassifier`: Métodos de ML (Random Forest, XGBoost, SVM)
- `HybridClassifier`: Combina métodos tradicionais e ML

**Métodos Principais**:
- `calculate_ndvi()`: Índice de vegetação
- `calculate_ndwi()`: Índice de água
- `calculate_ndmi()`: Índice de mineração
- `calculate_bsi()`: Índice de solo exposto
- `train_hybrid_model()`: Treina todos os modelos
- `ensemble_prediction()`: Predição ensemble
- `classify()`: Pipeline completo de classificação

### 4. Módulo de Detecção (`src/detection/`)

**Arquivo**: `mining_scar_detector.py`

**Responsabilidades**:
- Detecção de cicatrizes de garimpo
- Segmentação de objetos
- Análise morfológica
- Classificação: ativo vs abandonado
- Análise de contexto espacial
- Geração de relatórios

**Principais Classes**:
- `MiningScarDetector`: Detecta e caracteriza cicatrizes de garimpo

**Métodos Principais**:
- `detect_mining_scars()`: Detecta cicatrizes
- `extract_mining_objects()`: Extrai características dos objetos
- `filter_by_morphology()`: Filtra por tamanho e forma
- `calculate_spatial_context()`: Analisa proximidade a rios/estradas
- `segment_active_vs_abandoned()`: Classifica status
- `generate_detection_report()`: Gera relatório estatístico

### 5. Módulo de Monitoramento (`src/monitoring/`)

**Arquivo**: `change_detection.py`

**Responsabilidades**:
- Detecção de mudanças temporais
- Análise multi-temporal
- Classificação de tipos de mudança
- Geração de alertas
- Análise de tendências

**Principais Classes**:
- `ChangeDetector`: Detecta e analisa mudanças temporais

**Métodos Principais**:
- `detect_changes()`: Detecta mudanças entre duas imagens
- `classify_change_types()`: Classifica tipos de mudança (nova área, expansão, retração)
- `temporal_analysis()`: Análise de séries temporais
- `generate_alert()`: Gera alertas automáticos
- `compare_multi_temporal()`: Compara múltiplos períodos

### 6. Módulo de Visualização (`src/visualization/`)

**Arquivo**: `visualizer.py`

**Responsabilidades**:
- Visualização de mapas de classificação
- Visualização de mudanças temporais
- Geração de gráficos temporais
- Criação de dashboards
- Exportação para formatos geoespaciais
- Geração de relatórios

**Principais Classes**:
- `ResultsVisualizer`: Gera todas as visualizações e relatórios

**Métodos Principais**:
- `plot_classification_map()`: Plota mapa de classificação
- `plot_change_map()`: Plota mapa de mudanças
- `plot_temporal_analysis()`: Plota gráficos temporais
- `plot_mining_objects()`: Visualiza objetos detectados
- `plot_statistics_dashboard()`: Cria dashboard
- `export_results_to_geotiff()`: Exporta para GeoTIFF
- `generate_report()`: Gera relatório em texto

### 7. Módulo de Utilitários (`src/utils/`)

**Arquivo**: `config_loader.py`

**Responsabilidades**:
- Carregamento de configurações YAML
- Gerenciamento de parâmetros
- Acesso fácil a configurações

**Principais Classes**:
- `ConfigLoader`: Carrega e gerencia configurações

### 8. Pipeline Principal (`main_pipeline.py`)

**Responsabilidades**:
- Orquestração de todo o processo
- Interface de linha de comando
- Execução do pipeline completo

**Principais Classes**:
- `MiningDetectionPipeline`: Coordena todo o processo

**Métodos Principais**:
- `run_classification_pipeline()`: Executa classificação
- `run_detection_pipeline()`: Executa detecção
- `run_monitoring_pipeline()`: Executa monitoramento
- `run_visualization_pipeline()`: Executa visualização
- `run_full_pipeline()`: Executa pipeline completo

## Fluxo de Dados

```
Imagens de Satélite
        ↓
[Data Acquisition]
        ↓
[Preprocessing]
        ↓
[Hybrid Classification]
        ↓
[Detection]
        ↓
[Monitoring] (se dados temporais disponíveis)
        ↓
[Visualization]
        ↓
Produtos Finais
```

## Abordagem Híbrida

### Métodos Tradicionais
1. **K-means Clustering**: Classificação não supervisionada
2. **Maximum Likelihood**: Classificação supervisionada probabilística
3. **Spectral Angle Mapper**: Comparação de assinaturas espectrais
4. **Índices Espectrais**: NDVI, NDWI, NDMI, BSI

### Machine Learning
1. **Random Forest**: Ensemble de árvores de decisão
2. **XGBoost**: Gradient boosting
3. **SVM**: Support Vector Machine

### Ensemble
- Combina predições de múltiplos modelos
- Votação majoritária ou média ponderada
- Melhora robustez e acurácia

## Configuração

O sistema é altamente configurável através do arquivo `config/munduruku_config.yaml`:

```yaml
study_area:      # Área de estudo
satellite_data:  # Fontes de dados
preprocessing:   # Parâmetros de pré-processamento
classification:  # Configuração de classificação
detection:       # Critérios de detecção
monitoring:      # Parâmetros de monitoramento
output:          # Formatos de saída
visualization:   # Estilos de visualização
```

## Extensibilidade

O sistema foi projetado para ser facilmente extensível:

1. **Novos Satélites**: Adicione suporte em `satellite_data.py`
2. **Novos Algoritmos**: Adicione em `hybrid_classifier.py`
3. **Novos Índices**: Adicione em `SpectralIndices`
4. **Novas Visualizações**: Adicione em `visualizer.py`

## Dependências Principais

- **rasterio**: Leitura/escrita de dados raster
- **geopandas**: Manipulação de dados geoespaciais
- **numpy**: Computação numérica
- **scikit-learn**: Machine Learning
- **xgboost**: Gradient boosting
- **matplotlib/seaborn**: Visualização
- **opencv-python**: Processamento de imagens
- **scipy**: Algoritmos científicos

## Considerações de Desempenho

1. **Processamento em Lote**: Processe múltiplas imagens em paralelo
2. **Chunking**: Divida imagens grandes em tiles
3. **Cache**: Cache resultados intermediários
4. **GPU**: Use GPU para deep learning (se disponível)

## Validação

O sistema inclui métricas de validação:
- Acurácia geral
- Coeficiente Kappa
- Precision/Recall/F1-Score
- Matriz de confusão

## Produtos de Saída

1. **GeoTIFF**: Mapas raster georreferenciados
2. **Shapefile**: Vetores de objetos detectados
3. **GeoJSON**: Formato web-friendly
4. **KML**: Visualização no Google Earth
5. **PNG/PDF**: Mapas e gráficos
6. **TXT**: Relatórios textuais

## Boas Práticas

1. **Sempre valide** resultados com dados de campo
2. **Use múltiplas fontes** de dados quando possível
3. **Documente parâmetros** utilizados
4. **Mantenha registro** de versões de algoritmos
5. **Realize validação cruzada** de resultados
