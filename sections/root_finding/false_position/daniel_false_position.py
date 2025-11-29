import math

def falsePosition(x1, x2, tol, flag, func):
    # input validation
    if not callable(func):
        raise ValueError("func must be a callable function.")
    if x1 == x2:
        raise ValueError("x1 and x2 must be different values.")
    try:
        f1 = func(x1)
        f2 = func(x2)
    except Exception:
        raise ValueError("Function evaluation failed.")
    if math.isnan(f1) or math.isnan(f2):
        raise ValueError("Function returned NaN at one of the initial points.")
    if math.isinf(f1) or math.isinf(f2):
        raise ValueError("Function returned infinite value at one of the initial points.")
    if f1 * f2 >= 0:
        raise ValueError("Invalid interval: f(x1) and f(x2) must have opposite signs.")
    if flag not in [1, 2, 3, 4]:
        raise ValueError("Invalid flag. Expected one of [1, 2, 3, 4].")

    iter = 0
    x = x2 # set x to be used as the previous closest approximation
    while (True):
        iter += 1
        if (iter > 1000): # safety measure to make sure that the while loop doesn't go on forever
            print("\nIterations have exceeded 1000, terminating false position function.")
            return x, iter
        
        x3 = x2 - func(x2) * (x1 - x2) / (func(x1) - func(x2)) # calculate x3 using the false position method's formula
        if (func(x3) == 0): return x3, iter # check if the newest approximation is a root

        if (func(x1) * func(x3) < 0): x2 = x3 # determine which old bracket should be replaced with the newest approximation
        else: x1 = x3

        match flag: 
            case 1: # absolute approximate error
                if (abs(x3 - x) < tol): return x3, iter 
            case 2: # absolute relative approximate error
                if (abs((x3 - x) / x3) < tol): return x3, iter 
            case 3: # estimation of true absolute error
                if (abs(func(x3)) < tol): return x3, iter 
            case 4: # conjunction of absolute approximate error and estimated true absolute error
                if (abs(func(x3)) < tol and abs(x3 - x) < tol): return x3, iter 
        x = x3 # again set x to be used as the previous closest approximation
