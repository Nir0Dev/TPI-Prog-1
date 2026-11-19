"""Integrante 1 — Lectura, validación y guardado del CSV (único módulo que lo escribe)."""
import csv
import io
from pathlib import Path

RUTA_CSV = Path(__file__).resolve().parent / "data" / "paises.csv"
COLUMNAS_OBLIGATORIAS = ("nombre", "poblacion", "superficie", "continente")
CAMPOS_TEXTO = ("nombre", "continente")
CAMPOS_NUMERICOS = ("poblacion", "superficie")

# Topes: más que la población del mundo y más que la tierra firme del planeta
POBLACION_MAXIMA = 10_000_000_000
SUPERFICIE_MAXIMA = 150_000_000


# --- Funciones auxiliares ---
def limpiar_texto(valor):
    """Sacar espacios de más."""
    if valor is None:
        return ""
    return " ".join(str(valor).split())


def convertir_entero(valor):
    """Convertir a int; devuelve None si no es un entero."""
    if isinstance(valor, bool):
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


def formatear_numero(numero):
    """10000000000 -> 10.000.000.000"""
    return f"{numero:,}".replace(",", ".")


def resumir(texto, largo=30):
    """Acortar textos largos en los mensajes."""
    if len(texto) <= largo:
        return texto
    return texto[:largo] + "…"


def indice_de_pais(paises, nombre):
    """Posición del país en la lista (sin importar mayúsculas), o -1 si no está."""
    buscado = limpiar_texto(nombre).casefold()
    for indice, pais in enumerate(paises):
        if limpiar_texto(pais.get("nombre")).casefold() == buscado:
            return indice
    return -1


def leer_texto_csv(ruta):
    """Leer el archivo en UTF-8 o, si falla, en cp1252 (Excel)."""
    try:
        return ruta.read_text(encoding="utf-8-sig")
    except UnicodeDecodeError:
        return ruta.read_text(encoding="cp1252", errors="replace")


def detectar_separador(texto):
    """Usar ';' si el encabezado lo tiene (Excel en español) o ',' si no."""
    primera_linea = texto.split("\n", 1)[0]
    if primera_linea.count(";") > primera_linea.count(","):
        return ";"
    return ","


# --- Funciones principales ---
def crear_plantilla(ruta=RUTA_CSV):
    """Crear el CSV con el encabezado si no existe o está vacío."""
    ruta = Path(ruta)
    if ruta.exists() and ruta.stat().st_size > 0:
        return False
    ruta.parent.mkdir(parents=True, exist_ok=True)
    with open(ruta, "w", encoding="utf-8", newline="") as archivo:
        csv.writer(archivo).writerow(COLUMNAS_OBLIGATORIAS)
    return True


def validar_pais(pais):
    """Devolver (copia limpia del país, lista de errores). Sin errores = válido."""
    limpio = dict(pais)  # copia para no tocar el original
    errores = []

    for campo in CAMPOS_TEXTO:
        texto = limpiar_texto(pais.get(campo))
        if texto == "":
            errores.append(f"El campo '{campo}' no puede estar vacío.")
        elif not any(caracter.isalpha() for caracter in texto):
            errores.append(f"El campo '{campo}' debe contener letras (se recibió '{resumir(texto)}').")
        limpio[campo] = texto

    for campo in CAMPOS_NUMERICOS:
        texto = limpiar_texto(pais.get(campo))
        numero = convertir_entero(pais.get(campo))
        if texto == "":
            errores.append(f"El campo '{campo}' no puede estar vacío.")
        elif numero is None:
            errores.append(f"El campo '{campo}' debe ser un número entero (se recibió '{resumir(texto)}').")
        elif campo == "poblacion" and numero < 0:
            errores.append("La población no puede ser negativa.")
        elif campo == "poblacion" and numero > POBLACION_MAXIMA:
            errores.append(f"La población no puede superar {formatear_numero(POBLACION_MAXIMA)} "
                           "habitantes (sería más que la población del mundo).")
        elif campo == "superficie" and numero <= 0:
            errores.append("La superficie debe ser mayor a 0.")
        elif campo == "superficie" and numero > SUPERFICIE_MAXIMA:
            errores.append(f"La superficie no puede superar {formatear_numero(SUPERFICIE_MAXIMA)} km² "
                           "(sería más que toda la tierra firme del planeta).")
        else:
            limpio[campo] = numero

    return limpio, errores


