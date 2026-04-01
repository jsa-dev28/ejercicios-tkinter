import tkinter as tk
from tkinter import ttk
import math

class Calculadora(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(expand=True, fill="both")
        self.expresion = ""
        self.var_pantalla = tk.StringVar()
        self.construir_pantalla()
        self.construir_botones()

    def construir_pantalla(self):
        frame_pantalla = ttk.Frame(self, padding=10)
        frame_pantalla.pack(fill="x")
        pantalla = ttk.Entry(
            frame_pantalla,
            textvariable=self.var_pantalla,
            font=("Arial", 24),
            justify="right",
            state="readonly"
        )
        pantalla.pack(fill="x", ipady=10)

    def construir_botones(self):
        frame_botones = ttk.Frame(self, padding=10)
        frame_botones.pack(expand=True, fill="both")
        botones = [
            ["C",  "√",  "**", "/"],
            ["7",  "8",  "9",  "*"],
            ["4",  "5",  "6",  "-"],
            ["1",  "2",  "3",  "+"],
            ["0",  ".",  "⌫",  "="],
        ]
        for i, fila in enumerate(botones):
            for j, simbolo in enumerate(fila):
                boton = ttk.Button(
                    frame_botones,
                    text=simbolo,
                    command=self.command(simbolo)
                )
                boton.grid(row=i, column=j, sticky="nsew", padx=4, pady=4)

        for i in range(5):
            frame_botones.rowconfigure(i, weight=1)
        for j in range(4):
            frame_botones.columnconfigure(j, weight=1)

    def command(self, simbolo):
        return lambda: self.presionar(simbolo)

    def presionar(self, simbolo):
        if simbolo == "C":
            self.expresion = ""
            self.var_pantalla.set("")
        elif simbolo == "⌫":
            self.expresion = self.expresion[:-1]
            self.var_pantalla.set(self.expresion)
        elif simbolo == "=":
            self.calcular()
        elif simbolo == "√":
            self.calcular_raiz()
        else:
            self.expresion += simbolo
            self.var_pantalla.set(self.expresion)

    def calcular(self):
        try:
            resultado = eval(self.expresion)
            self.expresion = str(resultado)
            self.var_pantalla.set(self.expresion)
        except ZeroDivisionError:
            self.var_pantalla.set("Error: div/0")
            self.expresion = ""
        except Exception:
            self.var_pantalla.set("Error")
            self.expresion = ""

    def calcular_raiz(self):
        try:
            numero = float(self.expresion)
            if numero < 0:
                raise ValueError
            resultado = math.sqrt(numero)
            self.expresion = str(resultado)
            self.var_pantalla.set(self.expresion)
        except (ValueError, Exception):
            self.var_pantalla.set("Error")
            self.expresion = ""

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Calculadora")
    root.geometry("320x420")
    root.resizable(True, True)
    app = Calculadora(root)
    root.mainloop()