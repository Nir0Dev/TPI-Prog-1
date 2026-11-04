"""Integrante 1 — CSV, persistencia y validaciones.

Este módulo es el ÚNICO del proyecto que lee y escribe data/paises.csv.
Los países se manejan como una lista de diccionarios, por ejemplo:

    {"nombre": "Japón", "poblacion": 125124989, "superficie": 377969, "continente": "Asia"}

Además de las cuatro columnas obligatorias, un país puede traer columnas extra
(por ejemplo, las que agregue la API del integrante 4). Esas columnas se
conservan al cargar, actualizar y guardar.
"""
import csv
import io
from pathlib import Path

RUTA_CSV = Path(__file__).resolve().parent / "data" / "paises.csv"
COLUMNAS_OBLIGATORIAS = ("nombre", "poblacion", "superficie", "continente")
CAMPOS_TEXTO = ("nombre", "continente")
CAMPOS_NUMERICOS = ("poblacion", "superficie")


# ---------------------------------------------------------------------------
# Funciones auxiliares
# ---------------------------------------------------------------------------
def limpiar_texto(valor):
    """Pasar a texto, sacar espacios de los extremos y dejar uno solo entre palabras."""
    if valor is None:
        return ""
    return " ".join(str(valor).split())


def convertir_entero(valor):
    """Convertir un valor a int. Devuelve None si no representa un número entero.

    Acepta "45376763", 45376763 y también "2780400.0" o 2780400.0 (la API del
    Banco Mundial a veces entrega números con decimales en cero).
    """
    if isinstance(valor, bool):  # True/False no son datos válidos
        return None
    texto = limpiar_texto(valor)
    try:
        return int(texto)
    except ValueError:
        pass
    try:
        numero = float(texto)
    except ValueError:
        return None
    if numero.is_integer():
        return int(numero)
    return None


def indice_de_pais(paises, nombre):
    """Devolver la posición del país en la lista, o -1 si no está.

    Compara sin importar mayúsculas ni espacios de más: "  ARGENTINA " encuentra
    a "Argentina".
    """
    buscado = limpiar_texto(nombre).casefold()
    for indice, pais in enumerate(paises):
        if limpiar_texto(pais.get("nombre")).casefold() == buscado:
            return indice
    return -1


def leer_texto_csv(ruta):
    """Leer el archivo completo como texto.

    Primero prueba UTF-8 (con o sin BOM, como lo guarda Excel en "CSV UTF-8").
    Si falla, usa cp1252, que es como Excel en Windows guarda el "CSV" común.
    """
    try:
        return ruta.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return ruta.read_text(encoding="cp1252", errors="replace")


def detectar_separador(texto):
    """Excel en español separa con ';'. Si el encabezado tiene más ';' que ',', usar ';'."""
    primera_linea = texto.split("\n", 1)[0]
    if primera_linea.count(";") > primera_linea.count(","):
        return ";"
    return ","


# ---------------------------------------------------------------------------
# Funciones principales
# ---------------------------------------------------------------------------
def crear_plantilla(ruta=RUTA_CSV):
    """Crear carpeta y CSV con encabezados si falta; NO sobrescribir datos existentes.

    Devuelve True si creó la plantilla y False si el archivo ya tenía contenido.
    """
    ruta = Path(ruta)
    if ruta.exists() and ruta.stat().st_size > 0:
        return False
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        csv.writer(archivo).writerow(COLUMNAS_OBLIGATORIAS)
    return True


def validar_pais(pais):
    """Revisar un país y devolver una versión "limpia".

    Reglas: nombre y continente no vacíos y con letras; población entera >= 0;
    superficie entera > 0.

    Devuelve una tupla (pais_limpio, errores):
      - pais_limpio: copia del diccionario con textos limpios y números como int
        (las columnas extra se conservan).
      - errores: lista de mensajes. Si está vacía, el país es válido.
    No modifica el diccionario recibido.
    """
    limpio = dict(pais)  # copia: así no se toca el original
    errores = []

    for campo in CAMPOS_TEXTO:
        texto = limpiar_texto(pais.get(campo))
        if texto == "":
            errores.append(f"El campo '{campo}' no puede estar vacío.")
        elif not any(caracter.isalpha() for caracter in texto):
            errores.append(f"El campo '{campo}' debe contener letras (se recibió '{texto}').")
        limpio[campo] = texto

    for campo in CAMPOS_NUMERICOS:
        texto = limpiar_texto(pais.get(campo))
        numero = convertir_entero(pais.get(campo))
        if texto == "":
            errores.append(f"El campo '{campo}' no puede estar vacío.")
        elif numero is None:
            errores.append(f"El campo '{campo}' debe ser un número entero (se recibió '{texto}').")
        elif campo == "poblacion" and numero < 0:
            errores.append("La población no puede ser negativa.")
        elif campo == "superficie" and numero <= 0:
            errores.append("La superficie debe ser mayor a 0.")
        else:
            limpio[campo] = numero

    return limpio, errores


