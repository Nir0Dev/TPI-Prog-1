"""Menú principal compartido. Cada integrante integra su opción mediante PR."""
from gestion_paises import cargar_paises, agregar_pais, actualizar_pais, guardar_paises, indice_de_pais
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
    """Conectar entradas del usuario con módulos.

    Las opciones 1-2 corresponden a integrante 1, 3-7 a integrante 2
    (7 ordenamientos), 8 a integrante 3 y 9 a integrante 4.
    Cada responsable incorpora su caso cuando su módulo esté listo.
    """
    # Aplicar los cambios en una copia y confirmarlos cuando se guarden en CSV.
    paises_actualizados = list(paises)
    if opcion == "1":
        pais = {
            "nombre": input("Nombre: "),
            "poblacion": input("Población: "),
            "superficie": input("Superficie en km²: "),
            "continente": input("Continente: "),
        }
        exito, mensaje = agregar_pais(paises_actualizados, pais)
    elif opcion == "2":
        nombre = input("Nombre del país a modificar: ")
        # Buscar el país antes de pedir datos: si no existe, no tiene sentido seguir
        indice = indice_de_pais(paises, nombre)
        if indice == -1:
            print(f"No se encontró el país '{nombre.strip()}'.")
            return
        actual = paises[indice]
        print(f"Datos actuales de {actual['nombre']}: población {actual['poblacion']}, "
              f"superficie {actual['superficie']} km².")
        cambios = {}
        poblacion = input("Nueva población (Enter para conservar la actual): ").strip()
        superficie = input("Nueva superficie en km² (Enter para conservar la actual): ").strip()
        if poblacion:
            cambios["poblacion"] = poblacion
        if superficie:
            cambios["superficie"] = superficie
        exito, mensaje = actualizar_pais(paises_actualizados, nombre, cambios)
    
    elif opcion == "9":   
        codigo = input("Código de país (ej: ARG, BRA, PER): ").strip().upper()
        indicador = input("Indicador Banco Mundial (ej: SP.POP.TOTL): ").strip()
        if not codigo or not indicador:
            print("Faltan datos.")
            return
        datos = consultar_indicador(codigo, indicador)
        datos = transformar_indicadores(datos)
        exito, mensaje = preparar_registros_csv(paises_actualizados, datos)
        
    else:
        raise NotImplementedError(f"Opción {opcion} pendiente de integración")

    if not exito:
        print(mensaje)
        return
    if guardar_paises(paises_actualizados):
        paises[:] = paises_actualizados
        print(mensaje)
    else:
        print("Los cambios no pudieron guardarse. Volvé a intentarlo.")
    
def main():
    try:
        paises = cargar_paises()
    except (OSError, ValueError) as error:
        print(f"Error al cargar el CSV: {error}")
        return
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
