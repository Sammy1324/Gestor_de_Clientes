import copy
import unittest
import os
import csv
from Gestor import database as db
from Gestor import helpers

class TestDatabase(unittest.TestCase):

    def setUp(self):
        # Configuración inicial antes de cada prueba
        db.Clients.clients_list = [
            db.Client("11D", "John", "Doe"),
            db.Client("22S", "Jane", "Smith"),
            db.Client("33J", "Alice", "Johnson")
        ]
        # Crear un archivo temporal para pruebas
        self.test_file = "Gestor/tests/clients_test.csv"
        db.settings.DATABASE_PATH = self.test_file
        db.Clients.save()

    def tearDown(self):
        # Eliminar el archivo temporal después de cada prueba
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_search(self):
        # Caso: Cliente existente
        existing_client = db.Clients.search("11D")
        self.assertIsNotNone(existing_client)
        self.assertEqual(existing_client.name, "John")

        # Caso: Cliente no existente
        non_existing_client = db.Clients.search("99J")
        self.assertIsNone(non_existing_client)

    def test_create(self):
        # Crear un nuevo cliente
        new_client = db.Clients.create("44B", "Bob", "Brown")
        self.assertEqual(len(db.Clients.clients_list), 4)
        self.assertEqual(new_client.id, "44B")
        self.assertEqual(new_client.name, "Bob")
        self.assertEqual(new_client.last_name, "Brown")

        # Verificar que se haya guardado en el archivo
        with open(self.test_file, newline="\n") as file:
            reader = list(csv.reader(file, delimiter=";"))
        self.assertIn(["44B", "Bob", "Brown"], reader)

    def test_modify(self):
        # Modificar un cliente existente
        modified_client = db.Clients.modify("11D", "Joe", "Cranston")
        self.assertEqual(modified_client.name, "Joe")
        self.assertEqual(modified_client.last_name, "Cranston")

        # Verificar que los cambios se reflejen en el archivo
        with open(self.test_file, newline="\n") as file:
            reader = list(csv.reader(file, delimiter=";"))
        self.assertIn(["11D", "Joe", "Cranston"], reader)

    def test_delete(self):
        # Eliminar un cliente existente
        deleted_client = db.Clients.delete("11D")
        self.assertEqual(deleted_client.id, "11D")

        # Verificar que ya no esté en la lista
        self.assertIsNone(db.Clients.search("11D"))

        # Verificar que ya no esté en el archivo
        with open(self.test_file, newline="\n") as file:
            reader = list(csv.reader(file, delimiter=";"))
        self.assertNotIn(["11D", "John", "Doe"], reader)

    def test_save(self):
        # Modificar la lista y guardar
        db.Clients.create("55C", "Charlie", "Chaplin")
        db.Clients.save()

        # Verificar que los datos se guarden correctamente
        with open(self.test_file, newline="\n") as file:
            reader = list(csv.reader(file, delimiter=";"))
        self.assertIn(["55C", "Charlie", "Chaplin"], reader)

    def test_valid_id(self):
        # Validar IDs
        self.assertTrue(helpers.valid_id("00A", db.Clients.clients_list))
        self.assertFalse(helpers.valid_id("23223S", db.Clients.clients_list))
        self.assertFalse(helpers.valid_id("F35", db.Clients.clients_list))


if __name__ == "__main__":
    unittest.main()