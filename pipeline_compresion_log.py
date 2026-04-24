###### 17 P. 
# PIPELINE_COMPRESION_LOG.py 3.0
# Objetivo: Comprimir archivos y carpetas en formatos ZIP y TAR.GZ y crear un log con informacion de los archivos como tamaño en MB, tiempo de compresion, cantidad de archivos por carpeta y MD5 de carpeta RAIZ comprimida.
# Notas Version 3.0: Se añade funcion para contar el tiempo de compresion 
# Creación 20/04/2026
# Modificación: 24/04/2026
# Autor: Jorge Fernando Ortiz Bravo
######


from pathlib import Path
import tarfile
import zipfile
import hashlib
import csv
from dbfread import DBF
import shutil
import time


###### 
# DICCIONARIO
######

Carpetas_Objetivo= [
    "R01","R02","R03","R04","R05","R06","R07","R08",
    "R10","R11","R12","R13","R14","R15","R16","R17",
    "R18","R19","R20","R21","R22","R23","R24","R25",
    "R26","R27","R28","R29","R30","R31"
]

###### 
# FUNCIONES
######

# Calcula el tamaño de un archivo en Megabytes
def tamaño_mb_archivo(ruta: Path) -> float:
    return round(ruta.stat().st_size / (1024 * 1024), 4)


# Calcula el tamaño de una carpeta
def tamaño_mb_carpeta(ruta: Path) -> float:
    total = 0
    for archivo in ruta.iterdir():
        if archivo.is_file():
            total += archivo.stat().st_size
    return round(total / (1024 * 1024), 4)


# Calcula tamaño de carpeta nodriza
def tamaño_mb_carpeta_nodriza(ruta: Path) -> float:
    total = 0
    for archivo in ruta.rglob("*"):
        if archivo.is_file():
            total += archivo.stat().st_size
    return round(total / (1024 * 1024), 4)


# Cuenta archivos
def contar_archivos(ruta: Path) -> int:
    return sum(1 for archivo in ruta.rglob("*") if archivo.is_file())


# MD5
def calcular_md5(ruta_archivo: Path, chunk_size: int = 65536) -> str:
    md5 = hashlib.md5()
    with open(ruta_archivo, "rb") as f:
        for chunk in iter(lambda: f.read(chunk_size), b""):
            md5.update(chunk)
    return md5.hexdigest()


# Registros DBF
def contar_registros_dbf(ruta_archivo: Path) -> int | str:
    try:
        tabla = DBF(str(ruta_archivo), load=False)
        return len(tabla)
    except Exception:
        return "archivo dañado"


# Comprimir archivo ZIP
def comprimir_archivo_zip(ruta_archivo: Path, ruta_salida: Path) -> tuple[Path | None, str, float]:

    try:
        inicio = time.perf_counter()

        ruta_salida.mkdir(parents=True, exist_ok=True)
        zip_path = ruta_salida / f"{ruta_archivo.name}.zip"

        with zipfile.ZipFile(
            zip_path,
            mode="w",
            compression=zipfile.ZIP_DEFLATED,
            compresslevel=9
        ) as zipf:
            zipf.write(ruta_archivo, arcname=ruta_archivo.name)

        fin = time.perf_counter()

        tiempo_min = (fin - inicio) / 60  # minutos

        return zip_path, "", round(tiempo_min, 4)

    except Exception:
        return None, "no se pudo comprimir", 0


# Comprime carpeta en tar.gz
def comprimir_carpeta_tar(ruta_carpeta: str | Path, ruta_salida: str) -> tuple[Path | None, str, float]:

    try:
        inicio = time.perf_counter()

        carpeta = Path(ruta_carpeta)
        salida = Path(ruta_salida)
        salida.mkdir(parents=True, exist_ok=True)

        tar_path = salida / f"{carpeta.name}.tar.gz"

        with tarfile.open(tar_path, mode="w:gz", compresslevel=9) as tar:
            tar.add(carpeta, arcname=carpeta.name)

        fin = time.perf_counter()

        tiempo_horas = (fin - inicio) / 3600  # horas

        return tar_path, "", round(tiempo_horas, 4)

    except Exception:
        return None, "no se pudo comprimir", 0


###
# Creacion estructura interna
###
def crear_estructura_zip_interna(ruta_raiz: str, ruta_trabajo: str) -> Path:
    raiz = Path(ruta_raiz)
    trabajo = Path(ruta_trabajo)

    carpeta_destino = trabajo / raiz.name

    if carpeta_destino.exists():
        shutil.rmtree(carpeta_destino)

    carpeta_destino.mkdir(parents=True, exist_ok=True)

    for carpeta_entidad in raiz.iterdir():
        if carpeta_entidad.is_dir() and carpeta_entidad.name in Carpetas_Objetivo:
            destino_entidad = carpeta_destino / carpeta_entidad.name
            destino_entidad.mkdir(parents=True, exist_ok=True)

            for archivo in carpeta_entidad.iterdir():
                if archivo.is_file():
                    comprimir_archivo_zip(archivo, destino_entidad)

    return carpeta_destino


