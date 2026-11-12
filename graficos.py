import matplotlib.pyplot as plt
from estadisticas import resumen_estadistico,  estadisticas_pais

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
        f"Población: {datos['poblacion']} habitantes\n"
        f"Superficie: {datos['superficie']} km²\n"
        f"Continente: {datos['continente']}\n"
        f"Densidad: {datos['densidad']:.2f} habitantes por km²"
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
        f"Mayor población: {mayor['nombre']} ({mayor['poblacion']} habitantes)\n"
        f"Menor población: {menor['nombre']} ({menor['poblacion']} habitantes)\n"
        f"Promedio de población: {resumen['promedio_poblacion']:.2f} habitantes\n"
        f"Promedio de superficie: {resumen['promedio_superficie']:.2f} km²"
    )

    plt.figure(figsize=(10,8))
    plt.subplot(2,1,1)
    plt.bar(continentes, cantidades)
    plt.title("Cantidad de paises cargados por continente")
    plt.xlabel("Continente")
    plt.ylabel("Cantindad de paises")

    plt.subplot(2,1,2)
    plt.axis("off")
    plt.text(0, 0.9, texto, va="top", fontsize=11)

    plt.tight_layout()
    plt.show()