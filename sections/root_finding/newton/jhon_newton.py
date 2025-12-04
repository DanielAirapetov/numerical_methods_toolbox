import sympy as sp 
import math

def newton_method(x0, tolerance, flag, user_function):
    x = sp.Symbol('x')
    
    expression = sp.lambdify(x, user_function)
    derivative_expression = sp.lambdify(x, sp.diff(user_function, x))
    
    i = 0
    x1 = None
    estimated_root = None
    estimated_root_found = False
    
    while not(estimated_root_found) and i <= 1000:
        if expression(x0) == 0:
            estimated_root = x0
            estimated_root_found = True
        else:
            if derivative_expression(x0) == 0:
                x0 = float(input("Please enter a x0: "))
            else:
                x1 = x0 - (expression(x0) / derivative_expression(x0))
                
                if flag == 1:
                    if abs(x1 - x0) < tolerance:
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                elif flag == 2:
                    if (abs(x1 - x0) / abs(x1)) < tolerance:
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                elif flag == 3:
                    if (abs(expression(x1)) < tolerance):
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
                else:
                    if (abs(x1 - x0) < tolerance) and (abs(expression(x1)) < tolerance):
                        estimated_root = x1
                        estimated_root_found = True
                    else:
                        x0 = x1
            i += 1; 
    
    return estimated_root, i

