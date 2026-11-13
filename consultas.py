"""Integrante 2 — Búsquedas y filtros (sin alterar el CSV)."""
from operaciones import normalizar_texto

def pedir_entero(mensaje, minimo):
    while True:
        try:
            numero = int(input(f"{mensaje} "))

            if numero <= minimo:
                print(f"Error, debe elegir un numero mayor a {minimo}")
                continue
            
        except ValueError:
            print(f"Error, debe seleccionar un numero entero mayor a 0")
            continue
        return numero

def buscar_pais(paises, texto, exacta=False):
    """Buscar por nombre, parcial o exacto, ignorando mayúsculas."""
    try:
        texto = normalizar_texto(texto)
        if len(texto) <= 0:
            raise ValueError("No puede usar un texto vacío")
        paises_encontrados = []
        for pais in paises:
            nombre = normalizar_texto(pais["nombre"])
            if nombre.startswith(texto):
                paises_encontrados.append(pais)

        if not paises_encontrados:
            return None
        return paises_encontrados
    
    except ValueError as e:
        print(e)
        return None
    except Exception as e:
            print(f"Ocurrió un error inesperado. {e}")
            return None

def filtrar_continente(paises, continente):
    """Devolver países del continente solicitado."""
    continente = normalizar_texto(continente)
    try:
        if continente not in ["africa", "america", "asia", "europa", "oceania"]:
            raise ValueError(f"Continente '{continente}' no válido para filtrar.")
        
        paises_filtrados = []
        for pais in paises:
            if continente == normalizar_texto(pais["continente"]):
                paises_filtrados.append(pais)
        
        return paises_filtrados
        
    except ValueError as error:
        print(error)
        return None

def filtrar_rango(paises, campo):
    """campo: 'poblacion' o 'superficie'; validar rango y devolver coincidencias."""
    campo = "poblacion" if campo == "2" else "superficie"
    for pais in paises:
        print(pais["nombre"], pais[campo])
    print(f"Debe elejir un rango en de {campo} para filtrar: ")
    rango_inf = pedir_entero(f"Seleccione un mínimo para el rango de {campo}", 0)
    rango_sup = pedir_entero(f"Seleccione un máximo para el rango de {campo}", (rango_inf))

    paises_filtrados = filter(lambda pais: rango_inf <= pais[campo] <= rango_sup, paises)
    paises_filtrados = list(paises_filtrados)
    print(f"Filtrando paises por {campo} en el rango de {rango_inf:,} a {rango_sup:,}...".replace(",", "."))
    return paises_filtrados