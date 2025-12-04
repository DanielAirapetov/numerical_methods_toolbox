import sympy as sp
def newton(x0, delta, flag, f): # newtons method function
    x = sp.symbols('x')
    fdiff = sp.diff(f,x)
    fdiff = sp.lambdify(x,fdiff)
    f = sp.lambdify(x,f)
    i = 0 #initalize iterations counter
    if (f(x0) == 0): #check if inital x value is a root
        return x0, i
    error = float('inf') # initalize infinitely large error so it meets while loop condition
    xprev = x0 # initialize xprev which will be used in the loop to store previous x values
    while (error >= delta): # loop is stopped based on if error threshold is met
        if (fdiff(xprev) == 0): # if deriviative is zero its a critical point on the graph which will result in incorrect results 
            x0 = int(input("Please enter correct x0: "))
        xn = xprev - (f(xprev)/fdiff(xprev)) # write algorithm based on lecture notes
        if f(xn) == 0: # if f(xn) == 0 we already have a correct root
            return xn, i
        else: 
            if flag == 1: # calculate absolute approximate error
                error = abs(xn - xprev) 
            elif flag == 2: #calculate relative approximate error
                error = (abs(xn - xprev))/abs(xn)
            elif flag == 3: # estimate true absolute error
                error = abs(f(xn))
            elif flag == 4: # conjunction of true absolute error and relative approximate error
                error1 = abs(xn - xprev)
                error2 = abs(f(xn))
                if error1 <= delta and error2 <= delta: #both errors must meet the threshold
                    return xn, i
                else: #return the larger error so loop doesnt run forever
                    error = max(error1,error2)
            else: # error handling for incorrect flag 
                flag = int(input("Invalid flag argument. Enter valid flag (1-4): "))
        xprev = xn # make xn the new xprev
        i += 1 # increment iterations counter
        if i > 1000:
            print("Error. Infinite loop")
    return xn, i # if while loop is exited we have a solution

def getclosest(arr,f): #function to calculate which flag's result is closest to zero
    closest = float('inf')
    for i in range(len(arr)):
        if abs(f(arr[i])) < closest:
            closest = i + 1
    return closest
        


