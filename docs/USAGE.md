# Guia de Uso - Sistema de Detecção de Garimpo Ilegal

## Visão Geral

Este sistema implementa uma abordagem híbrida de processamento de imagens de Sensoriamento Remoto para mapear e monitorar cicatrizes de garimpo ilegal na Terra Indígena Munduruku, Bacia do Rio Tapajós, Pará.

## Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Instalação de Dependências

```bash
pip install -r requirements.txt
```

## Estrutura do Projeto

```
├── config/                    # Arquivos de configuração
│   └── munduruku_config.yaml # Configuração principal
├── src/                       # Código fonte
│   ├── data_acquisition/      # Aquisição de dados de satélite
│   ├── preprocessing/         # Pré-processamento de imagens
│   ├── classification/        # Classificação híbrida
│   ├── detection/            # Detecção de cicatrizes
│   ├── monitoring/           # Monitoramento temporal
│   ├── visualization/        # Visualização e relatórios
│   └── utils/                # Utilitários
├── docs/                     # Documentação
├── examples/                 # Exemplos de uso
├── main_pipeline.py          # Pipeline principal
└── requirements.txt          # Dependências
```

## Uso Básico

### Modo Demonstração

Execute o sistema em modo demonstração com dados sintéticos:

```bash
python main_pipeline.py --demo --output results/demo
```

### Uso com Imagens Reais

```bash
python main_pipeline.py \
    --image caminho/para/imagem.tif \
    --baseline caminho/para/baseline.tif \
    --output results/munduruku
```

### Opções de Linha de Comando

- `--config`: Caminho para arquivo de configuração personalizado
- `--image`: Caminho para imagem de entrada
- `--baseline`: Caminho para imagem de linha de base (opcional)
- `--output`: Diretório de saída (padrão: results)
- `--demo`: Executa em modo demonstração

## Componentes Principais

### 1. Aquisição de Dados

```python
from src.data_acquisition.satellite_data import SatelliteDataAcquisition

# Inicializa módulo de aquisição
acquisition = SatelliteDataAcquisition(config)

# Busca dados Sentinel-2
results = acquisition.search_sentinel2_data(
    start_date="2024-01-01",
    end_date="2024-12-31",
    max_cloud_coverage=20
)
```

### 2. Pré-processamento

```python
from src.preprocessing.image_preprocessing import ImagePreprocessor

# Inicializa pré-processador
preprocessor = ImagePreprocessor(config)

# Aplica pré-processamento completo
preprocessed_image = preprocessor.apply_full_preprocessing(
    image_data,
    dem=dem_data,
    cloud_mask=cloud_mask
)
```

### 3. Classificação Híbrida

```python
from src.classification.hybrid_classifier import HybridClassifier

# Inicializa classificador
classifier = HybridClassifier(config)

# Classifica imagem
classification = classifier.classify(
    image_data,
    training_data=(X_train, y_train),
    band_mapping={'blue': 0, 'green': 1, 'red': 2, 'nir': 3}
)
```

### 4. Detecção de Cicatrizes

```python
from src.detection.mining_scar_detector import MiningScarDetector

# Inicializa detector
detector = MiningScarDetector(config)

# Detecta cicatrizes
binary_mask, mining_objects = detector.detect_mining_scars(classification)

# Gera relatório
report = detector.generate_detection_report(mining_objects)
```

### 5. Monitoramento de Mudanças

```python
from src.monitoring.change_detection import ChangeDetector

# Inicializa detector de mudanças
change_detector = ChangeDetector(config)

# Detecta mudanças
change_types, stats = change_detector.classify_change_types(
    baseline_classification,
    comparison_classification
)
```

### 6. Visualização

```python
from src.visualization.visualizer import ResultsVisualizer

# Inicializa visualizador
visualizer = ResultsVisualizer(config)

# Plota mapa de classificação
visualizer.plot_classification_map(
    classification,
    save_path="results/classification_map.png"
)

# Gera dashboard
visualizer.plot_statistics_dashboard(
    detection_report,
    change_stats=change_stats,
    save_path="results/dashboard.png"
)
```

## Configuração

O arquivo `config/munduruku_config.yaml` contém todas as configurações do sistema:

- **study_area**: Coordenadas e informações da área de estudo
- **satellite_data**: Fontes de dados e critérios de qualidade
- **preprocessing**: Parâmetros de pré-processamento
- **classification**: Configuração da abordagem híbrida
- **detection**: Critérios de detecção de cicatrizes
- **monitoring**: Parâmetros de monitoramento temporal
- **output**: Formatos e resolução de saída
- **visualization**: Estilos e cores para visualização

## Produtos Gerados

O sistema gera os seguintes produtos:

1. **Mapas de Classificação**: Mapas temáticos da cobertura do solo
2. **Mapas de Mudanças**: Mapas mostrando expansão/retração de garimpo
3. **Inventário de Cicatrizes**: Lista detalhada de objetos detectados
4. **Análise Temporal**: Gráficos de evolução temporal
5. **Dashboard Estatístico**: Painel com estatísticas principais
6. **Relatórios**: Relatórios em formato texto
7. **Arquivos Geoespaciais**: GeoTIFF, Shapefile, GeoJSON

## Abordagem Híbrida

O sistema combina múltiplas técnicas:

### Métodos Tradicionais
- Classificação supervisionada (Maximum Likelihood)
- Classificação não supervisionada (K-means)
- Índices espectrais (NDVI, NDWI, NDMI, BSI)
- Spectral Angle Mapper (SAM)

### Machine Learning
- Random Forest
- XGBoost
- Support Vector Machine (SVM)

### Ensemble
- Votação majoritária
- Média ponderada
- Stacking

## Métricas de Validação

O sistema calcula as seguintes métricas:

- Acurácia geral (Overall Accuracy)
- Coeficiente Kappa
- Precisão (Precision)
- Revocação (Recall)
- F1-Score
- Matriz de Confusão

## Detecção de Mudanças

Tipos de mudança detectados:

1. **Nova Área de Garimpo**: Áreas que não existiam no período anterior
2. **Expansão**: Crescimento de áreas existentes
3. **Retração**: Redução de áreas de garimpo
4. **Recuperação**: Áreas que voltaram a ter vegetação
5. **Estável**: Áreas sem mudança significativa

## Alertas

O sistema pode gerar alertas automáticos quando:

- Nova área de garimpo é detectada acima do threshold configurado
- Expansão rápida é identificada
- Mudanças em áreas críticas são observadas

## Troubleshooting

### Erro: "Arquivo de configuração não encontrado"
- Verifique se o arquivo `config/munduruku_config.yaml` existe
- Use `--config` para especificar um caminho personalizado

### Erro: "Módulo não encontrado"
- Instale as dependências: `pip install -r requirements.txt`
- Verifique sua versão do Python: `python --version`

### Problemas de memória
- Reduza a resolução das imagens
- Processe áreas menores por vez
- Aumente a memória disponível

## Suporte

Para questões e suporte:
- Consulte a documentação completa em `docs/`
- Veja exemplos em `examples/`
- Abra uma issue no repositório

## Referências

Este sistema foi desenvolvido baseado em melhores práticas de:
- Sensoriamento Remoto
- Processamento Digital de Imagens
- Machine Learning para Classificação de Imagens
- Análise de Mudanças Temporais
