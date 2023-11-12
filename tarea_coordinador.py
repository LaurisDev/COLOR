import tkinter as tk
from tkinter import ttk
import sqlite3
from tkinter import messagebox

class AsignarTareaApp:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.geometry("400x250")
        self.ventana.title("Asignar Tarea")

        self.conn = sqlite3.connect('confeccionista.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla de tareas si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tareas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                tarea TEXT,
                descripcion TEXT,
                confeccionista_id INTEGER,
                FOREIGN KEY (confeccionista_id) REFERENCES confeccionista(id)
            )
        ''')
        self.conn.commit()

        # Crear la tabla de confeccionistas si no existe
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS confeccionista (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                usuario TEXT UNIQUE,
                contraseña TEXT
            )
        ''')
        self.conn.commit()

        self.label_confeccionista = tk.Label(self.ventana, text="Confeccionista:")
        self.label_confeccionista.grid(row=0, column=0, padx=10, pady=10)

        self.combobox_confeccionista = ttk.Combobox(self.ventana, state="readonly")
        self.combobox_confeccionista.grid(row=0, column=1, padx=10, pady=10)

        self.label_tarea = tk.Label(self.ventana, text="Tarea:")
        self.label_tarea.grid(row=1, column=0, padx=10, pady=10)

        self.entry_tarea = tk.Entry(self.ventana)
        self.entry_tarea.grid(row=1, column=1, padx=10, pady=10)

        self.label_descripcion = tk.Label(self.ventana, text="Descripción:")
        self.label_descripcion.grid(row=2, column=0, padx=10, pady=10)

        self.entry_descripcion = tk.Entry(self.ventana)
        self.entry_descripcion.grid(row=2, column=1, padx=10, pady=10)

        self.boton_asignar_tarea = tk.Button(self.ventana, text="Asignar Tarea", command=self.asignar_tarea)
        self.boton_asignar_tarea.grid(row=3, column=0, columnspan=2, pady=10)

        # Llenar la lista desplegable con los nombres de confeccionistas
        self.cargar_confeccionistas()

        self.ventana.mainloop()

    def cargar_confeccionistas(self):
        self.cursor.execute("SELECT usuario FROM confeccionista")
        confeccionistas = self.cursor.fetchall()
        confeccionistas = [confeccionista[0] for confeccionista in confeccionistas]
        self.combobox_confeccionista['values'] = confeccionistas

    def asignar_tarea(self):
        confeccionista_seleccionado = self.combobox_confeccionista.get()
        tarea = self.entry_tarea.get()
        descripcion = self.entry_descripcion.get()

        if confeccionista_seleccionado and tarea:
            try:
                # Intentar insertar el confeccionista (evitar duplicados)
                self.cursor.execute("INSERT OR IGNORE INTO confeccionista (usuario) VALUES (?)", (confeccionista_seleccionado,))
                self.conn.commit()

                # Obtener el id del confeccionista seleccionado
                self.cursor.execute("SELECT id FROM confeccionista WHERE usuario = ?", (confeccionista_seleccionado,))
                confeccionista_id = self.cursor.fetchone()[0]

                # Insertar tarea en la tabla de tareas
                self.cursor.execute("INSERT INTO tareas (tarea, descripcion, confeccionista_id) VALUES (?, ?, ?)",
                                    (tarea, descripcion, confeccionista_id))
                self.conn.commit()
                messagebox.showinfo("Tarea Asignada", f"Tarea asignada a {confeccionista_seleccionado}")
            except Exception as e:
                print(f"Error: {str(e)}")
                messagebox.showerror("Error", f"No se pudo asignar la tarea. Detalles: {str(e)}")
        else:
            messagebox.showerror("Error", "Por favor, selecciona un confeccionista y proporciona una tarea.")

if __name__ == "__main__":
    app = AsignarTareaApp()

