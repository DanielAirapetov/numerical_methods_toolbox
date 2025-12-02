import sympy as sp

def function(data_point, n = 0):
    equation = pow(data_point, 3) - 4 * data_point
    
    if n == 0:
        return equation
    else:
        x = sp.Symbols('x')
        equation = pow(x, 3) - 4 * x
        
        if n == 1:
            first_derivative = sp.diff(equation, x, 1)
            return first_derivative.subs(x, data_point)
        elif n == 2: 
            second_derivative = sp.diff(equation, x, 2)
            return second_derivative.subs(x, data_point)
        
def newtonMinMax(x0, tolerance):
    a = 1
    i = 1
     
    x_k = x0
    x_k_1 = x_k - a * (function(x_k, 1) / function(x_k, 2))
    
    while abs(x_k_1 - x_k) > tolerance and i <= 100:
        x_k = x_k_1
        x_k_1 = x_k - a * (function(x_k, 1) / function(x_k, 2))
        i += 1
        
    return x_k_1, i
    
def goldenSectionMethod(a, b, tolerance, flag, sym_func):

    x = sp.Symbol('x')
    function = sp.lambdify(x, sym_func, "numpy")

    golden_section = 1.618
    
    min_max = 0
    i = 0
    
    if flag == 1:

        while abs(b - a) > tolerance and i <= 1000:
            x1 = b - ((b - a) / golden_section)
            x2 = a + ((b - a) / golden_section)
            
            y1 = function(x1)
            y2 = function(x2)
            
            if y1 >= y2:
                a = x1
                
                x1 = x2
                x2 = a + ((b - a) / golden_section)
                
                y1 = function(x1)
                y2 = function(x2)
            else:
                b = x2 
                
                x2 = x1
                x1 = b - ((b - a) / golden_section)
                
                y1= function(x1)
                y2 = function(x2)
            
            i += 1
    elif flag == 2:
        while abs(b - a) > tolerance and i <= 1000:
                x1 = b - ((b - a) / golden_section)
                x2 = a + ((b - a) / golden_section)
                
                y1 = function(x1)
                y2 = function(x2)
                
                if y1 <= y2:
                    a = x1
                    
                    x1 = x2
                    x2 = a + ((b - a) / golden_section)
                    
                    y1 = function(x1)
                    y2 = function(x2)
                else:
                    b = x2
                    
                    x2 = x1
                    x1 = b - ((b - a) / golden_section)
                    
                    y1= function(x1)
                    y2 = function(x2)
                    
                i += 1

    min_max = (a + b) / 2
        
    return min_max, i
