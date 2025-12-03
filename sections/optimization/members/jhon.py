import numpy as np
import sympy as sp

        
def newtonMinMaxMethod(x0, tolerance, sym_func):

    x = sp.Symbol('x')
    function_diff1 = sp.diff(sym_func, x)
    function_diff2 = sp.diff(function_diff1, x)

    function = sp.lambdify(x, sym_func, "numpy")
    f_d1 = sp.lambdify(x, function_diff1, "numpy")
    f_d2 = sp.lambdify(x, function_diff2, "numpy")
    

    a = 1
    i = 1
     
    x1 = x0 - a * (f_d1(x0) / f_d2(x0))
    
    while np.abs(x1 - x0) > tolerance and i <= 1000:
        x0 = x1
        x1 = x0 - a * (f_d1(x0) / f_d2(x0))
        i += 1
        
    return x1, i
    
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
