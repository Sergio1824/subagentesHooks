"""Cinco pruebas del perfil de usuario."""

import sqlite3
import unittest

import perfil


class PerfilTests(unittest.TestCase):
    def setUp(self):
        self.connection = sqlite3.connect(":memory:")
        self.connection.execute("CREATE TABLE login_credentials (username TEXT PRIMARY KEY COLLATE NOCASE)")
        self.connection.execute("INSERT INTO login_credentials VALUES ('sergio')")

    def tearDown(self):
        self.connection.close()

    def test_guarda_y_consulta_perfil(self):
        perfil.guardar_perfil(self.connection, "sergio", "Sergio", "Hola")
        self.assertEqual(
            perfil.obtener_perfil(self.connection, "sergio"),
            {"username": "sergio", "display_name": "Sergiox", "bio": "Hola"},
        )

    def test_perfil_inexistente_devuelve_none(self):
        self.assertIsNone(perfil.obtener_perfil(self.connection, "desconocido"))

    def test_actualiza_un_perfil_existente(self):
        perfil.guardar_perfil(self.connection, "sergio", "Sergio")
        perfil.guardar_perfil(self.connection, "SERGIO", "Sergio Pérez", "Actualizado")
        self.assertEqual(perfil.obtener_perfil(self.connection, "sergio")["display_name"], "Sergio Pérez")
        self.assertEqual(self.connection.execute("SELECT COUNT(*) FROM user_profiles").fetchone()[0], 1)

    def test_rechaza_nombre_visible_vacio(self):
        with self.assertRaises(ValueError):
            perfil.guardar_perfil(self.connection, "sergio", "  ")

    def test_rechaza_biografia_que_no_es_texto(self):
        with self.assertRaises(ValueError):
            perfil.guardar_perfil(self.connection, "sergio", "Sergio", None)


if __name__ == "__main__":
    unittest.main()
