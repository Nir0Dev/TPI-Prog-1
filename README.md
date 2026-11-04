# TPI Programación 1 — Gestión de países

Plantilla de trabajo para cuatro integrantes. Las funciones de negocio están pendientes de implementar.

## Ejecutar

```bash
python main.py
```

Dependencias para gráficos y API:

```bash
python -m pip install -r requirements.txt
```

## Contrato de datos

Campos obligatorios del CSV: `nombre,poblacion,superficie,continente`. La API puede agregar columnas opcionales sin perder las originales.

`data/paises.csv` se crea automáticamente con encabezados cuando se implemente la carga en `gestion_paises.py`; por ahora hay una plantilla de encabezados.

## Responsables

1. `gestion_paises.py`: lectura, plantilla, altas, cambios y persistencia.
2. `consultas.py` y `operaciones.py`: búsqueda, filtrado, ordenamiento, eliminación y limpieza.
3. `estadisticas.py` y `graficos.py`: cálculos y ventana Matplotlib con gráfico arriba y datos debajo.
4. `api_paises.py`: consultas al Banco Mundial, transformación, validación y preparación de registros para guardar.

Cada integrante trabaja en una rama `feature/...`, implementa sus funciones y sus pruebas, y conecta sus opciones con los controladores ya definidos en `main.py`. Se recomienda integrar mediante PR para evitar conflictos.

## Estado

Esta entrega es **solo la estructura y las funciones base**, no una implementación terminada. Las funciones pendientes lanzan `NotImplementedError`; el menú captura ese estado y lo comunica sin cerrar la aplicación.
