"""
triangulos_estudio.py
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

        self.info = tk.Text(master, height=10, width=80)
        self.info.pack(padx=8, pady=(0,8))
        self.info.configure(state='disabled')

        self.draw()

    # ----------------------
    # Eventos/acciones
    # ----------------------
    def modo_changed(self, event=None):
        idx = self.modo_menu.current()
        if idx >= 0:
            self.modo_index.set(idx)
            self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
            self.draw()

    def nuevo_triangulo(self):
        self.tri = generar_triangulo(self.tipo.get())
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.show_solution = False
        self.show_hints = False
        self.modo_menu.current(self.modo_index.get())
        self.draw()

    def toggle_solution(self):
        self.show_solution = True
        self.show_hints = False

        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())

        self.info.configure(state='normal')
        self.info.delete("1.0", tk.END)

        self.info.insert(tk.END, "MEDIDAS MOSTRADAS (según modo):\n")
        for k, v in self.known.items():
            self.info.insert(tk.END, f"  {k} = {v}\n")

        self.info.insert(tk.END, "\nMEDIDAS OCULTAS (resolver):\n")
        for k in self.unknown:
            self.info.insert(tk.END, f"  {k}\n")

        self.info.insert(tk.END, "\n=== SOLUCIÓN ===\n")
        self.info.insert(tk.END, f"  A (arriba) = {self.tri['A']}°\n")
        self.info.insert(tk.END, f"  B (izquierda) = {self.tri['B']}°\n")
        self.info.insert(tk.END, f"  C (derecha) = {self.tri['C']}°\n")
        self.info.insert(tk.END, f"  a (opuesto a A) = {self.tri['a']}\n")
        self.info.insert(tk.END, f"  b (opuesto a B) = {self.tri['b']}\n")
        self.info.insert(tk.END, f"  c (opuesto a C) = {self.tri['c']}\n")

        self.info.configure(state='disabled')
        self.info.see(tk.END)


    def toggle_hint(self):
        self.show_hints = not self.show_hints
        if self.show_hints:
            self.show_solution = False
        self.known, self.unknown = seleccionar_medidas(self.tri, self.modo_index.get())
        self.draw()

    def mostrar_pista(self):
        pistas = []

        datos = ", ".join(sorted(self.known.keys()))
        pistas.append(f"Datos revelados: {datos if datos else 'ninguno'}.")

        idx = self.modo_index.get()
        if idx == 0:
            pistas.append("Estrategia: tienes 2 lados (a y b). Usa Ley de Cosenos.")
        elif idx == 1:
            pistas.append("Estrategia: 2 lados + 1 ángulo. Ley de Cosenos o Ley de Senos según corresponda.")
        elif idx == 2:
            pistas.append("Estrategia: 1 lado + 2 ángulos. Saca el ángulo faltante y usa Ley de Senos.")
        elif idx == 3:
            pistas.append("Estrategia: con 3 lados usa Ley de Cosenos.")
        else:
            pistas.append("Modo mostrar todo.")

        if 'a' in self.known and 'A' in self.known:
            pistas.append(f"Tip: a = {self.known['a']:.3f}, A = {self.known['A']:.2f}°. Usa a/sin(A) = b/sin(B).")

        self.info.configure(state='normal')
        self.info.insert(tk.END, "\n--- PISTA ---\n")
        for p in pistas:
            self.info.insert(tk.END, p + "\n")
        self.info.configure(state='disabled')
        self.info.see(tk.END)

    # ----------------------
    # Dibujado
    # ----------------------
    def draw(self):
        self.canvas.delete("all")
        self._draw_triangle()
        self._draw_labels()
        self._update_info_panel()

    def _draw_triangle(self):

        # lados (según tu convención: a = BC, b = AC, c = AB)
        a = float(self.tri['a'])  # BC
        b = float(self.tri['b'])  # AC
        c = float(self.tri['c'])  # AB

        margin = 40
        max_side = max(a, b, c)
        if max_side == 0:
            escala = 1.0
        else:
            escala = min((self.canvas_w - 2*margin) / max_side,
                        (self.canvas_h - 2*margin) / max_side) * 0.9

        # Longitudes escaladas
        a_len = a * escala   # distancia BC en píxeles
        b_len = b * escala   # distancia AC en píxeles (radio desde C hasta A)
        c_len = c * escala   # distancia AB en píxeles (radio desde B hasta A)

        # Colocamos la base BC horizontal, centrada hacia abajo
        Bx = (self.canvas_w - a_len) / 2
        By = self.canvas_h - margin
        Cx = Bx + a_len
        Cy = By

        # proteger contra a_len == 0
        d = a_len if a_len != 0 else 1e-6

        # Intersección de círculos centrados en B y C con radios c_len y b_len
        # x_proj = distancia desde B a la proyección de A sobre BC (en el eje BC)
        x_proj = (c_len*c_len - b_len*b_len + d*d) / (2*d)

        tmp = c_len*c_len - x_proj*x_proj
        if tmp < 0:
            # ajuste numérico (evita NaN)
            tmp = 0.0
        y_alt = math.sqrt(tmp)

        # Coordenadas de A (colocamos A hacia arriba de la base)
        Ax = Bx + x_proj
        Ay = By - y_alt

        # fallback si sale infinito/NaN
        if not (math.isfinite(Ax) and math.isfinite(Ay)):
            Ax = Bx + d/2
            Ay = By - max(40, max(b_len, c_len)/2)

        # guardar puntos (consistentes con labels: A arriba, B izquierda, C derecha)
        self.pts = {'A': (Ax, Ay), 'B': (Bx, By), 'C': (Cx, Cy)}

        # dibujar triángulo
        self.canvas.create_polygon(
            self.pts['B'][0], self.pts['B'][1],
            self.pts['C'][0], self.pts['C'][1],
            self.pts['A'][0], self.pts['A'][1],
            fill="#f0f7ff", outline="black", width=2
        )



    def _draw_labels(self):
        for label, (x, y) in self.pts.items():
            self.canvas.create_oval(x-4, y-4, x+4, y+4, fill="black")
            tx = x + 12 if x + 60 < self.canvas_w else x - 12
            ty = y - 8 if y - 20 > 0 else y + 12
            self.canvas.create_text(tx, ty, text=label, font=("Arial", 12, "bold"))

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
            ty = my - 10 if my > 20 else my + 10
            self.canvas.create_text(mx, ty, text=txt, font=("Arial", 10, "italic"))

        for ang in ['A','B','C']:
            x, y = self.pts[ang]
            txt = f"{ang} = {self.known[ang]:.2f}°" if ang in self.known else f"{ang} = ?"
            tx = x - 15 if x > 30 else x + 15
            ty = y - 20 if y > 30 else y + 15
            self.canvas.create_text(tx, ty, text=txt, font=("Arial", 9))

    def _update_info_panel(self):
        self.info.configure(state='normal')
        self.info.delete("1.0", tk.END)

        self.info.insert(tk.END, "MEDIDAS MOSTRADAS (según modo):\n")
        for k, v in self.known.items():
            self.info.insert(tk.END, f"  {k} = {v}\n")

        self.info.insert(tk.END, "\nMEDIDAS OCULTAS (resolver):\n")
        for k in self.unknown:
            self.info.insert(tk.END, f"  {k}\n")

        # if self.show_solution:
        #     self.info.insert(tk.END, "\n=== SOLUCIÓN ===\n")
        #     for key in ['A','B','C','a','b','c']:
        #         self.info.insert(tk.END, f"  {key} = {self.tri[key]}\n")

        if self.show_hints:
            self.info.insert(tk.END, "\n=== PISTA (automática) ===\n")
            self.info.insert(tk.END, "Presiona 'Pista' para más detalles.\n")

        self.info.configure(state='disabled')

# --------------------------
# Ejecutar app
# --------------------------
if __name__ == "__main__":
    root = tk.Tk()
    app = TriangulosApp(root)
    root.mainloop()
