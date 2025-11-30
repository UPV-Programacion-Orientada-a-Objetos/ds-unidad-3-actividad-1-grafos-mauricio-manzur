"""
NeuroNet GUI - Interfaz Gráfica de Usuario
Sistema de análisis de redes masivas con backend en C++
"""

import tkinter as tk
from tkinter import ttk, filedialog, messagebox, scrolledtext
import sys
import os

# Agregar el directorio raíz al path para importar el módulo compilado
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

try:
    import grafo_wrapper
except ImportError:
    print("ERROR: No se puede importar grafo_wrapper.")
    print("Por favor, compile el proyecto primero con: python setup.py build_ext --inplace")
    sys.exit(1)

from visualizador import VisualizadorGrafos


class NeuroNetGUI:
    """
    Interfaz gráfica principal para NeuroNet.
    Permite cargar datasets, ejecutar análisis y visualizar resultados.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("NeuroNet - Análisis de Redes Masivas")
        self.root.geometry("1200x800")
        self.root.configure(bg='#2C3E50')
        
        # Motor de grafos (C++)
        self.grafo = None
        self.archivo_actual = None
        
        # Configurar estilo
        self.configurar_estilo()
        
        # Crear interfaz
        self.crear_widgets()
        
    def configurar_estilo(self):
        """Configura el estilo visual de la aplicación"""
        style = ttk.Style()
        style.theme_use('clam')
        
        # Colores
        style.configure('TFrame', background='#2C3E50')
        style.configure('TLabel', background='#2C3E50', foreground='#ECF0F1', font=('Arial', 10))
        style.configure('Title.TLabel', font=('Arial', 16, 'bold'), foreground='#3498DB')
        style.configure('Metric.TLabel', font=('Arial', 12), foreground='#2ECC71')
        style.configure('TButton', font=('Arial', 10, 'bold'))
        
    def crear_widgets(self):
        """Crea todos los widgets de la interfaz"""
        
        # ========== HEADER ==========
        header_frame = ttk.Frame(self.root, padding="10")
        header_frame.pack(fill=tk.X)
        
        ttk.Label(
            header_frame,
            text="🌐 NeuroNet",
            style='Title.TLabel'
        ).pack(side=tk.LEFT, padx=10)
        
        ttk.Label(
            header_frame,
            text="Análisis y Visualización de Propagación en Redes Masivas",
            font=('Arial', 11, 'italic'),
            foreground='#95A5A6'
        ).pack(side=tk.LEFT, padx=10)
        
        # ========== PANEL IZQUIERDO: CONTROLES ==========
        left_panel = ttk.Frame(self.root, padding="10")
        left_panel.pack(side=tk.LEFT, fill=tk.Y, padx=10, pady=10)
        
        # Botón de carga
        ttk.Label(left_panel, text="Dataset", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 5))
        
        btn_cargar = tk.Button(
            left_panel,
            text="📁 Cargar Dataset",
            command=self.cargar_dataset,
            bg='#3498DB',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            cursor='hand2',
            padx=20,
            pady=10
        )
        btn_cargar.pack(fill=tk.X, pady=5)
        
        self.label_archivo = ttk.Label(left_panel, text="Ningún archivo cargado", foreground='#E74C3C')
        self.label_archivo.pack(anchor=tk.W, pady=5)
        
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # Métricas del grafo
        ttk.Label(left_panel, text="Métricas del Grafo", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        self.metricas_text = scrolledtext.ScrolledText(
            left_panel,
            width=35,
            height=12,
            bg='#34495E',
            fg='#ECF0F1',
            font=('Courier', 9),
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.metricas_text.pack(fill=tk.BOTH, expand=True, pady=5)
        self.metricas_text.insert(tk.END, "Esperando carga de datos...\n")
        self.metricas_text.config(state=tk.DISABLED)
        
        ttk.Separator(left_panel, orient=tk.HORIZONTAL).pack(fill=tk.X, pady=15)
        
        # Controles de BFS
        ttk.Label(left_panel, text="Búsqueda BFS", font=('Arial', 12, 'bold')).pack(anchor=tk.W, pady=(0, 10))
        
        ttk.Label(left_panel, text="Nodo Inicial:").pack(anchor=tk.W)
        self.entry_nodo_inicio = ttk.Entry(left_panel, width=20, font=('Arial', 10))
        self.entry_nodo_inicio.pack(fill=tk.X, pady=5)
        self.entry_nodo_inicio.insert(0, "0")
        
        ttk.Label(left_panel, text="Profundidad Máxima:").pack(anchor=tk.W, pady=(10, 0))
        self.scale_profundidad = tk.Scale(
            left_panel,
            from_=1,
            to=10,
            orient=tk.HORIZONTAL,
            bg='#34495E',
            fg='#ECF0F1',
            highlightthickness=0,
            length=250
        )
        self.scale_profundidad.set(2)
        self.scale_profundidad.pack(fill=tk.X, pady=5)
        
        btn_bfs = tk.Button(
            left_panel,
            text="🔍 Ejecutar BFS",
            command=self.ejecutar_bfs,
            bg='#2ECC71',
            fg='white',
            font=('Arial', 11, 'bold'),
            relief=tk.RAISED,
            cursor='hand2',
            padx=20,
            pady=10
        )
        btn_bfs.pack(fill=tk.X, pady=10)
        
        # ========== PANEL DERECHO: VISUALIZACIÓN ==========
        right_panel = ttk.Frame(self.root, padding="10")
        right_panel.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        ttk.Label(
            right_panel,
            text="Visualización de Subgrafo",
            font=('Arial', 14, 'bold'),
            foreground='#3498DB'
        ).pack(anchor=tk.W, pady=(0, 10))
        
        # Frame para el canvas de matplotlib
        self.canvas_frame = tk.Frame(right_panel, bg='white', relief=tk.SUNKEN, borderwidth=2)
        self.canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # Mensaje inicial
        self.label_placeholder = tk.Label(
            self.canvas_frame,
            text="Ejecute una búsqueda BFS para visualizar el subgrafo",
            font=('Arial', 12),
            bg='white',
            fg='#95A5A6'
        )
        self.label_placeholder.pack(expand=True)
        
        # ========== CONSOLA DE LOG ==========
        log_frame = ttk.Frame(self.root, padding="10")
        log_frame.pack(side=tk.BOTTOM, fill=tk.X, padx=10, pady=(0, 10))
        
        ttk.Label(log_frame, text="Consola de Eventos", font=('Arial', 10, 'bold')).pack(anchor=tk.W)
        
        self.console_text = scrolledtext.ScrolledText(
            log_frame,
            height=6,
            bg='#1C1C1C',
            fg='#00FF00',
            font=('Courier', 9),
            relief=tk.SUNKEN,
            borderwidth=2
        )
        self.console_text.pack(fill=tk.BOTH, expand=True)
        self.console_text.insert(tk.END, "[NeuroNet] Sistema inicializado.\n")
        self.console_text.config(state=tk.DISABLED)
        
    def log(self, mensaje):
        """Agrega un mensaje a la consola de log"""
        self.console_text.config(state=tk.NORMAL)
        self.console_text.insert(tk.END, f"{mensaje}\n")
        self.console_text.see(tk.END)
        self.console_text.config(state=tk.DISABLED)
    
    def cargar_dataset(self):
        """Abre un diálogo para cargar un archivo dataset"""
        archivo = filedialog.askopenfilename(
            title="Seleccionar Dataset",
            filetypes=[
                ("Archivos de texto", "*.txt"),
                ("Todos los archivos", "*.*")
            ]
        )
        
        if not archivo:
            return
        
        self.log(f"[GUI] Cargando archivo: {archivo}")
        
        try:
            # Crear instancia del grafo C++
            self.grafo = grafo_wrapper.PyGrafoDisperso()
            
            # Cargar datos
            self.root.config(cursor="wait")
            self.root.update()
            
            stats = self.grafo.cargar_datos(archivo)
            
            self.archivo_actual = archivo
            self.label_archivo.config(
                text=f"✓ {os.path.basename(archivo)}",
                foreground='#2ECC71'
            )
            
            # Actualizar métricas
            self.actualizar_metricas(stats)
            
            self.log(f"[GUI] Carga exitosa: {stats['num_nodos']} nodos, {stats['num_aristas']} aristas")
            self.log(f"[GUI] Tiempo de carga: {stats['tiempo_carga']:.2f} segundos")
            
            messagebox.showinfo(
                "Carga Exitosa",
                f"Dataset cargado correctamente\n\n" +
                f"Nodos: {stats['num_nodos']:,}\n" +
                f"Aristas: {stats['num_aristas']:,}\n" +
                f"Memoria: {stats['memoria_mb']:.2f} MB\n" +
                f"Tiempo: {stats['tiempo_carga']:.2f} seg"
            )
            
        except Exception as e:
            self.log(f"[ERROR] {str(e)}")
            messagebox.showerror("Error de Carga", f"No se pudo cargar el archivo:\n{str(e)}")
        
        finally:
            self.root.config(cursor="")
    
    def actualizar_metricas(self, stats):
        """Actualiza el panel de métricas con estadísticas del grafo"""
        self.metricas_text.config(state=tk.NORMAL)
        self.metricas_text.delete(1.0, tk.END)
        
        # Obtener estadísticas completas
        if self.grafo:
            stats_completas = self.grafo.get_estadisticas()
            
            texto = f"""
