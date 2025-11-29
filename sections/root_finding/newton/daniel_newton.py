import sympy as sp
import math

def newton(x0, tol, flag, sym_func):
    x = sp.Symbol('x') # make x a symbol
    func = sp.lambdify(x, sym_func)
    funcPrime = sp.lambdify(x, sp.diff(sym_func, x))

    # input validation
    if flag not in [1, 2, 3, 4]:
        raise ValueError("Invalid flag. Expected one of [1, 2, 3, 4].")
    try:
        f0 = func(x0)
        fp0 = funcPrime(x0)
    except Exception:
        raise ValueError("Function evaluation failed at initial x0.")
    if math.isnan(f0) or math.isnan(fp0):
        raise ValueError("Function returned NaN at initial x0.")
    if math.isinf(f0) or math.isinf(fp0):
        raise ValueError("Function returned infinite value at initial x0.")
    
    iter = 0
    while (True):
        if funcPrime(x0) == 0:
            raise ZeroDivisionError("Derivative is zero at x0 — cannot apply Newton-Raphson.")
        if (func(x0) == 0): return x0, iter # check if an exact root was located
        iter += 1
        
        x1 = x0 - func(x0) / funcPrime(x0) # apply the Newton-Raphson formula

        match flag: 
            case 1: # absolute approximate error
                if (abs(x1 - x0) < tol): return x1, iter 
            case 2: # absolute relative approximate error
                if (abs((x1 - x0) / x1) < tol): return x1, iter 
            case 3: # estimation of true absolute error
                if (abs(func(x1)) < tol): return x1, iter 
            case 4: # conjunction of absolute approximate error and estimated true absolute error
                if (abs(func(x1)) < tol and abs(x1 - x0) < tol): return x1, iter
    
        if (iter > 1000): # check if iterations has exceeded a "ridiculous" value (100)
            print("\nIterations have exceeded 1000, terminating Newton function.") 
            return x1, iter
        
        x0 = x1 # set x0 as the new closest root approximation for the next iteration of the while loop
