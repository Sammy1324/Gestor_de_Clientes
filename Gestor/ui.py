from tkinter import *
from tkinter import ttk
from tkinter.messagebox import askokcancel, WARNING, showerror
import database as db
import helpers

class centreWidgetMixin:
    def centre(self):
        self.update()
        w = self.winfo_width()
        h = self.winfo_height()
        ws = self.winfo_screenwidth()
        hs = self.winfo_screenheight()
        x = int((ws/2) - (w/2))
        y = int((hs/2) - (h/2))
        self.geometry(f"{w}x{h}+{x}+{y}")

class MainWindow(Tk, centreWidgetMixin):
    def __init__(self):
        super().__init__()
        self.title('Gestor de clientes')
        self.build()
        self.centre()
        self.load_clients()  # Cargar los clientes al iniciar
    
    def build(self):
        # Frame superior
        frame = Frame(self)
        frame.pack(padx=20, pady=10)

        # Etiquetas
        Label(frame, text="ID (2 ints y 1 char)").grid(row=0, column=0)
        Label(frame, text="Nombre (2 a 30 chars)").grid(row=0, column=1)
        Label(frame, text="Apellido (2 a 30 chars)").grid(row=0, column=2)

        # Campos de entrada
        self.id_entry = Entry(frame)
        self.id_entry.grid(row=1, column=0)
        self.name_entry = Entry(frame)
        self.name_entry.grid(row=1, column=1)
        self.last_name_entry = Entry(frame)
        self.last_name_entry.grid(row=1, column=2)

        # Frame para el Treeview
        frame_treeview = Frame(self)
        frame_treeview.pack(pady=10)

        # Treeview
        self.treeview = ttk.Treeview(frame_treeview)
        self.treeview['columns'] = ('DNI', 'Nombre', 'Apellido')

        # Columnas
        self.treeview.column("#0", width=0, stretch=NO)
        self.treeview.column("DNI", anchor=CENTER)
        self.treeview.column("Nombre", anchor=CENTER)
        self.treeview.column("Apellido", anchor=CENTER)

        # Encabezados
        self.treeview.heading("DNI", text="DNI", anchor=CENTER)
        self.treeview.heading("Nombre", text="Nombre", anchor=CENTER)
        self.treeview.heading("Apellido", text="Apellido", anchor=CENTER)

        # Scrollbar
        scrollbar = Scrollbar(frame_treeview)
        scrollbar.pack(side=RIGHT, fill=Y)
        self.treeview.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.treeview.yview)
        self.treeview.pack()

        # Frame inferior para los botones
        frame_buttons = Frame(self)
        frame_buttons.pack(pady=10)

        # Botones
        Button(frame_buttons, text="Crear", command=self.create).grid(row=0, column=0, padx=5)
        Button(frame_buttons, text="Modificar", command=self.modify).grid(row=0, column=1, padx=5)
        Button(frame_buttons, text="Borrar", command=self.delete).grid(row=0, column=2, padx=5)
    
    def create(self):
        try:
            # Obtén los valores de los campos de entrada
            id = helpers.read_text_tk(self.id_entry, 3, 3).upper()
            name = helpers.read_text_tk(self.name_entry, 2, 30).capitalize()
            last_name = helpers.read_text_tk(self.last_name_entry, 2, 30).capitalize()

            # Crear el cliente
            db.Clients.create(id, name, last_name)

            # Agregar al Treeview
            self.treeview.insert(
                parent='', index='end', iid=id,
                values=(id, name, last_name)
            )
        except ValueError as e:
            showerror("Error", str(e))
    
    def modify(self):
        # Obtener el cliente seleccionado
        selected_item = self.treeview.focus()
        if not selected_item:
            showerror("Error", "Por favor, selecciona un cliente para modificar.")
            return

        # Obtener los valores actuales del cliente
        current_values = self.treeview.item(selected_item, "values")
        if not current_values:
            showerror("Error", "No se pudo obtener la información del cliente.")
            return

        # Crear una subventana para modificar los datos
        modify_window = Toplevel(self)
        modify_window.title("Modificar cliente")
        modify_window.geometry("400x200")
        modify_window.transient(self)
        modify_window.grab_set()

        # Etiquetas y campos de entrada
        Label(modify_window, text="ID (no editable)").grid(row=0, column=0, padx=10, pady=10)
        Label(modify_window, text="Nombre").grid(row=1, column=0, padx=10, pady=10)
        Label(modify_window, text="Apellido").grid(row=2, column=0, padx=10, pady=10)

        id_entry = Entry(modify_window)
        id_entry.grid(row=0, column=1, padx=10, pady=10)
        id_entry.insert(0, current_values[0])
        id_entry.config(state="disabled")  # El ID no se puede modificar

        name_entry = Entry(modify_window)
        name_entry.grid(row=1, column=1, padx=10, pady=10)
        name_entry.insert(0, current_values[1])

        last_name_entry = Entry(modify_window)
        last_name_entry.grid(row=2, column=1, padx=10, pady=10)
        last_name_entry.insert(0, current_values[2])

        # Función para guardar los cambios
        def save_changes():
            new_name = name_entry.get().strip()
            new_last_name = last_name_entry.get().strip()

            if len(new_name) < 2 or len(new_name) > 30:
                showerror("Error", "El nombre debe tener entre 2 y 30 caracteres.")
                return
            if len(new_last_name) < 2 or len(new_last_name) > 30:
                showerror("Error", "El apellido debe tener entre 2 y 30 caracteres.")
                return

            # Actualizar los datos en la Treeview
            self.treeview.item(selected_item, values=(current_values[0], new_name, new_last_name))

            # Actualizar los datos en la base de datos
            db.Clients.modify(current_values[0], new_name, new_last_name)

            # Cerrar la subventana
            modify_window.destroy()

        # Botones
        Button(modify_window, text="Guardar", command=save_changes).grid(row=3, column=0, padx=10, pady=10)
        Button(modify_window, text="Cancelar", command=modify_window.destroy).grid(row=3, column=1, padx=10, pady=10)

    def delete(self):
        client = self.treeview.focus()
        if client:
            campos = self.treeview.item(client, 'values')
            if askokcancel(
                title='Confirmar borrado',
                message=f'¿Borrar a {campos[1]} {campos[2]}?',
                icon=WARNING
            ):
                self.treeview.delete(client)
                db.Clients.delete(campos[0])

    def load_clients(self):
        """
        Carga los clientes desde la base de datos al Treeview.
        """
        for client in db.Clients.clients_list:
            self.treeview.insert(
                parent='', index='end', iid=client.id,
                values=(client.id, client.name, client.last_name)
            )