def cargar_paises(ruta=RUTA_CSV):
    """Leer el CSV y devolver la lista de países válidos; avisa las filas descartadas."""
    ruta = Path(ruta)
    crear_plantilla(ruta)

    texto = leer_texto_csv(ruta)
    lector = csv.DictReader(io.StringIO(texto), delimiter=detectar_separador(texto))
    if lector.fieldnames is None:  # archivo vacío
        return []

    lector.fieldnames = [limpiar_texto(columna).lower() for columna in lector.fieldnames]
    faltantes = [columna for columna in COLUMNAS_OBLIGATORIAS if columna not in lector.fieldnames]
    if faltantes:
        raise ValueError(
            f"El archivo {ruta.name} no tiene las columnas obligatorias: {', '.join(faltantes)}. "
            f"El encabezado debe ser: {','.join(COLUMNAS_OBLIGATORIAS)}"
        )

    paises = []
    for fila in lector:
        motivo = ""
        pais, errores = validar_pais(fila)
        if None in fila:  # la fila tiene valores de más
            motivo = "tiene más valores que columnas."
        elif errores:
            motivo = " ".join(errores)
        elif indice_de_pais(paises, pais["nombre"]) != -1:
            motivo = f"'{pais['nombre']}' está repetido."

        if motivo:
            print(f"Aviso: línea {lector.line_num} descartada: {motivo}")
        else:
            paises.append(pais)

    return paises


def agregar_pais(paises, pais):
    """Validar y agregar un país nuevo. Devuelve (exito, mensaje)."""
    pais_limpio, errores = validar_pais(pais)
    if errores:
        return False, " ".join(errores)
    indice = indice_de_pais(paises, pais_limpio["nombre"])
    if indice != -1:
        return False, f"Ya existe un país con el nombre '{paises[indice]['nombre']}'."
    paises.append(pais_limpio)
    return True, f"País '{pais_limpio['nombre']}' agregado correctamente."


def actualizar_pais(paises, nombre, cambios):
    """Cambiar población y/o superficie de un país. Devuelve (exito, mensaje)."""
    indice = indice_de_pais(paises, nombre)
    if indice == -1:
        return False, f"No se encontró el país '{limpiar_texto(nombre)}'."
    if not cambios:
        return False, "Ingresá al menos un cambio de población o superficie."
    if any(campo not in CAMPOS_NUMERICOS for campo in cambios):
        return False, "Solo se pueden actualizar población y superficie."

    actualizado = paises[indice].copy()  # se valida la copia antes de reemplazar
    actualizado.update(cambios)
    pais_limpio, errores = validar_pais(actualizado)
    if errores:
        return False, " ".join(errores)
    paises[indice] = pais_limpio
    return True, f"País '{pais_limpio['nombre']}' actualizado correctamente."


def guardar_paises(paises, ruta=RUTA_CSV):
    """Guardar la lista en el CSV (con las columnas extra). Devuelve True si pudo."""
    ruta = Path(ruta)
    columnas = list(COLUMNAS_OBLIGATORIAS)
    for pais in paises:
        for clave in pais:
            if isinstance(clave, str) and clave not in columnas:
                columnas.append(clave)

    temporal = ruta.with_name(ruta.name + ".tmp")  # si falla, el original no se rompe
    try:
        ruta.parent.mkdir(parents=True, exist_ok=True)
        with open(temporal, "w", encoding="utf-8", newline="") as archivo:
            escritor = csv.DictWriter(archivo, fieldnames=columnas, restval="", extrasaction="ignore")
            escritor.writeheader()
            escritor.writerows(paises)
        temporal.replace(ruta)
    except OSError as error:
        if temporal.is_file():
            temporal.unlink()
        print(f"Error: no se pudo guardar {ruta.name}: {error}")
        return False
    return True
