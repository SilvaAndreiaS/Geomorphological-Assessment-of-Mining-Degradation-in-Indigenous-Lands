package src.java;

import java.util.ArrayList;
import java.util.List;

public class MapeamentoGarimpoMunduruku {

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

        public void calcularMatrizRisco() {
            double maxDist = 5.0;
            double distNorm = Math.max(0, (maxDist - proximidadeGarimpoKm) / maxDist);
            double maxArea = 420.0;
            double areaNorm = Math.min(1.0, areaGarimpoBuffer5kmHa / maxArea);

            double hidricoScore = 0.25;
            if (nivelImpactoHidrico.equalsIgnoreCase("Crítico")) {
                hidricoScore = 1.0;
            } else if (nivelImpactoHidrico.equalsIgnoreCase("Alto")) {
                hidricoScore = 0.75;
            } else if (nivelImpactoHidrico.equalsIgnoreCase("Médio")) {
                hidricoScore = 0.50;
            }

            this.scoreCalculado = (distNorm * 0.40) + (areaNorm * 0.35) + (hidricoScore * 0.25);

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
        System.out.println("Projeto: Avaliação geomorfológica da degradação causada pela mineração em terras indígenas");
        System.out.println("TI Munduruku — Bacia do Rio Tapajós / Rio Cabitutu");
    }
}
