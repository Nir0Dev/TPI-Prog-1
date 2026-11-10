# TPI Programación 1 — Gestión de países

**Proyecto grupal en desarrollo.** La gestión CSV y las opciones 1 y 2 están implementadas. Las opciones 3 a 9 están pendientes de desarrollar e integrar por sus responsables.

## Responsabilidades
| Integrante | Archivos | Funcionalidades |
|---|---|---|
| 1 | `gestion_paises.py` | CSV automático, plantilla, validaciones, agregar, modificar y guardar |
| 2 | `consultas.py`, `operaciones.py` | Buscar, filtrar, ordenar, eliminar y limpiar |
| 3 | `estadisticas.py`, `graficos.py` | Estadísticas, densidad y figuras Matplotlib con gráfico arriba y datos debajo |
| 4 | `api_paises.py` | API Banco Mundial: descargar población/superficie, transformar JSON, validar y preparar para guardar |

## Contrato compartido
Los datos son una `list[dict]` con `nombre`, `poblacion`, `superficie` y `continente`. La API puede incorporar columnas adicionales opcionales. `gestion_paises.py` es el único módulo que escribe CSV. El programa encuentra `data/paises.csv` automáticamente y crea una plantilla con encabezados cuando falta. Acepta CSV con coma o punto y coma, en UTF-8 o Windows cp1252. Si faltan columnas obligatorias, muestra el error y termina.

Los módulos de consultas y estadísticas **no guardan archivos**; trabajan con datos recibidos como argumentos. La API **no escribe directamente**: produce registros que el usuario podrá guardar mediante la capa de persistencia.

## Uso inicial
```bash
python -m pip install -r requirements.txt
python main.py
```
La opción 1 pide nombre, población, superficie y continente. Por ejemplo, `Japón`, `125800000`, `377975`, `Asia` produce el mensaje `País 'Japón' agregado correctamente.` y guarda los números como enteros. Rechaza campos vacíos, datos inválidos y nombres repetidos sin importar mayúsculas.

La opción 2 busca un nombre exacto sin importar mayúsculas y permite actualizar población, superficie o ambas. Enter conserva el valor actual de cada campo. Cada alta o modificación válida se guarda en CSV antes de confirmar el éxito. Las columnas adicionales se conservan.

Las funciones pendientes avisan que todavía falta su integración. Para ejecutar las pruebas del proyecto:

```bash
python3 -m unittest discover -s tests -v
```

## Trabajo en paralelo
Crear ramas `feature/csv`, `feature/consultas`, `feature/estadisticas`, `feature/api`. Cada integrante implementa y prueba sus funciones con datos de prueba independientes; la edición del `main.py` se integra mediante PRs, uno por vez. Nunca sobrescribir el trabajo de un compañero.

## Requisitos académicos
La consigna requiere filtros por continente/rango de población/rango de superficie, ordenamientos (nombre/población/superficie y dirección), mayor y menor población, promedios de población y superficie, conteo por continente, validación y un video de 10-15 minutos. Para el grupo de 4, según la presentación del profesor, los datos de la API deben descargarse, transformarse, validarse y persistirse en CSV.

El CSV final, la documentación PDF y el enlace público del video se agregarán durante la entrega.
