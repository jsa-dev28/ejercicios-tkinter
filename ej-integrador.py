import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class SistemaInventario(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.pack(fill="both", expand=True, padx=10, pady=10)

        self.datos = self.cargar_datos()
        self._construir_interfaz()
        self._refrescar_tabla()

    def cargar_datos(self):
        if os.path.exists("inventario.json"):
            with open("inventario.json", "r") as f:
                return json.load(f)
        return []

    def guardar_datos(self):
        with open("inventario.json", "w") as f:
            json.dump(self.datos, f, indent=2, ensure_ascii=False)
    
    def _construir_interfaz(self):
        self.frame_form = ttk.LabelFrame(self, text="Panel de operaciones")
        self.frame_form.grid(row=0, column=0, sticky="nsew", padx=(0,8), pady=0)

        self.frame_tabla = ttk.LabelFrame(self, text="Inventario")
        self.frame_tabla.grid(row=0, column=1, sticky="nsew")

        self.columnconfigure(1, weight=1)
        self.rowconfigure(0, weight=1)

        self._construir_formulario()
        self._construir_tabla()

    def _construir_formulario(self):
        f = self.frame_form

        self.var_codigo = tk.StringVar()
        self.var_nombre = tk.StringVar()
        self.var_precio = tk.StringVar()
        self.var_categoria = tk.StringVar()
        self.var_cantidad = tk.IntVar(value=0)

        campos = [
            ("Código:", self.var_codigo),
            ("Descripción:", self.var_nombre),
            ("Precio $:", self.var_precio),
            ("Categoría:", self.var_categoria),
        ]

        for i, (etiqueta, variable) in enumerate(campos):
            ttk.Label(f, text=etiqueta).grid(row=i, column=0, sticky="w", padx=8, pady=4)
            ttk.Entry(f, textvariable=variable, width=22).grid(row=i, column=1, padx=8, pady=4)

        ttk.Label(f, text="Cantidad:").grid(row=4, column=0, sticky="w", padx=8, pady=4)
        ttk.Spinbox(f, from_=0, to=9999, textvariable=self.var_cantidad, width=21).grid(
            row=4, column=1, padx=8, pady=4)

        ttk.Button(f, text="Guardar", command=self._guardar).grid(row=5, column=0, columnspan=2, pady=(16,4), sticky="ew", padx=8)
        ttk.Button(f, text="Modificar", command=self._modificar).grid(row=6, column=0, columnspan=2, pady=4, sticky="ew", padx=8)
        ttk.Button(f, text="Borrar", command=self._borrar).grid(row=7, column=0, columnspan=2, pady=4, sticky="ew", padx=8)
        ttk.Button(f, text="Limpiar", command=self._limpiar_form).grid(row=8, column=0, columnspan=2, pady=4, sticky="ew", padx=8)

    def _construir_tabla(self):
        f = self.frame_tabla

        columnas = ("codigo", "nombre", "precio", "categoria", "cantidad")
        self.tree = ttk.Treeview(f, columns=columnas, show="headings")

        self.tree.heading("codigo", text="Código")
        self.tree.heading("nombre", text="Descripción")
        self.tree.heading("precio", text="Precio $")
        self.tree.heading("categoria", text="Categoría")
        self.tree.heading("cantidad", text="Cantidad")

        self.tree.column("codigo", width=70,  anchor="center")
        self.tree.column("nombre", width=200)
        self.tree.column("precio", width=80,  anchor="e")
        self.tree.column("categoria", width=100, anchor="center")
        self.tree.column("cantidad", width=70,  anchor="center")

        scroll = ttk.Scrollbar(f, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scroll.set)

        self.tree.grid(row=0, column=0, sticky="nsew")
        scroll.grid(row=0, column=1, sticky="ns")

        f.columnconfigure(0, weight=1)
        f.rowconfigure(0, weight=1)

        self.tree.bind("<ButtonRelease-1>", self._seleccionar_fila)

    def _refrescar_tabla(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        for p in self.datos:
            self.tree.insert("", tk.END, values=(
                p["codigo"], p["nombre"], p["precio"],
                p["categoria"], p["cantidad"]
            ))

    def _guardar(self):
        codigo = self.var_codigo.get().strip()
        nombre = self.var_nombre.get().strip()
        precio = self.var_precio.get().strip()
        cat = self.var_categoria.get().strip()
        cant = self.var_cantidad.get()

        if not codigo or not nombre or not precio or not cat:
            messagebox.showwarning("Atención", "Completá todos los campos.")
            return

        if any(p["codigo"] == codigo for p in self.datos):
            messagebox.showerror("Error", f"El código '{codigo}' ya existe.")
            return

        try:
            precio_float = float(precio)
        except ValueError:
            messagebox.showerror("Error", "El precio debe ser un número.")
            return

        nuevo = {
            "codigo": codigo, "nombre": nombre,
            "precio": precio_float, "categoria": cat, "cantidad": cant
        }
        self.datos.append(nuevo)
        self.guardar_datos()
        self._refrescar_tabla()
        self._limpiar_form()

    def _seleccionar_fila(self, evento):
        seleccion = self.tree.selection()
        if not seleccion:
            return
        valores = self.tree.item(seleccion[0])["values"]
        self.var_codigo.set(valores[0])
        self.var_nombre.set(valores[1])
        self.var_precio.set(valores[2])
        self.var_categoria.set(valores[3])
        self.var_cantidad.set(valores[4])

    def _modificar(self):
        codigo = self.var_codigo.get().strip()
        for p in self.datos:
            if p["codigo"] == codigo:
                p["nombre"] = self.var_nombre.get().strip()
                p["precio"] = float(self.var_precio.get())
                p["categoria"] = self.var_categoria.get().strip()
                p["cantidad"] = self.var_cantidad.get()
                break
        else:
            messagebox.showerror("Error", "Código no encontrado.")
            return
        self.guardar_datos()
        self._refrescar_tabla()
        self._limpiar_form()

    def _borrar(self):
        codigo = self.var_codigo.get().strip()
        if not codigo:
            messagebox.showwarning("Atención", "Seleccioná un producto primero.")
            return
        confirmar = messagebox.askyesno("Confirmar", f"¿Borrar el producto '{codigo}'?")
        if not confirmar:
            return
        for i in range(len(self.datos)):
            if self.datos[i]["codigo"] == codigo:
                del self.datos[i]
                break
        self.guardar_datos()
        self._refrescar_tabla()
        self._limpiar_form()

    def _limpiar_form(self):
        self.var_codigo.set("")
        self.var_nombre.set("")
        self.var_precio.set("")
        self.var_categoria.set("")
        self.var_cantidad.set(0)

if __name__ == "__main__":
    root = tk.Tk()
    root.title("Sistema de Inventario")
    root.geometry("900x550")
    app = SistemaInventario(root)
    root.mainloop()