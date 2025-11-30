#include "GrafoDisperso.h"
#include <fstream>
#include <sstream>
#include <iostream>
#include <queue>
#include <stack>
#include <algorithm>
#include <chrono>

GrafoDisperso::GrafoDisperso() : num_nodos(0), num_aristas(0) {
    std::cout << "[C++ Core] Inicializando GrafoDisperso..." << std::endl;
}

GrafoDisperso::~GrafoDisperso() {
    // Los vectores se liberan automáticamente
}

void GrafoDisperso::cargarDatos(const char* archivo) {
    std::cout << "[C++ Core] Cargando dataset '" << archivo << "'..." << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    std::ifstream file(archivo);
    if (!file.is_open()) {
        throw std::runtime_error("No se puede abrir el archivo");
    }
    
    // Primera pasada: identificar todos los nodos únicos
    std::unordered_set<int> nodos_unicos;
    std::vector<std::pair<int, int>> aristas;
    
    std::string linea;
    int contador_lineas = 0;
    
    while (std::getline(file, linea)) {
        // Saltar comentarios y líneas vacías
        if (linea.empty() || linea[0] == '#') continue;
        
        std::istringstream iss(linea);
        int nodo1, nodo2;
        
        if (iss >> nodo1 >> nodo2) {
            nodos_unicos.insert(nodo1);
            nodos_unicos.insert(nodo2);
            aristas.push_back({nodo1, nodo2});
            contador_lineas++;
            
            // Log de progreso cada 100k aristas
            if (contador_lineas % 100000 == 0) {
                std::cout << "[C++ Core] Procesadas " << contador_lineas << " aristas..." << std::endl;
            }
        }
    }
    
    file.close();
    
    num_nodos = nodos_unicos.size();
    num_aristas = aristas.size();
    
    std::cout << "[C++ Core] Carga completa. Nodos: " << num_nodos 
              << " | Aristas: " << num_aristas << std::endl;
    
    // Crear mapeo de nodos a índices consecutivos
    int indice = 0;
    for (int nodo : nodos_unicos) {
        nodo_a_indice[nodo] = indice;
        indice_a_nodo[indice] = nodo;
        indice++;
    }
    
    // Crear estructura temporal de adyacencia
    adj_temp.resize(num_nodos);
    
    for (const auto& arista : aristas) {
        int idx1 = nodo_a_indice[arista.first];
        int idx2 = nodo_a_indice[arista.second];
        adj_temp[idx1].push_back(idx2);
    }
    
    // Ordenar vecinos para búsquedas eficientes
    for (auto& vecinos : adj_temp) {
        std::sort(vecinos.begin(), vecinos.end());
    }
    
    // Construir estructura CSR
    construirCSR();
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::milliseconds>(fin - inicio);
    
    std::cout << "[C++ Core] Estructura CSR construida. Memoria estimada: " 
              << getMemoriaEstimada() / (1024 * 1024) << " MB." << std::endl;
    std::cout << "[C++ Core] Tiempo de carga: " << duracion.count() << " ms." << std::endl;
}

void GrafoDisperso::construirCSR() {
    // Inicializar row_ptr
    row_ptr.resize(num_nodos + 1);
    row_ptr[0] = 0;
    
    // Construir row_ptr y vectores de datos
    for (int i = 0; i < num_nodos; i++) {
        row_ptr[i + 1] = row_ptr[i] + adj_temp[i].size();
        
        for (int vecino : adj_temp[i]) {
            col_indices.push_back(vecino);
            valores.push_back(1);  // Grafo no ponderado
        }
    }
    
    // Liberar memoria temporal
    adj_temp.clear();
    adj_temp.shrink_to_fit();
}

std::vector<int> GrafoDisperso::BFS(int nodoInicio, int profundidad) {
    std::cout << "[C++ Core] Ejecutando BFS desde nodo " << nodoInicio 
              << ", profundidad máxima: " << profundidad << std::endl;
    
    auto inicio = std::chrono::high_resolution_clock::now();
    
    if (nodo_a_indice.find(nodoInicio) == nodo_a_indice.end()) {
        std::cout << "[C++ Core] Nodo " << nodoInicio << " no existe en el grafo." << std::endl;
        return {};
    }
    
    int idx_inicio = nodoAIndice(nodoInicio);
    
    std::vector<int> resultado;
    std::unordered_set<int> visitados;
    std::queue<std::pair<int, int>> cola;  // (índice, nivel)
    
    cola.push({idx_inicio, 0});
    visitados.insert(idx_inicio);
    
    while (!cola.empty()) {
        auto [idx_actual, nivel] = cola.front();
        cola.pop();
        
        resultado.push_back(indiceANodo(idx_actual));
        
        // Si hemos alcanzado la profundidad máxima, no expandir más
        if (profundidad >= 0 && nivel >= profundidad) {
            continue;
        }
        
        // Obtener vecinos desde CSR
        int inicio_vecinos = row_ptr[idx_actual];
        int fin_vecinos = row_ptr[idx_actual + 1];
        
        for (int i = inicio_vecinos; i < fin_vecinos; i++) {
            int idx_vecino = col_indices[i];
            
            if (visitados.find(idx_vecino) == visitados.end()) {
                visitados.insert(idx_vecino);
                cola.push({idx_vecino, nivel + 1});
            }
        }
    }
    
    auto fin = std::chrono::high_resolution_clock::now();
    auto duracion = std::chrono::duration_cast<std::chrono::microseconds>(fin - inicio);
    
    std::cout << "[C++ Core] BFS completado. Nodos encontrados: " << resultado.size() 
              << ". Tiempo: " << duracion.count() / 1000.0 << " ms." << std::endl;
    
    return resultado;
}

