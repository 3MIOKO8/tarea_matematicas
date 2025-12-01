"""
Generador de triángulos aleatorios para practicar trigonometría.
Interfaz con tkinter que dibuja el triángulo y muestra solo algunas medidas.
Botones: Nuevo triángulo, Mostrar solución, Pista, Tipo, Modo.
"""

import tkinter as tk
from tkinter import ttk
import random, math

# --------------------------
# Utilidades matemáticas
# --------------------------
def law_of_cosines_angle(a, b, c):
    den = 2*a*b
    if den == 0:
        return None
    val = max(-1.0, min(1.0, (a*a + b*b - c*c) / den))
    return math.degrees(math.acos(val))

# --------------------------
# Generador de triángulos
# --------------------------
def generar_triangulo(tipo="aleatorio", scale=1.0):
    def random_angles_for(tipo):
        if tipo == "rectangulo":
            A = random.uniform(20,70)
            B = 90.0
            C = 90.0 - A
        elif tipo == "agudo":
            A = random.uniform(20,70)
            B = random.uniform(20, 80)
            C = 180 - A - B
            if C <= 0 or C >= 90:
                return None
        elif tipo == "obtuso":
            A = random.uniform(91,140)
            B = random.uniform(10, 60)
            C = 180 - A - B
            if C <= 0:
                return None
        else:
            A = random.uniform(20, 100)
            B = random.uniform(20, 120)
            C = 180 - A - B
            if C <= 5:
                return None
        return A, B, C

    angles = None
    for _ in range(30):
        angles = random_angles_for(tipo)
        if angles:
            break
    if not angles:
        angles = (50.0, 60.0, 70.0)
    A, B, C = angles

    a = random.uniform(4, 12) * scale
    sinA = math.sin(math.radians(A))
    if sinA == 0:
        return generar_triangulo(tipo, scale)
    k = a / sinA
    b = k * math.sin(math.radians(B))
    c = k * math.sin(math.radians(C))

    return {
        "a": round(a, 6),
        "b": round(b, 6),
        "c": round(c, 6),
        "A": round(A, 6),
        "B": round(B, 6),
        "C": round(C, 6)
    }

# --------------------------
# Modos y selección de medidas
# --------------------------
MODOS = [
    "2 lados (SAS) — oculto el resto",
    "2 lados + 1 ángulo (ASA/AAS)",
    "1 lado + 2 ángulos (AAS)",
    "3 lados (SSS)",
    "mostrar todo"
]

def seleccionar_medidas(tri, modo_index):
    keys = ['a','b','c','A','B','C']
    known = {}
    unknown = []

    if modo_index == 0:
        known['a'] = tri['a']
        known['b'] = tri['b']
        unknown = ['c','A','B','C']
    elif modo_index == 1:
        known['a'] = tri['a']
        known['b'] = tri['b']
        known['A'] = tri['A']
        unknown = ['c','B','C']
    elif modo_index == 2:
        known['a'] = tri['a']
        known['B'] = tri['B']
        known['C'] = tri['C']
        unknown = ['b','c','A']
    elif modo_index == 3:
        known['a'] = tri['a']
        known['b'] = tri['b']
        known['c'] = tri['c']
        unknown = ['A','B','C']
    else:
        for k in keys:
            known[k] = tri[k]
        unknown = []

    return known, unknown

