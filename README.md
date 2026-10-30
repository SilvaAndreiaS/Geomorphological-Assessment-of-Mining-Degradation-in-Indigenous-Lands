# Mapeamento Híbrido de Risco e Cicatrizes de Garimpo: Subsídio à Proteção da TI Munduruku
**Área de Estudo:** Terra Indígena Munduruku e Bacia do Rio Tapajós (Rio Cabitutu), Pará, Brasil  
**Coordenadas de Referência:** $6^\circ\ 15'\ \text{S}$, $57^\circ\ 45'\ \text{W}$  
**Versão do Documento:** 1.0 (Relatório Final de Metodologia e Avaliação de Risco)

---

## 1. Contexto Geral e Justificativa Diagnóstica
A Terra Indígena (TI) Munduruku, localizada no sudoeste do estado do Pará na Bacia Hidrográfica do Rio Tapajós, consolida-se atualmente como o segundo território indígena mais devastado pela atividade garimpeira no Brasil. O avanço das frentes de mineração ilegal de ouro ao longo dos principais leitos fluviais provocou alterações morfológicas profundas na paisagem, além de severa contaminação por mercúrio ($\text{Hg}$).

### Dados Chave do Impacto Territorial (2019–2023)
- **Área Acumulada de Garimpo (dez/2023):** 7.000 hectares.
- **Ritmo de Devastação Recente:** Entre 2019 e 2023, foram destruídos 5.600 hectares (80% do histórico acumulado).
- **Invasão do Entorno Comunitário:** Novas frentes abertas adjacentes a pelo menos 15 aldeias Munduruku.
- **Corpo Hídrico Mais Atingido:** Rio Cabitutu.
- **Dinâmica Recente:** Queda de 430,9 ha (2022) para 152 ha (2023) por operações estatais.

---

## 2. Metodologia Híbrida de Sensoriamento Remoto
Combinação de dados ópticos (MSI/Sentinel-2) e Radar de Abertura Sintética (SAR/Sentinel-1) integrados via Random Forest e U-Net.

### Índices Espectrais:
- **NDVI:** $(B8 - B4) / (B8 + B4)$ (Corte raso / Supressão vegetal)
- **MNDWI:** $(B3 - B11) / (B3 + B11)$ (Cavas e alteração hídrica)
- **BSI:** $[(B11 + B4) - (B8 + B2)] / [(B11 + B4) + (B8 + B2)]$ (Solo exposto / Rejeitos)

---

## 3. Matriz de Vulnerabilidade e Risco
Fórmula de Cálculo do Risco Normalizado:
$$Risco = (DistanciaGarimpo_{norm} \times 0.40) + (AreaDevastada_{norm} \times 0.35) + (ImpactoHidrico_{norm} \times 0.25)$$

---

## 4. Recomendações e Plano de Ação
1. Bases de Proteção Etnoambiental (BPEA) nas confluências dos rios Cabitutu e Tapajós.
2. Alertas em tempo real via SAR / Interferometria no Google Earth Engine.
3. Rastreamento de contaminação por $\text{Hg}$ nas 15 aldeias.
4. Reflorestamento e biorremediação de cavas abandonadas.

---

## 5. Implementação no Google Earth Engine (JavaScript)
Script de referência para o cálculo automatizado dos índices espectrais **NDVI**, **MNDWI** e **BSI** na área de estudo:

```javascript
// 1. Definição da Área de Interesse (ROI) - Rio Cabitutu / TI Munduruku
var roi = ee.Geometry.Point([-57.7500, -6.2500]).buffer(15000);

// 2. Máscara de nuvens para Sentinel-2 SR
function maskS2clouds(image) {
  var qa = image.select('QA60');
  var cloudBitMask = 1 << 10;
  var cirrusBitMask = 1 << 11;
  var mask = qa.bitwiseAnd(cloudBitMask).eq(0)
               .and(qa.bitwiseAnd(cirrusBitMask).eq(0));
  return image.updateMask(mask).divide(10000);
}

// 3. Carregamento e filtragem da coleção Sentinel-2 (2023)
var img = ee.ImageCollection('COPERNICUS/S2_SR_HARMONIZED')
  .filterBounds(roi)
  .filterDate('2023-01-01', '2023-12-31')
  .filter(ee.Filter.lt('CLOUDY_PIXEL_PERCENTAGE', 15))
  .map(maskS2clouds)
  .median()
  .clip(roi);

// 4. Cálculo dos Índices Espectrais
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

// 5. Visualização no Mapa
Map.centerObject(roi, 11);
Map.addLayer(img, {bands: ['B4', 'B3', 'B2'], min: 0.0, max: 0.3}, 'Sentinel-2 RGB');
Map.addLayer(ndvi, {min: -1, max: 1, palette: ['brown', 'yellow', 'darkgreen']}, 'NDVI');
Map.addLayer(mndwi, {min: -1, max: 1, palette: ['brown', 'white', 'blue']}, 'MNDWI');
Map.addLayer(bsi, {min: -1, max: 1, palette: ['green', 'yellow', 'red']}, 'BSI');
```
