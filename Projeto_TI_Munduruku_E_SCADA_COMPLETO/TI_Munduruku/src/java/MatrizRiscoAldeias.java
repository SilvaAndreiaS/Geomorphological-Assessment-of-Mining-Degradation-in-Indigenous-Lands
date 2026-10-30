package src.java;

import java.util.ArrayList;
import java.util.List;

public class MatrizRiscoAldeias {

    public static class Aldeia {
        String id;
        String nome;
        double proximidadeKm;
        double areaBuffer5kmHa;
        String riscoHidrico;
        double impactoHidricoScore;
        double scoreCalculado;
        String grauRisco;

        public Aldeia(String id, String nome, double proximidadeKm, double areaBuffer5kmHa, String riscoHidrico, double impactoHidricoScore) {
            this.id = id;
            this.nome = nome;
            this.proximidadeKm = proximidadeKm;
            this.areaBuffer5kmHa = areaBuffer5kmHa;
            this.riscoHidrico = riscoHidrico;
            this.impactoHidricoScore = impactoHidricoScore;
        }

        public void calcularRisco(double maxDist, double maxArea) {
            // Normalização inversa de distância (menor distância = maior risco)
            double distNorm = Math.max(0, (maxDist - proximidadeKm) / maxDist);
            double areaNorm = Math.min(1.0, areaBuffer5kmHa / maxArea);
            double hidricoNorm = impactoHidricoScore / 100.0;

            // Fórmula ponderada
            this.scoreCalculado = (distNorm * 0.40) + (areaNorm * 0.35) + (hidricoNorm * 0.25);

            // Classificação por limites fixos
            if (this.scoreCalculado >= 0.70) {
                this.grauRisco = "MUITO ALTO";
            } else if (this.scoreCalculado >= 0.50) {
                this.grauRisco = "ALTO";
            } else if (this.scoreCalculado >= 0.30) {
                this.grauRisco = "MÉDIO";
            } else {
                this.grauRisco = "BAIXO";
            }
        }
    }

    public static void main(String[] args) {
        List<Aldeia> aldeias = new ArrayList<>();
        aldeias.add(new Aldeia("A01", "Aldeia Cabitutu", 0.3, 420.0, "Crítico", 100.0));
        aldeias.add(new Aldeia("A02", "Aldeia Sawré Muybu (Entorno)", 0.8, 310.0, "Alto", 75.0));
        aldeias.add(new Aldeia("A03", "Aldeia A03", 1.1, 280.0, "Crítico", 100.0));
        aldeias.add(new Aldeia("A04", "Aldeia Karapanatuba", 1.4, 210.0, "Alto", 75.0));
        aldeias.add(new Aldeia("A05", "Aldeia Praia do Mangue", 1.8, 195.0, "Médio", 50.0));
        aldeias.add(new Aldeia("A15", "Aldeia Yuivi", 5.0, 25.0, "Baixo", 25.0));

        System.out.println("=== CÁLCULO DA MATRIZ DE RISCO DAS ALDEIAS (JAVA) ===");
        for (Aldeia a : aldeias) {
            a.calcularRisco(5.0, 420.0);
            System.out.printf("[%s] %-30s | Score: %.3f | Grau: %s%n", a.id, a.nome, a.scoreCalculado, a.grauRisco);
        }
    }
}
