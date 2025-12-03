import numpy as np
import sympy as sp
import math

def goldenSectionMethod(a,b, tol, flag, f): # golden section function for nonlinear optimization

    x = sp.Symbol("x")
    func = sp.lambdify(x, f, modules = ["math"])


    phi = (1 + np.sqrt(5))/2 # assign phi (golden ratio number)
    error = float('inf') #initialize large error so loop condition is met
    x1 = b - ((b-a)/phi) # initialize x1 based on formula 
    x2 = a + ((b-a)/phi) # initialize x2 as well
    i = 0 # count iterations
    while error >= tol and i < 1000: # loop conditions: if error meets a certain threshold and if theres reasonable number of iterations
        if flag == 1: #perform GS formula for minimum extrema 
            if func(x1) >= func(x2): #determine golden sections based on which y value is greater
                a = x1
                x1 = x2 
                x2 = a + ((b-a)/phi)
            else:
                b = x2 
                x2 = x1
                x1 = b - ((b-a)/phi)
        
        elif flag == 2: # GS formula for max extrema, same except based on if fx1 is less than fx2 (opposite of min)
            if func(x1) <= func(x2):
                a = x1
                x1 = x2 
                x2 = a + ((b-a)/phi)
            else:
                b = x2 
                x2 = x1
                x1 = b - ((b-a)/phi)
        i += 1 #increment iteration counter in loop
        
        
        error = np.abs(b-a) # error is determined based on the absolute distance between to brackets as they repeatedly shirk over iterations
        
    return (a+b)/2, i # return midpoint between a and b, representing local extrema and how many iterations it took to reach the required tolerance


def newtonMinMaxMethod(x0, tol, f): #Newtons method for nonlinear optimization
    x = sp.symbols('x') # define x as a symbol used in symbolic differentiation
    fDiffSym= sp.diff(f,x) # define first derivative using sympys diff functin
    f2DiffSym = sp.diff(fDiffSym,x) # get second derivative by using diff again on the first derviative
    f1_diff = sp.lambdify(x, fDiffSym, modules = ["math"]) #use sympys lambdify function to convert the symbolic string into a lambda function like the one used in GS method which makes calculations possible
    f2_diff= sp.lambdify(x, f2DiffSym, modules = ["math"])
    error = float('inf') # initalize large error so loop condition is met
    i = 0 # initialize iteration counter
    xprev = x0
    while error >= tol and i < 1000: # same condition as GS method
        i += 1 # increment i 
        xnew =  xprev - (f1_diff(xprev)/f2_diff(xprev)) # apply newton method formula
        error = abs(xnew - xprev) # error is the distance between the points again
        xprev = xnew # make the new xprev so operation could continue for k + 1 iters
        
    return xnew, i # condition is met, can return xnew as the local extrema and i as number of iterations it took to get there
