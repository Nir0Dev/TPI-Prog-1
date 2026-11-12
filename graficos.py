import matplotlib.pyplot as plt
from estadisticas import resumen_estadistico,  estadisticas_pais
from matplotlib.ticker import FuncFormatter
from matplotlib.widgets import Button


def crear_boton_volver(figura, posicion):
    """Crear un botón que cierre la figura."""
    boton = Button(figura.add_axes(posicion), "Volver")

    def volver(evento):
        plt.close(figura)

    boton.on_clicked(volver)

    return boton

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

    adicionales = 0

    for campo, valor in datos.items():
        if campo in ("nombre", "poblacion", "superficie",
                     "continente", "densidad", "anio"):
            continue

        if valor is None or str(valor).strip() == "":
            continue

        etiqueta = campo.replace("_", " ").capitalize()
        texto += f"\n{etiqueta}: {valor}"
        adicionales += 1

    if adicionales == 0:
        texto += "\n\nNo hay datos adicionales guardados para este país."

    figura = plt.figure(figsize=(12, 10))

    eje = figura.add_axes([0.12, 0.65, 0.80, 0.24])
    eje_texto = figura.add_axes([0.06, 0.14, 0.90, 0.42])
    eje_texto.axis("off")
    eje_texto.text(0, 1, texto, va="top", fontsize=9)

    boton_poblacion = Button(
        figura.add_axes([0.06, 0.04, 0.20, 0.05]),
        "Población"
    )
    boton_superficie = Button(
        figura.add_axes([0.29, 0.04, 0.20, 0.05]),
        "Superficie"
    )
    boton_densidad = Button(
        figura.add_axes([0.52, 0.04, 0.20, 0.05]),
        "Densidad"
    )
    boton_volver = crear_boton_volver(
        figura, [0.75, 0.04, 0.20, 0.05]
    )

    def dibujar(campo, titulo, unidad):
        eje.clear()

        valor = datos[campo]
        barras = eje.bar([datos["nombre"]], [valor], width=0.3)

        eje.set_xlim(-1, 1)
        eje.set_ylim(0, max(valor * 1.20, 1))
        eje.set_title(titulo)
        eje.set_ylabel(unidad)
        eje.yaxis.set_major_formatter(
            FuncFormatter(formatear_numero)
        )
        eje.bar_label(
            barras,
            labels=[formatear_numero(valor)],
            padding=3
        )

        figura.canvas.draw_idle()

    def ver_poblacion(evento):
        dibujar("poblacion", "Población", "Habitantes")

    def ver_superficie(evento):
        dibujar("superficie", "Superficie", "km²")

    def ver_densidad(evento):
        dibujar("densidad", "Densidad de población", "Habitantes por km²")


    boton_poblacion.on_clicked(ver_poblacion)
    boton_superficie.on_clicked(ver_superficie)
    boton_densidad.on_clicked(ver_densidad)

    ver_densidad(None)
    plt.show(block=True)

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

    figura = plt.figure(figsize=(10, 8))
    plt.subplot(2,1,1)
    plt.bar(continentes, cantidades)
    plt.title("Cantidad de paises cargados por continente")
    plt.xlabel("Continente")
    plt.ylabel("Cantindad de paises")
    plt.gca().yaxis.set_major_formatter(FuncFormatter(formatear_numero))

    plt.subplot(2,1,2)
    plt.axis("off")
    plt.text(0, 0.9, texto, va="top", fontsize=11)

    plt.tight_layout(rect=(0, 0.12, 1, 1))
    boton_volver = crear_boton_volver(
        figura, [0.40, 0.03, 0.20, 0.05]
    )
    plt.show(block=True)

