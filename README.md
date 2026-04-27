![Python](https://img.shields.io/badge/Python-3.x-blue)
![Status](https://img.shields.io/badge/status-complete-success)
![Made with Python](https://img.shields.io/badge/Made%20with-Python-blue?logo=python)
![Automation](https://img.shields.io/badge/Automation-Pipeline-green)
![Made with love](https://img.shields.io/badge/Made%20with-❤-red)

## PIPELINE DE COMPRESIÓN Y GENERACIÓN DE LOG - PYTHON

## DESCRIPCIÓN:

Este proyecto implementa un pipeline automatizado para la compresión de archivos y generación de logs detallados en formato CSV.

El sistema procesa una carpeta raíz que contiene múltiples subcarpetas, comprimiendo archivos individuales en formato ZIP, generando una estructura intermedia y finalmente creando un archivo consolidado en formato TAR.GZ.

Durante el proceso, se recolectan métricas relevantes como tamaño de archivos, cantidad de registros, hash MD5 y tiempos de compresión, permitiendo auditoría y trazabilidad completa.

## FUNCIONALIDADES PRINCIPALES:

Compresión individual de archivos en formato .zip
Generación de estructura intermedia de trabajo
Compresión final en formato .tar.gz
Generación automática de log en archivo .csv
Cálculo de tamaño de archivos y carpetas en MB
Conteo de archivos por carpeta
Cálculo de hash MD5 del archivo final
Lectura opcional de registros en archivos .dbf
Medición del tiempo de compresión (ZIP y TAR)
Eliminación automática de carpeta temporal

## TECNOLOGÍAS UTILIZADAS:

Python
pathlib
zipfile
tarfile
hashlib
csv
shutil
time
dbfread

## FLUJO DEL PROCESO:

Lectura de carpeta raíz
Filtrado de subcarpetas según configuración
Compresión individual de archivos en ZIP
Creación de estructura temporal
Compresión global en TAR.GZ
Cálculo de métricas (tamaño, MD5, tiempos)
Generación de log en CSV
Eliminación de archivos temporales

## ESTRUCTURA ESPERADA:

El script trabaja con una carpeta raíz que contiene subcarpetas:

Ejemplo:

Carpeta_Raiz/
R01/
R02/
R03/
...

Cada subcarpeta contiene archivos a procesar.

CONFIGURACIÓN DE CARPETAS A PROCESAR:

Las subcarpetas a procesar se definen mediante una lista configurable dentro del código:

Carpetas_Objetivo = [
"R01", "R02", "R03", ...
]

Este diseño permite adaptar el script a diferentes estructuras de carpetas sin depender de una nomenclatura fija.

Ejemplo personalizado:

Carpetas_Objetivo = [
"Ventas",
"Clientes",
"Reportes"
]

También es posible extender la lógica para:

Procesar todas las carpetas sin filtro
Leer configuración desde archivo externo (JSON/CSV)
Usar diccionarios para mapeo de nombres

## RESULTADOS GENERADOS:

El sistema produce:

Archivos .zip por cada archivo original
Un archivo consolidado en formato .tar.gz
Un archivo .csv con el log del proceso
Carpeta temporal de trabajo (eliminada automáticamente)

## COLUMNAS DEL LOG:

Archivo
Tamaño de archivos (MB)
Cantidad de archivos
MD5
Tipo de Archivo
Registros DBF
Tiempo Compresión
Notificación

## CONFIGURACIÓN:

Antes de ejecutar el script, se deben modificar las siguientes rutas:

ruta_raiz = "RUTA_DE_ENTRADA"
ruta_trabajo = "RUTA_TEMPORAL"
ruta_salida = "RUTA_DE_SALIDA"
ruta_log = "RUTA_DEL_LOG"

## EJECUCIÓN:

Ejecutar desde terminal:

python pipeline_compresion_log.py

## DEPENDENCIAS:

Instalar la librería necesaria:

pip install dbfread

## NOTAS*:

No incluir rutas personales en repositorios públicos
No subir archivos comprimidos generados
No subir logs con información sensible
El script está diseñado para procesamiento batch de grandes volúmenes de archivos

## AUTOR:

Jorge Fernando Ortiz Bravo
