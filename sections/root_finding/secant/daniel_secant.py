import math

def secant(x1, x2, tol, flag, func):
    # input validation
    if (abs(func(x1)) < abs(func(x2))): x1, x2 = x2, x1 # if f(x1) has a smaller magnitude than f(x2), swap them to maintain consitency
    if not callable(func):
        raise ValueError("func must be a callable function.")
    if x1 == x2:
        raise ValueError("x1 and x2 cannot be equal.")
    try:
        f1 = func(x1)
        f2 = func(x2)
    except Exception:
        raise ValueError("Function evaluation failed.")
    if math.isnan(f1) or math.isnan(f2):
        raise ValueError("Function returned NaN at one of the initial points.")
    if math.isinf(f1) or math.isinf(f2):
        raise ValueError("Function returned infinite value at one of the initial points.")
    if f2 == f1:
        raise ZeroDivisionError("Denominator is zero — secant method cannot proceed.")
    if flag not in [1, 2, 3, 4]:
        raise ValueError("Invalid flag. Expected one of [1, 2, 3, 4].")
    iter = 0
    while (True):
        iter += 1
        if (iter > 1000): # safety measure to make sure that the while loop doesn't go on forever
            print("\nIterations have exceeded 1000, terminating secant function.")
            return x2, iter
        
        x3 = x2 - func(x2) * (x1 - x2) / (func(x1) - func(x2)) # calculate x3 using the secant method's formula
        x1, x2 = x2, x3 # swap x1 with x2 and x2 with x3 to enable future iterations
        if (func(x2) == 0): return x2, iter # check if the newest approximation is a root

        match flag: 
            case 1: # absolute approximate error
                if (abs(x2 - x1) < tol): return x2, iter 
            case 2: # absolute relative approximate error
                if (abs((x2 - x1) / x2) < tol): return x2, iter 
            case 3: # estimation of true absolute error
                if (abs(func(x2)) < tol): return x2, iter 
            case 4: # conjunction of absolute approximate error and estimated true absolute error
                if (abs(func(x2)) < tol and abs(x2 - x1) < tol): return x2, iter 