def mostrar_grafico_barras(etiquetas, valores, titulo, unidad, texto, promedio=None):
    """Mostrar hasta 15 países por página con botones de navegación."""
    if not etiquetas or len(etiquetas) != len(valores):
        print("No hay datos válidos para mostrar el gráfico.")
        return

    por_pagina = 15
    cantidad = len(etiquetas)
    paginas = (cantidad + por_pagina - 1) // por_pagina
    estado = {"pagina": 0, "descendente": True}

    figura = plt.figure(figsize=(12, 9))

    eje = figura.add_axes([0.36, 0.40, 0.60, 0.50])
    eje_texto = figura.add_axes([0.06, 0.15, 0.90, 0.18])
    eje_texto.axis("off")
    eje_texto.text(0, 1, texto, va="top", fontsize=10)

    boton_anterior = Button(
        figura.add_axes([0.035, 0.04, 0.17, 0.05]),
        "Anterior"
    )
    boton_siguiente = Button(
        figura.add_axes([0.22, 0.04, 0.17, 0.05]),
        "Siguiente"
    )
    boton_descendente = Button(
        figura.add_axes([0.405, 0.04, 0.17, 0.05]),
        "Mayor a menor"
    )
    boton_ascendente = Button(
        figura.add_axes([0.59, 0.04, 0.17, 0.05]),
        "Menor a mayor"
    )
    boton_volver = Button(
        figura.add_axes([0.775, 0.04, 0.17, 0.05]),
        "Volver"
    )

    limite = max(valores)

    if promedio is not None:
        limite = max(limite, promedio)

    if limite <= 0:
        limite = 1

    def dibujar_pagina():
        inicio = estado["pagina"] * por_pagina
        fin = min(inicio + por_pagina, cantidad)

        indices = sorted(
            range(cantidad),
            key=lambda indice: valores[indice],
            reverse=estado["descendente"]
        )

        nombres_pagina = []
        valores_pagina = []

        for indice in indices[inicio:fin]:
            nombres_pagina.append(etiquetas[indice])
            valores_pagina.append(valores[indice])

        posiciones = range(len(nombres_pagina))

        eje.clear()

        barras = eje.barh(posiciones, valores_pagina)
        eje.set_yticks(posiciones, labels=nombres_pagina)
        eje.tick_params(axis="y", labelsize=8)

        # Mantener el primer país arriba y espacio para 15 filas.
        eje.set_ylim(por_pagina - 0.5, -0.5)
        eje.set_xlim(0, limite * 1.20)

        eje.set_xlabel(unidad)
        eje.xaxis.set_major_formatter(
            FuncFormatter(formatear_numero)
        )

        etiquetas_valores = []

        for valor in valores_pagina:
            etiquetas_valores.append(formatear_numero(valor))

        eje.bar_label(
            barras,
            labels=etiquetas_valores,
            padding=3,
            fontsize=8
        )

        if promedio is not None:
            eje.axvline(
                x=promedio,
                color="red",
                linestyle="--",
                label=f"Promedio general: {formatear_numero(promedio)}"
            )
            eje.legend(loc="lower right", fontsize=9)

        eje.set_title(
            f"{titulo}\n"
            f"Países {inicio + 1}–{fin} de {cantidad} "
            f"| Página {estado['pagina'] + 1} de {paginas}",
            fontsize=11
        )

        boton_anterior.set_active(estado["pagina"] > 0)
        boton_siguiente.set_active(estado["pagina"] < paginas - 1)

        figura.canvas.draw_idle()

    def pagina_anterior(evento):
        if estado["pagina"] > 0:
            estado["pagina"] -= 1
            dibujar_pagina()

    def pagina_siguiente(evento):
        if estado["pagina"] < paginas - 1:
            estado["pagina"] += 1
            dibujar_pagina()

    def volver(evento):
        plt.close(figura)

    def ordenar_descendente(evento):
        estado["descendente"] = True
        estado["pagina"] = 0
        dibujar_pagina()

    def ordenar_ascendente(evento):
        estado["descendente"] = False
        estado["pagina"] = 0
        dibujar_pagina()

    boton_descendente.on_clicked(ordenar_descendente)
    boton_ascendente.on_clicked(ordenar_ascendente)

    boton_anterior.on_clicked(pagina_anterior)
    boton_siguiente.on_clicked(pagina_siguiente)
    boton_volver.on_clicked(volver)

    dibujar_pagina()
    plt.show(block=True)

def mostrar_promedio_poblacion(paises):
    """Comparar las poblaciones con el promedio del dataset."""
    resumen = resumen_estadistico(paises)

    if resumen is None:
        return

    nombres, poblaciones = preparar_datos_grafico(paises, "poblacion")

    promedio = resumen["promedio_poblacion"]

    mayor = resumen["mayor_poblacion"]
    menor = resumen["menor_poblacion"]

    texto = (
        f"Cantidad de países analizados: {len(paises)}\n"
        f"Promedio de población: {formatear_numero(promedio)} habitantes\n"
        f"Mayor población: {mayor['nombre']} "
        f"({formatear_numero(mayor['poblacion'])} habitantes)\n"
        f"Menor población: {menor['nombre']} "
        f"({formatear_numero(menor['poblacion'])} habitantes)\n\n"
        "La línea roja indica el promedio general."
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