def cargar_paises(ruta=RUTA_CSV):
    """Leer el CSV y devolver una lista de diccionarios con los países válidos.

    - Si el archivo no existe, crea la plantilla con encabezados y devuelve [].
    - Si faltan columnas obligatorias, lanza ValueError (main avisa y termina,
      para no guardar encima de un archivo que no entendemos).
    - Las filas con errores o repetidas se descartan, avisando en pantalla el
      número de línea y el motivo.
    """
    ruta = Path(ruta)
    crear_plantilla(ruta)

    texto = leer_texto_csv(ruta)
    lector = csv.DictReader(io.StringIO(texto), delimiter=detectar_separador(texto))
    if lector.fieldnames is None:  # archivo vacío, sin encabezado
        return []

    # " Nombre" o "NOMBRE" en el encabezado cuentan como "nombre"
    lector.fieldnames = [limpiar_texto(columna).lower() for columna in lector.fieldnames]
    faltantes = [columna for columna in COLUMNAS_OBLIGATORIAS if columna not in lector.fieldnames]
    if faltantes:
        raise ValueError(
            f"El archivo {ruta.name} no tiene las columnas obligatorias: {', '.join(faltantes)}. "
            f"El encabezado debe ser: {','.join(COLUMNAS_OBLIGATORIAS)}"
        )

    paises = []
    for fila in lector:
        linea = lector.line_num
        if None in fila:  # DictReader guarda en la clave None los valores sobrantes
            print(f"Aviso: línea {linea} descartada: tiene más valores que columnas.")
            continue
        pais, errores = validar_pais(fila)
        if errores:
            print(f"Aviso: línea {linea} descartada: {' '.join(errores)}")
            continue
        if indice_de_pais(paises, pais["nombre"]) != -1:
            print(f"Aviso: línea {linea} descartada: '{pais['nombre']}' está repetido.")
            continue
        paises.append(pais)
    return paises


def agregar_pais(paises, pais):
    """Agregar un país nuevo a la lista (NO guarda el CSV; eso lo hace main).

    Recibe un diccionario con nombre, poblacion, superficie y continente
    (los números pueden venir como texto, tal cual los escribe el usuario).
    Devuelve una tupla (exito, mensaje):
      - (False, "<errores>") si validar_pais encuentra errores.
      - (False, "<aviso>") si ya existe un país con ese nombre.
      - (True, "<confirmación>") si lo agregó a la lista.
    """
    raise NotImplementedError  # TODO Cris


def actualizar_pais(paises, nombre, cambios):
    """Actualizar población y/o superficie de un país existente (NO guarda el CSV).

    cambios es un diccionario con "poblacion", "superficie" o ambas, por ejemplo
    {"poblacion": "46000000"}. Las columnas extra del país se conservan.
    Devuelve una tupla (exito, mensaje):
      - (False, ...) si el país no existe, si cambios está vacío o trae otros
        campos, o si los valores nuevos no pasan validar_pais. En esos casos el
        país queda como estaba.
      - (True, ...) si lo actualizó.
    """
    raise NotImplementedError  # TODO Cris


def guardar_paises(paises, ruta=RUTA_CSV):
    """Guardar la lista en el CSV; mantener columnas mínimas y extras de la API.

    Escribe primero en un archivo temporal y después lo renombra: si algo falla
    a mitad de camino, el CSV original queda intacto.
    Devuelve True si guardó y False si no pudo (por ejemplo, porque el archivo
    está abierto en Excel), mostrando el motivo.
    """
    ruta = Path(ruta)
    columnas = list(COLUMNAS_OBLIGATORIAS)
    for pais in paises:
        for clave in pais:
            if isinstance(clave, str) and clave not in columnas:
                columnas.append(clave)

    temporal = ruta.with_name(ruta.name + ".tmp")
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(temporal, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas, restval="", extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(paises)
        temporal.replace(ruta)
    except OSError as error:
        if temporal.is_file():  # borrar el temporal a medio escribir, si quedó
            temporal.unlink()
        print(f"Error: no se pudo guardar {ruta.name}: {error}")
        return False
    return True
