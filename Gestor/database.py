import settings
import csv

class Client:
    def __init__(self, id, name, last_name):
        self.id = id
        self.name = name
        self.last_name = last_name

    def __str__(self):
        return f"({self.id}) {self.name} {self.last_name}"
    
class Clients:
    clients_list = []

    with open(settings.DATABASE_PATH, newline="\n") as file:
        reader = csv.reader(file, delimiter=";")
        for id, name, last_name in reader:
            client = Client(id, name, last_name)
            clients_list.append(client)

    def search(id):
        for client in Clients.clients_list:
            if client.id == id:
                return client

    @staticmethod
    def create(id, name, last_name):
        client = Client(id, name, last_name)
        Clients.clients_list.append(client)
        return client
    
    @staticmethod
    def modify(id, name, last_name):
        for i, client in enumerate(Clients.clients_list):
            if client.id == id:
                Clients.clients_list[i].name = name
                Clients.clients_list[i].last_name = last_name
                return Clients.clients_list[i]
            
    @classmethod
    def delete(cls, id):
        client_to_delete = cls.search(id)
        if client_to_delete:
            cls.clients_list.remove(client_to_delete)
            return client_to_delete
        return None
    
    @staticmethod
    def save():
        with open("settings.DATABASE_PATH", "w", newline="\n") as file:
            writer = csv.writer(file, delimiter=";")
            for client in Clients.clients_list:
                writer.writerow([client.id, client.name, client.last_name])