package src.java;

import java.util.ArrayList;
import java.util.List;

/**
 * Mapeamento Híbrido de Risco e Cicatrizes de Garimpo
 * Subsídio à Proteção da TI Munduruku - Bacia do Rio Cabitutu / Tapajós
 */
public class MapeamentoGarimpoMunduruku {

    // Classe representando uma Aldeia Indígena e seu Risco Geospacial
    public static class AldeiaRisco {
        private String id;
        private String nome;
        private double proximidadeGarimpoKm;
        private double areaGarimpoBuffer5kmHa;
        private String nivelImpactoHidrico;
        private double scoreCalculado;
        private String grauRiscoFinal;

        public AldeiaRisco(String id, String nome, double proximidadeGarimpoKm, double areaGarimpoBuffer5kmHa, String nivelImpactoHidrico) {
            this.id = id;
            this.nome = nome;
            this.proximidadeGarimpoKm = proximidadeGarimpoKm;
            this.areaGarimpoBuffer5kmHa = areaGarimpoBuffer5kmHa;
            this.nivelImpactoHidrico = nivelImpactoHidrico;
            calcularMatrizRisco();
        }

        /**
         * Algoritmo de Cálculo da Matriz de Risco Territorial:
         * Risco = (DistanciaNormalizada * 0.40) + (AreaBufferNormalizada * 0.35) + (ImpactoHidricoNormalizado * 0.25)
         */
        public void calcularMatrizRisco() {
            // Normalização de Proximidade (Menor distância = Maior Risco)
            double maxDist = 5.0; // km
            double distNorm = Math.max(0, (maxDist - proximidadeGarimpoKm) / maxDist);

            // Normalização de Área Afetada no Buffer
            double maxArea = 420.0; // ha (Aldeia Cabitutu como referência máxima)
            double areaNorm = Math.min(1.0, areaGarimpoBuffer5kmHa / maxArea);

            // Escala de Impacto Hídrico (Contaminação por Hg e Turbidez)
            double hidricoScore = 0.25;
            if (nivelImpactoHidrico.equalsIgnoreCase("Crítico")) {
                hidricoScore = 1.0;
            } else if (nivelImpactoHidrico.equalsIgnoreCase("Alto")) {
                hidricoScore = 0.75;
            } else if (nivelImpactoHidrico.equalsIgnoreCase("Médio")) {
                hidricoScore = 0.50;
            }

            // Score ponderado final (0.0 a 1.0)
            this.scoreCalculado = (distNorm * 0.40) + (areaNorm * 0.35) + (hidricoScore * 0.25);

            // Definição do Grau de Risco
            if (this.scoreCalculado >= 0.70) {
                this.grauRiscoFinal = "MUITO ALTO";
            } else if (this.scoreCalculado >= 0.50) {
                this.grauRiscoFinal = "ALTO";
            } else if (this.scoreCalculado >= 0.30) {
                this.grauRiscoFinal = "MÉDIO";
            } else {
                this.grauRiscoFinal = "BAIXO";
            }
        }

        @Override
        public String toString() {
            return String.format("[%s] %-30s | Proximidade: %3.1f km | Área Buffer: %3.0f ha | Impacto Hídrico: %-7s | Score: %.3f | Grau: %s",
                    id, nome, proximidadeGarimpoKm, areaGarimpoBuffer5kmHa, nivelImpactoHidrico, scoreCalculado, grauRiscoFinal);
        }
    }

    public static void main(String[] args) {
        System.out.println("==========================================================================================================");
        System.out.println("   Munduruku GIS - Sistema de Mapeamento Híbrido de Risco e Cicatrizes de Garimpo (Versão Java)");
        System.out.println("   Coordenadas de Referência: 6° 15' S, 57° 45' W | Bacia do Rio Cabitutu");
        System.out.println("==========================================================================================================\n");

        List<AldeiaRisco> aldeias = new ArrayList<>();
        aldeias.add(new AldeiaRisco("A01", "Aldeia Cabitutu", 0.3, 420, "Crítico"));
        aldeias.add(new AldeiaRisco("A02", "Aldeia Sawré Muybu (Entorno)", 0.8, 310, "Alto"));
        aldeias.add(new AldeiaRisco("A03", "Aldeia A03", 1.1, 280, "Crítico"));
        aldeias.add(new AldeiaRisco("A04", "Aldeia Karapanatuba", 1.4, 210, "Alto"));
        aldeias.add(new AldeiaRisco("A05", "Aldeia Praia do Mangue", 1.8, 195, "Médio"));
        aldeias.add(new AldeiaRisco("A06", "Aldeia Praia do Índio", 2.1, 160, "Médio"));
        aldeias.add(new AldeiaRisco("A07", "Aldeia Poxisol", 2.5, 140, "Crítico"));
        aldeias.add(new AldeiaRisco("A08", "Aldeia Daudip", 2.8, 125, "Alto"));
        aldeias.add(new AldeiaRisco("A09", "Aldeia Posto Dawa", 3.2, 90, "Médio"));
        aldeias.add(new AldeiaRisco("A10", "Aldeia Caroebak", 3.5, 85, "Baixo"));
        aldeias.add(new AldeiaRisco("A11", "Aldeia Tropas", 3.9, 70, "Alto"));
        aldeias.add(new AldeiaRisco("A12", "Aldeia Kadiriri", 4.1, 55, "Baixo"));
        aldeias.add(new AldeiaRisco("A13", "Aldeia Datik", 4.5, 40, "Baixo"));
        aldeias.add(new AldeiaRisco("A14", "Aldeia Waro", 4.8, 35, "Baixo"));
        aldeias.add(new AldeiaRisco("A15", "Aldeia Yuivi", 5.0, 25, "Baixo"));

        for (AldeiaRisco aldeia : aldeias) {
            System.out.println(aldeia);
        }

        System.out.println("\n==========================================================================================================");
        System.out.println("   Mapeamento concluído com sucesso. Dados preparados para exportação GIS / Shapefile.");
        System.out.println("==========================================================================================================");
    }
}
