# Plano de Testes e Homologação (QA/QC)
## Projeto TI Munduruku — Mapeamento Híbrido

### 1. Testes Unitários de Código
- **Python (`monitor_garimpo.py`):** Validação dos intervalos matemáticos dos índices espectrais (NDVI, MNDWI, BSI) no intervalo $[-1.0, 1.0]$.
- **Java (`MatrizRiscoAldeias.java`):** Testes de borda para cálculo do risco (distância $= 0$, área $= 0$, normalizações).

### 2. Testes de Interface Web
- **Dashboard (`painel_interativo.html`):** Teste de responsividade em layouts Desktop e Mobile, renderização correta das bibliotecas Chart.js via CDN.

### 3. Validação do Classificador Machine Learning
- Avaliação do modelo U-Net / Random Forest com amostras de verdade terrestre:
  - Exatidão Global $\ge 92\%$
  - $F1	ext{-Score} \ge 0.88$ para cicatrizes garimpeiras.
