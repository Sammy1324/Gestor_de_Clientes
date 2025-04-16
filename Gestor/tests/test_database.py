import copy
import unittest
from Gestor import database as db
from Gestor import helpers

class TestDatabase(unittest.TestCase):

    def setUp(self):
        db.Clients.clients_list = [
            db.Client("11D", "John", "Doe"),
            db.Client("22S", "Jane", "Smith"),
            db.Client("33J", "Alice", "Johnson")
        ]

    def test_search(self):
        existing_client = db.Clients.search("11D")
        non_existing_client = db.Clients.search("99J")
        self.assertIsNotNone(existing_client)
        self.assertIsNone(non_existing_client)

    def test_create(self):
        new_client = db.Clients.create("44B", "Bob", "Brown")
        self.assertEqual(len(db.Clients.clients_list), 4)
        self.assertEqual(new_client.id, "44B")
        self.assertEqual(new_client.name, "Bob")
        self.assertEqual(new_client.last_name, "Brown")

    def test_modify(self):
        client_to_modify = copy.copy(db.Clients.search("11D"))
        modified_client = db.Clients.modify("11D", "Joe", "Cranston")
        self.assertEqual(client_to_modify.name, "John")
        self.assertEqual(modified_client.name, "Joe")

    def test_delete(self):
        deleted_client = db.Clients.delete("11D")
        researched_client = db.Clients.search("11D")
        self.assertNotEqual(deleted_client, researched_client)

    def test_valid_id(self):
        print(f"Validating ID: {'00A'}, Clients List: {[client.id for client in db.Clients.clients_list]}")
        self.assertTrue(helpers.valid_id("00A", db.Clients.clients_list))
        print(f"Validating ID: {'23223S'}, Clients List: {[client.id for client in db.Clients.clients_list]}")
        self.assertFalse(helpers.valid_id("23223S", db.Clients.clients_list))
        print(f"Validating ID: {'F35'}, Clients List: {[client.id for client in db.Clients.clients_list]}")
        self.assertFalse(helpers.valid_id("F35", db.Clients.clients_list))
        
    if __name__ == "__main__":
        unittest.main()

""" 
python -m pytest Gestor/tests/test_database.py
así puedo ejecutar pytest"""

"""
python -m unittest Gestor/tests/test_database.py
así puedo ejecutar unittest"""