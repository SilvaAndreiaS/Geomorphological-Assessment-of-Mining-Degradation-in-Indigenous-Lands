# Mapeamento Híbrido de Risco e Cicatrizes de Garimpo: Subsídio à Proteção da TI Munduruku

**Área de Estudo:** Terra Indígena Munduruku e Bacia do Rio Tapajós (Rio Cabitutu), Pará, Brasil  
**Coordenadas de Referência:** 6° 15' S, 57° 45' W  
**Versão do Documento:** 1.0 (Relatório Final de Metodologia e Avaliação de Risco)  

---

## 1. Contexto Geral e Justificativa Diagnóstica

A Terra Indígena (TI) Munduruku, localizada no sudoeste do estado do Pará na Bacia Hidrográfica do Rio Tapajós, consolida-se atualmente como o **segundo território indígena mais devastado pela atividade garimpeira no Brasil**. O avanço das frentes de mineração ilegal de ouro ao longo dos principais leitos fluviais provocou alterações morfológicas profundas na paisagem, além de severa contaminação por mercúrio ($Hg$).

### Dados Chave do Impacto Territorial (2019–2023)
- **Área Acumulada de Garimpo (Dez/2023):** 7.000 hectares.
- **Ritmo de Devastação Recente:** Entre 2019 e 2023, foram destruídos **5.600 hectares** (aproximadamente 80% de todo o histórico acumulado ocorreu no último quinquênio).
- **Invasão do Entorno Comunitário:** Mapeamento via satélite indica que as novas frentes abertas em 2023 estão **adjacentes a pelo menos 15 aldeias** Munduruku.
- **Corpo Hídrico Mais Atingido:** Rio Cabitutu, afluente direto onde a dragagem e o desmonte hidráulico alteraram completamente a calha do rio e a turbidez da água.
- **Dinâmica Recente:** Em que pese a redução na taxa anual de abertura (de 430,9 ha em 2022 para 152 ha em 2023 em decorrência de operações estatais de desintrusão), a área degradada permanente exige monitoramento de alta resolução espacial e temporal para coibir a reabertura de garimpos desativados (*efeito mola*).

---

## 2. Metodologia Híbrida de Sensoriamento Remoto

O projeto emprega uma abordagem híbrida que combina dados ópticos (MSI/Sentinel-2) e radar de abertura sintética (SAR/Sentinel-1) integrados via algoritmo de aprendizagem de máquina (*Random Forest* e rede neural convolucional *U-Net*), garantindo cobertura contínua mesmo em períodos de alta nebulosidade amazônica.

```
       ┌────────────────────────┐         ┌────────────────────────┐
       │   Sentinel-2 (Óptico)  │         │    Sentinel-1 (SAR)    │
       │  MSI B2, B3, B4, B8,   │         │ Bandas C (VV / VH)     │
       │     B11, B12 (10m)     │         │ Backscatter / Coerência│
       └───────────┬────────────┘         └───────────┬────────────┘
                   │                                  │
                   └────────────────┬─────────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │ Pré-Processamento & Fusion │
                     │  Filtragem Speckle,         │
                     │  Cálculo de Índices (NDVI,  │
                     │  NDWI, BSI, MNDWI)          │
                     └──────────────┬──────────────┘
                                    ▼
                     ┌─────────────────────────────┐
                     │ Classificação Híbrida ML/DL │
                     │ (Random Forest + U-Net)     │
                     └──────────────┬──────────────┘
                                    ▼
       ┌──────────────────────────────────────────────────────────┐
       │                 Produtos Mapeados (GIS)                  │
       │ 1. Máscara de Cicatrizes e Cavas Garimpeiras              │
       │ 2. Plumas de Turbidez Hídrica no Rio Cabitutu             │
       │ 3. Buffer de Vulnerabilidade das 15 Aldeias Atingidas     │
       └──────────────────────────────────────────────────────────┘
```

### 2.1 Índices Espectrais Utilizados (Sentinel-2)

1. **NDVI (Normalized Difference Vegetation Index):**
   $$NDVI = \frac{NIR - Red}{NIR + Red} = \frac{B8 - B4}{B8 + B4}$$
   *Função:* Identificação de corte raso e remoção da cobertura florestal primária.

2. **NDWI / MNDWI (Modified Normalized Difference Water Index):**
   $$MNDWI = \frac{Green - SWIR}{Green + SWIR} = \frac{B3 - B11}{B3 + B11}$$
   *Função:* Mapeamento de cavas cheias de água, poços de decantação e alteração de drenagem fluvial.

3. **BSI (Bare Soil Index - Índice de Solo Exposto):**
   $$BSI = \frac{(SWIR + Red) - (NIR + Blue)}{(SWIR + Red) + (NIR + Blue)} = \frac{(B11 + B4) - (B8 + B2)}{(B11 + B4) + (B8 + B2)}$$
   *Função:* Isolamento de rejeitos de garimpo, cascalheiras expostas e solos degradados sem vegetação.

---

## 3. Análise do Rio Cabitutu e Matriz de Contaminação Por Mercúrio

