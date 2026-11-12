def resumen_estadistico(paises):
    """Mayor y menor población; promedio población/superficie; conteo continente.

    Manejar lista vacía y devolver un diccionario para mostrar en consola/figura.
    """
    if not paises:
        print("No hay paises cargados para calcular estadisticas.")
        return None

    mayor = paises[0]
    menor = paises[0]

    suma_poblacion = 0
    suma_superficie = 0
    cantidad = 0

    paises_por_continente = {}

    for pais in paises:
        suma_poblacion += pais["poblacion"]
        suma_superficie += pais["superficie"]
        cantidad += 1

        continente = pais["continente"]

        if continente in paises_por_continente:
            paises_por_continente[continente] += 1
        else:
            paises_por_continente[continente] = 1

        if pais["poblacion"] > mayor["poblacion"]:
            mayor = pais
            
        if pais["poblacion"] < menor["poblacion"]:
            menor = pais

    promedio_poblacion = suma_poblacion / cantidad
    promedio_superficie = suma_superficie / cantidad

    return {
        "mayor_poblacion": mayor,
        "menor_poblacion": menor,
        "promedio_poblacion": promedio_poblacion,
        "promedio_superficie": promedio_superficie,
        "paises_por_continente": paises_por_continente
    }

def calcular_densidad(pais):
    """Habitantes por km²; no dividir por cero."""
    poblacion = pais["poblacion"]
    superficie = pais["superficie"]

    if superficie <= 0:
        print("Error: la superficie debe ser mayor a cero para calcular la densidad.")
        return None

    if poblacion < 0:
        print("Error: la poblacion no puede ser negativa.")
        return None

    densidad = poblacion / superficie
    return densidad

def estadisticas_pais(pais):
    """Preparar nombre, población, superficie, continente, densidad y extras."""
    densidad = calcular_densidad(pais)

    if densidad is None:
        return None

    resultado = pais.copy()
    resultado["densidad"] = densidad

    return resultado
