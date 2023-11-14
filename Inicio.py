import tkinter as tk
import subprocess

class MenuPrincipal:
    def __init__(self):
        self.ventana = tk.Tk()
        self.ventana.title("Menú Principal")
        self.ventana.geometry("300x200")
        self.ventana.config(bg="#C48C8D")

        self.font_style_title = ("Arial", 16)
        self.titulo = "¡COLORS!"
        self.etiqueta_titulo = tk.Label(self.ventana, text=self.titulo, font=self.font_style_title, bg="#C48C8D")
        self.etiqueta_titulo.place(relx=0.5, rely=0.09, anchor="center")

        # Botón para Coordinador
        btn_coordinador = tk.Button(self.ventana, text="Coordinador", command=self.abrir_coordinador)
        btn_coordinador.pack(pady=40)

        # Botón para Confeccionista
        btn_confeccionista = tk.Button(self.ventana, text="Confeccionista", command=self.abrir_confeccionista)
        btn_confeccionista.pack(pady=20)

        self.ventana.mainloop()

    def abrir_coordinador(self):
        try:
            subprocess.Popen(["python", "coordinador.py"])
        except FileNotFoundError:
            print("El archivo ui_coordinador.py no se encuentra.")

    def abrir_confeccionista(self):
        try:
            subprocess.Popen(["python", "confeccionista.py"])
        except FileNotFoundError:
            print("El archivo ui_confeccionista.py no se encuentra.")
if __name__ == "__main__":
    app = MenuPrincipal()