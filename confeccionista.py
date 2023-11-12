import subprocess
import tkinter as tk
import sqlite3
from tkinter import messagebox

class Inicio:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Perfil confeccionista")
        self.ventana.geometry("470x300")
        self.ventana.configure(bg="#A58CFA")

        self.font_style_title = ("Arial", 16)
        self.titulo = "¡Bienvenid@ a COLORS!"
        self.etiqueta_titulo = tk.Label(self.ventana, text=self.titulo, font=self.font_style_title, bg="#A58CFA")
        self.etiqueta_titulo.place(relx=0.5, rely=0.09, anchor="center")

        # Crear una conexión a la base de datos
        self.conn = sqlite3.connect('confeccionista.db')
        self.cursor = self.conn.cursor()

        # Crear la tabla de usuarios si no existe
        self.cursor.execute('''CREATE TABLE IF NOT EXISTS confeccionista (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            usuario TEXT,
            contraseña TEXT
        )''')
        self.conn.commit()

        # Crear campos de entrada
        self.entry_usuario = tk.Entry(self.ventana)
        self.entry_password = tk.Entry(self.ventana, show='*')

        self.label_usuario = tk.Label(self.ventana, text="Usuario:")
        self.label_password = tk.Label(self.ventana, text="Contraseña")

        self.label_usuario.grid(row=0, column=0, padx=80, pady=60)
        self.entry_usuario.grid(row=0, column=1, padx=0, pady=60)
        self.label_password.grid(row=1, column=0, padx=80, pady=5)
        self.entry_password.grid(row=1, column=1, padx=0, pady=5)

        self.boton_iniciar = tk.Button(self.ventana, text="Iniciar Sesión", command=self.iniciar_sesion, width=20, height=1)
        self.boton_iniciar.grid(row=5, column=1, padx=6, pady=50)

        # Crear usuarios de coordinador predefinidos al inicio del programa
        self.crear_usuarios_predefinidos()

        self.ventana.mainloop()

    def iniciar_sesion(self):
        usuario = self.entry_usuario.get()
        password = self.entry_password.get()

        if usuario and password:
            self.cursor.execute("SELECT * FROM confeccionista WHERE usuario = ? AND contraseña = ?", (usuario, password))
            if self.cursor.fetchone() is not None:
                try:
                    # Ejecuta "ui_menu.py" en la misma ubicación que este archivo
                    subprocess.Popen(["python", "asignado_confeccionista.py"])
                except FileNotFoundError:
                    print("El archivo del menú no se encuentra.")
            else:
                messagebox.showerror("Error", "Usuario o contraseña incorrectos")
        else:
            messagebox.showerror("Error", "Por favor, ingresa usuario y contraseña.")

    def crear_usuarios_predefinidos(self):
        # Puedes agregar tantos usuarios predefinidos como desees
        usuarios_predefinidos = [
            ("Emily", "12361211")
        ]

        for usuario, contraseña in usuarios_predefinidos:
            try:
                self.cursor.execute("INSERT INTO confeccionista (usuario, contraseña) VALUES (?, ?)", (usuario, contraseña))
                self.conn.commit()
            except sqlite3.IntegrityError:
                # El usuario ya existe, omitirlo
                pass

if __name__ == "__main__":
    app = Inicio()
