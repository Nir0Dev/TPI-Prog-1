# TPI Programación 1 — Gestión de países

**Plantilla de trabajo; no es una solución terminada.** Los módulos contienen funciones base pendientes de desarrollar por cada integrante.

## Responsabilidades
| Integrante | Archivos | Funcionalidades |
|---|---|---|
| 1 | `gestion_paises.py` | CSV automático, plantilla, validaciones, agregar, modificar y guardar |
| 2 | `consultas.py`, `operaciones.py` | Buscar, filtrar, ordenar, eliminar y limpiar |
| 3 | `estadisticas.py`, `graficos.py` | Estadísticas, densidad y figuras Matplotlib con gráfico arriba y datos debajo |
| 4 | `api_paises.py` | API Banco Mundial: descargar población/superficie, transformar JSON, validar y preparar para guardar |

## Contrato compartido
Los datos son una `list[dict]` con `nombre`, `poblacion`, `superficie` y `continente`. La API puede incorporar columnas adicionales opcionales. `gestion_paises.py` es el único módulo que escribe CSV. El CSV estará en `data/paises.csv`; **el integrante 1 debe implementar** que se encuentre automáticamente y que se cree una plantilla con encabezados cuando falte.

Los módulos de consultas y estadísticas **no guardan archivos**; trabajan con datos recibidos como argumentos. La API **no escribe directamente**: produce registros que el usuario podrá guardar mediante la capa de persistencia.

## Uso inicial
```bash
python -m pip install -r requirements.txt
python main.py
```
El menú de consola es un andamiaje: las funciones pendientes avisan que no están implementadas.

## Trabajo en paralelo
Crear ramas `feature/csv`, `feature/consultas`, `feature/estadisticas`, `feature/api`. Cada integrante implementa y prueba sus funciones con datos de prueba independientes; la edición del `main.py` se integra mediante PRs, uno por vez. Nunca sobrescribir el trabajo de un compañero.

## Requisitos académicos
La consigna requiere filtros por continente/rango de población/rango de superficie, ordenamientos (nombre/población/superficie y dirección), mayor y menor población, promedios de población y superficie, conteo por continente, validación y un video de 10-15 minutos. Para el grupo de 4, según la presentación del profesor, los datos de la API deben descargarse, transformarse, validarse y persistirse en CSV.

El CSV final, la documentación PDF y el enlace público del video se agregarán durante la entrega.
