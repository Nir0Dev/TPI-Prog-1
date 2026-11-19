# TPI Programación 1 — Gestión de datos de países

Trabajo Práctico Integrador de Programación 1 de la Tecnicatura Universitaria en Programación, UTN Facultad Regional Mendoza.

Aplicación de consola en Python que permite administrar países desde un archivo CSV, realizar búsquedas, filtros y ordenamientos, calcular estadísticas y visualizar gráficos con Matplotlib. También permite descargar información del Banco Mundial y confirmar su integración con los datos locales.

## Integrantes

- Cristian Papa
- Sebastián Julián
- Bruno Mantovan
- Nicolás Ontivero

## Requisitos e instalación

- Python 3.10 o superior (compatible con Matplotlib 3.8).
- Dependencias declaradas en `requirements.txt`: Matplotlib y Requests.
- Un entorno de escritorio para abrir las ventanas de los gráficos.
- Internet únicamente para instalar dependencias y consultar la API; las operaciones sobre el CSV y los gráficos funcionan sin conexión una vez instaladas las dependencias.

Clonar el repositorio y ejecutar desde su carpeta:

```bash
git clone https://github.com/Nir0Dev/TPI-Prog-1.git
cd TPI-Prog-1
python -m pip install -r requirements.txt
python main.py
```

En sistemas donde Python 3 se invoque como `python3`, reemplazar `python` por `python3`.

## Datos y archivo CSV

El dataset está en [`data/paises.csv`](data/paises.csv). El programa lo encuentra automáticamente, independientemente de la carpeta desde la que se ejecute. Si el archivo falta o está vacío, crea una plantilla con los encabezados obligatorios.

Cada país se representa con un diccionario y los países se almacenan en una lista. Las cuatro columnas obligatorias son:

| Campo | Tipo y validación |
|---|---|
| `nombre` | Texto no vacío y con letras. |
| `poblacion` | Entero entre 0 y 10.000.000.000 habitantes. |
| `superficie` | Entero mayor que 0 y hasta 150.000.000 km². |
| `continente` | Texto no vacío y con letras. |

Ejemplo de formato, con datos ilustrativos:

```csv
nombre,poblacion,superficie,continente
Argentina,45376763,2780400,América
Japón,125800000,377975,Asia
Brasil,213993437,8515767,América
Alemania,83149300,357022,Europa
```

El lector acepta coma o punto y coma como separador, UTF-8 con o sin BOM y codificación Windows cp1252. Convierte los números y avisa si descarta filas inválidas o repetidas. Si faltan columnas obligatorias, informa el error y termina antes de mostrar el menú. Las filas descartadas se eliminan del archivo al confirmar un guardado posterior; conviene corregirlas antes si se necesitan conservar.

Las columnas adicionales de la API se conservan al cargar, modificar y guardar: código de país, región, capital, coordenadas y año, entre otras. Los campos `anio` y `anio_api` se almacenan, pero no se muestran en los resultados de los países.

## Menú e instrucciones de uso

| Opción | Funcionamiento |
|---|---|
| **1. Agregar país** | Solicita nombre, población, superficie y continente. Valida los datos y evita nombres repetidos sin distinguir mayúsculas ni espacios adicionales. Guarda el alta válida. |
| **2. Modificar país** | Busca por nombre completo y permite cambiar población, superficie o ambas. Enter conserva el valor actual. Guarda los cambios válidos y conserva los campos adicionales. |
| **3. Eliminar país** | Busca el nombre ignorando mayúsculas y acentos. Solicita confirmación S/N antes de guardar la eliminación. |
| **4. Limpiar todos los registros** | Solicita confirmación S/N. Al aceptar, guarda el CSV sin países y con los encabezados obligatorios. No restaura el dataset inicial. |
| **5. Buscar país** | Busca por el inicio del nombre, ignorando mayúsculas, acentos y espacios extremos. Muestra cantidad de coincidencias y datos con formato `Nombre: valor`, sin llaves. |
| **6. Filtrar países** | Permite filtrar por continente, rango de población o rango de superficie. Muestra los continentes disponibles antes de solicitar uno. Por continente muestra nombres; por población o superficie, nombre y el valor correspondiente. |
| **7. Ordenar países** | Ordena por nombre o población de forma ascendente. Para superficie permite elegir `asc` o `dsc`. Muestra nombre y, cuando corresponde, el campo utilizado. Pregunta si se desea guardar el orden en el CSV. |
| **8. Mostrar estadísticas** | Abre un submenú con resumen general, ficha de un país y gráficos comparativos de población o superficie. |
| **9. Consultar API Banco Mundial / incorporar datos** | Descarga, valida y prepara países nuevos y datos adicionales de países existentes. Informa los omitidos y solicita confirmación antes de guardar. |
| **0. Salir** | Finaliza el programa. |

Las búsquedas y los filtros no modifican el CSV. En los rangos se incluyen ambos límites, pero la entrada exige un mínimo mayor que cero y un máximo mayor que el mínimo. Los continentes admitidos por el filtro son América, África, Asia, Europa y Oceanía.

La opción 7 solo conserva el orden si se responde **S** y la escritura es exitosa. Las operaciones que guardan datos actualizan la lista activa después del guardado. `gestion_paises.py` centraliza la persistencia y escribe primero un archivo temporal para proteger el CSV ante fallos de escritura.

### Estadísticas y gráficos: opción 8

