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
    elif opcion == "3":
        lista_actualizada = eliminar_pais(paises_actualizados, input("Nombre del país a eliminar: "))
        if lista_actualizada is None:
            return
        print("¿Estás seguro de eliminar el país? (S/N): ", end="")
        confirmacion = input().strip().lower()
        if confirmacion == "s":
            paises_actualizados = lista_actualizada
            exito, mensaje = True, "País eliminado correctamente."
        else:
            exito, mensaje = False, "Eliminación cancelada."
    elif opcion == "4":
        lista_vacia = limpiar_paises(paises_actualizados)
        print("¿Estás seguro de limpiar todos los registros? (S/N): ", end="")
        confirmacion = input().strip().lower()
        if confirmacion == "s":
            paises_actualizados = lista_vacia
            exito, mensaje = True, "Todos los registros han sido eliminados de la lista."
        else:
            exito, mensaje = False, "Limpieza cancelada."
    elif opcion == "5":
        print("Ingrese el nombre del país que desea buscar: ", end="")
        nombre = input()
        paises_encontrados = buscar_pais(paises_actualizados, nombre)

        if paises_encontrados is not None and len(paises_encontrados) == 1:
            print(f"Coincidencia encontrada: \n{paises_encontrados[0]}")
            return
        elif paises_encontrados is not None and len(paises_encontrados) > 1:
            print(f"Se encontraron varias coincidencias para {nombre}")
            for pais in paises_encontrados:
                print(pais)
            return
        else:
            exito, mensaje = False, print(f"No hay ningún país que coincida con {nombre}")
    elif opcion == "6":
        while True:
            print("Desea filtrar por\n1) Continente\n2) Población\n3) Superficie")
            eleccion = input().strip()
            match eleccion:
                case "1":
                    print("Seleccione un continente para mostrar la información de sus paises: ", end="")
                    continente = input()
                    paises_filtrados = filtrar_continente(paises_actualizados, continente)
                    print(f"Mostrando la información disponible para los paises de {continente.lower().strip()}")
                    for pais in paises_filtrados:
                        print(pais)
                    return
                case "2" | "3":
                    paises_filtrados = filtrar_rango(paises_actualizados, eleccion)
                    for pais in paises_filtrados:
                        print(pais)
                    return
                case _:
                    print("Error, debe elegir opción 1, 2 o 3")
                    continue

    elif opcion == "7":
        parametro = input("¿Desea ordenar por nombre, población o superficie? ")
        lista_ordenada = ordenar_paises(paises_actualizados, parametro)
        for pais in lista_ordenada:
            print(pais)

        return
        #En caso de querer actualizar el csv con la lista ordenada utilizar el codigo de abajo y eliminar el return de la linea anterior
        """ paises_actualizados = lista_ordenada

        if lista_ordenada == None:
            exito, mensaje = False, "Fallo al ordenar la lista."
        else:
            exito, mensaje = True, f"Se ha ordenado la lista en base al parametro '{parametro}'" """
    
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
