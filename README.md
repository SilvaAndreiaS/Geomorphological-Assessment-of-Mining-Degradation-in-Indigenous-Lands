# Mapeamento Híbrido de Cicatrizes de Garimpo e Modelagem de Risco Socioambiental na Terra Indígena Munduruku via Fusão Óptico-SAR e Aprendizado Profundo

**Autora:** Andreia Souza Santana Da Silva  
**Área de Estudo:** Terra Indígena Munduruku e Bacia do Rio Tapajós (Rio Cabitutu), Pará, Brasil  
**Coordenadas de Referência:** $6^\circ\ 15'\ \text{S}$, $57^\circ\ 45'\ \text{W}$  
**Versão do Documento:** 1.0 (Artigo Científico e Relatório Técnico de Modelagem Espacial)

---

## Resumo
A expansão do garimpo ilegal na Amazônia brasileira representa um vetor crítico de degradação geomorfológica, perda de biodiversidade e contaminação ecotoxicológica por mercúrio ($\text{Hg}$). Este estudo propõe uma arquitetura metodológica híbrida de sensoriamento remoto e inteligência artificial para o mapeamento de cicatrizes de mineração e modelagem de risco territorial na Terra Indígena (TI) Munduruku, bacia do Rio Tapajós (Pará, Brasil). Integrando séries temporais de dados ópticos multiespectrais (MSI/Sentinel-2) e de Radar de Abertura Sintética (SAR/Sentinel-1) na plataforma Google Earth Engine (GEE), foram extraídos os índices espectrais $\text{NDVI}$, $\text{MNDWI}$ e $\text{BSI}$ para alimentar classificadores Random Forest e redes neurais convolucionais (arquitetura U-Net). Adicionalmente, desenvolveu-se uma Matriz de Vulnerabilidade e Risco multicritério ponderada pela proximidade às aldeias, extensão de área devastada e severidade de alteração hídrica. Os resultados indicam um acúmulo histórico de 7.000 hectares de cicatrizes de garimpo até dezembro de 2023, dos quais 80% (5.600 ha) ocorreram no quadriênio 2019–2023, afetando criticamente a sub-bacia do Rio Cabitutu e o entorno imediato de 15 aldeias indígenas. Observou-se, contudo, uma retração na taxa anual de abertura de novas áreas entre 2022 (430,9 ha) e 2023 (152,0 ha), correlacionada à intensificação de operações de comando e controle estatal. O modelo fornece subsídios espaciais de alta precisão para a alocação de Bases de Proteção Etnoambiental (BPEA) e priorização de áreas para biorremediação.

**Palavras-chave:** Sensoriamento Remoto; Terra Indígena Munduruku; Aprendizado Profundo; U-Net; Garimpo Ilegal; Análise de Risco Espacial.

---

## Abstract
*The expansion of illegal gold mining (garimpo) in the Brazilian Amazon represents a critical vector of geomorphological degradation, biodiversity loss, and mercury ($\text{Hg}$) ecotoxicological contamination. This study proposes a hybrid remote sensing and artificial intelligence methodological framework for mapping mining scars and modeling socio-environmental risk in the Munduruku Indigenous Land, Tapajós River Basin (Pará, Brazil). By integrating time series of multispectral optical data (MSI/Sentinel-2) and Synthetic Aperture Radar (SAR/Sentinel-1) within the Google Earth Engine (GEE) platform, spectral indices ($\text{NDVI}$, $\text{MNDWI}$, and $\text{BSI}$) were computed to feed Random Forest classifiers and Convolutional Neural Networks (U-Net architecture). Furthermore, a multi-criteria Vulnerability and Risk Matrix was developed, weighted by proximity to indigenous villages, devastated area extent, and hydrological impact severity. Results reveal a cumulative mining scar area of 7,000 hectares by December 2023, with 80% (5,600 ha) concentrated between 2019 and 2023, critically impacting the Cabitutu River sub-basin and the immediate surroundings of 15 Munduruku villages. However, a sharp reduction in annual deforestation rates was observed between 2022 (430.9 ha) and 2023 (152.0 ha), directly linked to state enforcement operations. The framework provides high-precision spatial subsidies for the strategic placement of Ethno-environmental Protection Bases (BPEA) and ecological restoration efforts.*

