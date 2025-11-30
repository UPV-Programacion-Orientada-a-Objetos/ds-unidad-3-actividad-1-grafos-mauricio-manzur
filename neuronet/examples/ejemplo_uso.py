"""
Ejemplo de uso de NeuroNet sin interfaz gráfica
Demuestra el uso programático del wrapper de Python
"""

import sys
import os

# Agregar path para importar el módulo
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

try:
    import grafo_wrapper
except ImportError:
    print("ERROR: No se puede importar grafo_wrapper.")
    print("Compile el proyecto primero: python setup.py build_ext --inplace")
    sys.exit(1)


def ejemplo_basico():
    """
    Ejemplo básico de carga y análisis de un grafo
    """
    print("="*60)
    print("  NeuroNet - Ejemplo de Uso Programático")
    print("="*60)
    
    # Crear instancia del grafo
    print("\n[1] Creando instancia del motor de grafos...")
    grafo = grafo_wrapper.PyGrafoDisperso()
    
    # Cargar datos
    print("\n[2] Cargando dataset...")
    archivo = sys.argv[1] if len(sys.argv) > 1 else "datasets/test_graph.txt"
    
    try:
        stats = grafo.cargar_datos(archivo)
        
        print(f"\n✓ Datos cargados exitosamente:")
        print(f"  - Nodos:        {stats['num_nodos']:,}")
        print(f"  - Aristas:      {stats['num_aristas']:,}")
        print(f"  - Memoria:      {stats['memoria_mb']:.2f} MB")
        print(f"  - Tiempo carga: {stats['tiempo_carga']:.3f} seg")
        
    except Exception as e:
        print(f"\n✗ Error al cargar: {e}")
        return
    
    # Obtener estadísticas completas
    print("\n[3] Obteniendo estadísticas del grafo...")
    stats_completas = grafo.get_estadisticas()
    
    print(f"\n  Nodo con mayor grado: {stats_completas['nodo_mayor_grado']}")
    print(f"  Grado máximo:          {stats_completas['grado_max']:,}")
    
    # Ejecutar BFS
    print("\n[4] Ejecutando BFS desde nodo 0 con profundidad 2...")
    nodos_visitados = grafo.ejecutar_bfs(0, 2)
    
    print(f"\n  Nodos visitados: {len(nodos_visitados)}")
    print(f"  Primeros 10 nodos: {nodos_visitados[:10]}")
    
    # Obtener aristas del subgrafo
    print("\n[5] Obteniendo aristas del subgrafo...")
    aristas = grafo.get_aristas_subgrafo(nodos_visitados)
    
    print(f"\n  Aristas en el subgrafo: {len(aristas)}")
    print(f"  Primeras 5 aristas: {aristas[:5]}")
    
    # Verificar vecinos de un nodo
    if len(nodos_visitados) > 0:
        nodo_ejemplo = nodos_visitados[0]
        vecinos = grafo.get_vecinos(nodo_ejemplo)
        print(f"\n[6] Vecinos del nodo {nodo_ejemplo}: {len(vecinos)}")
        print(f"  Primeros vecinos: {vecinos[:10]}")
    
    # Ejecutar DFS
    print("\n[7] Ejecutando DFS desde nodo 0...")
    nodos_dfs = grafo.ejecutar_dfs(0)
    print(f"\n  Nodos alcanzados por DFS: {len(nodos_dfs)}")
    
    print("\n" + "="*60)
    print("  Ejemplo completado exitosamente")
    print("="*60)


def ejemplo_comparacion_bfs_profundidad():
    """
    Ejemplo que compara BFS con diferentes profundidades
    """
    print("\nEJEMPLO ADICIONAL: Comparación de profundidades BFS")
    print("-"*60)
    
    grafo = grafo_wrapper.PyGrafoDisperso()
    grafo.cargar_datos("datasets/test_graph.txt")
    
    print("\nResultados de BFS desde nodo 0 con diferentes profundidades:\n")
    
    for prof in range(1, 6):
        nodos = grafo.ejecutar_bfs(0, prof)
        print(f"  Profundidad {prof}: {len(nodos):4d} nodos alcanzados")
    
    print("\n" + "-"*60)


if __name__ == "__main__":
    ejemplo_basico()
    print("\n")
    
    # Descomentar para ver ejemplo adicional:
    # ejemplo_comparacion_bfs_profundidad()
