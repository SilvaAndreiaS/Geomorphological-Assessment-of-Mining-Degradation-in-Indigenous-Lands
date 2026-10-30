# Mapeamento Híbrido de Risco e Cicatrizes de Garimpo: Subsídio à Proteção da TI Munduruku
**Área de Estudo:** Terra Indígena Munduruku e Bacia do Rio Tapajós (Rio Cabitutu), Pará, Brasil  
**Coordenadas de Referência:** 6° 15' S, 57° 45' W  
**Versão do Documento:** 1.0 (Relatório Final de Metodologia e Avaliação de Risco)

---

## 1. Contexto Geral e Justificativa Diagnóstica
A Terra Indígena (TI) Munduruku, localizada no sudoeste do estado do Pará na Bacia Hidrográfica do Rio Tapajós, consolida-se atualmente como o segundo território indígena mais devastado pela atividade garimpeira no Brasil. O avanço das frentes de mineração ilegal de ouro ao longo dos principais leitos fluviais provocou alterações morfológicas profundas na paisagem, além de severa contaminação por mercúrio (Hg).

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
$$Risco = (DistanciaGarimpo_{norm} 	imes 0.40) + (AreaDevastada_{norm} 	imes 0.35) + (ImpactoHidrico_{norm} 	imes 0.25)$$

---

## 4. Recomendações e Plano de Ação
1. Bases de Proteção Etnoambiental (BPEA) nas confluências dos rios Cabitutu e Tapajós.
2. Alertas em tempo real via SAR / Interferometria no Google Earth Engine.
3. Rastreamento de contaminação por Hg nas 15 aldeias.
4. Reflorestamento e biorremediação de cavas abandonadas.
