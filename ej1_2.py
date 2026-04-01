import tkinter as tk

class AlineacionFutbol(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, width=600, height=770)
        self.pack_propagate(False)  # el Frame mantiene su tamaño fijo
        self.pack()
        self.drag_idx = None
        self._construir_cancha()
        self._cargar_jugadores()
        self._enlazar_eventos()

    def _construir_cancha(self):
        try:
            self.img_cancha = tk.PhotoImage(file="assets/cancha.png")
            
            # Un Canvas del tamaño de la ventana reemplaza al Label de fondo
            self.canvas = tk.Canvas(self, width=600, height=770, highlightthickness=0)
            self.canvas.place(x=0, y=0)
            
            # Dibujamos la cancha como fondo del canvas
            self.canvas.create_image(0, 0, image=self.img_cancha, anchor="nw")
        except Exception as e:
            print("Error al cargar imagen de la cancha:", e)

    def _cargar_jugadores(self):
        try:
            nombres = ["arquero","def1","def2","def3","def4",
                    "med1","med2","med3","del1","del2","del3"]
            posiciones = [
                (290,700),(80,540),(190,580),(370,580),(500,540),
                (130,390),(300,300),(460,390),(90,180),(300,100),(490,180)
            ]
            self.imagenes = []
            self.ids_canvas = []  # guardamos los IDs que devuelve el canvas

            for i, nombre in enumerate(nombres):
                img = tk.PhotoImage(file=f"assets/{nombre}.png")
                self.imagenes.append(img)
                
                x, y = posiciones[i]
                # create_image dibuja la imagen respetando la transparencia
                id_item = self.canvas.create_image(x, y, image=img, anchor="center")
                self.ids_canvas.append(id_item)
        except Exception as e:
            print("Error al cargar imágenes:", e)

    def _enlazar_eventos(self):
        for i, id_item in enumerate(self.ids_canvas):
            self.canvas.tag_bind(id_item, "<ButtonPress-1>",
                                lambda e, idx=i: self._inicio_drag(e, idx))
            self.canvas.tag_bind(id_item, "<B1-Motion>",
                                lambda e, idx=i: self._durante_drag(e, idx))
            self.canvas.tag_bind(id_item, "<ButtonRelease-1>",
                                lambda e, idx=i: self._fin_drag(e, idx))

    def _inicio_drag(self, event, idx):
        self.drag_idx = idx

    def _durante_drag(self, event, idx):
        # movemos el item del canvas directamente a la posición del mouse
        self.canvas.coords(self.ids_canvas[idx], event.x, event.y)

    def _fin_drag(self, event, idx):
        x_s, y_s = event.x, event.y

        for i, id_item in enumerate(self.ids_canvas):
            if i == idx:
                continue
            # coords() devuelve la posición actual del item
            x_o, y_o = self.canvas.coords(id_item)
            if ((x_s - x_o)**2 + (y_s - y_o)**2)**0.5 < 60:
                # intercambiamos: el arrastrado va donde estaba el otro
                self.canvas.coords(self.ids_canvas[idx], x_o, y_o)
                self.canvas.coords(self.ids_canvas[i], x_s, y_s)
                return
root = tk.Tk()
root.title("Alineación táctica")
root.geometry("600x770")
root.resizable(False, False)
AlineacionFutbol(root)
root.mainloop()