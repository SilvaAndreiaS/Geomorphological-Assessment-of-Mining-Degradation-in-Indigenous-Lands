# Avaliação geomorfológica da degradação causada pela mineração em terras indígenas
**Visibilidade:** Público  
**Área de Estudo:** Terra Indígena Munduruku e Bacia do Rio Tapajós (Rio Cabitutu), Pará, Brasil  
**Coordenadas de Referência:** 6° 15' S, 57° 45' W  
**Versão do Documento:** 1.0 (Relatório Final de Metodologia e Avaliação de Risco)

---

## Descrição do Projeto
O principal objetivo deste projeto é desenvolver e aplicar uma abordagem híbrida de processamento de imagens de Sensoriamento Remoto para o mapeamento e monitoramento precisos das cicatrizes de garimpo ilegal na Terra Indígena Munduruku, localizada na Bacia do Rio Tapajós, no estado do Pará.

---

## 1. Contexto Geral e Justificativa Diagnóstica
A Terra Indígena (TI) Munduruku consolida-se atualmente como o segundo território indígena mais devastado pela atividade garimpeira no Brasil. O avanço das frentes de mineração ilegal de ouro ao longo dos principais leitos fluviais provocou alterações morfológicas profundas na paisagem, além de severa contaminação por mercúrio (Hg).

### Dados Chave do Impacto Territorial (2019–2023)
- **Área Acumulada de Garimpo (dez/2023):** 7.000 hectares.
- **Ritmo de Devastação Recente:** Entre 2019 e 2023, foram destruídos 5.600 hectares (aproximadamente 80% do histórico acumulado).
- **Invasão do Entorno Comunitário:** Novas frentes abertas adjacentes a pelo menos 15 aldeias Munduruku.
- **Corpo Hídrico Mais Atingido:** Rio Cabitutu, onde a dragagem e o desmonte hidráulico alteraram a calha do rio.

---

## 2. Metodologia Híbrida de Sensoriamento Remoto
Combinação de dados ópticos (MSI/Sentinel-2) e Radar de Abertura Sintética (SAR/Sentinel-1) integrados via algoritmos de aprendizagem de máquina (Random Forest e rede neural U-Net).

### Índices Espectrais:
- **NDVI:** $(B8 - B4) / (B8 + B4)$ (Corte raso / Supressão vegetal)
- **MNDWI:** $(B3 - B11) / (B3 + B11)$ (Cavas e alteração hídrica)
- **BSI:** $[(B11 + B4) - (B8 + B2)] / [(B11 + B4) + (B8 + B2)]$ (Solo exposto / Rejeitos)

---

## 3. Matriz de Vulnerabilidade e Risco
Fórmula de Cálculo do Risco Normalizado:
$$Risco = (DistanciaGarimpo_{norm} 	imes 0.40) + (AreaDevastada_{norm} 	imes 0.35) + (ImpactoHidrico_{norm} 	imes 0.25)$$
