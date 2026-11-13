# api_paises.py - Integrante 4: API Banco Mundial
# Responsabilidad: descargar, validar y entregar registros.
# NO escribe el CSV, solo devuelve lista de diccionarios validados.
import requests
import unicodedata
from time import sleep
from gestion_paises import (
    convertir_entero,
    validar_pais,
    limpiar_texto,
    agregar_pais
)

URL_POBLACION = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
URL_SUPERFICIE = "https://api.worldbank.org/v2/country/all/indicator/AG.SRF.TOTL.K2"
URL_CATALOGO = "https://api.worldbank.org/v2/es/country"
ANIO = "2023"

def _descargar_registros(url, nombre, parametros):
    """Descargar todas las páginas y devolver una lista de diccionarios."""
    registros = []
    pagina = 1
    params = parametros.copy()

    while True:
        params["page"] = pagina

        for intento in range(1, 4):
            try:
                respuesta = requests.get(
                    url,
                    params=params,
                    timeout=(10, 45)
                )
                respuesta.raise_for_status()
                break

            except requests.exceptions.RequestException as error:
                print(
                    f"Error al descargar {nombre}, "
                    f"página {pagina}, intento {intento} de 3: {error}"
                )

                if error.response is not None:
                    estado = error.response.status_code

                    if estado < 500 and estado != 429:
                        return []

                if intento == 3:
                    print(
                        "Se agotaron los intentos. "
                        "Los datos del CSV se conservan."
                    )
                    return []

                sleep(intento * 2)

        try:
            datos = respuesta.json()
        except ValueError:
            print(f"La respuesta de {nombre} no contiene JSON válido.")
            return []

        if not isinstance(datos, list) or len(datos) != 2:
            print(f"La respuesta de {nombre} tiene un formato inesperado.")
            return []

        informacion = datos[0]
        filas = datos[1]

        if not isinstance(informacion, dict):
            print(f"La información de páginas de {nombre} no es válida.")
            return []

        if filas is None:
            print(f"No hay datos disponibles para {nombre}.")
            return []

        if not isinstance(filas, list):
            print(f"Los registros de {nombre} no tienen el formato esperado.")
            return []

        try:
            paginas = int(informacion["pages"])
        except (KeyError, TypeError, ValueError):
            print(f"No se pudo interpretar la paginación de {nombre}.")
            return []

        if paginas < pagina:
            print(f"La paginación de {nombre} es inconsistente.")
            return []

        for fila in filas:
            if not isinstance(fila, dict):
                print(f"Se recibió un registro inválido en {nombre}.")
                return []

            registros.append(fila)

        if not filas:
            print(f"No se recibieron registros en la página {pagina} de {nombre}.")
            return []

        if pagina >= paginas:
            return registros

        pagina += 1


def _descargar_indicador(url, nombre_indicador):
    """Descargar los registros de un indicador para el año elegido."""
    parametros = {
        "format": "json",
        "per_page": 400,
        "date": ANIO
    }

    return _descargar_registros(url, nombre_indicador, parametros)


def descargar_catalogo():
    """Descargar los datos descriptivos de los países."""
    parametros = {
        "format": "json",
        "per_page": 400
    }

    return _descargar_registros(
        URL_CATALOGO,
        "catálogo de países",
        parametros
    )
def obtener_continente(codigo_pais, codigo_region):
    """Determinar el continente usando la región y las excepciones geográficas."""
    codigo = str(codigo_pais or "").strip().upper()
    region = str(codigo_region or "").strip().upper()

    if not codigo:
        return None

    if region in ("LCN", "NAC"):
        return "América"

    if region == "SSF":
        return "África"

    if region == "SAS":
        return "Asia"

    if region in ("MEA", "MNA"):
        paises_africanos = (
            "DZA", "DJI", "EGY", "LBY",
            "MAR", "SDN", "TUN", "ESH"
        )

        if codigo in paises_africanos:
            return "África"

        return "Asia"

    if region == "ECS":
        paises_asiaticos = (
            "ARM", "AZE", "CYP", "GEO", "KAZ",
            "KGZ", "TJK", "TKM", "TUR", "UZB"
        )

        if codigo in paises_asiaticos:
            return "Asia"

        return "Europa"

    if region == "EAS":
        paises_oceania = (
            "ASM", "AUS", "COK", "FJI", "FSM",
            "GUM", "KIR", "MHL", "MNP", "NCL",
            "NFK", "NIU", "NRU", "NZL", "PCN",
            "PLW", "PNG", "PYF", "SLB", "TKL",
            "TON", "TUV", "VUT", "WLF", "WSM",
            "UMI"
        )

        if codigo in paises_oceania:
            return "Oceanía"

        return "Asia"

    return None

