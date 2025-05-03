import sys

DATABASE_PATH = "Gestor/clientes.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "Gestor/tests/clients_test.csv"