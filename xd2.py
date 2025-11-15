import tkinter as tk
import random
import math

# ===============================
# FUNCIONES PRINCIPALES
# ===============================

def generar_triangulo():
    global a, b, c, A, B, C, modo
    
    canvas.delete("all")
    etiqueta_resultado.config(text="")
    etiqueta_pistas.config(text="")  

    modo = random.choice(["AAS", "SSA"])  

    A = random.uniform(30, 80)
    B = random.uniform(40, 70)
    C = 180 - (A + B)

    if C <= 10:
        return generar_triangulo()

    a = random.uniform(4, 10)
    b = (a * math.sin(math.radians(B))) / math.sin(math.radians(A))
    c = (a * math.sin(math.radians(C))) / math.sin(math.radians(A))

    dibujar_triangulo(a, b, c, A, B, C)

    if modo == "AAS":
        texto = f"MEDIDAS MOSTRADAS (modo AAS):\n  A = {A:.3f}\n  B = {B:.3f}\n  a = {a:.3f}\n\nMEDIDAS A RESOLVER:\n  C\n  b\n  c"
    else:
        texto = f"MEDIDAS MOSTRADAS (modo SSA):\n  a = {a:.3f}\n  b = {b:.3f}\n  A = {A:.3f}\n\nMEDIDAS A RESOLVER:\n  B\n  C\n  c"

    etiqueta_datos.config(text=texto)


def dibujar_triangulo(a, b, c, A, B, C):
    escala = 40
    Ax, Ay = 50, 300
    Bx, By = Ax + c * escala, 300
    Cx = Ax + b * escala * math.cos(math.radians(A))
    Cy = Ay - b * escala * math.sin(math.radians(A))

    canvas.create_polygon(Ax, Ay, Bx, By, Cx, Cy, outline="black", fill="lightblue", width=2)
    canvas.create_text(Ax, Ay + 15, text="A")
    canvas.create_text(Bx, By + 15, text="B")
    canvas.create_text(Cx, Cy - 15, text="C")


# ===============================
# FUNCIONES BOTONES
# ===============================

def mostrar_respuesta():
    texto = (
        f"=== RESPUESTAS ===\n"
        f"  a = {a:.6f}\n"
        f"  b = {b:.6f}\n"
        f"  c = {c:.6f}\n"
        f"  A = {A:.6f}\n"
        f"  B = {B:.6f}\n"
        f"  C = {C:.6f}"
    )
    
    etiqueta_resultado.config(text=texto)


def mostrar_pista():
    pistas = [
        "Pista: Usa la Ley de Senos → a/sin(A) = b/sin(B) = c/sin(C)",
        "Pista: La suma de los ángulos internos siempre es 180°",
        "Pista: Si conoces 2 ángulos, el tercero es 180 - A - B",
        "Pista: Si conoces un lado y su ángulo opuesto, puedes obtener todo",
        "Pista: En triángulos oblicuángulos NO hay pitágoras"
    ]
    
    pista = random.choice(pistas)
    etiqueta_pistas.config(text=pista)


# ===============================
# INTERFAZ
# ===============================

root = tk.Tk()
root.title("Generador de Triángulos — Modo Estudio")

canvas = tk.Canvas(root, width=500, height=350, bg="white")
canvas.pack()

etiqueta_datos = tk.Label(root, text="", font=("Arial", 12), justify="left")
etiqueta_datos.pack()

etiqueta_resultado = tk.Label(root, text="", font=("Arial", 12), fg="green")
etiqueta_resultado.pack()

etiqueta_pistas = tk.Label(root, text="", font=("Arial", 12), fg="blue")
etiqueta_pistas.pack()

frame_botones = tk.Frame(root)
frame_botones.pack(pady=10)

tk.Button(frame_botones, text="Nuevo Triángulo", command=generar_triangulo).grid(row=0, column=0, padx=10)
tk.Button(frame_botones, text="Mostrar Respuesta", command=mostrar_respuesta).grid(row=0, column=1, padx=10)
tk.Button(frame_botones, text="Pista", command=mostrar_pista).grid(row=0, column=2, padx=10)

generar_triangulo()

root.mainloop()