def preparar_catalogo(registros):
    """Organizar los países por código y conservar sus datos adicionales."""
    catalogo = {}

    for registro in registros:
        if not isinstance(registro, dict):
            continue

        codigo = str(registro.get("id") or "").strip().upper()
        nombre = str(registro.get("name") or "").strip()
        region = registro.get("region")

        if not codigo or not nombre:
            continue

        if not isinstance(region, dict):
            continue

        codigo_region = str(region.get("id") or "").strip()

        # Excluir agrupaciones y registros sin región identificable.
        if codigo_region in ("", "NA"):
            continue
        
        continente = obtener_continente(codigo, codigo_region)

        if continente is None:
            print(
                f"Se omitió {nombre}: "
                f"no se pudo determinar el continente "
                f"para la región '{codigo_region}'."
            )
            continue

        catalogo[codigo] = {
            "nombre": nombre,
            "continente": continente,
            "codigo_pais": codigo,
            "region": region.get("value") or "",
            "capital": registro.get("capitalCity") or "",
            "latitud": registro.get("latitude") or "",
            "longitud": registro.get("longitude") or ""
        }

    return catalogo

def _extraer_valor(registro, campo=None):
    """Convertir población a entero y redondear superficie al km²."""
    valor = registro.get("value")

    if campo == "superficie":
        if isinstance(valor, bool):
            return None

        try:
            return round(float(valor))
        except (ValueError, TypeError, OverflowError):
            return None

    return convertir_entero(valor)

def _validar_pais(nombre, poblacion, superficie, continente):
    """Valida un país. Devuelve (es_valido, motivo)."""
    if not nombre or not continente:
        return False, "falta nombre o continente"
    if poblacion is None:
        return False, "población no numérica o faltante"
    if superficie is None:
        return False, "falta superficie"
    if superficie <= 0:
        return False, "superficie debe ser mayor a 0"
    if poblacion <= 0:
        return False, "población debe ser mayor a 0"
    return True, ""

def normalizar_nombre_pais(nombre):
    """Normalizar espacios, mayúsculas y acentos para comparar nombres."""
    texto = limpiar_texto(nombre).casefold()
    texto = unicodedata.normalize("NFD", texto)

    resultado = ""

    for caracter in texto:
        if unicodedata.category(caracter) != "Mn":
            resultado += caracter

    return resultado

def _eliminar_duplicados(paises_nuevos, paises_existentes):
    """Omitir países existentes y repetidos por nombre normalizado."""
    nombres = {
        normalizar_nombre_pais(pais.get("nombre"))
        for pais in paises_existentes
    }

    nuevos = []

    for pais in paises_nuevos:
        nombre = normalizar_nombre_pais(pais.get("nombre"))

        if nombre in nombres:
            print(f"Duplicado ignorado: {pais['nombre']}")
            continue

        nombres.add(nombre)
        nuevos.append(pais)

    return nuevos

def unir_datos_paises(catalogo, datos_pob, datos_sup):
    """Unir los indicadores con el catálogo y validar cada país."""
    paises_por_codigo = {}

    for codigo, datos in catalogo.items():
        pais = datos.copy()
        pais["poblacion"] = None
        pais["superficie"] = None
        pais["anio"] = int(ANIO)

        paises_por_codigo[codigo] = pais

    indicadores = (
        ("poblacion", datos_pob),
        ("superficie", datos_sup)
    )

    for campo, registros in indicadores:
        for registro in registros:
            if not isinstance(registro, dict):
                continue

            codigo = str(
                registro.get("countryiso3code") or ""
            ).strip().upper()

            if codigo not in paises_por_codigo:
                continue

            if str(registro.get("date")) != str(ANIO):
                continue

            paises_por_codigo[codigo][campo] = _extraer_valor(
                registro, campo
            )

    validos = []
    omitidos = 0

    for pais in paises_por_codigo.values():
        pais_limpio, errores = validar_pais(pais)

        if errores:
            omitidos += 1

            nombre = pais.get("nombre") or "País sin nombre"
            print(f"País omitido: {nombre}")

            for error in errores:
                print(f"  - {error}")

            continue
        validos.append(pais_limpio)

    if omitidos > 0:
        print(
            f"Se omitieron {omitidos} países "
            "con datos obligatorios ausentes o inválidos."
        )

    return validos