1. **Cantidad por continente y resumen general:** mayor y menor población, promedios de población y superficie y cantidad de países por continente.
2. **Estadísticas de un país:** población, superficie, continente, densidad y datos adicionales disponibles. La densidad se calcula como población / superficie. Los botones permiten alternar población, superficie y densidad.
3. **Población: comparación, extremos y promedio:** barras por país, extremos y línea de promedio general.
4. **Superficie por país y promedio:** barras por país y línea de promedio general.
5. **Volver al menú principal.**

Los gráficos comparativos muestran hasta 15 países por página, con botones Anterior, Siguiente, Mayor a menor, Menor a mayor y Volver. El orden de los gráficos es solo visual y no modifica el CSV. Se informa cuando faltan países o existen datos que impiden calcular las estadísticas.

### Integración con el Banco Mundial: opción 9

Se consulta el catálogo descriptivo en español y los indicadores `SP.POP.TOTL` (población) y `AG.SRF.TOTL.K2` (superficie) para **2023**. El catálogo descriptivo no está filtrado por ese año.

La comparación con los países locales utiliza nombres completos normalizados: ignora mayúsculas, espacios adicionales y acentos. No requiere códigos en el CSV ni reconoce automáticamente nombres alternativos. Los códigos se utilizan para unir las respuestas de la API internamente.

- Incorpora países nuevos con datos obligatorios válidos.
- En coincidencias existentes, conserva población y superficie locales y completa campos adicionales vacíos.
- Si también coincide el continente normalizado, adopta la escritura del nombre y del continente de la API.
- Muestra los países omitidos y los motivos; informa cuántos países se incorporarían o completarían.
- Solicita confirmación **S/N** antes de guardar. El año recibido no implica que se hayan actualizado la población y superficie locales conservadas.

La descarga controla paginación, tiempos máximos de conexión y lectura y hasta tres intentos por página ante fallos recuperables. Si falla una descarga requerida, cancela la integración del conjunto parcial. Sin internet se puede continuar usando el CSV local.

## Ejemplos de entradas y salidas

Para reproducir los ejemplos siguientes, usar este conjunto **ficticio de prueba**, guardando primero una copia del CSV habitual. Reiniciar el programa después de reemplazar el archivo. No ejecutar la opción 9 durante estos ejemplos, porque cambiaría el conjunto si se confirma la integración.

```csv
nombre,poblacion,superficie,continente
Argentina,100,10,América
Argelia,300,30,África
Perú,200,20,América
```

### Búsqueda parcial

Entrada: opción **5**, nombre **ARG**.

```text
Coincidencias encontradas: 2
Nombre: Argentina | Poblacion: 100 | Superficie: 10 | Continente: América
Nombre: Argelia | Poblacion: 300 | Superficie: 30 | Continente: África
```

### Filtro de población y validación

Entrada: opción **6**, filtro **2**. Escribir `abc` como mínimo para comprobar el rechazo; luego ingresar mínimo `100` y máximo `200`.

```text
Error, debe seleccionar un numero entero mayor a 0
```

Después de ingresar los límites válidos:

```text
Filtrando paises por poblacion en el rango de 100 a 200...
Nombre: Argentina | Población: 100
Nombre: Perú | Población: 200
```

### Resumen estadístico

Entrada: opción **8**, subopción **1**. Se abre una figura con estos resultados:

| Estadística | Resultado esperado |
|---|---|
| Mayor población | Argelia: 300 habitantes |
| Menor población | Argentina: 100 habitantes |
| Promedio de población | 200 habitantes |
| Promedio de superficie | 20 km² |
| Cantidad por continente | América: 2; África: 1 |

El botón Volver cierra la figura y regresa al submenú.

## Organización y participación de los integrantes

| Integrante | Responsabilidad principal | Archivos |
|---|---|---|
| Cristian Papa — integrante 1 | Carga y guardado CSV, plantilla, validaciones, altas y modificaciones. | `gestion_paises.py` |
| Bruno Mantovan — integrante 2 | Búsquedas, filtros, ordenamiento, eliminación y limpieza. | `consultas.py`, `operaciones.py` |
| Nicolás Ontivero — integrante 3 | Cálculo de estadísticas y densidad, gráficos e interacción con las figuras. Integración y ajustes de módulos compartidos y API. | `estadisticas.py`, `graficos.py`, ajustes en `main.py` y `api_paises.py` |
| Sebastián Julián — integrante 4 | Implementación inicial de la consulta API, transformación y preparación de registros. | `api_paises.py` |

`main.py` conecta las funciones con el menú. La integración entre módulos se trabajó mediante ramas y revisiones del equipo.

## Documentación y video de entrega

- **Repositorio:** https://github.com/Nir0Dev/TPI-Prog-1
- **Informe de trabajo editable:** https://docs.google.com/document/d/1z5xGx5NavVmho__BVpo4ETUs22piHVO2/edit
- **Documentación final en PDF — pendiente:** agregar el enlace público al PDF o subir el archivo directamente en la raíz del repositorio y enlazarlo aquí. El informe editable no reemplaza este requisito.
- **Video demostrativo público de 10 a 15 minutos — pendiente:** incorporar aquí el enlace definitivo y comprobar sus permisos de visualización.

Según la consigna, la entrega final se presenta en un archivo `.zip` que incluye el código fuente completo y la documentación en PDF. El repositorio debe incluir el dataset CSV y este README con los enlaces obligatorios completos antes de entregar.
