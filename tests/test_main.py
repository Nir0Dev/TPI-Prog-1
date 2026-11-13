"""Pruebas de las opciones CSV del menú con archivos temporales."""
import contextlib
import io
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

import main
from gestion_paises import cargar_paises, guardar_paises
from tests.test_gestion_paises import pais_ejemplo


class TestMenuCSV(unittest.TestCase):
    def setUp(self):
        carpeta = tempfile.TemporaryDirectory()
        self.addCleanup(carpeta.cleanup)
        self.ruta = Path(carpeta.name) / "data" / "paises.csv"
        self.guardado = self.enterContext(patch(
            "main.guardar_paises", side_effect=lambda paises: guardar_paises(paises, self.ruta)
        ))
        self.enterContext(patch("main.cargar_paises", side_effect=lambda: cargar_paises(self.ruta)))

    def ejecutar(self, opcion, paises, entradas):
        salida = io.StringIO()
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(salida):
            main.ejecutar_opcion(opcion, paises)
        return salida.getvalue()

    def test_agregar_guarda_numeros_y_confirma(self):
        paises = []
        salida = self.ejecutar("1", paises, [" Japón ", "125800000", "377975", "Asia"])
        self.assertEqual(paises, cargar_paises(self.ruta))
        self.assertEqual(paises[0]["poblacion"], 125800000)
        self.assertIn("agregado correctamente", salida)

    def test_agregar_invalido_o_repetido_evitar_guardado(self):
        for nombre, poblacion in [("Brasil", "mucha"), (" ARGENTINA ", "100")]:
            with self.subTest(nombre=nombre):
                paises = [pais_ejemplo()]
                self.ejecutar("1", paises, [nombre, poblacion, "100", "América"])
                self.assertEqual(paises, [pais_ejemplo()])
        self.guardado.assert_not_called()

    def test_actualizar_un_campo_conserva_el_otro_y_extras(self):
        paises = [pais_ejemplo(iso3="ARG")]
        salida = self.ejecutar("2", paises, [" ARGENTINA ", "46000000", ""])
        self.assertEqual(paises[0], pais_ejemplo(poblacion=46000000, iso3="ARG"))
        self.assertEqual(cargar_paises(self.ruta), paises)
        self.assertIn("población 45376763, superficie 2780400", salida)  # datos actuales
        self.assertIn("actualizado correctamente", salida)

    def test_actualizar_pais_inexistente_no_pide_datos(self):
        paises = [pais_ejemplo()]
        # Solo se da el nombre: si el menú pidiera población o superficie, input() fallaría
        salida = self.ejecutar("2", paises, [" Narnia "])
        self.assertIn("No se encontró el país 'Narnia'", salida)
        self.guardado.assert_not_called()
        self.assertEqual(paises, [pais_ejemplo()])

    def test_actualizar_sin_cambios_evitar_guardado(self):
        paises = [pais_ejemplo()]
        salida = self.ejecutar("2", paises, ["Argentina", "", ""])
        self.assertIn("al menos un cambio", salida)
        self.guardado.assert_not_called()
        self.assertEqual(paises, [pais_ejemplo()])

    def test_fallo_de_guardado_conserva_lista_y_archivo(self):
        paises = [pais_ejemplo()]
        guardar_paises(paises, self.ruta)
        original = self.ruta.read_bytes()
        self.ruta.with_name("paises.csv.tmp").mkdir()
        for opcion, entradas in [
            ("1", ["Japón", "125800000", "377975", "Asia"]),
            ("2", ["Argentina", "46000000", ""]),
        ]:
            with self.subTest(opcion=opcion):
                salida = self.ejecutar(opcion, paises, entradas)
                self.assertIn("Volvé a intentarlo", salida)
                self.assertNotIn("correctamente", salida)
                self.assertEqual(paises, [pais_ejemplo()])
                self.assertEqual(self.ruta.read_bytes(), original)

    def test_main_carga_agrega_modifica_y_persiste_entre_ejecuciones(self):
        entradas = ["1", "Japón", "125800000", "377975", "Asia", "0"]
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(io.StringIO()):
            main.main()
        entradas = ["2", "japón", "126000000", "", "0"]
        with patch("builtins.input", side_effect=entradas), contextlib.redirect_stdout(io.StringIO()):
            main.main()
        self.assertEqual(cargar_paises(self.ruta), [{
            "nombre": "Japón", "poblacion": 126000000, "superficie": 377975, "continente": "Asia"
        }])

    def test_main_csv_invalido_termina_antes_del_menu(self):
        self.ruta.parent.mkdir(parents=True)
        original = "nombre,poblacion\nArgentina,45376763\n"
        self.ruta.write_text(original, encoding="utf-8")
        salida = io.StringIO()
        with patch("builtins.input") as entrada, contextlib.redirect_stdout(salida):
            main.main()
        entrada.assert_not_called()
        self.guardado.assert_not_called()
        self.assertIn("Error al cargar el CSV", salida.getvalue())
        self.assertEqual(self.ruta.read_text(encoding="utf-8"), original)

    def test_main_opcion_invalida_permite_continuar(self):
        # No usa ninguna opción de otro integrante: así la prueba sigue valiendo
        # a medida que se integran las opciones 3 a 9.
        salida = io.StringIO()
        with patch("builtins.input", side_effect=["x", "99", "0"]), contextlib.redirect_stdout(salida):
            main.main()
        self.assertEqual(salida.getvalue().count("Opción inválida"), 2)
        self.assertIn("Hasta luego", salida.getvalue())
        self.guardado.assert_not_called()


if __name__ == "__main__":
    unittest.main()
