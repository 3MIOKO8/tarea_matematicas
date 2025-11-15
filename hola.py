"""
triangulos_estudio.py
Generador de triángulos aleatorios para practicar trigonometría.
Interfaz con tkinter que dibuja el triángulo y muestra solo algunas medidas.
Botones: Nuevo triángulo, Mostrar solución, Cambiar modo (qué se revela), Tipo de triángulo.
"""

import tkinter as tk
from tkinter import ttk, messagebox
import random, math

# --------------------------
# Utilidades matemáticas
# --------------------------
def law_of_cosines_side(a, b, C_deg):
    C = math.radians(C_deg)
    return math.sqrt(a*a + b*b - 2*a*b*math.cos(C))

def law_of_cosines_angle(a, b, c):
    # devuelve ángulo opuesto a c en grados
    # cos(C) = (a^2 + b^2 - c^2) / (2ab)
    num = a*a + b*b - c*c
    den = 2*a*b
    if den == 0:
        return None
    val = max(-1, min(1, num/den))
    return math.degrees(math.acos(val))

def law_of_sines_angle(a, A_deg, b):
    # A en grados, devuelve B en grados usando a/sinA = b/sinB
    A = math.radians(A_deg)
    if math.sin(A) == 0:
        return None
    ratio = b * math.sin(A) / a
    if ratio <= -1 or ratio >= 1:
        # posible ambigüedad o no existe
        ratio = max(-1, min(1, ratio))
    return math.degrees(math.asin(ratio))

# --------------------------
# Generador de triángulos
# --------------------------
def generar_triangulo(tipo="aleatorio", scale=1.0):
    """
    Genera triángulo con lados a, b, c (en unidades)
    y ángulos A, B, C (en grados), donde:
      - a está opuesto a A, b opuesto a B, c opuesto a C
    'tipo' puede ser: "aleatorio", "rectangulo", "agudo", "obtuso".
    """
    # generamos ángulos primero para asegurar sumen 180
    if tipo == "rectangulo":
        # forzar uno en 90
        A = random.uniform(20,70)
        B = 90.0
        C = 90.0 - A
    elif tipo == "agudo":
        # todos < 90
        A = random.uniform(20,70)
        B = random.uniform(20, 89 - A/2)
        C = 180 - A - B
        # ajustar si C>=90
        if C >= 90:
            B = random.uniform(20, 60)
            C = 180 - A - B
    elif tipo == "obtuso":
        # uno > 90
        A = random.uniform(91, 140)
        B = random.uniform(10, 70)
        C = 180 - A - B
        if C <= 0:
            # fallback
            return generar_triangulo("aleatorio", scale)
    else:
        # aleatorio válido
        A = random.uniform(20, 100)
        B = random.uniform(20, 120)
        C = 180 - A - B
        if C <= 5:
            return generar_triangulo(tipo, scale)

    # Escoger una escala/base para los lados: elegimos a (lado opuesto A) al azar
    a = random.uniform(4, 12) * scale
    # usar ley de senos para obtener b y c: a/sin(A) = b/sin(B) = c/sin(C)
    sinA = math.sin(math.radians(A))
    if sinA == 0:
        return generar_triangulo(tipo, scale)
    k = a / sinA
    b = k * math.sin(math.radians(B))
    c = k * math.sin(math.radians(C))

    # redondear valores para presentar
    tri = {
        "a": round(a, 3),
        "b": round(b, 3),
        "c": round(c, 3),
        "A": round(A, 6),
        "B": round(B, 6),
        "C": round(C, 6)
    }
    return tri

# --------------------------
# Lógica para decidir qué mostrar (modos)
# --------------------------
MODOS = [
    "2 lados (SAS) + ángulo incluido oculto (pide hallar otro ángulo/lado)",
    "2 lados + 1 ángulo (ASA o AAS)",
    "1 lado + 2 ángulos (resuelve por ley de senos)",
    "3 lados (SSS) — comprobar cálculos",
    "mostrar todo (práctica rápida)"
]

