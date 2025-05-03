import sys
import menu
import ui
import database as db  

if __name__ == "__main__":
    # Cargar clientes al iniciar
    db.Clients.load()
    
    # Si pasamos un argumento -t lanzamos el modo terminal
    if len(sys.argv) > 1 and sys.argv[1] == "-t":
        menu.start()
    # En cualquier otro caso lanzamos el modo gráfico
    else:
        app = ui.MainWindow()
        app.mainloop()