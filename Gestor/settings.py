import sys

DATABASE_PATH = "Gestor/clients.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "Gestor/tests/clients_test.csv"