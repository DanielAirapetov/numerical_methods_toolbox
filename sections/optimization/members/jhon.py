import sympy as sy

def function(data_point, n = 0):
    equation = pow(data_point, 3) - 4 * data_point
    
    if n == 0:
        return equation
    else:
        x = sy.symbols('x')
        equation = pow(x, 3) - 4 * x
        
        if n == 1:
            first_derivative = sy.diff(equation, x, 1)
            return first_derivative.subs(x, data_point)
        elif n == 2: 
            second_derivative = sy.diff(equation, x, 2)
            return second_derivative.subs(x, data_point)
        
def newton_min_max(x0, tolerance):
    a = 1
    i = 1
     
    x_k = x0
    x_k_1 = x_k - a * (function(x_k, 1) / function(x_k, 2))
    
    while abs(x_k_1 - x_k) > tolerance and i <= 100:
        x_k = x_k_1
        x_k_1 = x_k - a * (function(x_k, 1) / function(x_k, 2))
        i += 1
        
    return x_k_1, i
    
def GoldenSection(a, b, tolerance):
    golden_section = 1.618
    
    a1 = a
    b1 = b
    
    min = None
    min_i = 0
        
    while abs(b1 - a1) > tolerance and min_i <= 1000:
        x1 = b1 - ((b1 - a1) / golden_section)
        x2 = a1 + ((b1 - a1) / golden_section)
        
        y1 = function(x1)
        y2 = function(x2)
        
        if y1 >= y2:
            a1 = x1
            
            x1 = x2
            x2 = a1 + ((b1 - a1) / golden_section)
            
            y1 = function(x1)
            y2 = function(x2)
        else:
            b1 = x2 
            
            x2 = x1
            x1 = b1 - ((b1 - a1) / golden_section)
            
            y1= function(x1)
            y2 = function(x2)
        
        min_i += 1
            
    min = (a1 + b1) / 2
    
    a2 = a
    b2 = b
        
    max = None
    max_i = 0
    
    while abs(b2 - a2) > tolerance and max_i <= 1000:
        x1 = b2 - ((b2 - a2) / golden_section)
        x2 = a2 + ((b2 - a2) / golden_section)
        
        y1 = function(x1)
        y2 = function(x2)
        
        if y1 <= y2:
            a2 = x1
            
            x1 = x2
            x2 = a2 + ((b2 - a2) / golden_section)
            
            y1 = function(x1)
            y2 = function(x2)
        else:
            b2 = x2
            
            x2 = x1
            x1 = b2 - ((b2 - a2) / golden_section)
            
            y1= function(x1)
            y2 = function(x2)
            
        max_i += 1
                    
    max = (a2 + b2) / 2
    
    return min, max, min_i, max_i
