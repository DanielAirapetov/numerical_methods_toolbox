def goldenSection(a,b, tol, flag, f): # golden section function for nonlinear optimization
    phi = (1 + np.sqrt(5))/2 # assign phi (golden ratio number)
    error = float('inf') #initialize large error so loop condition is met
    x1 = b - ((b-a)/phi) # initialize x1 based on formula 
    x2 = a + ((b-a)/phi) # initialize x2 as well
    i = 0 # count iterations
    while error >= tol and i < 1000: # loop conditions: if error meets a certain threshold and if theres reasonable number of iterations
        i += 1 #increment iteration counter in loop
        if flag == 'min': #perform GS formula for minimum extrema 
            if f(x1) >= f(x2): #determine golden sections based on which y value is greater
                a = x1
                x1 = x2 
                x2 = a + ((b-a)/phi)
            else:
                b = x2 
                x2 = x1
                x1 = b - ((b-a)/phi)
        
        elif flag == 'max': # GS formula for max extrema, same except based on if fx1 is less than fx2 (opposite of min)
            if f(x1) <= f(x2):
                a = x1
                x1 = x2 
                x2 = a + ((b-a)/phi)
            else:
                b = x2 
                x2 = x1
                x1 = b - ((b-a)/phi)
        
        
        error = abs(b-a) # error is determined based on the absolute distance between to brackets as they repeatedly shirk over iterations
        
    return (a+b)/2, i # return midpoint between a and b, representing local extrema and how many iterations it took to reach the required tolerance
