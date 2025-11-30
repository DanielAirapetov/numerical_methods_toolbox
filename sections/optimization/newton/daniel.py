import sympy as sp

def newton_method_optimization(x_prev, tol, sym_func):
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