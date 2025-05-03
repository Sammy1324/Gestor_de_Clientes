import os
import platform
import re

def clear_screen():
    os.system("cls" if platform.system() == "Windows" else "clear")

def read_text(min_lenght=0, max_lenght=100, message=None):
    print(message) if message else None

    while True:
        text = input("> ")
        if len(text) >= min_lenght and len(text) <= max_lenght:
            return text
        
def valid_id(id, clients_list):
    if not re.match("^[0-9]{2}[A-Z]$", id.strip()):
        print("ID no válido")
        return False
    for client in clients_list:
        if client.id == id:
            print("ID ya existe")
            return False
    return True