def seleccionar_medidas(tri, modo_index):
    """
    Dado tri dict y un modo, devuelve:
      known: dict de medidas que se muestran
      unknown: lista de claves que quedan ocultas
    Claves: 'a','b','c','A','B','C'
    """
    keys = ['a','b','c','A','B','C']
    known = {}
    unknown = []

    modo = MODOS[modo_index]

    if modo_index == 0:
        # Mostrar a y b, ocultar c y sus ángulos (SAS común)
        known['a'] = tri['a']
        known['b'] = tri['b']
        # mostrar (opcional) ángulo A o B aleatorio? dejaremos ambos ocultos
        unknown = ['c','A','B','C']
    elif modo_index == 1:
        # 2 lados + 1 ángulo: mostrar a,b y A
        known['a'] = tri['a']
        known['b'] = tri['b']
        known['A'] = tri['A']
        unknown = ['c','B','C']
    elif modo_index == 2:
        # 1 lado + 2 ángulos: mostrar a, B, C
        known['a'] = tri['a']
        known['B'] = tri['B']
        known['C'] = tri['C']
        unknown = ['b','c','A']
    elif modo_index == 3:
        # 3 lados (SSS)
        known['a'] = tri['a']
        known['b'] = tri['b']
        known['c'] = tri['c']
        unknown = ['A','B','C']
    else:
        # mostrar todo
        for k in keys:
            known[k] = tri[k]
        unknown = []

    return known, unknown

