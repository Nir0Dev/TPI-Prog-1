"""Integrante 2 — Ordenamiento y eliminación; persistencia a cargo del I1."""

def ordenar_paises(paises, campo, descendente=False):
    """Ordenar por nombre/poblacion/superficie, sin mutar lista original."""
    raise NotImplementedError

def eliminar_pais(paises, nombre):
    """Devolver lista sin país seleccionado; confirmación se solicita en main."""
    pais_elegido = nombre.strip().lower()
    for i, pais in enumerate(paises):
        if pais["nombre"].strip().lower() == pais_elegido:
            return (paises[:i] + paises[(i + 1):])

    print(f"No se encontró el país '{nombre.strip()}'.")
    return None

def limpiar_paises(paises):
    """Devolver lista vacía; main exige CONFIRMAR y gestion_paises guarda encabezados."""
    if len(paises) == 0:
        print("La lista ya está vacía.")
        return paises
    paises.clear()
    return paises