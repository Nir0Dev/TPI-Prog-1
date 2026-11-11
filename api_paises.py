# api_paises.py - Integrante 4: API Banco Mundial
# Responsabilidad: descargar, validar y entregar registros.
# NO escribe el CSV, solo devuelve lista de diccionarios validados.
import requests

URL_POBLACION = "https://api.worldbank.org/v2/country/all/indicator/SP.POP.TOTL"
URL_SUPERFICIE = "https://api.worldbank.org/v2/country/all/indicator/AG.SRF.TOTL.K2"
ANIO = "2023"

def _descargar_indicador(url, nombre_indicador):
    """Descarga un indicador del Banco Mundial. Devuelve lista de registros JSON."""
    try:
        params = {"format": "json", "per_page": 20000, "date": ANIO}
        respuesta = requests.get(url, params=params, timeout=20)
        respuesta.raise_for_status()
        datos = respuesta.json()
        # La API devuelve [metadata, [registros]] . Si no hay datos, devuelve []
        if len(datos) < 2 or datos[1] is None:
            print(f"Sin datos para {nombre_indicador}")
            return []
        return datos[1]
    except requests.exceptions.RequestException as e:
        print(f"Error de conexión con la API ({nombre_indicador}): {e}")
        return []

def _extraer_valor(registro):
    """Devuelve el valor numérico o None si falta / no es numérico."""
    valor = registro.get("value")
    if valor is None:
        return None
    try:
        return int(float(valor))
    except (ValueError, TypeError):
        return None

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

def _eliminar_duplicados(paises_nuevos, paises_existentes):
    """Evita duplicados por nombre (sin mayúsculas). Devuelve lista sin repetidos."""
    nombres_existentes = set()
    for p in paises_existentes:
        nombres_existentes.add(p["nombre"].lower())

    sin_duplicados = []
    for p in paises_nuevos:
        nombre_min = p["nombre"].lower()
        if nombre_min in nombres_existentes:
            print(f"Duplicado ignorado: {p['nombre']} - registro repetido")
            continue
        nombres_existentes.add(nombre_min)
        sin_duplicados.append(p)
    return sin_duplicados

def obtener_paises_api(paises_existentes):
    """Función principal de tu parte. Descarga, une, valida y devuelve registros."""
    print(f"Descargando datos del Banco Mundial ({ANIO})...")

    datos_pob = _descargar_indicador(URL_POBLACION, "Población SP.POP.TOTL")
    datos_sup = _descargar_indicador(URL_SUPERFICIE, "Superficie AG.SRF.TOTL.K2")

    # 1. Armar diccionario por código de país: {codigo: {nombre, poblacion, superficie, continente}}
    paises_por_codigo = {}

    for r in datos_pob:
        codigo = r["country"]["id"]
        paises_por_codigo[codigo] = {
            "nombre": r["country"]["value"],
            "poblacion": _extraer_valor(r),
            "superficie": None,
            "continente": r["country"].get("region", {}).get("value", "Sin región")
        }

    for r in datos_sup:
        codigo = r["country"]["id"]
        if codigo in paises_por_codigo:
            paises_por_codigo[codigo]["superficie"] = _extraer_valor(r)# se saca poblacion y supef _extraer_valor

    # 2. Validar cada uno
    validos = []
    for codigo in paises_por_codigo:
        d = paises_por_codigo[codigo]
        # Caso ejemplo del profesor: Kosovo falta superficie -> se descarta
        # Brasil población no numérica -> _extraer_valor devuelve None -> se descarta
        # Chile superficie <= 0 -> se descarta
        es_valido, motivo = _validar_pais(d["nombre"], d["poblacion"], d["superficie"], d["continente"])
        if not es_valido:
            print(f"Descartado {d['nombre']}: {motivo}")
            continue
        validos.append(d)

    # 3. Evitar duplicados contra lo que ya hay en el CSV
    # Caso ejemplo: ARGENTINA repetido -> se ignora
    validos = _eliminar_duplicados(validos, paises_existentes)

    print(f"Listo: {len(validos)} países validados desde la API.")
    return validos

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

# --- Adaptadores para que main.py pueda importar ---

def consultar_indicador(codigo_indicador="SP.POP.TOTL", pais="all"):
    """Consulta un indicador en la API del Banco Mundial y devuelve la lista cruda."""
    import requests
    url = f"https://api.worldbank.org/v2/country/{pais}/indicator/{codigo_indicador}"
    resp = requests.get(url, params={"format": "json", "per_page": 20000}, timeout=30)
    resp.raise_for_status()
    datos = resp.json()
    if isinstance(datos, list) and len(datos) > 1:
        return datos[1]
    return datos if isinstance(datos, list) else []

def transformar_indicadores(datos):
    """Pasa los datos crudos de la API a lista de dicts limpios."""
    registros = []
    if isinstance(datos, list) and len(datos) == 2 and isinstance(datos[1], list):
        datos = datos[1]
    for item in datos or []:
        try:
            registros.append({
                "pais": item.get("country", {}).get("value") if isinstance(item.get("country"), dict) else item.get("pais"),
                "codigo_pais": item.get("countryiso3code") or item.get("codigo_pais"),
                "anio": int(item.get("date")) if str(item.get("date", "")).isdigit() else item.get("anio"),
                "indicador": item.get("indicator", {}).get("value") if isinstance(item.get("indicator"), dict) else item.get("indicador"),
                "valor": item.get("value") if item.get("value") is not None else item.get("valor"),
            })
        except Exception:
            continue
    return registros

def preparar_registros_csv(registros):
    """Deja solo registros validos y listos para guardar en CSV."""
    listos = []
    for r in registros or []:
        if not r.get("pais") or r.get("valor") is None or r.get("anio") is None:
            continue
        listos.append({
            "pais": str(r["pais"]),
            "codigo_pais": str(r.get("codigo_pais", "")),
            "anio": int(r["anio"]),
            "indicador": str(r.get("indicador", "")),
            "valor": float(r["valor"]),
        })
    return listos

def validar_registros_api(registros):
    """Alias para compatibilidad con el esqueleto original."""
    return preparar_registros_csv(registros)

if __name__ == "__main__":
    probar_validaciones_simuladas()