# --------------------------
# Tkinter GUI
# --------------------------
class TriangulosApp:
    def __init__(self, master):
        self.master = master
        master.title("Triángulos - Sistema de estudio")
        self.canvas_w = 520
        self.canvas_h = 420

        # estado
        self.tipo = tk.StringVar(value="aleatorio")
        self.modo_index = tk.IntVar(value=1)
        self.tri = generar_triangulo(self.tipo.get())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.show_solution = False
        self.show_hints = False

        # UI
        control_frame = ttk.Frame(master, padding=8)
        control_frame.pack(side="top", fill="x")

        ttk.Label(control_frame, text="Tipo:").grid(row=0,column=0,sticky="w")
        tipo_menu = ttk.Combobox(control_frame, values=["aleatorio","rectangulo","agudo","obtuso"], textvariable=self.tipo, state="readonly", width=10)
        tipo_menu.grid(row=0,column=1, padx=4)
        tipo_menu.bind("<<ComboboxSelected>>", lambda e: self.nuevo_triangulo())

        ttk.Label(control_frame, text="Modo:").grid(row=0,column=2, sticky="w", padx=(10,0))
        modo_menu = ttk.Combobox(control_frame, values=MODOS, state="readonly", width=48)
        modo_menu.current(self.modo_index.get())
        modo_menu.grid(row=0,column=3, columnspan=2, sticky="w", padx=4)
        def modo_changed(event):
            idx = modo_menu.current()
            self.modo_index.set(idx)
            self.nuevo_triangulo()
        modo_menu.bind("<<ComboboxSelected>>", modo_changed)

        ttk.Button(control_frame, text="Nuevo triángulo", command=self.nuevo_triangulo).grid(row=1,column=0, pady=6)
        ttk.Button(control_frame, text="Mostrar solución", command=self.toggle_solution).grid(row=1,column=1, pady=6)
        ttk.Button(control_frame, text="Pista", command=self.toggle_hint).grid(row=1,column=2, pady=6)

        # Canvas
        self.canvas = tk.Canvas(master, width=self.canvas_w, height=self.canvas_h, bg="white")
        self.canvas.pack(padx=8, pady=8)

        # Área info textual a la derecha/abajo
        self.info = tk.Text(master, height=8, width=80)
        self.info.pack(padx=8, pady=(0,8))
        self.info.configure(state='disabled')

        self.draw()

    def nuevo_triangulo(self):
        self.tri = generar_triangulo(self.tipo.get())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.show_solution = False
        self.show_hints = False
        self.draw()

    def toggle_solution(self):
        self.show_solution = not self.show_solution
        if self.show_solution:
            self.show_hints = False
        self.draw()


    def toggle_hint(self):
        self.show_hints = not self.show_hints
        if self.show_hints:
            self.show_solution = False
        self.draw()

    def draw(self):
        self.canvas.delete("all")
        a = self.tri['a']
        b = self.tri['b']
        c = self.tri['c']

        # --- Escalado del triángulo ---
        margin = 40
        max_side = max(a, b, c)
        escala = min((self.canvas_w - 2*margin) / max_side,
                    (self.canvas_h - 2*margin) / max_side) * 0.9

        # --- Vértices B y C ---
        Bx = margin
        By = self.canvas_h - margin

        Cx = Bx + c * escala
        Cy = By

        # --- Cálculo del vértice A con intersección de círculos ---
        d = c * escala  # distancia BC

        # proyección sobre BC
        x_proj = (b*b*escala*escala - a*a*escala*escala + d*d) / (2*d)
        # altura sobre BC
        y_alt = math.sqrt(max(b*b*escala*escala - x_proj*x_proj, 0))

        Ax = Bx + x_proj
        Ay = By - y_alt

        pts = {'A': (Ax, Ay), 'B': (Bx, By), 'C': (Cx, Cy)}

        # Dibujar triángulo
        self.canvas.create_polygon(
            Bx, By, Cx, Cy, Ax, Ay,
            fill="#f0f3ff",
            outline="black",
            width=2
        )

        # Dibujar puntos
        for label, (x, y) in pts.items():
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")
            self.canvas.create_text(x+12, y-8, text=label, font=("Arial", 12, "bold"))

        # Dibujar lados
        def midpoint(p1, p2):
            return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

        side_points = {
            'a': ('B', 'C'),
            'b': ('A', 'C'),
            'c': ('A', 'B')
        }

        for side in ['a','b','c']:
            p1 = pts[side_points[side][0]]
            p2 = pts[side_points[side][1]]
            mx, my = midpoint(p1, p2)

            if side in self.known:
                txt = f"{side} = {self.known[side]:.2f}"
            else:
                txt = f"{side} = ?"

            self.canvas.create_text(mx, my-10, text=txt, font=("Arial", 10, "italic"))

        # Dibujar ángulos
        for ang in ['A','B','C']:
            x, y = pts[ang]
            if ang in self.known:
                txt = f"{ang} = {self.known[ang]:.2f}°"
            else:
                txt = f"{ang} = ?"
            self.canvas.create_text(x-15, y-20, text=txt, font=("Arial", 9))

        # Panel info
        self.info.configure(state='normal')
        self.info.delete("1.0", tk.END)

        self.info.insert(tk.END, "MEDIDAS MOSTRADAS:\n")
        for k, v in self.known.items():
            self.info.insert(tk.END, f"  {k} = {v}\n")

        self.info.insert(tk.END, "\nOCULTAS (resolver):\n")
        for k in self.unknown:
            self.info.insert(tk.END, f"  {k}\n")

        # Solución
        if self.show_solution:
            self.info.insert(tk.END, "\n=== SOLUCIÓN ===\n")
            for k in ['a','b','c','A','B','C']:
                self.info.insert(tk.END, f"  {k} = {self.tri[k]}\n")

        # Pista
        elif self.show_hints:
            self.info.insert(tk.END, "\n=== PISTA ===\n")
            idx = self.modo_index.get()

            if idx == 0:
                self.info.insert(tk.END, "Modo SAS: usa ley de cosenos.\n")
            elif idx == 1:
                self.info.insert(tk.END, "2 lados + 1 ángulo: usa ley de senos o cosenos.\n")
            elif idx == 2:
                self.info.insert(tk.END, "1 lado + 2 ángulos: suma=180°, luego ley de senos.\n")
            elif idx == 3:
                self.info.insert(tk.END, "3 lados: aplica ley de cosenos.\n")
            else:
                self.info.insert(tk.END, "Modo completo.\n")

        self.info.configure(state='disabled')

    

# --------------------------
# Ejecutar app
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriangulosApp(root)
    root.mainloop()
