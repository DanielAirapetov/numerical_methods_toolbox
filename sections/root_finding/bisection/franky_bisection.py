import math

def bisection(x1, x2, thres, flag, f): # calling arguments are default brackets, tolerance value, a lambda function, and flag
    while f(x1)*f(x2) > 0: # check if valid brackets were given 
        x1 = float(input("Invalid brackets. Enter new x1: ")) #if not ask for new ones
        x2 = float(input("Enter new x2: "))
    error = float('inf') # set error to infinity so it meets the condition of the while loop
    i = 0 # set iterations to 0
    x_prev = (x1+x2)/2  # initialize x_prev as first midpoint, will be changed it iteration
    while error >= thres:
        i += 1
        xi = (x1+x2)/2 # let xi (new bracket for this iteration) equal the mean the mean of x1 and x2
        if f(x1)*f(xi) < 0: #change brackets based on if sign changes within them
            x2 = xi # x2 is replaced with new bracket
        elif f(x1)*f(xi) > 0: 
            x1 = xi # x1 is replaced with new brack
        else: # in this case f(x3) would be equal to zero so x3 would be a root
            return xi, i - 1 #doing i - 1 because i is holding an extra iteration in order to skip flags on iteration 1
        if i > 1: #on the first iteration xi - xprev will be zero so dont perform checks on iteration 1
            if flag == 1: # calculate absolute approximate error
                error = abs(xi - x_prev)
            elif flag == 2: #calculate relative approximate error
                error = (abs(xi - x_prev))/abs(xi)
            elif flag == 3: # estimate true absolute error
                error = abs(f(xi))
            elif flag == 4: # conjunction of true absolute error and relative approximate error
                error1 = abs(xi - x_prev)
                error2 = abs(f(xi))
                if error1 <= thres and error2 <= thres: #both errors must meet the threshold
                    return xi, i - 1
                else: #return the larger error so loop doesnt run forever
                    error = max(error1,error2)
                
            else: # error handling for incorrect flag 
                flag = int(input("Invalid flag argument. Enter valid flag (1-4): "))
        if error <= thres: # if error calculated based on flag meets the threshold return xi as root 
            return xi, i - 1
        else:
            x_prev = xi # set the new x values as the previous for next iteration
        
            
def main():
    function1 = lambda x: 2*math.sin(x) - math.exp(x)/4 - 1 # write using pythons lambda functions 2sin(x) - e^x/4 - 1
    x1, x2 = -7.0, -5.0 # set the first set of brackets
    x3, x4 = -5.0, -3.0 # set the second set
    delta = 10e-6 # set our tolerance threshold
    
    roots1= [] #create an empty list of roots for closeness calculation done later
    roots2 = []
    print("Bisection function results for function 2sin(x) - e^x/4 - 1: ")
    for i in range(1,5): # print values for every stopping criteria 
        root1, iterations1 = bisection(x1,x2,delta,i,function1) # call flag i because we have iterations 1-4 and flags 1-4
        print(f"[-7,-5]: Flag {i}: root : {root1}, iterations: {iterations1}") # print result
        roots1.append(root1) #add to list of roots
        root2, iterations2 = bisection(x3,x4,delta,i,function1) #do same operations for other set of brackets
        print(f"[-5,-3]: Flag {i}: root : {root2}, iterations: {iterations2}")
        roots2.append(root2)
    closest1 = roots1.index(min(roots1, key=abs)) + 1 #calculate flag closest to zero by getting the smallest roots absolute value and then finding its position in the list and add 1 because indeces are 0-4 but flag 1-4
    closest2 = roots2.index(min(roots2, key=abs)) + 1
    print(f"Closest flag to 0 for [-7,-5]: {closest1}")
    print(f"Clostest flag to 0 for [-5,-3]: {closest2}")

    
    function2 = lambda x: math.cos(2*x) + math.sin(3*x)
    
    x1, x2 = -1, 0 # choosing brackets from graphing calculator, making sure only one root is between each bracket
    x3, x4 = 0, 2
    x5, x6 = 2, 3
    root1, iter1 = bisection(x1,x2, delta, 4, function2,) #use the flag for conjuction true abs err and relative abs err
    root2, iter2 = bisection(x3,x4, delta, 4, function2)
    root3, iter3 = bisection(x5,x6, delta, 4, function2)
    
    print("f(x) = cos(2x) + sin(3x), three roots between x = [-1, 3]: ") # display results
    print(f"{root1}, {iter1} iterations")
    print(f"{root2}, {iter2} iterations")
    print(f"{root3}, {iter3} iterations")
    

if __name__ == "__main__":
    main() 
    
        

        
    


