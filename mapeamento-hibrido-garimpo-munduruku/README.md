# Mapeamento Híbrido de Risco e Cicatrizes de Garimpo: Subsídio à Proteção da TI Munduruku

**Área:** Sensoriamento Remoto, Processamento Digital de Imagens, Ciência de Dados e Geoprocessamento  
**Local de estudo:** Terra Indígena Munduruku, bacia do rio Tapajós, Pará, Brasil  
**Status:** Em desenvolvimento  

## 1. Visão geral
Este projeto propõe desenvolver uma abordagem híbrida de processamento de imagens de sensoriamento remoto para identificar, mapear e monitorar cicatrizes de garimpo na Terra Indígena Munduruku, localizada na bacia do rio Tapajós, no estado do Pará.

A proposta combina análise espectral, processamento de imagens, classificação computacional e análise espacial para distinguir áreas potencialmente afetadas pelo garimpo de outras feições da paisagem. O objetivo é produzir informações geoespaciais que possam subsidiar o monitoramento ambiental, a fiscalização e a proteção territorial.

## 2. Contexto e relevância socioambiental
A atividade garimpeira pode provocar desmatamento, remoção do solo, alteração da drenagem, degradação de ecossistemas e riscos de contaminação dos recursos hídricos. Na Terra Indígena Munduruku, o monitoramento dessas alterações é particularmente importante devido à pressão sobre o território e aos possíveis impactos sobre comunidades indígenas e ambientes fluviais.

## 3. Estrutura do Repositório
```text
mapeamento-hibrido-garimpo-munduruku/
├── README.md
├── requirements.txt
├── .gitignore
├── docs/
│   ├── metodologia.md
│   ├── fundamentacao_teorica.md
│   └── referencias.md
├── data/
│   └── README.md
├── notebooks/
│   ├── 01_analise_imagens.ipynb
│   ├── 02_indices_espectrais.ipynb
│   ├── 03_classificacao_hibrida.ipynb
│   └── 04_mapeamento_risco.ipynb
├── src/
│   ├── preprocessamento.py
│   ├── indices_espectrais.py
│   ├── classificacao.py
│   ├── analise_temporal.py
│   └── avaliacao.py
├── results/
│   └── README.md
└── figures/
    └── fluxograma_metodologico.png
```

## ⚙️ Como Executar
1. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
2. Explore os notebooks em `notebooks/` para acompanhar o fluxo de análise e processamento.
