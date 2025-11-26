import sympy as sp

def newton(x0, tol, f): #Newtons method for nonlinear optimization
    x = sp.symbols('x') # define x as a symbol used in symbolic differentiation
    fDiffSym= sp.diff(f,x) # define first derivative using sympys diff functin
    f2DiffSym = sp.diff(fDiffSym,x) # get second derivative by using diff again on the first derviative
    f1_diff = sp.lambdify(x, fDiffSym, 'numpy') #use sympys lambdify function to convert the symbolic string into a lambda function like the one used in GS method which makes calculations possible
    f2_diff= sp.lambdify(x, f2DiffSym, 'numpy')
    error = float('inf') # initalize large error so loop condition is met
    i = 0 # initialize iteration counter
    xprev = x0
    while error >= tol and i < 1000: # same condition as GS method
        i += 1 # increment i 
        xnew =  xprev - (f1_diff(xprev)/f2_diff(xprev)) # apply newton method formula
        error = abs(xnew - xprev) # error is the distance between the points again
        xprev = xnew # make the new xprev so operation could continue for k + 1 iters
        
    return xnew, i # condition is met, can return xnew as the local extrema and i as number of iterations it took to get there
