"""Integrante 4 — API pública World Bank Indicators (HTTP/JSON).

Indicadores: SP.POP.TOTL (población) y AG.SRF.TOTL.K2 (superficie).
Las regiones del Banco Mundial no son equivalentes a continentes.
"""
API_BASE = "https://api.worldbank.org/v2"

def consultar_indicador(codigo_iso3, indicador, inicio=None, fin=None):
    """GET con requests, timeout, errores HTTP, JSON y ausencia de datos."""
    raise NotImplementedError

def transformar_indicadores(respuesta_poblacion, respuesta_superficie):
    """Convertir respuestas JSON en lista de diccionarios con datos utilizables."""
    raise NotImplementedError

def validar_registros_api(registros):
    """Descartar datos faltantes/incorrectos y detectar duplicados."""
    raise NotImplementedError

def preparar_registros_csv(registros, paises_locales):
    """Preparar altas/actualizaciones y campos opcionales sin escribir CSV.

    La confirmación del usuario y guardar_paises() se ejecutan desde main.
    """
    raise NotImplementedError