######
# LOG
######

def escribir_log_csv(registros: list[dict], ruta_log: Path) -> None:
    columnas = [
        "Archivo","Tamaño de archivos","Cantidad de archivos",
        "MD5","Tipo de Archivo","Registros DBF", "Tiempo Compresion","Notificacion"
    ]

    ruta_log.parent.mkdir(parents=True, exist_ok=True)

    with open(ruta_log, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.DictWriter(f, fieldnames=columnas)
        writer.writeheader()
        writer.writerows(registros)

def generar_log_compresion(
    ruta_raiz: str,
    ruta_trabajo: str,
    ruta_salida: str,
    ruta_log: str,
    calcular_dbf: bool = False
) -> None:

    raiz = Path(ruta_raiz)
    salida = Path(ruta_salida)
    log_path = Path(ruta_log)

    registros = []

    # Crear estructura con ZIP internos
    carpeta_preparada = crear_estructura_zip_interna(ruta_raiz, ruta_trabajo)

    # RAIZ original
    registros.append({
        "Archivo": raiz.name,
        "Tamaño de archivos": tamaño_mb_carpeta_nodriza(raiz),
        "Cantidad de archivos": contar_archivos(raiz),
        "MD5": "",
        "Tipo de Archivo": "carpeta",
        "Registros DBF": "",
        "Notificacion": "",
    })

    for carpeta in raiz.iterdir():
        if carpeta.is_dir() and carpeta.name in Carpetas_Objetivo:

            registros.append({
                "Archivo": carpeta.name,
                "Tamaño de archivos": tamaño_mb_carpeta(carpeta),
                "Cantidad de archivos": contar_archivos(carpeta),
                "MD5": "",
                "Tipo de Archivo": "carpeta",
                "Registros DBF": "",
                "Notificacion": "",
            })

            carpeta_zip = carpeta_preparada / carpeta.name

            for archivo in carpeta.iterdir():
                if archivo.is_file():

                    registros_dbf = ""
                    notificacion = ""

                    if archivo.suffix.lower() == ".dbf" and calcular_dbf:
                        resultado = contar_registros_dbf(archivo)
                        if resultado == "archivo dañado":
                            notificacion = "archivo dañado"
                        else:
                            registros_dbf = resultado

                    # archivo original
                    registros.append({
                        "Archivo": archivo.name,
                        "Tamaño de archivos": tamaño_mb_archivo(archivo),
                        "Cantidad de archivos": "",
                        "MD5": "",
                        "Tipo de Archivo": ".dbf",
                        "Registros DBF": registros_dbf,
                        "Notificacion": notificacion,
                    })

                    # archivo zip interno
                    zip_generado, notif_zip, tiempo_zip = comprimir_archivo_zip(archivo, carpeta_zip)

                    registros.append({
                        "Archivo": zip_generado.name,
                        "Tamaño de archivos": tamaño_mb_archivo(zip_generado),
                        "Cantidad de archivos": "",
                        "MD5": "",
                        "Tipo de Archivo": ".zip",
                        "Registros DBF": "",
                        "Tiempo Compresion": tiempo_zip,
                        "Notificacion": "",
                    })

    tar_path, notif_tar, tiempo_tar = comprimir_carpeta_tar(carpeta_preparada, salida)

    registros.append({
        "Archivo": tar_path.name,
        "Tamaño de archivos": tamaño_mb_archivo(tar_path),
        "Cantidad de archivos": "",
        "MD5": calcular_md5(tar_path),
        "Tipo de Archivo": ".tar.gz",
        "Registros DBF": "",
        "Tiempo Compresion": tiempo_tar,
        "Notificacion": notif_tar,
    })

    escribir_log_csv(registros, log_path)

    print(f"Log generado en: {log_path}")

    shutil.rmtree(ruta_trabajo) # borrar carpeta temporal

######
# Ejecucion
######

ruta_raiz = r"E:\Carpeta_con_Subcarpetas_DBF"
ruta_trabajo = r"E:\TEMP_COMPRESION"
ruta_salida = r"E:\Carpeta_salida_Comprimida"
ruta_log = r"E:\Log.csv"

generar_log_compresion(
    ruta_raiz=ruta_raiz,
    ruta_trabajo=ruta_trabajo,
    ruta_salida=ruta_salida,
    ruta_log=ruta_log,
    calcular_dbf=True
)