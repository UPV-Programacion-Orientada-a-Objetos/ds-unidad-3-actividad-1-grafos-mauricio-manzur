#ifndef GRAFO_DISPERSO_H
#define GRAFO_DISPERSO_H

#include "GrafoBase.h"
#include <unordered_map>
#include <unordered_set>

/**
 * Implementación de un grafo usando formato CSR (Compressed Sparse Row)
 * para optimizar el uso de memoria en grafos dispersos (sparse).
 * 
 * La matriz de adyacencia se representa con tres vectores:
 * - row_ptr: Punteros de inicio para cada nodo
 * - col_indices: Índices de columna (vecinos)
 * - valores: Valores de las aristas (1 para grafos no ponderados)
 */
class GrafoDisperso : public GrafoBase {
private:
    // Estructura CSR
    std::vector<int> row_ptr;      // Punteros de inicio de fila (tamaño: num_nodos + 1)
    std::vector<int> col_indices;  // Índices de columnas (vecinos)
    std::vector<int> valores;      // Valores de aristas (1 para no ponderado)
    
    // Mapeo de IDs
    std::unordered_map<int, int> nodo_a_indice;  // ID original -> índice interno
    std::unordered_map<int, int> indice_a_nodo;  // índice interno -> ID original
    
    // Estadísticas
    int num_nodos;
    int num_aristas;
    
    // Dataset temporal para construcción
    std::vector<std::vector<int>> adj_temp;
    
    /**
     * Convierte la representación temporal a formato CSR
     */
    void construirCSR();
    
    /**
     * Convierte un ID de nodo original a índice interno
     */
    int nodoAIndice(int nodo) const;
    
    /**
     * Convierte un índice interno a ID de nodo original
     */
    int indiceANodo(int indice) const;
    
public:
    GrafoDisperso();
    ~GrafoDisperso();
    
    // Implementación de métodos virtuales puros
    void cargarDatos(const char* archivo) override;
    std::vector<int> BFS(int nodoInicio, int profundidad) override;
    std::vector<int> DFS(int nodoInicio) override;
    int obtenerGrado(int nodo) override;
    std::vector<int> getVecinos(int nodo) override;
    int getNumNodos() const override;
    int getNumAristas() const override;
    int getNodoMayorGrado() override;
    std::vector<std::pair<int, int>> getAristasSubgrafo(const std::vector<int>& nodos) override;
    
    /**
     * Obtiene la memoria estimada utilizada por la estructura CSR
     * @return Memoria en bytes
     */
    size_t getMemoriaEstimada() const;
};

#endif // GRAFO_DISPERSO_H
