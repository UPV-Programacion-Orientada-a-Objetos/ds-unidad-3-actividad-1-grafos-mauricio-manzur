#!/bin/bash
# Script de inicio rápido para NeuroNet

echo "=========================================="
echo "  NeuroNet - Inicio Rápido"
echo "=========================================="
echo ""

# Verificar si ya está compilado
if [ ! -f "grafo_wrapper.cpython-312-x86_64-linux-gnu.so" ]; then
    echo "⚠️  Módulo no compilado. Ejecutando compilación..."
    echo ""
    ./venv/bin/python setup.py build_ext --inplace
    
    if [ $? -ne 0 ]; then
        echo ""
        echo "❌ Error en la compilación. Verifique que tiene:"
        echo "   - Compilador C++ (g++)"
        echo "   - Python 3.7+"
        echo "   - Dependencias instaladas (pip install -r requirements.txt)"
        exit 1
    fi
    echo ""
    echo "✅ Compilación exitosa!"
    echo ""
fi

# Verificar datasets
if [ ! -f "datasets/test_graph.txt" ]; then
    echo "📊 Generando datasets de prueba..."
    cd datasets && ../venv/bin/python download_script.py && cd ..
    echo ""
fi

echo "🚀 Iniciando NeuroNet GUI..."
echo ""
./venv/bin/python src/python/neuronet_gui.py
