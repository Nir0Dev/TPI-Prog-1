"""Pruebas del integrante 1 (gestion_paises.py).

Ejecutar desde la raíz del repo:  python -m unittest discover -s tests -v
Cada prueba usa una carpeta temporal: nunca toca data/paises.csv.
"""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path

from gestion_paises import (
    COLUMNAS_OBLIGATORIAS,
    actualizar_pais,
    agregar_pais,
    cargar_paises,
    crear_plantilla,
    guardar_paises,
    validar_pais,
)

ENCABEZADO = ",".join(COLUMNAS_OBLIGATORIAS)


def pais_ejemplo(**cambios):
    pais = {"nombre": "Argentina", "poblacion": 45376763, "superficie": 2780400, "continente": "América"}
    pais.update(cambios)
    return pais


class ConCarpetaTemporal(unittest.TestCase):
    def setUp(self):
        self._carpeta = tempfile.TemporaryDirectory()
        self.ruta = Path(self._carpeta.name) / "data" / "paises.csv"

    def tearDown(self):
        self._carpeta.cleanup()

    def escribir(self, contenido, encoding="utf-8"):
        self.ruta.parent.mkdir(parents=True, exist_ok=True)
        self.ruta.write_bytes(contenido.encode(encoding))

    def cargar_en_silencio(self):
        """Cargar el CSV y devolver (paises, texto impreso en pantalla)."""
        salida = io.StringIO()
        with contextlib.redirect_stdout(salida):
            paises = cargar_paises(self.ruta)
        return paises, salida.getvalue()


class TestCrearPlantilla(ConCarpetaTemporal):
    def test_crea_carpeta_y_encabezado_si_falta(self):
        self.assertTrue(crear_plantilla(self.ruta))
        self.assertEqual(self.ruta.read_text(encoding="utf-8").strip(), ENCABEZADO)

    def test_no_sobrescribe_datos_existentes(self):
        self.escribir(ENCABEZADO + "\nJapón,125800000,377975,Asia\n")
        self.assertFalse(crear_plantilla(self.ruta))
        self.assertIn("Japón", self.ruta.read_text(encoding="utf-8"))

    def test_archivo_vacio_recibe_encabezado(self):
        self.escribir("")
        self.assertTrue(crear_plantilla(self.ruta))
        self.assertEqual(self.ruta.read_text(encoding="utf-8").strip(), ENCABEZADO)


class TestValidarPais(unittest.TestCase):
    def test_pais_valido_con_numeros_en_texto(self):
        limpio, errores = validar_pais({"nombre": "  Japón ", "poblacion": "125800000",
                                        "superficie": " 377975 ", "continente": "Asia"})
        self.assertEqual(errores, [])
        self.assertEqual(limpio, {"nombre": "Japón", "poblacion": 125800000,
                                  "superficie": 377975, "continente": "Asia"})

    def test_no_modifica_el_original(self):
        original = pais_ejemplo(poblacion="100")
        validar_pais(original)
        self.assertEqual(original["poblacion"], "100")

    def test_campos_vacios(self):
        _, errores = validar_pais({"nombre": "", "poblacion": " ", "superficie": None})
        self.assertEqual(len(errores), 4)

    def test_casos_de_la_presentacion(self):
        casos = [
            pais_ejemplo(nombre="Kosovo", superficie=""),       # falta superficie
            pais_ejemplo(nombre="Brasil", poblacion="mucha"),   # población no numérica
            pais_ejemplo(nombre="Chile", superficie=0),          # superficie debe ser > 0
            pais_ejemplo(poblacion=-1),
            pais_ejemplo(superficie="12.5"),
            pais_ejemplo(continente="123"),
        ]
        for pais in casos:
            with self.subTest(pais=pais):
                _, errores = validar_pais(pais)
                self.assertNotEqual(errores, [])

    def test_acepta_decimales_en_cero_y_conserva_extras(self):
        limpio, errores = validar_pais(pais_ejemplo(superficie=2780400.0, iso3="ARG"))
        self.assertEqual(errores, [])
        self.assertEqual(limpio["superficie"], 2780400)
        self.assertEqual(limpio["iso3"], "ARG")


class TestCargarPaises(ConCarpetaTemporal):
    def test_si_no_existe_crea_plantilla_y_devuelve_lista_vacia(self):
        paises, _ = self.cargar_en_silencio()
        self.assertEqual(paises, [])
        self.assertTrue(self.ruta.exists())

    def test_carga_y_convierte_numeros(self):
        self.escribir(ENCABEZADO + "\nArgentina,45376763,2780400,América\nJapón,125800000,377975,Asia\n")
        paises, salida = self.cargar_en_silencio()
        self.assertEqual(len(paises), 2)
        self.assertEqual(paises[1]["poblacion"], 125800000)
        self.assertEqual(salida, "")

    def test_descarta_filas_invalidas_y_repetidas(self):
        self.escribir(ENCABEZADO + "\n"
                      "Argentina,45407904,2780400,América\n"
                      "Kosovo,1800000,,Europa\n"
                      "Brasil,mucha,8515767,América\n"
                      "Chile,19000000,0,América\n"
                      "ARGENTINA,1,1,América\n"
                      "Uruguay,3400000,176215,América,sobra\n"
                      "Alemania,83149300,357022,Europa\n")
        paises, salida = self.cargar_en_silencio()
        self.assertEqual([p["nombre"] for p in paises], ["Argentina", "Alemania"])
        self.assertEqual(salida.count("descartada"), 5)
        self.assertIn("línea 6", salida)  # la fila de ARGENTINA repetida

    def test_faltan_columnas_lanza_error(self):
        self.escribir("nombre,poblacion,continente\nArgentina,45376763,América\n")
        with self.assertRaises(ValueError):
            self.cargar_en_silencio()

    def test_formatos_de_excel(self):
        # Excel en español: separador ';' y codificación cp1252, o UTF-8 con BOM
        contenido = "Nombre;Poblacion;Superficie;Continente\nJapón;125800000;377975;Asia\n"
        for encoding in ("cp1252", "utf-8-sig"):
            with self.subTest(encoding=encoding):
                self.escribir(contenido, encoding)
                paises, _ = self.cargar_en_silencio()
                self.assertEqual(paises[0]["nombre"], "Japón")

    def test_conserva_columnas_extra(self):
        self.escribir(ENCABEZADO + ",iso3\nArgentina,45376763,2780400,América,ARG\n")
        paises, _ = self.cargar_en_silencio()
        self.assertEqual(paises[0]["iso3"], "ARG")


