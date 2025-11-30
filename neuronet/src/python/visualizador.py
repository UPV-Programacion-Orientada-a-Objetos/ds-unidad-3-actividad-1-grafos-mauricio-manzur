"""
NeuroNet: Visualizador de Subgrafos
Módulo para visualización de resultados usando NetworkX
"""

import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')


class VisualizadorGrafos:
    """
    Clase para manejar la visualización de grafos usando NetworkX.
    NetworkX se usa SOLO para dibujar, no para cálculos.
    """
    
    @staticmethod
    def dibujar_subgrafo(nodos, aristas, nodo_inicio=None, parent_widget=None):
        """
        Dibuja un subgrafo en un canvas de matplotlib.
        
        Args:
            nodos (list): Lista de IDs de nodos
            aristas (list): Lista de tuplas (nodo1, nodo2)
            nodo_inicio (int): Nodo inicial para destacar
            parent_widget: Widget padre de Tkinter
            
        Returns:
            FigureCanvasTkAgg: Canvas de matplotlib para embeber en Tkinter
        """
        # Crear grafo dirigido de NetworkX (solo para visualización)
        G = nx.DiGraph()
        
        # Agregar nodos
        G.add_nodes_from(nodos)
        
        # Agregar aristas
        G.add_edges_from(aristas)
        
        # Crear figura de matplotlib
        fig, ax = plt.subplots(figsize=(10, 8))
        
        # Elegir layout según tamaño
        if len(nodos) < 100:
            pos = nx.spring_layout(G, k=0.5, iterations=50)
        elif len(nodos) < 500:
            pos = nx.kamada_kawai_layout(G)
        else:
            # Para grafos grandes, usar layout circular
            pos = nx.circular_layout(G)
        
        # Colores de nodos
        node_colors = []
        for nodo in G.nodes():
            if nodo == nodo_inicio:
                node_colors.append('#FF6B6B')  # Rojo para nodo inicial
            else:
                node_colors.append('#4ECDC4')  # Turquesa para otros
        
        # Dibujar el grafo
        nx.draw_networkx_nodes(
            G, pos, 
            node_color=node_colors,
            node_size=300,
            alpha=0.9,
            ax=ax
        )
        
        nx.draw_networkx_edges(
            G, pos,
            edge_color='#95A5A6',
            arrows=True,
            arrowsize=15,
            width=1.5,
            alpha=0.6,
            ax=ax,
            connectionstyle='arc3,rad=0.1'
        )
        
        # Etiquetas solo si hay pocos nodos
        if len(nodos) <= 50:
            labels = {nodo: str(nodo) for nodo in G.nodes()}
            nx.draw_networkx_labels(
                G, pos,
                labels,
                font_size=8,
                font_weight='bold',
                ax=ax
            )
        
        # Configuración del plot
        ax.set_title(
            f'Subgrafo Resultante - {len(nodos)} nodos, {len(aristas)} aristas',
            fontsize=14,
            fontweight='bold',
            pad=20
        )
        ax.axis('off')
        plt.tight_layout()
        
        # Si se proporciona parent_widget, crear canvas de Tkinter
        if parent_widget:
            canvas = FigureCanvasTkAgg(fig, master=parent_widget)
            canvas.draw()
            return canvas
        else:
            plt.show()
            return None
    
    @staticmethod
    def obtener_metricas_visuales(nodos, aristas):
        """
        Calcula métricas básicas del subgrafo para mostrar.
        
        Args:
            nodos (list): Lista de nodos
            aristas (list): Lista de aristas
            
        Returns:
            dict: Diccionario con métricas
        """
        G = nx.DiGraph()
        G.add_nodes_from(nodos)
        G.add_edges_from(aristas)
        
        metricas = {
            'num_nodos': len(nodos),
            'num_aristas': len(aristas),
            'densidad': nx.density(G) if len(nodos) > 0 else 0,
            'componentes_conexas': nx.number_weakly_connected_components(G)
        }
        
        return metricas
