"""
Script para generar datasets de prueba y descargar datasets de SNAP
"""

import urllib.request
import gzip
import os


def crear_dataset_pequeno(archivo="test_graph.txt", num_nodos=50):
    """
    Crea un dataset pequeño para pruebas rápidas.
    Grafo de tipo "estrella" con algunos ciclos.
    """
    print(f"Creando dataset de prueba: {archivo}")
    
    with open(archivo, 'w') as f:
        # Escribir comentario
        f.write("# Grafo de prueba generado automáticamente\n")
        f.write(f"# Nodos: {num_nodos}, Tipo: Estrella con ciclos\n")
        
        # Nodo central conectado a todos
        for i in range(1, num_nodos):
            f.write(f"0 {i}\n")
        
        # Algunos nodos forman cadenas
        for i in range(1, num_nodos - 1, 5):
            f.write(f"{i} {i+1}\n")
            if i + 2 < num_nodos:
                f.write(f"{i+1} {i+2}\n")
        
        # Algunos ciclos
        if num_nodos > 10:
            f.write("5 10\n")
            f.write("10 15\n")
            f.write("15 5\n")
    
    print(f"✓ Dataset creado: {archivo}")


def crear_dataset_lineal(archivo="linear_graph.txt", longitud=100):
    """
    Crea un grafo lineal simple: 0→1→2→3→...
    Útil para verificar BFS con profundidad.
    """
    print(f"Creando grafo lineal: {archivo}")
    
    with open(archivo, 'w') as f:
        f.write("# Grafo lineal para pruebas de BFS\n")
        
        for i in range(longitud - 1):
            f.write(f"{i} {i+1}\n")
    
    print(f"✓ Grafo lineal creado: {archivo}")


def descargar_dataset_snap(url, nombre_archivo):
    """
    Descarga un dataset de SNAP y lo descomprime.
    """
    print(f"Descargando {nombre_archivo} desde SNAP...")
    
    # Descargar archivo .gz
    archivo_gz = nombre_archivo + ".gz"
    
    try:
        urllib.request.urlretrieve(url, archivo_gz)
        print(f"✓ Descarga completa: {archivo_gz}")
        
        # Descomprimir
        print(f"Descomprimiendo...")
        with gzip.open(archivo_gz, 'rb') as f_in:
            with open(nombre_archivo, 'wb') as f_out:
                f_out.write(f_in.read())
        
        print(f"✓ Archivo listo: {nombre_archivo}")
        
        # Eliminar .gz
        os.remove(archivo_gz)
        
        return True
        
    except Exception as e:
        print(f"✗ Error durante la descarga: {e}")
        return False


def main():
    """
    Función principal para gestión de datasets
    """
    print("="*50)
    print("  NeuroNet - Gestor de Datasets")
    print("="*50)
    
    # Crear datasets de prueba
    print("\n[1/3] Creando datasets de prueba locales...")
    crear_dataset_pequeno("test_graph.txt", num_nodos=50)
    crear_dataset_lineal("linear_graph.txt", longitud=100)
    
    print("\n[2/3] Creando dataset mediano...")
    crear_dataset_pequeno("medium_graph.txt", num_nodos=1000)
    
    print("\n[3/3] Opciones de descarga SNAP:")
    print("""
    Datasets disponibles (descomentar para descargar):
    
    1. web-Google (875k nodos, 5M aristas) - Red de páginas web
       URL: https://snap.stanford.edu/data/web-Google.txt.gz
    
    2. amazon0601 (403k nodos, 3.3M aristas) - Red de productos
       URL: https://snap.stanford.edu/data/amazon0601.txt.gz
    
    3. roadNet-CA (1.9M nodos, 2.7M aristas) - Red de carreteras
       URL: https://snap.stanford.edu/data/roadNet-CA.txt.gz
    
    Para descargar, descomente las líneas correspondientes abajo.
    """)
    
    # Descomentar para descargar datasets reales:
    # descargar_dataset_snap(
    #     "https://snap.stanford.edu/data/web-Google.txt.gz",
    #     "web-Google.txt"
    # )
    
    print("\n" + "="*50)
    print("Datasets listos. Utilice los archivos .txt para pruebas.")
    print("="*50)


if __name__ == "__main__":
    main()
