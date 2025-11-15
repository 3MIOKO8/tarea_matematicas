import random
import tkinter as tk

# ---------------------------------------------------------
# GENERAR FUNCIÓN PERO CON X FIJA ENTRE 2 Y 7 (1 decimal)
# ---------------------------------------------------------
def generar_funcion():
    # coeficientes
    a = random.randint(-10, 10)
    b = random.randint(1, 10)
    c = random.randint(-5, 5)
    d = random.randint(1, 5)
    e = random.randint(-15, 15)

    # X aleatoria con 1 decimal
    x_random = round(random.uniform(2, 7), 1)

    # f(x_random) únicamente
    def f():
        return (a / b * x_random * c) / d + e

    formula = f"f({x_random}) = (({a}/{b}) * {x_random} * {c}) / {d} + {e}"
    return f, formula, x_random


# ---------------------------------------------------------
# MOSTRAR SOLO EL VALOR GENERADO
# ---------------------------------------------------------
def mostrar_funcion(formula, resultado):
    print("\nFunción generada:")
    print(formula)
    print(f"Resultado numérico: {round(resultado, 3)}\n")


# ---------------------------------------------------------
# MAIN
# ---------------------------------------------------------
f, formula, x_random = generar_funcion()
resultado = f()
mostrar_funcion(formula, resultado)
