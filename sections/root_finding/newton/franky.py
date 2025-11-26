import numpy as np
from scipy.misc import derivative # python library for differentiation
import math
def newton(x0, delta, flag, f): # newtons method function
    i = 0 #initalize iterations counter
    if (f(x0) == 0): #check if inital x value is a root
        return x0, i
    error = float('inf') # initalize infinitely large error so it meets while loop condition
    xprev = x0 # initialize xprev which will be used in the loop to store previous x values
    while (error >= delta): # loop is stopped based on if error threshold is met
        if (derivative(f,xprev) == 0): # if deriviative is zero its a critical point on the graph which will result in incorrect results 
            x0 = int(input("Please enter correct x0: "))
        xn = xprev - (f(xprev)/derivative(f,xprev)) # write algorithm based on lecture notes
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
        
def main():
    function1 = lambda x: 2*math.sin(x) - math.exp(x)/4 - 1 
    x1 = -7.0 #set starting point for root between x = [-7,-5]
    x2 = -4.0 #set starting point for root between x = [-5,-3]
    delta = 10e-6 # set our tolerance threshold
    
    roots1 = [] #create an empty list of roots for closeness calculation done later
    roots2 = []
    print("Newton method results for function 2sin(x) - e^x/4 - 1: ")
    for i in range(1,5): # print values for every stopping criteria 
        root1, iterations1 = newton(x1,delta,i,function1) # call flag i because we have iterations 1-4 and flags 1-4
        print(f"x0 = -7: Flag {i}: root : {root1}, iterations: {iterations1}") # print result
        roots1.append(root1) #add to list of roots
        root2, iterations2 = newton(x2,delta,i,function1) #do same operations for other set of brackets
        print(f"x0 = -4: Flag {i}: root : {root2}, iterations: {iterations2}")
        roots2.append(root2)
    
    closest1 = getclosest(roots1,function1) # get flag closest to zero for each function
    closest2 = getclosest(roots2,function1)
    
    
    print(f"Closest flag to 0 for Newton Method x0 = -7: {closest1}") # print flags for each closest method: 
    print(f"Closest flag to 0 for Newton Method x0 = -4: {closest2}")

    function2 = lambda x: math.pow(x,3) - 1 - math.cos(x) #finding the point where x^3 - 1 and cos(x) intersect
    #defining the function as the subtraction of the two because where they intersect is when the functions are equal to another, then just subtract from both sides with algebra
    
    solution, iter = newton(0, delta, i, function2) #setting x0 as 0 based on graphing calculator 
    print(f"y = cos(x) & y = x^3 - 1 intersect at the point x = {solution}") #print result
    print(f"{iter} iterations")
    
    
if __name__ == "__main__":
    main() 

