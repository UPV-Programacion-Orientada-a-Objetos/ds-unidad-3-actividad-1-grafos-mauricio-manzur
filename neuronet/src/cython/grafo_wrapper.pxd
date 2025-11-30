# distutils: language = c++
# cython: language_level=3

from libcpp.vector cimport vector
from libcpp.pair cimport pair
from libcpp.string cimport string

cdef extern from "GrafoDisperso.h":
    cdef cppclass GrafoDisperso:
        GrafoDisperso() except +
        void cargarDatos(const char* archivo) except +
        vector[int] BFS(int nodoInicio, int profundidad) except +
        vector[int] DFS(int nodoInicio) except +
        int obtenerGrado(int nodo) except +
        vector[int] getVecinos(int nodo) except +
        int getNumNodos() except +
        int getNumAristas() except +
        int getNodoMayorGrado() except +
        vector[pair[int, int]] getAristasSubgrafo(const vector[int]& nodos) except +
        size_t getMemoriaEstimada() except +