class TestGuardarPaises(ConCarpetaTemporal):
    def test_guardar_y_volver_a_cargar(self):
        datos = [pais_ejemplo(), pais_ejemplo(nombre="Japón", iso3="JPN")]
        self.assertTrue(guardar_paises(datos, self.ruta))
        paises, _ = self.cargar_en_silencio()
        self.assertEqual(paises[1]["poblacion"], 45376763)
        self.assertEqual(paises[1]["iso3"], "JPN")
        self.assertEqual(paises[0]["iso3"], "")  # columna extra vacía para quien no la tiene

    def test_lista_vacia_conserva_encabezado(self):
        self.assertTrue(guardar_paises([], self.ruta))
        self.assertEqual(self.ruta.read_text(encoding="utf-8").strip(), ENCABEZADO)

    def test_si_falla_no_rompe_el_original(self):
        self.escribir(ENCABEZADO + "\nArgentina,45376763,2780400,América\n")
        self.ruta.with_name(self.ruta.name + ".tmp").mkdir()  # fuerza un error al escribir
        with contextlib.redirect_stdout(io.StringIO()):
            self.assertFalse(guardar_paises([], self.ruta))
        self.assertIn("Argentina", self.ruta.read_text(encoding="utf-8"))


# ---------------------------------------------------------------------------
# Pruebas de la parte de Cris: fallan hasta implementar agregar/actualizar.
# ---------------------------------------------------------------------------
class TestAgregarPais(unittest.TestCase):
    def test_agrega_pais_valido_con_numeros_en_texto(self):
        paises = [pais_ejemplo()]
        exito, mensaje = agregar_pais(paises, {"nombre": "Japón", "poblacion": "125800000",
                                               "superficie": "377975", "continente": "Asia"})
        self.assertTrue(exito)
        self.assertIsInstance(mensaje, str)
        self.assertEqual(len(paises), 2)
        self.assertEqual(paises[1]["poblacion"], 125800000)  # quedó como int

    def test_rechaza_campos_invalidos(self):
        paises = []
        exito, mensaje = agregar_pais(paises, pais_ejemplo(nombre="Brasil", poblacion="mucha"))
        self.assertFalse(exito)
        self.assertIn("poblacion", mensaje)
        self.assertEqual(paises, [])

    def test_rechaza_repetido_sin_importar_mayusculas(self):
        paises = [pais_ejemplo()]
        exito, _ = agregar_pais(paises, pais_ejemplo(nombre="  ARGENTINA "))
        self.assertFalse(exito)
        self.assertEqual(len(paises), 1)


class TestActualizarPais(unittest.TestCase):
    def test_actualiza_y_conserva_extras(self):
        paises = [pais_ejemplo(iso3="ARG")]
        exito, _ = actualizar_pais(paises, "argentina", {"poblacion": "46000000", "superficie": 2780401})
        self.assertTrue(exito)
        self.assertEqual(paises[0]["poblacion"], 46000000)
        self.assertEqual(paises[0]["superficie"], 2780401)
        self.assertEqual(paises[0]["iso3"], "ARG")

    def test_actualiza_solo_un_campo(self):
        paises = [pais_ejemplo()]
        exito, _ = actualizar_pais(paises, "Argentina", {"superficie": "2780401"})
        self.assertTrue(exito)
        self.assertEqual(paises[0]["poblacion"], 45376763)
        self.assertEqual(paises[0]["superficie"], 2780401)

    def test_pais_inexistente(self):
        exito, _ = actualizar_pais([pais_ejemplo()], "Narnia", {"poblacion": 1})
        self.assertFalse(exito)

    def test_valor_invalido_no_cambia_nada(self):
        paises = [pais_ejemplo()]
        exito, _ = actualizar_pais(paises, "Argentina", {"poblacion": "100", "superficie": "0"})
        self.assertFalse(exito)
        self.assertEqual(paises[0], pais_ejemplo())

    def test_rechaza_cambios_vacios_u_otros_campos(self):
        for cambios in ({}, {"nombre": "Otra"}, {"continente": "Asia"}):
            with self.subTest(cambios=cambios):
                paises = [pais_ejemplo()]
                exito, _ = actualizar_pais(paises, "Argentina", cambios)
                self.assertFalse(exito)
                self.assertEqual(paises[0], pais_ejemplo())


if __name__ == "__main__":
    unittest.main()
