# Pruebas del equipo

Cada integrante agrega pruebas propias, preferentemente con `unittest` de la biblioteca estándar. Se pueden usar listas/diccionarios de prueba y respuestas JSON simuladas; no hay que esperar al CSV definitivo ni a la conexión de red.

- I1: plantilla, CSV vacío, CSV inválido, agregar/actualizar y preservación de columnas extra.
- I2: búsquedas parciales, rangos inválidos, orden, eliminar y limpiar sin perder encabezados.
- I3: estadísticas, lista vacía, densidad y figuras con `plt.show()` sin guardar archivos.
- I4: HTTP simulado, errores, transformación JSON, registro incompleto y deduplicación.

Cuando haya pruebas, ejecutar: `python -m unittest discover -s tests -v`.
