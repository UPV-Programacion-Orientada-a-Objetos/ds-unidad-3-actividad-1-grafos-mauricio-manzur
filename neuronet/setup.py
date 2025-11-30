from setuptools import setup, Extension
from Cython.Build import cythonize
import numpy as np

# Configuración de la extensión de Cython
extension = Extension(
    name="grafo_wrapper",
    sources=[
        "src/cython/grafo_wrapper.pyx",
        "src/cpp/GrafoDisperso.cpp"
    ],
    language="c++",
    include_dirs=[
        "src/cpp",
        np.get_include()
    ],
    extra_compile_args=[
        "-std=c++11",
        "-O3",
        "-Wall"
    ],
    extra_link_args=["-std=c++11"]
)

setup(
    name="NeuroNet",
    version="1.0.0",
    description="Sistema de Análisis de Redes Masivas con C++ y Python",
    author="Global Connectivity Watch",
    ext_modules=cythonize(
        [extension],
        compiler_directives={
            'language_level': "3",
            'embedsignature': True
        }
    ),
    zip_safe=False,
)
