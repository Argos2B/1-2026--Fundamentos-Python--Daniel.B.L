#-------------------------------------------------#
#-------Cajero automatico actividad 3 clase 4-----#
import tkinter as tk
from tkinter import messagebox, simpledialog

class CajeroGOKU:
    def __init__(self, ventana):
        self.ventana = ventana
        self.ventana.title("Cajero Automático Futurista")
        self.ventana.geometry("520x620")
        self.ventana.resizable(False, False)

        self.saldo = 1000.00

        self.canvas = tk.Canvas(self.ventana, width=520, height=620, highlightthickness=0)
        self.canvas.pack(fill="both", expand=True)

        self.crear_fondo_futurista()
        self.crear_interfaz()

    def crear_fondo_futurista(self):
        for i in range(620):
            color = f"#{0:02x}{int(10 + i / 8):02x}{int(35 + i / 5):02x}"
            self.canvas.create_line(0, i, 520, i, fill=color)

        for x in range(0, 520, 40):
            self.canvas.create_line(x, 0, x + 160, 620, fill="#00f5ff", width=1)

        for y in range(0, 620, 45):
            self.canvas.create_line(0, y, 520, y + 120, fill="#7d2cff", width=1)

        self.canvas.create_oval(60, 80, 460, 480, outline="#00f5ff", width=2)
        self.canvas.create_oval(100, 120, 420, 440, outline="#7d2cff", width=2)
        self.canvas.create_oval(140, 160, 380, 400, outline="#00ff99", width=1)

    def crear_interfaz(self):
        self.panel = tk.Frame(self.ventana, bg="#07111f", bd=3, relief="ridge")
        self.panel.place(x=80, y=80, width=360, height=460)

        titulo = tk.Label(
            self.panel,
            text="CAJERO AUTOMÁTICO",
            font=("Arial", 19, "bold"),
            bg="#07111f",
            fg="#00f5ff"
        )
        titulo.pack(pady=25)

        self.pantalla = tk.Label(
            self.panel,
            text="Seleccione una opción",
            font=("Arial", 13),
            bg="#020812",
            fg="#00ff99",
            width=30,
            height=4,
            wraplength=290,
            relief="sunken"
        )
        self.pantalla.pack(pady=15)

        self.crear_boton("Consultar saldo", self.consultar_saldo)
        self.crear_boton("Depositar dinero", self.depositar)
        self.crear_boton("Retirar dinero", self.retirar)
        self.crear_boton("Salir", self.salir)

    def crear_boton(self, texto, comando):
        boton = tk.Button(
            self.panel,
            text=texto,
            command=comando,
            font=("Arial", 13, "bold"),
            bg="#00f5ff",
            fg="#020812",
            activebackground="#00ff99",
            activeforeground="#020812",
            width=24,
            height=2,
            bd=0,
            cursor="hand2"
        )
        boton.pack(pady=8)

    def mostrar(self, mensaje):
        self.pantalla.config(text=mensaje)

    def consultar_saldo(self):
        self.mostrar(f"Su saldo actual es: ₡{self.saldo:.2f}")

    def depositar(self):
        cantidad = simpledialog.askfloat("Depósito", "Ingrese la cantidad a depositar:")

        if cantidad is None:
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida.")
        else:
            self.saldo += cantidad
            self.mostrar(f"Depósito exitoso.\nNuevo saldo: ₡{self.saldo:.2f}")

    def retirar(self):
        cantidad = simpledialog.askfloat("Retiro", "Ingrese la cantidad a retirar:")

        if cantidad is None:
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "Debe ingresar una cantidad válida.")
        elif cantidad > self.saldo:
            messagebox.showwarning("Fondos insuficientes", "No tiene saldo suficiente.")
        else:
            self.saldo -= cantidad
            self.mostrar(f"Retiro exitoso.\nNuevo saldo: ₡{self.saldo:.2f}")

    def salir(self):
        respuesta = messagebox.askyesno("Salir", "¿Desea salir del cajero?")
        if respuesta:
            self.ventana.destroy()


ventana = tk.Tk()
app = CajeroGOKU(ventana)
ventana.mainloop() 