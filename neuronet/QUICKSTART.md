# Instrucciones de Inicio Rápido

## Para usar NeuroNet inmediatamente

### Opción 1: Ejecutar GUI (Recomendado)
```bash
cd /home/manzur/.gemini/antigravity/scratch/neuronet
./run.sh
```

### Opción 2: Ejecutar ejemplo de código
```bash
cd /home/manzur/.gemini/antigravity/scratch/neuronet
./venv/bin/python examples/ejemplo_uso.py
```

### Opción 3: Uso en tu propio script
```python
import sys
sys.path.insert(0, '/home/manzur/.gemini/antigravity/scratch/neuronet')
import grafo_wrapper

grafo = grafo_wrapper.PyGrafoDisperso()
stats = grafo.cargar_datos('/ruta/a/dataset.txt')
nodos = grafo.ejecutar_bfs(nodo_inicio=0, profundidad=3)
```

## Datasets incluidos

- `datasets/test_graph.txt` - 50 nodos (pruebas rápidas)
- `datasets/linear_graph.txt` - 100 nodos (validación BFS)
- `datasets/medium_graph.txt` - 1000 nodos (tests intermedios)

## Estructura del proyecto

El proyecto completo está en: `/home/manzur/.gemini/antigravity/scratch/neuronet`

Consulta el [README.md](file:///home/manzur/.gemini/antigravity/scratch/neuronet/README.md) para documentación completa.
