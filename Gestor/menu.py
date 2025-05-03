import os
import platform
import helpers
import database as db

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

helpers.clear_screen()

def start():
    while True:
        clear_screen()

        print("==========================")
        print("Bienvenid@ al Manager")
        print("==========================")
        print("1. Listar clientes")
        print("2. Buscar cliente")
        print("3. Crear cliente")
        print("4. Modificar cliente")
        print("5. Eliminar cliente")
        print("6. Salir")
        print("==========================")

        option = input("Selecciona una opción: ")
        clear_screen()

        if option not in ["1", "2", "3", "4", "5", "6"]:
            print("Opción no válida. Intenta de nuevo.")
            continue

        if option == "1":
            print("Listando clientes...\n")
            for client in db.Clients.clients_list:
                print(client)
        if option == "2":
            print("Buscando cliente...\n")
            id = helpers.read_text(3, 3, "ID (2 ints and 1 char)").upper()
            client = db.Clients.search(id)
            print(client) if client else print("Cliente no encontrado")
        if option == "3":
            print("Creando cliente...\n")
            while 1:
                id = helpers.read_text(3, 3, "ID (2 ints and 1 char)").upper()
                if helpers.valid_id(id, db.Clients.clients_list):
                    break
            name = helpers.read_text(2, 30, "Nombre (2-30 chars)").capitalize()
            last_name = helpers.read_text(2, 30, "Apellido (2-30 chars)").capitalize()
            db.Clients.create(id, name, last_name)
            print("Cliente creado con éxito")
        if option == "4":
            print("Modificando cliente...\n")
            id = helpers.read_text(3, 3, "ID (2 ints and 1 char)").upper()
            client = db.Clients.search(id)
            if client:
                name = helpers.read_text(2, 30, "Nombre (2-30 chars)").capitalize()
                last_name = helpers.read_text(2, 30, "Apellido (2-30 chars)").capitalize()
                db.Clients.modify(id, name, last_name)
                print("Cliente modificado con éxito")
            else:
                print("Cliente no encontrado")
        if option == "5":
            print("Eliminando cliente...\n")
            id = helpers.read_text(3, 3, "ID (2 ints and 1 char)").upper()
            print("Cliente borrado con éxito") if db.Clients.delete(id) else print("Cliente no encontrado")
        if option == "6":
            print("Saliendo...\n")
            break

        input("\nPresiona Enter para continuar...")