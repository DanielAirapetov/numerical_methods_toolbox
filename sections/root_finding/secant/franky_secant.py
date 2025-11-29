def secant(x1,x2,delta,flag,f): 
    if abs(f(x1)) < abs(f(x2)): # make sure x1 is the smaller bracket
        x1,x2 = x2, x1    
    error = float('inf') # initalize error
    i = 1 # initialize iteration counter
    while (error >= delta): #while the tolerance threshold has not been exceeded
        xn = x2 - f(x2) * (x1-x2)/(f(x1) - f(x2)) #iteratively get the secant line between the two points 
        x1 = x2 # make the inner point the new outer point
        x2 = xn # make xn the new inner point
        if f(x2) == 0: # if f(x2) == 0 we already have a correct root
            return x2, i
        else: 
            if flag == 1: # calculate absolute approximate error
                error = abs(x1 - x2)
            elif flag == 2: #calculate relative approximate error
                error = (abs(x1 - x2))/abs(x2)
            elif flag == 3: # estimate true absolute error
                error = abs(f(x2))
            elif flag == 4: # conjunction of true absolute error and relative approximate error
                error1 = abs(x1 - x2)
                error2 = abs(f(x2))
                if error1 <= delta and error2 <= delta: #both errors must meet the threshold
                    return x2, i 
                else: #return the larger error so loop doesnt run forever
                    error = max(error1,error2)  
            else: # error handling for incorrect flag 
                flag = int(input("Invalid flag argument. Enter valid flag (1-4): "))
        i+=1  #add to iteration counter  
        if (i > 100):
            print("Error: Infinite loop")   
            return
               
    
    return x2, i # when while loop is exected return x2 
