"""Pruebas iniciales de estructura (no sustituyen pruebas funcionales)."""
import unittest
from gestion_paises import COLUMNAS_OBLIGATORIAS
from main import OPCIONES

class TestContrato(unittest.TestCase):
    def test_columnas_obligatorias(self):
        self.assertEqual(COLUMNAS_OBLIGATORIAS, ("nombre", "poblacion", "superficie", "continente"))

    def test_menu_estadisticas_unificado(self):
        self.assertIn("gráfico", OPCIONES["8"].lower())

if __name__ == "__main__":
    unittest.main()
