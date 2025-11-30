#ifndef GRAFO_BASE_H
#define GRAFO_BASE_H

#include <vector>
#include <string>

/**
 * Clase abstracta que define la interfaz para un grafo.
 * Todos los métodos son virtuales puros para forzar la implementación
 * en las clases derivadas.
 */
class GrafoBase {
public:
    virtual ~GrafoBase() {}
    
    /**
     * Carga un grafo desde un archivo en formato Edge List
     * @param archivo Ruta al archivo (formato: "nodo1 nodo2" por línea)
     */
    virtual void cargarDatos(const char* archivo) = 0;
    
    /**
     * Búsqueda en anchura (Breadth-First Search) desde un nodo inicial
     * @param nodoInicio Nodo desde el cual iniciar la búsqueda
     * @param profundidad Profundidad máxima a explorar (-1 para ilimitado)
     * @return Vector con los IDs de nodos visitados
     */
    virtual std::vector<int> BFS(int nodoInicio, int profundidad) = 0;
    
    /**
     * Búsqueda en profundidad (Depth-First Search) desde un nodo inicial
     * @param nodoInicio Nodo desde el cual iniciar la búsqueda
     * @return Vector con los IDs de nodos visitados
     */
    virtual std::vector<int> DFS(int nodoInicio) = 0;
    
    /**
     * Obtiene el grado de salida de un nodo (número de vecinos)
     * @param nodo ID del nodo
     * @return Número de aristas salientes desde el nodo
     */
    virtual int obtenerGrado(int nodo) = 0;
    
    /**
     * Obtiene los vecinos directos de un nodo
     * @param nodo ID del nodo
     * @return Vector con los IDs de los nodos vecinos
     */
    virtual std::vector<int> getVecinos(int nodo) = 0;
    
    /**
     * @return Número total de nodos en el grafo
     */
    virtual int getNumNodos() const = 0;
    
    /**
     * @return Número total de aristas en el grafo
     */
    virtual int getNumAristas() const = 0;
    
    /**
     * Encuentra el nodo con el mayor grado en el grafo
     * @return ID del nodo con más conexiones
     */
    virtual int getNodoMayorGrado() = 0;
    
    /**
     * Obtiene las aristas del subgrafo resultante de una búsqueda
     * @param nodos Vector de nodos del subgrafo
     * @return Vector de pares (nodo1, nodo2) representando aristas
     */
    virtual std::vector<std::pair<int, int>> getAristasSubgrafo(const std::vector<int>& nodos) = 0;
};

#endif // GRAFO_BASE_H
