"""Integrante 2 — Búsquedas y filtros (sin alterar el CSV)."""

def buscar_pais(paises, texto, exacta=False):
    """Buscar por nombre, parcial o exacto, ignorando mayúsculas."""
    raise NotImplementedError

def filtrar_continente(paises, continente):
    """Devolver países del continente solicitado."""
    raise NotImplementedError

def filtrar_rango(paises, campo, minimo, maximo):
    """campo: 'poblacion' o 'superficie'; validar rango y devolver coincidencias."""
    raise NotImplementedError
