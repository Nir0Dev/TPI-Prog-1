"""Integrante 2 — Ordenamiento y eliminación; persistencia a cargo del I1."""
import unicodedata

def normalizar_texto(texto):
    texto = unicodedata.normalize("NFD", texto)
    texto = "".join(c for c in texto if unicodedata.category(c) != "Mn")
    texto.strip().lower()
    return texto


def ordenar_paises(paises, campo, descendente=False):
    """Ordenar por nombre/poblacion/superficie, sin mutar lista original."""
    campo = normalizar_texto(campo)
    try:
        if campo not in ["nombre", "poblacion", "superficie"]:
            raise ValueError(f"Campo '{campo}' no válido para ordenar.")

        if campo == "superficie":
            while True:
                print("Desea ordenar por superficie de forma ascendente('asc') o desendente('dsc'): ", end="")
                opcion = input("").strip().lower()
                if opcion not in ("asc", "dsc"):
                    print("Debe seleccionar 'asc' o 'dsc'")
                    continue
                else: 
                    descendente = opcion == "dsc"
                    break

        paises_ordenados = sorted(paises, key=lambda x: x[campo], reverse=descendente)
        return paises_ordenados, campo
    except ValueError as error:
        print(error)
        return None

def eliminar_pais(paises, nombre):
    """Devolver lista sin país seleccionado; confirmación se solicita en main."""
    pais_elegido = normalizar_texto(nombre)

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