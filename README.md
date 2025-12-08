# Sistema de Detecção de Garimpo Ilegal - Terra Indígena Munduruku

## 🎯 Objetivo

O principal objetivo deste projeto é desenvolver e aplicar uma **abordagem híbrida de processamento de imagens de Sensoriamento Remoto** para o mapeamento e monitoramento precisos das cicatrizes de garimpo ilegal na Terra Indígena Munduruku, localizada na Bacia do Rio Tapajós, no estado do Pará.

## 🌟 Características Principais

### Abordagem Híbrida Inovadora

Este sistema combina o melhor de dois mundos:

**Métodos Tradicionais de Sensoriamento Remoto:**
- Classificação Supervisionada (Maximum Likelihood)
- Classificação Não Supervisionada (K-means)
- Índices Espectrais (NDVI, NDWI, NDMI, BSI)
- Spectral Angle Mapper (SAM)

**Técnicas de Machine Learning:**
- Random Forest
- XGBoost
- Support Vector Machine (SVM)
- Ensemble Learning (Votação e Média Ponderada)

### Funcionalidades Completas

✅ **Aquisição de Dados**: Suporte para Sentinel-2, Landsat-8 e outras fontes
✅ **Pré-processamento Avançado**: Correção atmosférica, normalização, remoção de nuvens
✅ **Classificação Híbrida**: Combinação de métodos tradicionais e ML
✅ **Detecção de Cicatrizes**: Identificação e caracterização de áreas de garimpo
✅ **Monitoramento Temporal**: Análise de mudanças ao longo do tempo
✅ **Alertas Automáticos**: Notificações de nova atividade mineradora
✅ **Visualização Rica**: Mapas, gráficos e dashboards informativos
✅ **Relatórios Detalhados**: Documentação completa dos resultados

## 📦 Instalação

### Requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passo a Passo

1. Clone o repositório:
```bash
git clone https://github.com/SilvaAndreiaS/n-lise-do-Impacto-Morfol-gico-do-Garimpo-Fluvial-e-Terrestre-em-Terras-Ind-genas.git
cd n-lise-do-Impacto-Morfol-gico-do-Garimpo-Fluvial-e-Terrestre-em-Terras-Ind-genas
```

2. Instale as dependências:
```bash
pip install -r requirements.txt
```

## 🚀 Uso Rápido

### Modo Demonstração

Execute o sistema em modo demonstração com dados sintéticos:

```bash
python main_pipeline.py --demo --output results/demo
```

### Uso com Imagens Reais

```bash
python main_pipeline.py \
    --image caminho/para/imagem_atual.tif \
    --baseline caminho/para/imagem_baseline.tif \
    --output results/munduruku
```

### Exemplos de Código

Execute os exemplos incluídos:

```bash
python examples/example_usage.py
```

## 📊 Pipeline de Processamento

O sistema executa as seguintes etapas:

```
1. AQUISIÇÃO DE DADOS
   └─ Sentinel-2 / Landsat-8
   
2. PRÉ-PROCESSAMENTO
   ├─ Correção Atmosférica
   ├─ Normalização Radiométrica
   ├─ Correção Topográfica
   └─ Remoção de Nuvens/Sombras
   
3. CLASSIFICAÇÃO HÍBRIDA
   ├─ Extração de Features Espectrais
   ├─ Cálculo de Índices (NDVI, NDWI, NDMI, BSI)
   ├─ Métodos Tradicionais
   ├─ Machine Learning (RF, XGBoost, SVM)
   └─ Ensemble Learning
   
4. DETECÇÃO DE CICATRIZES
   ├─ Segmentação de Objetos
   ├─ Análise Morfológica
   ├─ Classificação: Ativo vs Abandonado
   └─ Análise de Contexto Espacial
   
5. MONITORAMENTO TEMPORAL
   ├─ Detecção de Mudanças
   ├─ Análise Multi-temporal
   ├─ Geração de Alertas
   └─ Análise de Tendências
   
6. VISUALIZAÇÃO E RELATÓRIOS
   ├─ Mapas Temáticos
   ├─ Mapas de Mudanças
   ├─ Gráficos Temporais
   ├─ Dashboard Estatístico
   └─ Relatórios em Texto
```

## 📂 Estrutura do Projeto

```
├── config/                           # Configurações
│   └── munduruku_config.yaml        # Config principal
│
├── src/                              # Código fonte
│   ├── data_acquisition/             # Aquisição de dados
│   │   └── satellite_data.py
│   ├── preprocessing/                # Pré-processamento
│   │   └── image_preprocessing.py
│   ├── classification/               # Classificação
│   │   └── hybrid_classifier.py
│   ├── detection/                    # Detecção
│   │   └── mining_scar_detector.py
│   ├── monitoring/                   # Monitoramento
│   │   └── change_detection.py
│   ├── visualization/                # Visualização
│   │   └── visualizer.py
│   └── utils/                        # Utilitários
│       └── config_loader.py
│
├── docs/                             # Documentação
│   └── USAGE.md                      # Guia de uso detalhado
│
├── examples/                         # Exemplos
│   └── example_usage.py              # Exemplos de código
│
├── main_pipeline.py                  # Pipeline principal
├── requirements.txt                  # Dependências
└── README.md                         # Este arquivo
```

## 🎨 Produtos Gerados

O sistema gera diversos produtos úteis:

1. **Mapas de Classificação**: Identificação de classes de cobertura do solo
2. **Mapas de Mudanças**: Visualização de expansão/retração de garimpo
3. **Inventário de Cicatrizes**: Lista detalhada com localização e características
4. **Séries Temporais**: Evolução da área de garimpo ao longo do tempo
5. **Dashboard Estatístico**: Painel com métricas principais
6. **Relatórios**: Documentação completa em formato texto
7. **Arquivos Geoespaciais**: GeoTIFF, Shapefile, GeoJSON, KML

## 🔧 Configuração

O arquivo `config/munduruku_config.yaml` permite personalizar:

- Área de estudo e coordenadas
- Fontes de dados de satélite
- Parâmetros de pré-processamento
- Algoritmos de classificação
- Critérios de detecção
- Thresholds de alertas
- Estilos de visualização

## 📈 Métricas de Validação

O sistema calcula:

- **Acurácia Geral (Overall Accuracy)**
- **Coeficiente Kappa**
- **Precisão (Precision)**
- **Revocação (Recall)**
- **F1-Score**
- **Matriz de Confusão**

## 🌍 Área de Estudo

**Terra Indígena Munduruku**
- **Localização**: Bacia do Rio Tapajós, Pará, Brasil
- **Coordenadas**: Aproximadamente 6°-8°S, 56.5°-58.5°W
- **Importância**: Uma das áreas mais afetadas por garimpo ilegal na Amazônia

## 📚 Documentação Adicional

- [Guia de Uso Detalhado](docs/USAGE.md)
- [Exemplos de Código](examples/example_usage.py)

## 🤝 Contribuindo

Contribuições são bem-vindas! Por favor:

1. Faça um Fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob licença apropriada para pesquisa e conservação ambiental.

## 👥 Autores

Projeto desenvolvido para apoiar o monitoramento e proteção da Terra Indígena Munduruku.

## 🙏 Agradecimentos

Este sistema foi desenvolvido com o objetivo de contribuir para a proteção dos territórios indígenas e da Amazônia contra o garimpo ilegal.

## 📧 Contato

Para questões, sugestões ou colaborações, por favor abra uma issue neste repositório.

---

**⚠️ Nota Importante**: Este sistema é uma ferramenta de apoio à decisão. As detecções automáticas devem ser validadas por especialistas e verificadas em campo quando possível.
