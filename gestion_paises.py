"""Integrante 1 — CSV, persistencia y validaciones."""
from pathlib import Path

RUTA_CSV = Path(__file__).resolve().parent / "data" / "paises.csv"
COLUMNAS_OBLIGATORIAS = ("nombre", "poblacion", "superficie", "continente")

def crear_plantilla(ruta=RUTA_CSV):
    """Crear carpeta y CSV con encabezados si falta; NO sobrescribir datos existentes."""
    raise NotImplementedError

def cargar_paises(ruta=RUTA_CSV):
    """Devolver lista[dict]; usar csv.DictReader, validar y tipar números."""
    raise NotImplementedError

def validar_pais(pais):
    """Comprobar campos obligatorios no vacíos, población >= 0 y superficie > 0."""
    raise NotImplementedError

def agregar_pais(paises, pais):
    """Agregar registro validado sin duplicar nombres; devolver lista actualizada."""
    raise NotImplementedError

def actualizar_pais(paises, nombre, cambios):
    """Actualizar país existente preservando columnas extras; devolver resultado."""
    raise NotImplementedError

def guardar_paises(paises, ruta=RUTA_CSV):
    """Guardar con csv.DictWriter; mantener columnas mínimas y extras de la API."""
    raise NotImplementedError
