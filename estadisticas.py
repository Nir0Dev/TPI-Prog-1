def resumen_estadistico(paises):
    """Calcular estadísticas generales y manejar datos incorrectos."""
    if not paises:
        print("No hay países cargados para calcular estadísticas.")
        return None

    try:
        mayor = paises[0]
        menor = paises[0]

        suma_poblacion = 0
        suma_superficie = 0
        cantidad = 0

        paises_por_continente = {}

        for pais in paises:
            poblacion = pais["poblacion"]
            superficie = pais["superficie"]
            continente = pais["continente"]

            if poblacion < 0:
                print("Error: hay un país con población negativa.")
                return None

            if superficie <= 0:
                print("Error: hay un país con superficie menor o igual a cero.")
                return None

            if poblacion != poblacion or poblacion == float("inf"):
                print("Error: hay un país con población no finita.")
                return None

            if superficie != superficie or superficie == float("inf"):
                print("Error: hay un país con superficie no finita.")
                return None

            if not continente:
                print("Error: hay un país sin continente.")
                return None

            suma_poblacion += poblacion
            suma_superficie += superficie

            if suma_poblacion == float("inf"):
                print("Error: la suma de población es demasiado grande.")
                return None

            if suma_superficie == float("inf"):
                print("Error: la suma de superficie es demasiado grande.")
                return None
            cantidad += 1

            if continente in paises_por_continente:
                paises_por_continente[continente] += 1
            else:
                paises_por_continente[continente] = 1

            if poblacion > mayor["poblacion"]:
                mayor = pais

            if poblacion < menor["poblacion"]:
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

    except KeyError:
        print("Error: faltan datos obligatorios en alguno de los países.")
        return None

    except TypeError:
        print("Error: la estructura de los países o el tipo de sus datos es incorrecto.")
        return None

    except ZeroDivisionError:
        print("Error: no se pueden calcular promedios sin países.")
        return None

    except IndexError:
        print("Error: no se pudo acceder al primer país de la lista.")
        return None
    except OverflowError:
        print("Error: los valores son demasiado grandes para realizar el cálculo.")
        return None

def calcular_densidad(pais):
    """Calcular habitantes por km² y manejar datos incorrectos."""
    try:
        poblacion = pais["poblacion"]
        superficie = pais["superficie"]

        if poblacion < 0:
            print("Error: la población no puede ser negativa.")
            return None

        if superficie < 0:
            print("Error: la superficie no puede ser negativa.")
            return None

        if poblacion != poblacion or poblacion == float("inf"):
            print("Error: la población debe ser un número finito.")
            return None

        if superficie != superficie or superficie == float("inf"):
            print("Error: la superficie debe ser un número finito.")
            return None

        densidad = poblacion / superficie

        if densidad != densidad or densidad == float("inf"):
            print("Error: el resultado de la densidad es demasiado grande o inválido.")
            return None

        return densidad

    except ZeroDivisionError:
        print("Error: no se puede calcular la densidad con superficie cero.")
        return None

    except KeyError:
        print("Error: faltan los datos de población o superficie del país.")
        return None

    except TypeError:
        print("Error: el país debe contener población y superficie numéricas.")
        return None
    except OverflowError:
        print("Error: los valores son demasiado grandes para realizar el cálculo.")
        return None

def estadisticas_pais(pais):
    """Preparar nombre, población, superficie, continente, densidad y extras."""
    densidad = calcular_densidad(pais)

    if densidad is None:
        return None

    resultado = pais.copy()
    resultado["densidad"] = densidad

    return resultado
