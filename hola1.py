import random
import tkinter as tk

# ---------------------------------------------------------
# GENERADOR DE FUNCIONES ALEATORIAS CON *, /
# ---------------------------------------------------------
def generar_funcion():
    a = random.randint(-10, 10)
    b = random.randint(1, 10)
    c = random.randint(-5, 5)
    d = random.randint(1, 5)
    e = random.randint(-15, 15)

    def f(x):
        return (a / b * x * c) / d + e

    formula = f"f(x) = (({a}/{b}) * x * {c}) / {d} + {e}"
    return f, formula


# ---------------------------------------------------------
# GRAFICAR Y EXPORTAR PNG
# ---------------------------------------------------------
def graficar_y_exportar(f, formula):

    root = tk.Tk()
    root.title("Plano generado")

    w = 600
    h = 600
    canvas = tk.Canvas(root, width=w, height=h, bg="white")
    canvas.pack()

    cx = w // 2
    cy = h // 2
    escala = 25

    canvas.create_line(0, cy, w, cy, width=2)
    canvas.create_line(cx, 0, cx, h, width=2)

    for i in range(0, w, escala):
        canvas.create_line(i, cy - 5, i, cy + 5)
    for j in range(0, h, escala):
        canvas.create_line(cx - 5, j, cx + 5, j)

    puntos = []
    for x_pix in range(w):
        x_math = (x_pix - cx) / escala
        y_math = f(x_math)
        y_pix = cy - y_math * escala
        puntos.append((x_pix, y_pix))

    for i in range(len(puntos) - 1):
        canvas.create_line(puntos[i][0], puntos[i][1],
                           puntos[i + 1][0], puntos[i + 1][1],
                           fill="blue")

    canvas.create_text(300, 20, text=formula, fill="black", font=("Arial", 12))

    # -----------------------
    # 5 PUNTOS ALEATORIOS SIN MOSTRAR RESULTADO
    # -----------------------
    xs = [round(random.uniform(2, 7), 1) for _ in range(5)]
    ys = [f(x) for x in xs]   # Se enviarán a web pero NO se muestran

    # Dibujar puntos rojos en el plano
    for x_val in xs:
        y_val = f(x_val)
        x_pix = cx + x_val * escala
        y_pix = cy - y_val * escala
        r = 4
        canvas.create_oval(x_pix-r, y_pix-r, x_pix+r, y_pix+r, fill="red")

    # -----------------------
    # EXPORTAR PNG
    # -----------------------
    canvas.postscript(file="plano.ps", colormode="color")

    try:
        from PIL import Image
        img = Image.open("plano.ps")
        img.save("plano.png")
        print("\nImagen exportada como plano.png")
    except:
        print("\nNecesitas instalar pillow con: pip install pillow")

    root.mainloop()

    return xs, ys, "plano.png"
    

# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
f, formula = generar_funcion()
xs, ys, imagen = graficar_y_exportar(f, formula)

# Datos para web
print("\nValores generados (SOLO X visibles en web):")
print(xs)

print("\nResultados ocultos (para botón PISTA):")
print(ys)

print("\nImagen para web:")
print(imagen)
