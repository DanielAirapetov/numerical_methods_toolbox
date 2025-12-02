import numpy as np
import sympy as sp


x = sp.Symbol('x')

def goldenSectionMethod(a, b, delta, flag, f):

    phi = (1 + np.sqrt(5)) / 2
    error = float('inf')
    iterations = 0
    max_iter = 1000

    x1 = b - ((b - a) / phi)
    x2 = a + ((b - a) / phi)

    while error > delta and iterations < max_iter:

        if flag == 1:
            if f.subs(x, x1) >= f.subs(x, x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        elif flag == 2:
            if f.subs(x, x1) <= f.subs(x, x2):
                a = x1
                x1 = x2
                x2 = a + ((b - a) / phi)
            else:
                b = x2
                x2 = x1
                x1 = b - ((b - a) / phi)

        error = np.abs(b - a)
        iterations += 1

    return ((a + b) / 2), iterations


def newtonMinMaxMethod(x0, f, delta):

    iterations = 0
    max_iter = 1000
    error = float('inf')

    f_first = sp.diff(f, x)
    f_second = sp.diff(f_first, x)

    alpha = 1

    while error > delta and iterations < max_iter:

        x_next = x0 - (alpha * (f_first.subs(x, x0) / f_second.subs(x, x0)))
        error = np.abs(x_next - x0)
        x0 = x_next
        iterations += 1

    return x_next, iterations


