import settings
import csv
import unittest

class Client:
    def __init__(self, id, name, last_name):
        self.id = id
        self.name = name
        self.last_name = last_name

    def __str__(self):
        return f"({self.id}) {self.name} {self.last_name}"
    
class Clients:
    clients_list = []
    
    try:
        with open(settings.DATABASE_PATH, newline="\n") as file:
            reader = csv.reader(file, delimiter=";")
            for id, name, last_name in reader:
                client = Client(id, name, last_name)
                clients_list.append(client)
    except FileNotFoundError:
        print(f"El archivo {settings.DATABASE_PATH} no existe. Se creará uno nuevo al guardar.")
    except Exception as e:
        print(f"Error al leer el archivo: {e}")

    def search(id):
        for client in Clients.clients_list:
            if client.id == id:
                return client
    @staticmethod
    def load():
        try:
            with open(settings.DATABASE_PATH, newline="\n") as file:
                reader = csv.reader(file, delimiter=";")
                Clients.clients_list = [
                    Client(id, name, last_name) for id, name, last_name in reader
                ]
        except FileNotFoundError:
            print(f"El archivo {settings.DATABASE_PATH} no existe. Se creará uno nuevo al guardar.")
        except Exception as e:
            print(f"Error al cargar el archivo: {e}")
    @staticmethod
    def create(id, name, last_name):
        # Verificar si el cliente ya existe
        if any(client.id == id for client in Clients.clients_list):
            raise ValueError(f"El cliente con ID {id} ya existe.")
        
        client = Client(id, name, last_name)
        Clients.clients_list.append(client)
        Clients.save()  # Guardar automáticamente
        return client
    
    @staticmethod
    def modify(id, name, last_name):
        for i, client in enumerate(Clients.clients_list):
            if client.id == id:
                Clients.clients_list[i].name = name
                Clients.clients_list[i].last_name = last_name
                Clients.save()  # Guardar automáticamente
                return Clients.clients_list[i]
            
    @classmethod
    def delete(cls, id):
        client_to_delete = cls.search(id)
        if client_to_delete:
            cls.clients_list.remove(client_to_delete)
            cls.save()  # Guardar automáticamente
            return client_to_delete
        return None
    
    @staticmethod
    def save():
        try:
            with open(settings.DATABASE_PATH, "w", newline="\n") as file:
                writer = csv.writer(file, delimiter=";")
                for client in Clients.clients_list:
                    writer.writerow([client.id, client.name, client.last_name])
        except Exception as e:
            print(f"Error al guardar el archivo: {e}")

class TestClients(unittest.TestCase):
    def test_save(self):
        Clients.create("55C", "Charlie", "Chaplin")
        Clients.save()
        with open(settings.DATABASE_PATH, newline="\n") as file:
            reader = csv.reader(file, delimiter=";")
            clients = list(reader)
        self.assertIn(["55C", "Charlie", "Chaplin"], clients)