# --------------------------
# Interfaz Tkinter
# --------------------------
class TriangulosApp:
    def __init__(self, master):
        self.master = master
        master.title("Triángulos - Sistema de estudio")
        self.canvas_w = 520
        self.canvas_h = 420

        self.tipo = tk.StringVar(value="aleatorio")
        self.modo_index = tk.IntVar(value=1)
        self.tri = generar_triangulo(self.tipo.get())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.show_solution = False
        self.show_hints = False

        self.inputs = {}

        control_frame = ttk.Frame(master, padding=8)
        control_frame.pack(side="top", fill="x")

        ttk.Label(control_frame, text="Tipo:").grid(row=0,column=0,sticky="w")
        tipo_menu = ttk.Combobox(control_frame,
                                 values=["aleatorio","rectangulo","agudo","obtuso"],
                                 textvariable=self.tipo, state="readonly", width=12)
        tipo_menu.grid(row=0,column=1, padx=4)
        tipo_menu.bind("<<ComboboxSelected>>", lambda e: self.nuevo_triangulo())

        ttk.Label(control_frame, text="Modo:").grid(row=0,column=2, sticky="w", padx=(10,0))
        self.modo_menu = ttk.Combobox(control_frame, values=MODOS, state="readonly", width=48)
        self.modo_menu.grid(row=0,column=3, columnspan=2, sticky="w", padx=4)
        self.modo_menu.current(self.modo_index.get())
        self.modo_menu.bind("<<ComboboxSelected>>", self.modo_changed)

        ttk.Button(control_frame, text="Nuevo triángulo", command=self.nuevo_triangulo).grid(row=1,column=0, pady=6)
        ttk.Button(control_frame, text="Mostrar solución", command=self.toggle_solution).grid(row=1,column=1, pady=6)
        ttk.Button(control_frame, text="Pista", command=self.mostrar_pista).grid(row=1,column=2, pady=6)

        self.canvas = tk.Canvas(master, width=self.canvas_w, height=self.canvas_h, bg="white")
        self.canvas.pack(padx=8, pady=8)

        self.inputs_frame = ttk.Frame(master, padding=6)
        self.inputs_frame.pack()

        ttk.Button(self.inputs_frame, text="Verificar respuestas",
                   command=self.verificar_respuestas).pack(pady=6)

        self.info = tk.Text(master, height=10, width=80)
        self.info.pack(padx=8, pady=(0,8))
        self.info.configure(state='disabled')

        self.draw()

    # --------------------------
    # Crear entradas
    # --------------------------
    def crear_inputs(self):
        for widget in self.inputs_frame.winfo_children():
            if isinstance(widget, ttk.Entry) or isinstance(widget, ttk.Label):
                widget.destroy()

        self.inputs.clear()

        if not self.unknown:
            ttk.Label(self.inputs_frame, text="No hay valores ocultos.").pack()
            return

        for k in self.unknown:
            ttk.Label(self.inputs_frame, text=f"{k} =").pack(anchor="w")
            e = ttk.Entry(self.inputs_frame, width=20)
            e.pack(anchor="w", pady=2)
            self.inputs[k] = e

    # --------------------------
    # Verificar respuestas
    # --------------------------
    def verificar_respuestas(self):
        if not self.unknown:
            return

        self.info.configure(state="normal")
        self.info.insert(tk.END, "\n=== RESULTADOS ===\n")

        correctos = 0
        total = len(self.unknown)

        for k in self.unknown:
            entrada = self.inputs[k].get().strip()
            if entrada == "":
                self.info.insert(tk.END, f"{k}: ❌ No ingresado\n")
                continue

            try:
                val = float(entrada)
            except:
                self.info.insert(tk.END, f"{k}: ❌ No es un número válido\n")
                self.inputs[k].config(fg="red")
                continue

            real = self.tri[k]

            if abs(val - real) < 0.1:
                self.info.insert(tk.END, f"{k}: ✔ Correcto ({val})\n")
                self.inputs[k].config(fg="green")
                correctos += 1
            else:
                self.info.insert(tk.END, f"{k}: ❌ Incorrecto — el valor correcto es {real}\n")
                self.inputs[k].config(fg="red")

        if correctos == total:
            self.info.insert(tk.END, "\n🎉 ¡Perfecto! Todas las respuestas son correctas.\n")

        self.info.configure(state='disabled')
        self.info.see(tk.END)


    # ----------------------
    # Eventos
    # ----------------------
    def modo_changed(self, event=None):
        self.modo_index.set(self.modo_menu.current())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.draw()

    def nuevo_triangulo(self):
        self.tri = generar_triangulo(self.tipo.get())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.draw()

    def toggle_solution(self):
        self.show_solution = True
        self.show_hints = False
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())

        self.info.configure(state="normal")
        self.info.delete("1.0", tk.END)

        self.info.insert(tk.END, "\n=== SOLUCIÓN COMPLETA ===\n")
        for k in ['A','B','C','a','b','c']:
            self.info.insert(tk.END, f"{k} = {self.tri[k]}\n")

        self.info.configure(state="disabled")

    def mostrar_pista(self):
        pistas = []

        datos = ", ".join(sorted(self.known.keys()))
        pistas.append(f"Datos revelados: {datos if datos else 'ninguno'}.")

        idx = self.modo_index.get()
        if idx == 0:
            pistas.append("Estrategia: 2 lados → Ley de Cosenos.")
        elif idx == 1:
            pistas.append("Estrategia: 2 lados + 1 ángulo → Ley de Senos / Cosenos.")
        elif idx == 2:
            pistas.append("Estrategia: 1 lado + 2 ángulos → Ley de Senos.")
        elif idx == 3:
            pistas.append("Estrategia: 3 lados → Ley de Cosenos.")

        self.info.configure(state="normal")
        self.info.insert(tk.END, "\n--- PISTA ---\n")
        for p in pistas:
            self.info.insert(tk.END, p + "\n")
        self.info.configure(state="disabled")

    # ----------------------
    # Dibujar
    # ----------------------
    def draw(self):
        self.canvas.delete("all")
        self._draw_triangle()
        self._draw_labels()
        self._update_info_panel()
        self.crear_inputs()

    def _draw_triangle(self):
        a = float(self.tri['a'])
        b = float(self.tri['b'])
        c = float(self.tri['c'])

        margin = 40
        max_side = max(a, b, c)
        escala = min((self.canvas_w - 2*margin) / max_side,
                     (self.canvas_h - 2*margin) / max_side) * 0.9

        a_len = a * escala
        b_len = b * escala
        c_len = c * escala

        Bx = (self.canvas_w - a_len) / 2
        By = self.canvas_h - margin
        Cx = Bx + a_len
        Cy = By

        d = a_len
        x_proj = (c_len*c_len - b_len*b_len + d*d) / (2*d)
        tmp = c_len*c_len - x_proj*x_proj
        if tmp < 0:
            tmp = 0
        y_alt = math.sqrt(tmp)

        Ax = Bx + x_proj
        Ay = By - y_alt

        self.pts = {'A': (Ax, Ay), 'B': (Bx, By), 'C': (Cx, Cy)}

        self.canvas.create_polygon(
            Bx, By, Cx, Cy, Ax, Ay,
            fill="#f0f7ff", outline="black", width=2
        )

    def _draw_labels(self):
        for label, (x, y) in self.pts.items():
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")
            self.canvas.create_text(x+12, y-8, text=label, font=("Arial", 12, "bold"))

        def midpoint(p1, p2):
            return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

        side_points = {
            'a': ('B','C'),
            'b': ('A','C'),
            'c': ('A','B')
        }

        for side in ['a','b','c']:
            p1 = self.pts[side_points[side][0]]
            p2 = self.pts[side_points[side][1]]
            mx, my = midpoint(p1, p2)
            txt = f"{side} = {self.known[side]:.3f}" if side in self.known else f"{side} = ?"
            self.canvas.create_text(mx, my - 12, text=txt, font=("Arial", 10, "italic"))

        for ang in ['A','B','C']:
            x, y = self.pts[ang]
            txt = f"{ang} = {self.known[ang]:.2f}°" if ang in self.known else f"{ang} = ?"
            self.canvas.create_text(x - 15, y - 20, text=txt, font=("Arial", 9))

    def _update_info_panel(self):
        self.info.configure(state='normal')
        self.info.delete("1.0", tk.END)

        self.info.insert(tk.END, "MEDIDAS MOSTRADAS (según modo):\n")
        for k, v in self.known.items():
            self.info.insert(tk.END, f"  {k} = {v}\n")

        self.info.insert(tk.END, "\nMEDIDAS OCULTAS:\n")

        # ========= NUEVO SISTEMA DE INPUTS DENTRO DEL PANEL ==========
        self.inputs.clear()

        for k in self.unknown:
            self.info.insert(tk.END, f"  {k} = ")

            e = tk.Entry(self.info, width=12, font=("Consolas", 11))
            self.info.window_create(tk.END, window=e)
            self.inputs[k] = e

            self.info.insert(tk.END, "\n")
        # =============================================================

        if self.show_hints:
            self.info.insert(tk.END, "\n(Pista activa)\n")

        self.info.configure(state='disabled')


# --------------------------
# Ejecutar app
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriangulosApp(root)
    root.mainloop()
