import matplotlib.pyplot as plt
from estadisticas import resumen_estadistico,  estadisticas_pais
from matplotlib.ticker import FuncFormatter

def mostrar_estadisticas_pais(pais, historia=None):
    """Una figura: gráfico arriba y datos del país debajo, usando plt.show().

    Si existe historia de API, graficar evolución poblacional.
    Si no, elegir una visualización comparable y explicar magnitudes/unidades.
    """
    datos = estadisticas_pais(pais)

    if datos is None:
        return

    texto = (
        f"País: {datos['nombre']}\n"
        f"Población: {formatear_numero(datos['poblacion'])} habitantes\n"
        f"Superficie: {formatear_numero(datos['superficie'])} km²\n"
        f"Continente: {datos['continente']}\n"
        f"Densidad: {formatear_numero(datos['densidad'])} habitantes por km²"
    )

    for campo, valor in datos.items():
        if campo not in ("nombre", "poblacion", "superficie", "continente", "densidad"):
            texto += f"\n{campo}: {valor}"

    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.bar([datos["nombre"]], [datos["densidad"]], width=0.3)
    plt.xlim(-1, 1)
    plt.title("Densidad de población")
    plt.xlabel("País")
    plt.ylabel("Habitantes por km²")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_numero))

    plt.subplot(2, 1, 2)
    plt.axis("off")
    plt.text(0, 0.9, texto, va="top", fontsize=11)

    plt.tight_layout()
    plt.show()

def mostrar_estadisticas_generales(paises):
    """Una figura de comparación + valores de estadísticas debajo."""
    resumen = resumen_estadistico(paises)

    if resumen is None:
        return
    
    continentes = []
    cantidades = []

    for continente, cantidad in resumen["paises_por_continente"].items():
        continentes.append(continente)
        cantidades.append(cantidad)

    mayor = resumen["mayor_poblacion"]
    menor = resumen["menor_poblacion"]

    texto = (
        f"Mayor población: {mayor['nombre']} "
        f"({formatear_numero(mayor['poblacion'])} habitantes)\n"
        f"Menor población: {menor['nombre']} "
        f"({formatear_numero(menor['poblacion'])} habitantes)\n"
        f"Promedio de población: "
        f"{formatear_numero(resumen['promedio_poblacion'])} habitantes\n"
        f"Promedio de superficie: "
        f"{formatear_numero(resumen['promedio_superficie'])} km²"
    )

    plt.figure(figsize=(10,8))
    plt.subplot(2,1,1)
    plt.bar(continentes, cantidades)
    plt.title("Cantidad de paises cargados por continente")
    plt.xlabel("Continente")
    plt.ylabel("Cantindad de paises")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_numero))

    plt.subplot(2,1,2)
    plt.axis("off")
    plt.text(0, 0.9, texto, va="top", fontsize=11)

    plt.tight_layout()
    plt.show()

def mostrar_grafico_barras(etiquetas, valores, titulo, unidad, texto, promedio=None):
    """Mostrar barras arriba y los resultados debajo."""
    plt.figure(figsize=(10, 8))

    plt.subplot(2, 1, 1)
    plt.bar(etiquetas, valores)
    plt.title(titulo)
    plt.ylabel(unidad)

    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_numero))

    plt.xticks(rotation=90, fontsize=8)

    if promedio is not None:
        plt.axhline(
            y=promedio,
            color="red",
            linestyle="--",
            label=f"Promedio: {formatear_numero(promedio)}"
        )
        plt.legend()

    plt.subplot(2, 1, 2)
    plt.axis("off")
    plt.text(0, 0.9, texto, va="top", fontsize=11)

    plt.tight_layout()
    plt.show()

def mostrar_extremos_poblacion(paises):
    """Mostrar todos los países ordenados por población."""
    resumen = resumen_estadistico(paises)

    if resumen is None:
        return

    nombres, poblaciones = preparar_datos_grafico(paises, "poblacion")

    mayor = resumen["mayor_poblacion"]
    menor = resumen["menor_poblacion"]

    texto = (
        f"Mayor población: {mayor['nombre']} "
        f"({formatear_numero(mayor['poblacion'])} habitantes)\n"
        f"Menor población: {menor['nombre']} "
        f"({formatear_numero(menor['poblacion'])} habitantes)\n\n"
        "Los países se muestran de mayor a menor población."
    )

    mostrar_grafico_barras(
        nombres,
        poblaciones,
        "Países ordenados por población: mayor a menor",
        "Habitantes",
        texto
    )

def mostrar_promedio_poblacion(paises):
    """Comparar las poblaciones con el promedio del dataset."""
    resumen = resumen_estadistico(paises)

    if resumen is None:
        return

    nombres, poblaciones = preparar_datos_grafico(paises, "poblacion")

    promedio = resumen["promedio_poblacion"]

    texto = (
        f"Cantidad de países analizados: {len(paises)}\n"
        f"Promedio de población: {formatear_numero(promedio)} habitantes\n\n"
        "Cada barra representa la población de un país.\n"
        "La línea roja indica el promedio de los países cargados."
    )

    mostrar_grafico_barras(
        nombres,
        poblaciones,
        "Población por país y promedio",
        "Habitantes",
        texto,
        promedio
    )

def formatear_numero(valor, posicion=None):
    """Mostrar millones con M y miles con m."""
    if abs(valor) >= 1000000:
        numero = valor / 1000000
        sufijo = " M"
    elif abs(valor) >= 1000:
        numero = valor / 1000
        sufijo = " m"
    else:
        numero = valor
        sufijo = ""

    texto = f"{numero:,.2f}"
    texto = texto.replace(",", "_")
    texto = texto.replace(".", ",")
    texto = texto.replace("_", ".")
    texto = texto.rstrip("0").rstrip(",")

    return texto + sufijo

def mostrar_promedio_superficie(paises):
    """Comparar las superficies con el promedio del dataset."""
    resumen = resumen_estadistico(paises)

    if resumen is None:
        return

    nombres, superficies = preparar_datos_grafico(paises, "superficie")

    promedio = resumen["promedio_superficie"]

    texto = (
        f"Cantidad de países analizados: {len(paises)}\n"
        f"Promedio de superficie: {formatear_numero(promedio)} km²\n\n"
        "Cada barra representa la superficie de un país.\n"
        "La línea roja indica el promedio de los países cargados.\n"
    
    )

    mostrar_grafico_barras(
        nombres,
        superficies,
        "Superficie por país y promedio",
        "Superficie en km²",
        texto,
        promedio
    )

def preparar_datos_grafico(paises, campo):
    """Preparar nombres y valores de mayor a menor, sin cambiar la lista original."""
    ordenados = sorted(
        paises,
        key=lambda pais: pais[campo],
        reverse=True
    )

    nombres = []
    valores = []

    for pais in ordenados:
        nombres.append(pais["nombre"])
        valores.append(pais[campo])

    return nombres, valores