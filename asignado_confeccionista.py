import tkinter as tk
import sqlite3
from tkinter import messagebox


class VentanaAsignadoConfeccionista(tk.Tk):
    def __init__(self, confeccionista_id):
        super().__init__()

        self.title("Tareas Asignadas")
        self.geometry("400x300")

        self.confeccionista_id = confeccionista_id

        self.conn = sqlite3.connect('confeccionista.db')
        self.cursor = self.conn.cursor()

        self.label_titulo = tk.Label(self, text="Tareas Asignadas", font=("Arial", 16))
        self.label_titulo.pack(pady=10)

        self.listbox_tareas = tk.Listbox(self, selectmode=tk.SINGLE)
        self.listbox_tareas.pack(pady=40)

        self.cargar_tareas_asignadas()

        self.listbox_tareas.bind('<<ListboxSelect>>', self.mostrar_detalles)

    def cargar_tareas_asignadas(self):
        self.cursor.execute("SELECT id, tarea, descripcion FROM tareas WHERE confeccionista_id = ?", (self.confeccionista_id,))
        tareas = self.cursor.fetchall()

        for tarea in tareas:
            tarea_str = f"Asignación {tarea[0]}: {tarea[1]}"
            self.listbox_tareas.insert(tk.END, tarea_str)

    def mostrar_detalles(self, event):
        seleccion = self.listbox_tareas.curselection()
        if seleccion:
            tarea_id = seleccion[0] + 1  # Ajustar según la indexación de la base de datos
            detalles = self.obtener_detalles_tarea(tarea_id)

            # Crear una nueva ventana para mostrar los detalles y los botones Aceptar y Denegar
            ventana_detalles = tk.Toplevel(self)
            ventana_detalles.title(f"Detalles de Asignación {tarea_id}")
            ventana_detalles.resizable(0,0)

            label_detalles = tk.Label(ventana_detalles, text=detalles, font=("Arial", 12))
            label_detalles.pack(pady=40)

            btn_aceptar = tk.Button(ventana_detalles, text="Aceptar", command=lambda: self.accion_tarea(tarea_id, "Aceptar"))
            btn_aceptar.pack(pady=5)

            btn_denegar = tk.Button(ventana_detalles, text="Denegar", command=lambda: self.accion_tarea(tarea_id, "Denegar"))
            btn_denegar.pack(pady=6)

    def accion_tarea(self, tarea_id, accion):
        # Aquí puedes realizar la lógica correspondiente, por ejemplo, actualizar el estado en la base de datos
        if accion == "Aceptar":
            messagebox.showinfo("Acción", f"Tarea {tarea_id} aceptada con éxito.")
        elif accion == "Denegar":
            messagebox.showinfo("Acción", f"Tarea {tarea_id} denegada con éxito.")
        else:
            messagebox.showinfo("Acción", "Acción no reconocida.")

    def obtener_detalles_tarea(self, tarea_id):
        self.cursor.execute("SELECT tarea, descripcion FROM tareas WHERE id = ?", (tarea_id,))
        tarea = self.cursor.fetchone()
        if tarea:
            return f"Tarea: {tarea[0]}\nDescripción: {tarea[1]}"
        else:
            return "Detalles no encontrados"


confeccionista_actual = {"id": 1, "nombre": "Emily"}  # Cambia esto con la estructura real de tu confeccionista


def obtener_confeccionista_id():
    return confeccionista_actual["id"]

# Este fragmento debería estar en tu script donde se inicia la aplicación
if __name__ == "__main__":
    # Obtén el ID del confeccionista, por ejemplo, de algún lugar en tu aplicación
    confeccionista_id = obtener_confeccionista_id()

    app = VentanaAsignadoConfeccionista(confeccionista_id)
    app.mainloop()