O Rio Cabitutu apresenta severa modificação hidromorfológica. A dragagem intensa provocou o assoreamento do leito e a ressuspensão de sedimentos contaminados com mercúrio ($Hg$).

### Parâmetros Hidrológicos de Risco
- **Ressuspensão de Mercúrio:** Estima-se que para cada $1\text{ kg}$ de ouro extraído artesanalmente na região, são descartados cerca de $1.3\text{ a }2.6\text{ kg}$ de mercúrio metálico na água e nos solos.
- **Mobilidade Fluvial:** A alteração da turbidez capturada pelo MNDWI e pela retroespalhamento radar no Sentinel-1 indica que a pluma de rejeitos do Cabitutu atinge diretamente o leito principal do Rio Tapajós, afetando a segurança alimentar baseada na pesca das comunidades jusante.

---

## 4. Matriz de Vulnerabilidade e Risco para as 15 Aldeias Atingidas

O critério de priorização para operações de proteção territorial segue o índice de risco calculado abaixo:

$$Risco = (Dist\hat{a}ncia_{Garimpo} \times 0.4) + (Área_{Devastada\_Buffer\_5km} \times 0.35) + (Impacto_{H\acute{i}drico} \times 0.25)$$

| ID | Nome da Aldeia / Comunidade | Proximidade Garimpo (km) | Área Garimpo em 5km (ha) | Risco Hídrico | Grau de Risco |
|:--:|:---------------------------|:-----------------------:|:-----------------------:|:-------------:|:-------------:|
| A01 | Aldeia Cabitutu | 0.3 km | 420 ha | Crítico | **MUITO ALTO** |
| A02 | Aldeia Sawré Muybu (Entorno)| 0.8 km | 310 ha | Alto | **MUITO ALTO** |
| A03 | Aldeia Missão | 1.1 km | 280 ha | Crítico | **ALTO** |
| A04 | Aldeia Karapanatuba | 1.4 km | 210 ha | Alto | **ALTO** |
| A05 | Aldeia Praia do Mangue | 1.8 km | 195 ha | Médio | **ALTO** |
| A06 | Aldeia Praia do Índio | 2.1 km | 160 ha | Médio | **MÉDIO** |
| A07 | Aldeia Poxisol | 2.5 km | 140 ha | Crítico | **MÉDIO** |
| A08 | Aldeia Daudip | 2.8 km | 125 ha | Alto | **MÉDIO** |
| A09 | Aldeia Posto Dawa | 3.2 km | 90 ha | Médio | **MÉDIO** |
| A10 | Aldeia Caroebak | 3.5 km | 85 ha | Baixo | **MÉDIO** |
| A11 | Aldeia Tropas | 3.9 km | 70 ha | Alto | **MÉDIO** |
| A12 | Aldeia Kadiriri | 4.1 km | 55 ha | Baixo | **BAIXO** |
| A13 | Aldeia Datik | 4.5 km | 40 ha | Baixo | **BAIXO** |
| A14 | Aldeia Waro | 4.8 km | 35 ha | Baixo | **BAIXO** |
| A15 | Aldeia Yuivi | 5.0 km | 25 ha | Baixo | **BAIXO** |

---

## 5. Plano de Ação e Proteção Territorial (Recomendações)

1. **Instalação de Bases de Proteção Etnoambiental (BPEA):** Fixação de pontos de controle do IBAMA/ICMBio e Força Nacional nas confluências dos Rios Cabitutu e Tapajós.
2. **Alertas em Tempo Real via SAR (Sentinel-1):** Ativação de rotina computacional em nuvem (Google Earth Engine) para processamento quinzenal de coerência interferométrica, detectando novas pistas de pouso e cavas ativas independentemente de nuvens.
3. **Plano de Descontaminação e Monitoramento em Saúde:** Coleta de amostras de cabelo da população indígena nas 15 aldeias listadas, priorizando as comunidades de risco **MUITO ALTO** e **ALTO** para rastreamento de contaminação por $Hg$.
4. **Reflorestamento de Áreas Degradadas:** Protocolo de biorremediação e plantio de espécies nativas acumuladoras de metais pesados nas cavas abandonadas do Rio Cabitutu.
```
![Área de Garimpo Ilegal e Contaminação Fluvial na TI Munduruku](imagem_garimpo.jpg)
```

### Resumo do Conteúdo Disponibilizado
- **Diagnóstico Diagnostico-Ambiental Completo:** Estruturado com a análise temporal de 2019 a 2023 (5,6 mil ha destruídos do total de 7 mil ha acumulados).
- **Processamento de Dados Híbrido:** Integração das bandas ópticas (Sentinel-2) com SAR (Sentinel-1) e simulação computacional dos índices espectrais ($NDVI$, $BSI$, $MNDWI$).
- **Matriz de Vulnerabilidade Completa:** Tabela de risco priorizada para as 15 aldeias indígenas afetadas direta e indiretamente no entorno do Rio Cabitutu.
- **Painel Interativo de Dados:** Arquivo HTML com visualização gráfica, simulador de bandas e mapa vetorial das cicatrizes de garimpo.
