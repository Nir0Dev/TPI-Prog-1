"""Menú principal compartido. Cada integrante integra su opción mediante PR."""
from gestion_paises import cargar_paises, agregar_pais, actualizar_pais, guardar_paises
from consultas import buscar_pais, filtrar_continente, filtrar_rango
from operaciones import eliminar_pais, limpiar_paises, ordenar_paises
from estadisticas import resumen_estadistico, calcular_densidad
from graficos import mostrar_estadisticas_pais, mostrar_estadisticas_generales
from api_paises import consultar_indicador, transformar_indicadores, preparar_registros_csv

OPCIONES = {
    "1": "Agregar país",
    "2": "Modificar país",
    "3": "Eliminar país",
    "4": "Limpiar todos los registros",
    "5": "Buscar país",
    "6": "Filtrar países",
    "7": "Ordenar países",
    "8": "Mostrar estadísticas (gráfico y datos)",
    "9": "Consultar API Banco Mundial / incorporar datos",
    "0": "Salir",
}

def mostrar_menu():
    print("\n=== GESTIÓN DE PAÍSES ===")
    for clave, titulo in OPCIONES.items():
        print(f"{clave}. {titulo}")

def ejecutar_opcion(opcion, paises):
    """TODO (compartido): conectar entradas del usuario con módulos.

    Las opciones 1-2 corresponden a integrante 1, 3-7 a integrante 2
    (7 ordenamientos), 8 a integrante 3 y 9 a integrante 4.
    Cada responsable incorpora su caso cuando su módulo esté listo.
    """
    raise NotImplementedError(f"Opción {opcion} pendiente de integración")

def main():
    print("Plantilla del TPI: las funciones todavía están por implementar.")
    paises = []  # TODO I1: cargar desde data/paises.csv automáticamente
    while True:
        mostrar_menu()
        opcion = input("Elegí una opción: ").strip()
        if opcion == "0":
            print("Hasta luego.")
            break
        if opcion not in OPCIONES:
            print("Opción inválida.")
            continue
        try:
            ejecutar_opcion(opcion, paises)
        except NotImplementedError as error:
            print(f"[PENDIENTE] {error}")

if __name__ == "__main__":
    main()