╔═══════════════════════════════╗
║     ESTADÍSTICAS DEL GRAFO    ║
╚═══════════════════════════════╝

📊 Nodos Totales:     {stats_completas['num_nodos']:,}
🔗 Aristas Totales:   {stats_completas['num_aristas']:,}

🎯 Nodo Mayor Grado:  {stats_completas['nodo_mayor_grado']}
   └─ Grado:          {stats_completas['grado_max']:,}

💾 Memoria CSR:       {stats_completas['memoria_mb']:.2f} MB
⏱️  Tiempo Carga:     {stats_completas['tiempo_carga_seg']:.2f} seg

═══════════════════════════════════
Formato: CSR (Compressed Sparse Row)
Backend: C++ optimizado
            """
            
            self.metricas_text.insert(tk.END, texto)
        
        self.metricas_text.config(state=tk.DISABLED)
    
    def ejecutar_bfs(self):
        """Ejecuta la búsqueda BFS y visualiza el resultado"""
        if not self.grafo:
            messagebox.showwarning("Sin Datos", "Por favor, cargue un dataset primero.")
            return
        
        try:
            nodo_inicio = int(self.entry_nodo_inicio.get())
            profundidad = int(self.scale_profundidad.get())
            
            self.log(f"[GUI] Ejecutando BFS desde nodo {nodo_inicio}, profundidad {profundidad}")
            
            self.root.config(cursor="wait")
            self.root.update()
            
            # Ejecutar BFS (en C++)
            nodos_visitados = self.grafo.ejecutar_bfs(nodo_inicio, profundidad)
            
            if not nodos_visitados:
                messagebox.showwarning(
                    "Sin Resultados",
                    f"El nodo {nodo_inicio} no existe en el grafo o no tiene vecinos."
                )
                self.root.config(cursor="")
                return
            
            # Obtener aristas del subgrafo (en C++)
            aristas = self.grafo.get_aristas_subgrafo(nodos_visitados)
            
            self.log(f"[GUI] BFS completado: {len(nodos_visitados)} nodos, {len(aristas)} aristas")
            
            # Visualizar
            self.visualizar_subgrafo(nodos_visitados, aristas, nodo_inicio)
            
        except ValueError:
            messagebox.showerror("Error de Entrada", "Por favor, ingrese un número válido para el nodo inicial.")
        except Exception as e:
            self.log(f"[ERROR] {str(e)}")
            messagebox.showerror("Error en BFS", str(e))
        finally:
            self.root.config(cursor="")
    
    def visualizar_subgrafo(self, nodos, aristas, nodo_inicio):
        """Visualiza el subgrafo usando NetworkX"""
        # Limpiar canvas anterior
        for widget in self.canvas_frame.winfo_children():
            widget.destroy()
        
        self.log(f"[GUI] Generando visualización...")
        
        # Crear visualización
        canvas = VisualizadorGrafos.dibujar_subgrafo(
            nodos,
            aristas,
            nodo_inicio,
            self.canvas_frame
        )
        
        if canvas:
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
            self.log(f"[GUI] Visualización completada")


def main():
    """Función principal"""
    root = tk.Tk()
    app = NeuroNetGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
