import numpy as np
import sympy as sp


def goldenSectionMethod(a, b, tol, flag, sym_func):

    x = sp.Symbol("x")
    func = sp.lambdify(x, sym_func, "numpy")

    GOLDEN_SECTION = (1 + 5**0.5) / 2
    x1 = b - (b-a) / GOLDEN_SECTION
    x2 = a + (b-a) / GOLDEN_SECTION
    y1 = func(x1)
    y2 = func(x2)
    iter = 0
    while abs(b-a) > tol:
        if iter > 1000:
            print("Iterations have exceeded 1000, terminating function.")
            break
        if flag == 1:
                if y1 >= y2:
                    a = x1
                    x1 = x2
                    x2 = a + (b-a) / GOLDEN_SECTION
                    y1 = y2
                    y2 = func(x2)
                else:
                    b = x2
                    x2 = x1
                    x1 = b - (b-a) / GOLDEN_SECTION
                    y2 = y1
                    y1 = func(x1)
        elif flag == 2:
                if y1 <= y2:
                    a = x1
                    x1 = x2
                    x2 = a + (b-a) / GOLDEN_SECTION
                    y1 = y2
                    y2 = func(x2)
                else:
                    b = x2
                    x2 = x1
                    x1 = b - (b-a) / GOLDEN_SECTION
                    y2 = y1
                    y1 = func(x1)
        iter+=1
    return (a+b)/2, iter


def newtonMinMaxMethod(x_prev, tol, sym_func):
    # Backtracking Line Search 
    def backtracking(f, f_I, f_II, x_0):
        alpha = 1
        c = 10**-4
        f_0 = f(x_0)
        grad = f_I(x_0)
        direction = -1 * grad / f_II(x_0)
        if f_II(x_0) > 0:
            while f(x_0 + alpha * direction) > f_0 + c * alpha * grad * direction:
                alpha /= 2
                if alpha < 10**-6:
                    break
        else:
            while f(x_0 + alpha * direction) < f_0 + c * alpha * grad * direction:
                alpha /= 2
                if alpha < 10**-6:
                    break
        return alpha
    
    x = sp.Symbol('x') # make x a symbol
    sym_func_I = sp.diff(sym_func, x)
    sym_func_II = sp.diff(sym_func_I, x)
    func = sp.lambdify(x, sym_func)
    func_I = sp.lambdify(x, sym_func_I)
    func_II = sp.lambdify(x, sym_func_II)

    iter = 0
    while True:
        if iter > 1000:
            print("Iterations have exceeded 1000, terminating function.")
            break
        if abs(func_II(x_prev)) < 10**-10:
            print("Second derivative is 0, terminating function")
            break
        alpha = backtracking(func, func_I, func_II, x_prev)
        x_next = x_prev - alpha * (func_I(x_prev) / func_II(x_prev))
        if abs(x_next - x_prev) <= tol:
            break
        x_prev = x_next
        iter+=1
    return x_prev, func(x_prev), iter