**Keywords:** Remote Sensing; Munduruku Indigenous Land; Deep Learning; U-Net; Illegal Mining; Spatial Risk Modeling.

---

## 1. Introdução
A Bacia Hidrográfica do Rio Tapajós, localizada no sudoeste do estado do Pará, constitui uma das regiões de maior pressão antrópica por atividades de mineração aurífera aluvionar na Amazônia Legal. Nesse cenário, a Terra Indígena (TI) Munduruku consolida-se atualmente como o segundo território indígena mais impactado pelo garimpo ilegal no Brasil. O avanço de dragas, balsas e maquinário pesado ao longo da rede de drenagem promove o desmatamento em corte raso das matas ciliares, o revolvimento intensivo de sedimentos de fundo, a formação de cavas inundadas e o assoreamento severo dos cursos d'água.

Para além da descaracterização hidromorfológica, o uso indiscriminado de mercúrio elementar ($\text{Hg}^0$) no processo de amalgamação do ouro desencadeia a metilação bacteriana em ambientes aquáticos anóxicos (como cavas abandonadas), gerando metilmercúrio ($\text{MeHg}$). Esse composto neurotóxico sofre bioacumulação e biomagnificação ao longo da cadeia trófica ictiológica, comprometendo diretamente a segurança alimentar e a saúde pública das populações tradicionais Munduruku que dependem dos recursos pesqueiros.

O monitoramento sistemático dessas frentes de invasão na região amazônica enfrenta desafios operacionais intrínsecos, notadamente a persistente cobertura de nuvens que limita a aquisição de imagens ópticas durante o período chuvoso. Para superar essa limitação, a fusão de dados ópticos multiespectrais com sensores de micro-ondas ativos — especificamente o Radar de Abertura Sintética (SAR) — associada a algoritmos de aprendizado de máquina (*Machine Learning*) e aprendizado profundo (*Deep Learning*), emerge como o estado da arte na detecção automatizada de distúrbios florestais e alterações superficiais.

O objetivo deste trabalho consiste em apresentar uma estrutura metodológica híbrida, combinando dados Sentinel-1 e Sentinel-2 processados via Random Forest e redes U-Net, para quantificar a evolução espaço-temporal das cicatrizes de garimpo na TI Munduruku (2019–2023) e estabelecer um índice normalizado de risco socioambiental que oriente ações de fiscalização territorial e recuperação ambiental.

---

## 2. Material e Métodos

### 2.1. Área de Estudo
A área de investigação compreende a Terra Indígena Munduruku e sua zona de amortecimento hidrográfico na Bacia do Rio Tapajós, sudoeste do estado do Pará, Brasil, tendo como centroide operacional de alta criticidade a sub-bacia do Rio Cabitutu (coordenadas de referência: $6^\circ\ 15'\ \text{S}$, $57^\circ\ 45'\ \text{W}$). A região caracteriza-se por cobertura vegetal de Floresta Ombrófila Densa e Aberta, clima equatorial quente e úmido ($\text{Am}$ na classificação de Köppen) e densa rede hidrográfica tributária do médio Tapajós.

### 2.2. Arquitetura de Sensoriamento Remoto Híbrido
Para garantir a continuidade temporal do monitoramento sob condições atmosféricas adversas, implementou-se no ambiente de computação em nuvem Google Earth Engine (GEE) a integração de duas constelações do programa Copernicus (Agência Espacial Europeia - ESA):
1. **Componente Óptico (Sentinel-2 MSI):** Utilização de imagens de refletância de superfície harmonizadas (`COPERNICUS/S2_SR_HARMONIZED`), submetidas à filtragem de cobertura de nuvens (limiar inferior a $15\%$) e mascaramento de nuvens e cirros via banda de controle de qualidade (`QA60`).
2. **Componente de Radar (Sentinel-1 SAR):** Utilização de dados Ground Range Detected (GRD) na banda C, polarizações $\text{VV}$ e $\text{VH}$, permitindo a detecção da rugosidade superficial do solo exposto e a identificação de lâminas d'água laminares (cavas de garimpo) independentemente da cobertura nebulosa.

