import sys

DATABASE_PATH = "clients.csv"

if "pytest" in sys.argv[0]:
    DATABASE_PATH = "Gestor/tests/clients_test.csv"