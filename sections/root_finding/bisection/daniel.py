import math

def bisection(x1, x2, tol, flag, func):
    # input validation
    if x1 > x2:
        x1, x2 = x2, x1
    if not callable(func):
        raise ValueError("func must be a callable function.")
    if func(x1) * func(x2) >= 0:
        raise ValueError("Invalid interval: f(x1) and f(x2) must have opposite signs.")
    if math.isnan(func(x1)) or math.isnan(func(x2)):
        raise ValueError("Function returned NaN at one of the endpoints.")
    if math.isinf(func(x1)) or math.isinf(func(x2)):
        raise ValueError("Function returned infinite value at one of the endpoints.")
    if flag not in [1, 2, 3, 4]:
        raise ValueError("Invalid flag. Expected one of [1, 2, 3, 4].")

    iter = 0 # define an iteration variable
    while (True): # the while loop
        x3 = (x1 + x2) / 2 # find a new bracket
        if (func(x3) == 0): return x3, iter # check if x3 is a root

        if (func(x3) < 0): # check if x3 has a negative y value
            x1 = x3 # replace x1 with x3 as a new bracket
        else: # x3 must have a positive y value
            x2 = x3 # replace x2 with x3

        match flag: # match statement for each value of flag
            case 1: # absolute approximate error
                if (abs(x1 - x2) < tol): return x1, iter # if the calculated error < tolerance, return the root and number of iterations, terminating the loop
            case 2: # absolute relative approximate error
                if (abs((x1 - x2) / x1) < tol): return x1, iter # if the calculated error < tolerance, return the root and number of iterations, terminating the loop
            case 3: # estimation of true absolute error
                if (abs(func(x1)) < tol): return x1, iter # if the calculated error < tolerance, return the root and number of iterations, terminating the loop
            case 4: # conjunction of absolute approximate error and estimated true absolute error
                if (abs(func(x1)) < tol and abs(x1 - x2) < tol): return x1, iter # if the calculated error < tolerance, return the root and number of iterations, terminating the loop

        iter += 1 # increment iter by one
        if (iter > 1000): # check if iterations has exceeded a "ridiculous" value (1000)
            print("\nIterations have exceeded 1000, terminating bisection function.") # notify the user that iterations have exceeded 100
            return x1, iter # return the approximate root and number of iterations