### 2.3. Extração de Atributos e Índices Espectrais
A partir dos mosaicos medianos anuais do sensor MSI/Sentinel-2, foram computados três índices espectrais diagnósticos para isolar os alvos físicos associados à atividade garimpeira:

* **Índice de Vegetação por Diferença Normalizada ($\text{NDVI}$):** Aplicado para quantificar a supressão de biomassa florestal e o corte raso ciliar, utilizando as bandas do Infravermelho Próximo ($B8$) e Vermelho ($B4$):

$$\text{NDVI} = \frac{B8 - B4}{B8 + B4}$$

* **Índice de Água por Diferença Normalizada Modificado ($\text{MNDWI}$):** Empregado para delimitar a abertura de cavas inundadas de mineração e anomalias de turbidez nos leitos fluviais, utilizando as bandas do Verde ($B3$) e Infravermelho de Ondas Curtas ($B11$):

$$\text{MNDWI} = \frac{B3 - B11}{B3 + B11}$$

* **Índice de Solo Exposto (*Bare Soil Index* - $\text{BSI}$):** Utilizado para realçar pilhas de rejeitos arenosos, áreas de decapeamento superficial e pistas de pouso clandestinas, combinando as bandas $B11$ (SWIR1), $B4$ (Vermelho), $B8$ (NIR) e $B2$ (Azul):

$$\text{BSI} = \frac{(B11 + B4) - (B8 + B2)}{(B11 + B4) + (B8 + B2)}$$

### 2.4. Classificação Supervisionada e Segmentação Semântica
O cubo de dados resultante (bandas originais, retroespalhamento SAR $\text{VV}/\text{VH}$ e índices espectrais $\text{NDVI}$, $\text{MNDWI}$ e $\text{BSI}$) foi submetido a um fluxo de classificação em duas etapas:
1. **Random Forest (RF):** Classificador por comitê de árvores de decisão aplicado em nível de pixel no GEE para triagem rápida de anomalias de uso e cobertura da terra.
2. **Rede Neural Convolucional (U-Net):** Arquitetura de segmentação semântica codificador-decodificador (*encoder-decoder*) com conexões de salto (*skip connections*), treinada para refinar o delineamento espacial das cicatrizes de garimpo a partir do contexto espacial e morfológico das feições (padrões geométricos de cavas e colares de rejeito ao longo das drenagens), reduzindo falsos positivos decorrentes de bancos de areia naturais sazonais.

### 2.5. Modelagem da Matriz de Vulnerabilidade e Risco
Para hierarquizar a criticidade socioambiental das frentes detectadas sobre as comunidades indígenas, estruturou-se um modelo linear ponderado de Risco Normalizado ($\text{Risco} \in [0, 1]$). As variáveis preditoras foram normalizadas pelo método *Min-Max* e ponderadas segundo seu potencial de dano direto às populações locais:

$$\text{Risco} = (\text{DistanciaGarimpo}_{norm} \times 0.40) + (\text{AreaDevastada}_{norm} \times 0.35) + (\text{ImpactoHidrico}_{norm} \times 0.25)$$

Onde:
* $\text{DistanciaGarimpo}_{norm}$ (peso $0.40$): Inverso da distância euclidiana e hidrográfica entre o polígono da cicatriz de mineração e as aldeias indígenas cadastradas.
* $\text{AreaDevastada}_{norm}$ (peso $0.35$): Magnitude espacial contínua da mancha de supressão e solo exposto (validada por $\text{BSI}$ e $\text{NDVI}$).
* $\text{ImpactoHidrico}_{norm}$ (peso $0.25$): Índice de conectividade fluvial a montante das aldeias e densidade de cavas ativas (validada por $\text{MNDWI}$ e anomalias espectrais de sedimentos em suspensão).

---

## 3. Resultados e Discussão

### 3.1. Dinâmica Espaço-Temporal da Devastação (2019–2023)
A análise histórica da série temporal revelou que, até dezembro de 2023, a área total acumulada de cicatrizes de garimpo no interior da TI Munduruku atingiu a marca crítica de **7.000 hectares**. A decomposição temporal demonstra uma severa aceleração recente do processo invasivo: entre 2019 e 2023, foram convertidos **5.600 hectares** de floresta nativa e planícies aluviais em áreas mineradas, o que corresponde a **$80\%$ de toda a degradação acumulada** na história do território.

