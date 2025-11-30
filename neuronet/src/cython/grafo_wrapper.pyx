# distutils: language = c++
# distutils: sources = src/cpp/GrafoDisperso.cpp
# cython: language_level=3

from grafo_wrapper cimport GrafoDisperso
from libcpp.vector cimport vector
from libcpp.pair cimport pair
import time

cdef class PyGrafoDisperso:
    """
    Wrapper de Python para la clase GrafoDisperso de C++.
    Proporciona una interfaz Pythonic para el motor de grafos optimizado.
    """
    cdef GrafoDisperso* c_grafo  # Puntero a la instancia de C++
    cdef public double tiempo_carga  # Tiempo de carga en segundos
    
    def __cinit__(self):
        """Constructor: Crea una instancia del grafo C++"""
        self.c_grafo = new GrafoDisperso()
        self.tiempo_carga = 0.0
        print("[Cython] Wrapper creado exitosamente")
    
    def __dealloc__(self):
        """Destructor: Libera la memoria del grafo C++"""
        if self.c_grafo != NULL:
            del self.c_grafo
            print("[Cython] Memoria liberada")
    
    def cargar_datos(self, archivo):
        """
        Carga un grafo desde un archivo en formato Edge List.
        
        Args:
            archivo (str): Ruta al archivo dataset
            
        Returns:
            dict: Diccionario con estadísticas de carga
        """
        inicio = time.time()
        
        # Convertir string de Python a bytes para C++
        archivo_bytes = archivo.encode('utf-8')
        
        print(f"[Cython] Iniciando carga de '{archivo}'...")
        
        try:
            self.c_grafo.cargarDatos(archivo_bytes)
        except Exception as e:
            print(f"[Cython] Error durante la carga: {e}")
            raise
        
        self.tiempo_carga = time.time() - inicio
        
        # Retornar estadísticas
        return {
            'num_nodos': self.c_grafo.getNumNodos(),
            'num_aristas': self.c_grafo.getNumAristas(),
            'tiempo_carga': self.tiempo_carga,
            'memoria_mb': self.c_grafo.getMemoriaEstimada() / (1024 * 1024)
        }
    
    def ejecutar_bfs(self, int nodo_inicio, int profundidad=-1):
        """
        Ejecuta Búsqueda en Anchura (BFS) desde un nodo inicial.
        
        Args:
            nodo_inicio (int): Nodo desde el cual iniciar la búsqueda
            profundidad (int): Profundidad máxima (-1 para ilimitado)
            
        Returns:
            list: Lista de nodos visitados (IDs originales)
        """
        print(f"[Cython] Solicitud BFS desde nodo {nodo_inicio}, profundidad {profundidad}")
        
        cdef vector[int] resultado_cpp
        
        try:
            resultado_cpp = self.c_grafo.BFS(nodo_inicio, profundidad)
        except Exception as e:
            print(f"[Cython] Error en BFS: {e}")
            return []
        
        # Convertir vector de C++ a lista de Python
        resultado_py = list(resultado_cpp)
        
        print(f"[Cython] Retornando {len(resultado_py)} nodos a Python")
        return resultado_py
    
    def ejecutar_dfs(self, int nodo_inicio):
        """
        Ejecuta Búsqueda en Profundidad (DFS) desde un nodo inicial.
        
        Args:
            nodo_inicio (int): Nodo desde el cual iniciar la búsqueda
            
        Returns:
            list: Lista de nodos visitados
        """
        print(f"[Cython] Solicitud DFS desde nodo {nodo_inicio}")
        
        cdef vector[int] resultado_cpp = self.c_grafo.DFS(nodo_inicio)
        return list(resultado_cpp)
    
    def obtener_grado(self, int nodo):
        """
        Obtiene el grado (número de vecinos) de un nodo.
        
        Args:
            nodo (int): ID del nodo
            
        Returns:
            int: Grado del nodo
        """
        return self.c_grafo.obtenerGrado(nodo)
    
    def get_vecinos(self, int nodo):
        """
        Obtiene los nodos vecinos de un nodo dado.
        
        Args:
            nodo (int): ID del nodo
            
        Returns:
            list: Lista de IDs de nodos vecinos
        """
        cdef vector[int] vecinos_cpp = self.c_grafo.getVecinos(nodo)
        return list(vecinos_cpp)
    
    def get_num_nodos(self):
        """Retorna el número total de nodos en el grafo"""
        return self.c_grafo.getNumNodos()
    
    def get_num_aristas(self):
        """Retorna el número total de aristas en el grafo"""
        return self.c_grafo.getNumAristas()
    
    def get_nodo_mayor_grado(self):
        """
        Encuentra el nodo con el mayor número de conexiones.
        
        Returns:
            int: ID del nodo con mayor grado
        """
        return self.c_grafo.getNodoMayorGrado()
    
    def get_aristas_subgrafo(self, nodos):
        """
        Obtiene las aristas entre un conjunto de nodos.
        
        Args:
            nodos (list): Lista de IDs de nodos
            
        Returns:
            list: Lista de tuplas (nodo1, nodo2) representando aristas
        """
        cdef vector[int] nodos_cpp
        cdef vector[pair[int, int]] aristas_cpp
        
        # Convertir lista de Python a vector de C++
        for nodo in nodos:
            nodos_cpp.push_back(nodo)
        
        aristas_cpp = self.c_grafo.getAristasSubgrafo(nodos_cpp)
        
        # Convertir vector de pares de C++ a lista de tuplas de Python
        aristas_py = [(arista.first, arista.second) for arista in aristas_cpp]
        
        return aristas_py
    
    def get_memoria_estimada(self):
        """
        Retorna la memoria estimada utilizada por la estructura CSR.
        
        Returns:
            float: Memoria en MB
        """
        return self.c_grafo.getMemoriaEstimada() / (1024 * 1024)
    
    def get_estadisticas(self):
        """
        Retorna un diccionario con todas las estadísticas del grafo.
        
        Returns:
            dict: Estadísticas completas
        """
        nodo_max = self.get_nodo_mayor_grado()
        
        return {
            'num_nodos': self.get_num_nodos(),
            'num_aristas': self.get_num_aristas(),
            'nodo_mayor_grado': nodo_max,
            'grado_max': self.obtener_grado(nodo_max),
            'memoria_mb': self.get_memoria_estimada(),
            'tiempo_carga_seg': self.tiempo_carga
        }
