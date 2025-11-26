def regulafalsi(x1, x2, delta, flag, f): # calling arguments are default brackets, tolerance value, a lambda function, and flag
    if f(x1)*f(x2) > 0: # check if valid brackets were given 
        x1 = float(input("Invalid brackets. Enter new x1: ")) #if not ask for new ones
        x2 = float(input("Enter new x2: ")) #if not ask for new ones
        return
    error = float('inf') # set error to infinity so it meets the condition of the while loop
    i = 0 # set iterations to 0
    x_prev = x2 - f(x2) * (x1-x2)/(f(x1) - f(x2)) # initatlize xprev using the formula of secant line between the brackets
    while error >= delta:
        i += 1 #increment iteration at the start of loop
        xi = x2 - f(x2) * (x1-x2)/(f(x1) - f(x2)) 
        if f(x1)*f(xi) < 0: #change brackets based on if sign changes within them
            x2 = xi # x2 is replaced with new bracket
        elif f(x1)*f(xi) > 0: 
            x1 = xi # x1 is replaced with new brack
        else: # in this case f(x3) would be equal to zero so x3 would be a root
            return xi, i - 1 #doing i - 1 because i is holding an extra iteration in order to skip flags on iteration 1
        if (i > 1): #on the first iteration xi - xprev will be zero so dont perform checks on iteration 1
            if flag == 1: # calculate absolute approximate error
                error = abs(xi - x_prev)
            elif flag == 2: #calculate relative approximate error
                error = (abs(xi - x_prev))/abs(xi)
            elif flag == 3: # estimate true absolute error
                error = abs(f(xi))
            elif flag == 4: # conjunction of true absolute error and relative approximate error
                error1 = abs(xi - x_prev)
                error2 = abs(f(xi))
                if error1 <= delta and error2 <= delta: #both errors must meet the threshold
                    return xi, i - 1
                else: #return the larger error so loop doesnt run forever
                    error = max(error1,error2)
            
            else: # error handling for incorrect flag 
                flag = int(input("Invalid flag argument. Enter valid flag (1-4): "))
        
        if error <= delta: # if error calculated based on flag meets the threshold return xi as root 
            return xi, i - 1
        else:
            x_prev = xi # set the new x values as the previous for next iteration
  

        