def preparar_integracion_api(paises_existentes, paises_api):
    """Preparar una copia con países nuevos y datos adicionales faltantes."""
    preparados = []

    for pais in paises_existentes:
        preparados.append(pais.copy())

    campos_adicionales = (
        "codigo_pais", "region", "capital",
        "latitud", "longitud", "anio_api"
    )

    continentes_validos = (
        "américa", "europa", "asia",
        "áfrica", "oceanía", "antártida"
    )

    incorporados = 0
    completados = 0

    for recibido in paises_api:
        pais_api, errores = validar_pais(recibido)

        if errores:
            print("Registro descartado: " + " ".join(errores))
            continue

        if pais_api["continente"].casefold() not in continentes_validos:
            print(
                f"Registro descartado: continente inválido "
                f"de {pais_api['nombre']}."
            )
            continue

        if pais_api.get("anio") is not None:
            pais_api["anio_api"] = pais_api["anio"]

        nombre_api = normalizar_nombre_pais(pais_api["nombre"])
        indice = None

        for posicion, pais_local in enumerate(preparados):
            nombre_local = normalizar_nombre_pais(
                pais_local["nombre"]
            )

            if nombre_api == nombre_local:
                indice = posicion
                break

        if indice is None:
            agregado, aviso = agregar_pais(preparados, pais_api)

            if agregado:
                incorporados += 1
            else:
                print(aviso)

            continue

        pais_local = preparados[indice]
        hubo_cambios = False

        continente_local = normalizar_nombre_pais(
            pais_local.get("continente")
        )
        continente_api = normalizar_nombre_pais(
            pais_api.get("continente")
        )

        if continente_local == continente_api:
            for campo in ("nombre", "continente"):
                if pais_local.get(campo) != pais_api[campo]:
                    pais_local[campo] = pais_api[campo]
                    hubo_cambios = True      
        for campo in campos_adicionales:
            actual = pais_local.get(campo)
            nuevo = pais_api.get(campo)

            actual_vacio = (
                actual is None or str(actual).strip() == ""
            )

            nuevo_vacio = (
                nuevo is None or str(nuevo).strip() == ""
            )

            if actual_vacio and not nuevo_vacio:
                pais_local[campo] = nuevo
                hubo_cambios = True

        if hubo_cambios:
            completados += 1

    return preparados, incorporados, completados

def obtener_paises_api(paises_existentes):
    """Descargar, unir y validar los países antes de incorporarlos."""
    print(f"Descargando datos del Banco Mundial ({ANIO})...")

    registros_catalogo = descargar_catalogo()

    if not registros_catalogo:
        print("No se pudo obtener un catálogo completo.")
        return []

    catalogo = preparar_catalogo(registros_catalogo)

    if not catalogo:
        print("El catálogo no contiene países utilizables.")
        return []

    datos_pob = _descargar_indicador(
        URL_POBLACION,
        "Población SP.POP.TOTL"
    )

    if not datos_pob:
        print("No se pudo obtener población. Importación cancelada.")
        return []

    datos_sup = _descargar_indicador(
        URL_SUPERFICIE,
        "Superficie AG.SRF.TOTL.K2"
    )

    if not datos_sup:
        print("No se pudo obtener superficie. Importación cancelada.")
        return []

    validos = unir_datos_paises(catalogo, datos_pob, datos_sup)

    preparados = _eliminar_duplicados(validos, [])

    print(f"Listo: {len(preparados)} países preparados para integrar.")

    return preparados

# --- Prueba con datos simulados, sin internet (para demostrar validaciones) ---
def probar_validaciones_simuladas():
    """Simula exactamente los ejemplos del profesor sin internet."""
    simulados = [
        {"nombre": "Kosovo", "poblacion": 1700000, "superficie": None, "continente": "Europa"},
        {"nombre": "Brasil", "poblacion": None, "superficie": 8515767, "continente": "América"},
        {"nombre": "Chile", "poblacion": 19000000, "superficie": 0, "continente": "América"},
        {"nombre": "Argentina", "poblacion": 45376763, "superficie": 2780400, "continente": "América"},
        {"nombre": "Japón", "poblacion": 125800000, "superficie": 377975, "continente": "Asia"},
    ]
    existentes = [{"nombre": "Argentina", "poblacion": 45376763, "superficie": 2780400, "continente": "América"}]

    validos = []
    for d in simulados:
        es_valido, motivo = _validar_pais(d["nombre"], d["poblacion"], d["superficie"], d["continente"])
        if not es_valido:
            print(f"Descartado {d['nombre']}: {motivo}")
            continue
        validos.append(d)

    validos = _eliminar_duplicados(validos, existentes)
    print("Resultado simulado:", validos)
    return validos

if __name__ == "__main__":
    probar_validaciones_simuladas()