std::vector<int> GrafoDisperso::DFS(int nodoInicio) {
    std::cout << "[C++ Core] Ejecutando DFS desde nodo " << nodoInicio << std::endl;
    
    if (nodo_a_indice.find(nodoInicio) == nodo_a_indice.end()) {
        return {};
    }
    
    int idx_inicio = nodoAIndice(nodoInicio);
    
    std::vector<int> resultado;
    std::unordered_set<int> visitados;
    std::stack<int> pila;
    
    pila.push(idx_inicio);
    
    while (!pila.empty()) {
        int idx_actual = pila.top();
        pila.pop();
        
        if (visitados.find(idx_actual) != visitados.end()) {
            continue;
        }
        
        visitados.insert(idx_actual);
        resultado.push_back(indiceANodo(idx_actual));
        
        // Obtener vecinos desde CSR
        int inicio_vecinos = row_ptr[idx_actual];
        int fin_vecinos = row_ptr[idx_actual + 1];
        
        for (int i = fin_vecinos - 1; i >= inicio_vecinos; i--) {
            int idx_vecino = col_indices[i];
            if (visitados.find(idx_vecino) == visitados.end()) {
                pila.push(idx_vecino);
            }
        }
    }
    
    std::cout << "[C++ Core] DFS completado. Nodos visitados: " << resultado.size() << std::endl;
    
    return resultado;
}

int GrafoDisperso::obtenerGrado(int nodo) {
    if (nodo_a_indice.find(nodo) == nodo_a_indice.end()) {
        return 0;
    }
    
    int idx = nodoAIndice(nodo);
    return row_ptr[idx + 1] - row_ptr[idx];
}

std::vector<int> GrafoDisperso::getVecinos(int nodo) {
    std::vector<int> vecinos;
    
    if (nodo_a_indice.find(nodo) == nodo_a_indice.end()) {
        return vecinos;
    }
    
    int idx = nodoAIndice(nodo);
    int inicio = row_ptr[idx];
    int fin = row_ptr[idx + 1];
    
    for (int i = inicio; i < fin; i++) {
        vecinos.push_back(indiceANodo(col_indices[i]));
    }
    
    return vecinos;
}

int GrafoDisperso::getNumNodos() const {
    return num_nodos;
}

int GrafoDisperso::getNumAristas() const {
    return num_aristas;
}

int GrafoDisperso::getNodoMayorGrado() {
    int max_grado = -1;
    int nodo_max = -1;
    
    for (int i = 0; i < num_nodos; i++) {
        int grado = row_ptr[i + 1] - row_ptr[i];
        if (grado > max_grado) {
            max_grado = grado;
            nodo_max = indiceANodo(i);
        }
    }
    
    std::cout << "[C++ Core] Nodo con mayor grado: " << nodo_max 
              << " (grado: " << max_grado << ")" << std::endl;
    
    return nodo_max;
}

std::vector<std::pair<int, int>> GrafoDisperso::getAristasSubgrafo(const std::vector<int>& nodos) {
    std::vector<std::pair<int, int>> aristas;
    std::unordered_set<int> conjunto_nodos(nodos.begin(), nodos.end());
    
    for (int nodo : nodos) {
        if (nodo_a_indice.find(nodo) == nodo_a_indice.end()) {
            continue;
        }
        
        int idx = nodoAIndice(nodo);
        int inicio = row_ptr[idx];
        int fin = row_ptr[idx + 1];
        
        for (int i = inicio; i < fin; i++) {
            int vecino = indiceANodo(col_indices[i]);
            
            // Solo incluir aristas donde ambos nodos están en el subgrafo
            if (conjunto_nodos.find(vecino) != conjunto_nodos.end()) {
                aristas.push_back({nodo, vecino});
            }
        }
    }
    
    return aristas;
}

size_t GrafoDisperso::getMemoriaEstimada() const {
    size_t memoria = 0;
    memoria += row_ptr.size() * sizeof(int);
    memoria += col_indices.size() * sizeof(int);
    memoria += valores.size() * sizeof(int);
    memoria += nodo_a_indice.size() * (sizeof(int) * 2 + 32);  // Overhead de unordered_map
    memoria += indice_a_nodo.size() * (sizeof(int) * 2 + 32);
    return memoria;
}

int GrafoDisperso::nodoAIndice(int nodo) const {
    auto it = nodo_a_indice.find(nodo);
    return (it != nodo_a_indice.end()) ? it->second : -1;
}

int GrafoDisperso::indiceANodo(int indice) const {
    auto it = indice_a_nodo.find(indice);
    return (it != indice_a_nodo.end()) ? it->second : -1;
}
