"""
Módulo de visualização de resultados
Gera mapas, gráficos e relatórios
"""

import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
from matplotlib import patches
from typing import Dict, List, Optional, Tuple
import seaborn as sns
from pathlib import Path


class ResultsVisualizer:
    """Classe para visualização de resultados"""
    
    def __init__(self, config: Dict):
        """
        Inicializa o visualizador
        
        Args:
            config: Configuração do projeto
        """
        self.config = config
        self.visualization_config = config.get('visualization', {})
        self.color_scheme = self.visualization_config.get('map_style', {}).get('color_scheme', {})
        
        # Define estilo padrão
        plt.style.use('seaborn-v0_8-darkgrid')
        sns.set_palette("husl")
    
    def plot_classification_map(
        self, 
        classification: np.ndarray,
        title: str = "Mapa de Classificação",
        class_names: Optional[Dict[int, str]] = None,
        save_path: Optional[str] = None
    ):
        """
        Visualiza mapa de classificação
        
        Args:
            classification: Array de classificação
            title: Título do mapa
            class_names: Dicionário {classe_id: nome}
            save_path: Caminho para salvar a figura
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Define cores para cada classe
        if class_names is None:
            class_names = {
                0: 'Garimpo Ativo',
                1: 'Garimpo Abandonado',
                2: 'Floresta',
                3: 'Água',
                4: 'Solo Exposto'
            }
        
        # Cria colormap personalizado
        colors = [
            self.color_scheme.get('garimpo_ativo', '#FF0000'),
            self.color_scheme.get('garimpo_abandonado', '#FFA500'),
            self.color_scheme.get('floresta', '#00FF00'),
            self.color_scheme.get('agua', '#0000FF'),
            self.color_scheme.get('solo_exposto', '#8B4513')
        ]
        
        n_classes = len(np.unique(classification))
        cmap = mcolors.ListedColormap(colors[:n_classes])
        
        # Plota classificação
        im = ax.imshow(classification, cmap=cmap, interpolation='nearest')
        
        # Adiciona legenda
        legend_elements = [
            patches.Patch(facecolor=colors[i], label=class_names.get(i, f'Classe {i}'))
            for i in range(n_classes)
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Mapa salvo em: {save_path}")
        
        plt.show()
    
    def plot_change_map(
        self, 
        change_types: np.ndarray,
        title: str = "Mapa de Mudanças",
        save_path: Optional[str] = None
    ):
        """
        Visualiza mapa de mudanças temporais
        
        Args:
            change_types: Array com tipos de mudança
            title: Título do mapa
            save_path: Caminho para salvar a figura
        """
        fig, ax = plt.subplots(figsize=(12, 10))
        
        # Define cores para tipos de mudança
        change_colors = {
            0: '#FFFFFF',  # Sem mudança
            1: '#FF0000',  # Nova área
            2: '#FF6B6B',  # Expansão
            3: '#00FF00',  # Retração
            4: '#FFFF00'   # Estável
        }
        
        change_names = {
            0: 'Sem mudança',
            1: 'Nova área de garimpo',
            2: 'Expansão de garimpo',
            3: 'Retração de garimpo',
            4: 'Garimpo estável'
        }
        
        # Cria colormap
        unique_types = np.unique(change_types)
        colors = [change_colors.get(t, '#808080') for t in unique_types]
        cmap = mcolors.ListedColormap(colors)
        
        # Plota mudanças
        im = ax.imshow(change_types, cmap=cmap, interpolation='nearest')
        
        # Adiciona legenda
        legend_elements = [
            patches.Patch(facecolor=change_colors.get(t, '#808080'), 
                         label=change_names.get(t, f'Tipo {t}'))
            for t in unique_types
        ]
        ax.legend(handles=legend_elements, loc='upper right', fontsize=10)
        
        ax.set_title(title, fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Mapa de mudanças salvo em: {save_path}")
        
        plt.show()
    
    def plot_temporal_analysis(
        self, 
        temporal_stats: Dict,
        save_path: Optional[str] = None
    ):
        """
        Visualiza análise temporal
        
        Args:
            temporal_stats: Estatísticas temporais
            save_path: Caminho para salvar a figura
        """
        dates = temporal_stats.get('dates', [])
        areas = temporal_stats.get('total_mining_area_hectares', [])
        
        fig, ax = plt.subplots(figsize=(14, 6))
        
        # Plota evolução temporal
        ax.plot(dates, areas, marker='o', linewidth=2, markersize=8, color='#FF4444')
        ax.fill_between(dates, areas, alpha=0.3, color='#FF4444')
        
        ax.set_xlabel('Período', fontsize=12, fontweight='bold')
        ax.set_ylabel('Área de Garimpo (hectares)', fontsize=12, fontweight='bold')
        ax.set_title('Evolução Temporal da Área de Garimpo', fontsize=14, fontweight='bold')
        
        # Rotaciona labels do eixo x
        plt.xticks(rotation=45, ha='right')
        
        # Adiciona grid
        ax.grid(True, alpha=0.3)
        
        # Adiciona anotações
        if len(areas) > 0:
            max_idx = np.argmax(areas)
            ax.annotate(f'Máximo: {areas[max_idx]:.2f} ha',
                       xy=(dates[max_idx], areas[max_idx]),
                       xytext=(10, 10), textcoords='offset points',
                       bbox=dict(boxstyle='round,pad=0.5', fc='yellow', alpha=0.7),
                       arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Gráfico temporal salvo em: {save_path}")
        
        plt.show()
    
    def plot_mining_objects(
        self, 
        image: np.ndarray,
        mining_objects: List[Dict],
        title: str = "Objetos de Garimpo Detectados",
        save_path: Optional[str] = None
    ):
        """
        Visualiza objetos de garimpo detectados sobre a imagem
        
        Args:
            image: Imagem de fundo
            mining_objects: Lista de objetos detectados
            title: Título da figura
            save_path: Caminho para salvar a figura
        """
        fig, ax = plt.subplots(figsize=(14, 12))
        
        # Mostra imagem de fundo (assume RGB)
        if image.shape[0] <= 3:
            # Se shape é (bands, height, width), transpõe para (height, width, bands)
            image_display = np.transpose(image[:3], (1, 2, 0))
        else:
            image_display = image
        
        # Normaliza para visualização
        image_display = (image_display - np.min(image_display)) / (np.max(image_display) - np.min(image_display))
        
        ax.imshow(image_display)
        
        # Desenha bounding boxes dos objetos
        for obj in mining_objects:
            bbox = obj.get('bbox')
            if bbox:
                minr, minc, maxr, maxc = bbox
                rect = patches.Rectangle(
                    (minc, minr), maxc - minc, maxr - minr,
                    linewidth=2, edgecolor='red', facecolor='none'
                )
                ax.add_patch(rect)
                
                # Adiciona label com área
                area_ha = obj.get('area_hectares', 0)
                ax.text(minc, minr - 5, f'{area_ha:.2f} ha',
                       color='red', fontsize=8, fontweight='bold',
                       bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.7))
        
        ax.set_title(f"{title} ({len(mining_objects)} objetos)", fontsize=14, fontweight='bold')
        ax.axis('off')
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Visualização de objetos salva em: {save_path}")
        
        plt.show()
    
    def plot_statistics_dashboard(
        self, 
        detection_report: Dict,
        change_stats: Optional[Dict] = None,
        save_path: Optional[str] = None
    ):
        """
        Cria dashboard com estatísticas
        
        Args:
            detection_report: Relatório de detecção
            change_stats: Estatísticas de mudança (opcional)
            save_path: Caminho para salvar a figura
        """
        fig = plt.figure(figsize=(16, 10))
        gs = fig.add_gridspec(3, 3, hspace=0.3, wspace=0.3)
        
        # Estatísticas gerais
        ax1 = fig.add_subplot(gs[0, :])
        ax1.axis('off')
        
        stats_text = f"""
        RELATÓRIO DE DETECÇÃO DE GARIMPO - TERRA INDÍGENA MUNDURUKU
        
        Total de Objetos Detectados: {detection_report.get('total_objects', 0)}
        Área Total de Garimpo: {detection_report.get('total_area_hectares', 0):.2f} hectares
        Garimpos Ativos: {detection_report.get('active_count', 0)}
        Garimpos Abandonados: {detection_report.get('abandoned_count', 0)}
        Área Média por Objeto: {detection_report.get('average_area_m2', 0):.2f} m²
        """
        
        ax1.text(0.1, 0.5, stats_text, fontsize=12, verticalalignment='center',
                fontfamily='monospace',
                bbox=dict(boxstyle='round', facecolor='wheat', alpha=0.5))
        
        # Gráfico de pizza: Ativos vs Abandonados
        ax2 = fig.add_subplot(gs[1, 0])
        active = detection_report.get('active_count', 0)
        abandoned = detection_report.get('abandoned_count', 0)
        
        if active + abandoned > 0:
            ax2.pie([active, abandoned], labels=['Ativos', 'Abandonados'],
                   autopct='%1.1f%%', colors=['#FF4444', '#FFA500'])
            ax2.set_title('Status dos Garimpos', fontweight='bold')
        
        # Histograma de áreas
        ax3 = fig.add_subplot(gs[1, 1])
        areas = [obj.get('area_hectares', 0) for obj in detection_report.get('objects', [])]
        if areas:
            ax3.hist(areas, bins=20, color='#4444FF', alpha=0.7, edgecolor='black')
            ax3.set_xlabel('Área (hectares)')
            ax3.set_ylabel('Frequência')
            ax3.set_title('Distribuição de Tamanhos', fontweight='bold')
        
        # Estatísticas de mudança (se disponível)
        if change_stats:
            ax4 = fig.add_subplot(gs[1, 2])
            
            categories = ['Nova\nÁrea', 'Expansão', 'Retração', 'Net\nChange']
            values = [
                change_stats.get('new_mining_area_hectares', 0),
                change_stats.get('expansion_area_hectares', 0),
                change_stats.get('retraction_area_hectares', 0),
                change_stats.get('net_change_hectares', 0)
            ]
            
            colors = ['#FF0000', '#FF6B6B', '#00FF00', '#FFFF00']
            bars = ax4.bar(categories, values, color=colors, edgecolor='black')
            
            ax4.set_ylabel('Área (hectares)')
            ax4.set_title('Mudanças Detectadas', fontweight='bold')
            ax4.grid(True, alpha=0.3, axis='y')
            
            # Adiciona valores nas barras
            for bar in bars:
                height = bar.get_height()
                ax4.text(bar.get_x() + bar.get_width()/2., height,
                        f'{height:.1f}',
                        ha='center', va='bottom', fontsize=9, fontweight='bold')
        
        plt.suptitle('Dashboard de Análise de Garimpo', fontsize=16, fontweight='bold', y=0.98)
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"Dashboard salvo em: {save_path}")
        
        plt.show()
    
    def export_results_to_geotiff(
        self, 
        data: np.ndarray,
        output_path: str,
        metadata: Dict
    ):
        """
        Exporta resultados para GeoTIFF
        
        Args:
            data: Array de dados
            output_path: Caminho de saída
            metadata: Metadados geoespaciais
        """
        import rasterio
        from rasterio.transform import from_bounds
        
        # Prepara metadados
        height, width = data.shape if data.ndim == 2 else data.shape[1:]
        count = 1 if data.ndim == 2 else data.shape[0]
        
        # Cria arquivo GeoTIFF
        with rasterio.open(
            output_path,
            'w',
            driver='GTiff',
            height=height,
            width=width,
            count=count,
            dtype=data.dtype,
            crs=metadata.get('crs', 'EPSG:4326'),
            transform=metadata.get('transform'),
            compress='lzw'
        ) as dst:
            if data.ndim == 2:
                dst.write(data, 1)
            else:
                for i in range(count):
                    dst.write(data[i], i + 1)
        
        print(f"GeoTIFF exportado para: {output_path}")
    
    def generate_report(
        self, 
        detection_report: Dict,
        temporal_analysis: Optional[Dict] = None,
        change_stats: Optional[Dict] = None,
        output_dir: str = "results"
    ):
        """
        Gera relatório completo em formato texto
        
        Args:
            detection_report: Relatório de detecção
            temporal_analysis: Análise temporal (opcional)
            change_stats: Estatísticas de mudança (opcional)
            output_dir: Diretório de saída
        """
        output_path = Path(output_dir) / "relatorio_garimpo.txt"
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write("=" * 80 + "\n")
            f.write("RELATÓRIO DE MAPEAMENTO DE GARIMPO ILEGAL\n")
            f.write("Terra Indígena Munduruku - Bacia do Rio Tapajós, Pará\n")
            f.write("=" * 80 + "\n\n")
            
            # Estatísticas de detecção
            f.write("1. ESTATÍSTICAS DE DETECÇÃO\n")
            f.write("-" * 40 + "\n")
            f.write(f"Total de objetos detectados: {detection_report.get('total_objects', 0)}\n")
            f.write(f"Área total de garimpo: {detection_report.get('total_area_hectares', 0):.2f} hectares\n")
            f.write(f"Garimpos ativos: {detection_report.get('active_count', 0)}\n")
            f.write(f"Garimpos abandonados: {detection_report.get('abandoned_count', 0)}\n")
            f.write(f"Área média por objeto: {detection_report.get('average_area_m2', 0):.2f} m²\n\n")
            
            # Análise temporal
            if temporal_analysis:
                f.write("2. ANÁLISE TEMPORAL\n")
                f.write("-" * 40 + "\n")
                f.write(f"Tendência: {temporal_analysis.get('trend', 'N/A')}\n")
                dates = temporal_analysis.get('dates', [])
                areas = temporal_analysis.get('total_mining_area_hectares', [])
                for date, area in zip(dates, areas):
                    f.write(f"  {date}: {area:.2f} hectares\n")
                f.write("\n")
            
            # Mudanças detectadas
            if change_stats:
                f.write("3. MUDANÇAS DETECTADAS\n")
                f.write("-" * 40 + "\n")
                f.write(f"Nova área de garimpo: {change_stats.get('new_mining_area_hectares', 0):.2f} ha\n")
                f.write(f"Expansão de garimpo: {change_stats.get('expansion_area_hectares', 0):.2f} ha\n")
                f.write(f"Retração de garimpo: {change_stats.get('retraction_area_hectares', 0):.2f} ha\n")
                f.write(f"Mudança líquida: {change_stats.get('net_change_hectares', 0):.2f} ha\n\n")
            
            f.write("=" * 80 + "\n")
            f.write("Fim do relatório\n")
        
        print(f"Relatório gerado em: {output_path}")