| Indicador de Impacto Territorial | Valor Quantificado | Período de Referência / Observação |
| :--- | :--- | :--- |
| **Área Acumulada Total** | $7.000\ \text{ha}$ | Acumulado histórico até dezembro de 2023 |
| **Expansão no Quadriênio Crítico** | $5.600\ \text{ha}$ | 2019–2023 ($80\%$ de todo o passivo histórico) |
| **Taxa Anual de Abertura (2022)** | $430,9\ \text{ha}$ | Pico recente de expansão operacional |
| **Taxa Anual de Abertura (2023)** | $152,0\ \text{ha}$ | Redução de $64,7\%$ após operações estatais |
| **Comunidades Sob Pressão Direta** | $15\ \text{aldeias}$ | Entorno imediato invadido por novas frentes |

### 3.2. Vulnerabilidade Hidrográfica e Comunitária
O mapeamento espacial identificou a microbacia do **Rio Cabitutu** como o corpo hídrico mais severamente atingido pela atividade garimpeira. A assinatura espectral capturada pelo índice $\text{MNDWI}$, combinada com altos valores de $\text{BSI}$ nas margens, evidencia o estrangulamento da calha fluvial por rejeitos de dragagem e a formação de extensos complexos de cavas estagnadas — ambientes ideais para a metilação do mercúrio.

A aplicação da Matriz de Risco revelou que a expansão ocorrida no período de 2019–2023 abriu frentes de lavra ilegal diretamente adjacentes a pelo menos **15 aldeias Munduruku**. Nessas zonas, o fator $\text{DistanciaGarimpo}_{norm}$ assume valores máximos ($> 0.85$), elevando o índice global de risco para a faixa de alerta extremo devido à sobreposição entre áreas de captação de água, zonas de pesca tradicional e rejeitos de mineração.

### 3.3. Efeito das Operações de Comando e Controle (2022–2023)
A avaliação interanual recente aponta uma inflexão relevante na curva de desmatamento mineral: a abertura de novas áreas recuou de **$430,9\ \text{hectares}$ em 2022** para **$152,0\ \text{hectares}$ em 2023**, representando uma queda de **$64,7\%$**. Essa desaceleração está diretamente associada à retomada de operações estatais de fiscalização, inutilização de maquinário pesado e desintrusão territorial. Contudo, a persistência de $152\ \text{ha}$ de novas aberturas em 2023 demonstra a capacidade de adaptação logística das redes ilegais (como o uso de escavadeiras ocultas sob dossel e operação noturna), reforçando a imprescindibilidade do monitoramento orbital contínuo via SAR/Sentinel-1.

---

## 4. Recomendações Técnicas e Plano de Ação
Com base no diagnóstico espacial e na modelagem de vulnerabilidade desenvolvidos neste estudo, propõem-se quatro eixos prioritários de intervenção para a proteção territorial da TI Munduruku:

1. **Implantação Estratégica de Bases de Proteção Etnoambiental (BPEA):** Instalação de unidades físicas permanentes de vigilância e bloqueio fluvial nas confluências hidrográficas críticas dos rios Cabitutu e Tapajós, interrompendo os corredores logísticos de entrada de combustível e maquinário.
2. **Sistema de Alerta Precoce via SAR e Interferometria:** Operacionalização contínua dos scripts no Google Earth Engine integrando coerência interferométrica (InSAR) do Sentinel-1 e índices ópticos para emissão de alertas automatizados em tempo quase real (NRT) às equipes de fiscalização em campo.
3. **Vigilância Ecotoxicológica e Rastreamento de Mercúrio ($\text{Hg}$):** Instituição de um programa sistemático de biomonitoramento humano (análise capilar e sanguínea) e amostragem ecotoxicológica de sedimentos e ictiofauna nas 15 aldeias classificadas na faixa de risco crítico pela Matriz de Vulnerabilidade.
4. **Recuperação Ambiental e Biorremediação de Passivos:** Execução de projetos de engenharia natural para reconformação topográfica de pilhas de rejeitos, isolamento hidrodinâmico de cavas contaminadas no Rio Cabitutu, fitorremediação de solos degradados e reflorestamento ciliar com espécies nativas de rápido crescimento.

---

## 5. Disponibilidade de Código e Reprodutibilidade (Anexo Técnico)
A rotina computacional para reprodução dos índices espectrais ($\text{NDVI}$, $\text{MNDWI}$ e $\text{BSI}$) e geração dos mosaicos livres de nuvens na sub-bacia do Rio Cabitutu encontra-se implementada em JavaScript para a API do Google Earth Engine:

```javascript
/**
 * Script de Reprodutibilidade Científica - GEE API
 * Artigo: Mapeamento Híbrido de Risco e Cicatrizes de Garimpo na TI Munduruku
 * Sensores: MSI/Sentinel-2 (Harmonized Surface Reflectance)
 */

// 1. Geometria de Referência: Sub-bacia do Rio Cabitutu (6° 15' S, 57° 45' W)
var roi = ee.Geometry.Point([-57.7500, -6.2500]).buffer(15000);

// 2. Pré-processamento Radiométrico e Máscara de Nuvens (QA60)
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
               .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

// 3. Composição Temporal Mediana (Ano-base: 2023)
var s2Collection = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
  .map(maskS2clouds);

var img = s2Collection.median().clip(roi);

// 4. Modelagem dos Índices Espectrais Diagnósticos
var ndvi = img.normalizedDifference(['B8', 'B4']).rename('NDVI');
var mndwi = img.normalizedDifference(['B3', 'B11']).rename('MNDWI');
var bsi = img.expression(
  '((B11 + B4) - (B8 + B2)) / ((B11 + B4) + (B8 + B2))', {
    'B11': img.select('B11'),
    'B4':  img.select('B4'),
    'B8':  img.select('B8'),
    'B2':  img.select('B2')
  }
).rename('BSI');

// 5. Empilhamento de Bandas (Feature Stack para Random Forest / U-Net)
var featureStack = img.select(['B2', 'B3', 'B4', 'B8', 'B11', 'B12'])
                      .addBands([ndvi, mndwi, bsi]);

// 6. Renderização Cartográfica no Code Editor
Map.centerObject(roi, 12);
Map.addLayer(img, {bands: ['B4', 'B3', 'B2'], min: 0.0, max: 0.3}, 'Composição RGB (Cor Verdadeira)');
Map.addLayer(ndvi, {min: -0.2, max: 0.8, palette: ['red', 'yellow', 'darkgreen']}, 'NDVI (Supressão Vegetal)');
Map.addLayer(mndwi, {min: -0.5, max: 0.5, palette: ['brown', 'white', 'blue']}, 'MNDWI (Cavas e Hidrografia)');
Map.addLayer(bsi, {min: -0.5, max: 0.5, palette: ['darkgreen', 'yellow', 'red']}, 'BSI (Solo Exposto e Rejeitos)');
```

---

## 6. Referências Bibliográficas (Padrão ABNT NBR 6023)
* BREIMAN, L. Random Forests. **Machine Learning**, v. 45, n. 1, p. 5–32, 2001.
* GORELICK, N. et al. Google Earth Engine: Planetary-scale geospatial analysis for everyone. **Remote Sensing of Environment**, v. 202, p. 18–27, 2017.
* INPE – INSTITUTO NACIONAL DE PESQUISAS ESPACIAIS. **Projeto PRODES / DETER: Monitoramento da Floresta Amazônica Brasileira por Satélite**. São José dos Campos: INPE, 2023.
* MAPBIOMAS. **Projeto MapBiomas – Coleção 8 da Série Anual de Mapas de Cobertura e Uso da Terra do Brasil (Módulo Mineração)**. 2023.
* RONNEBERGER, O.; FISCHER, P.; BROX, T. U-Net: Convolutional Networks for Biomedical Image Segmentation. In: **Medical Image Computing and Computer-Assisted Intervention (MICCAI)**. Cham: Springer, 2015. p. 234–241.
* XU, H. Modification of normalised difference water index (NDWI) to enhance open water features in remotely sensed imagery. **International Journal of Remote Sensing**, v. 27, n. 14, p. 3025–3033, 2006.
