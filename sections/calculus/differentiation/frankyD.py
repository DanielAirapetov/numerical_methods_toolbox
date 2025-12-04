def lagrange(x, vector_x, vector_y): #lagrangian interpolation function 
    result = 0 # initalize result which will be added to later
    n = len(vector_x) #set n as the length of the vectors
    for i in range(n): #iteration for the length of the vectors 
        L_x = 1 #initializing L_x as one because we will multiply in nested loop, also resest for each iteration
        for j in range(n): # nested loop for L_x calculation
            if i != j: # only do it on seperate iterations so no division by zero
                L_x *= (x - vector_x[j])/(vector_x[i] - vector_x[j]) #peform formula for weighting function L(x)
        result += L_x*vector_y[i] #multiply L_x by output at current iteration and add for each iteration based on lagranges formula, 
    
    return result #return result

def num_diff(x0, x_vector, fx_vector, h, flag, type):
    n = len(x_vector)
    if type == 1:  # quadratic interpolation type
        #find the index where x0 would be inserted
        idx = 0
        for i in range(n-1):
            if x_vector[i] <= x0 <= x_vector[i+1]:
                idx = i
                break
        
        # select 3 points around x0
        if idx == 0:
            indices = [0, 1, 2]
        elif idx >= n-2:
            indices = [n-3, n-2, n-1]
        else:
            indices = [idx-1, idx, idx+1]
            
    elif type == 2:  # cubic 
        idx = 0
        for i in range(n-1):
            if x_vector[i] <= x0 <= x_vector[i+1]:
                idx = i
                break
        
        # select 4 points around x0
        if idx == 0:
            indices = [0, 1, 2, 3]
        elif idx == 1:
            indices = [0, 1, 2, 3]
        elif idx >= n-2:
            indices = [n-4, n-3, n-2, n-1]
        else:
            indices = [idx-1, idx, idx+1, idx+2]
   
    x = [x_vector[i] for i in indices] # use list comprension to only use points based on interpolation type
    fx = [fx_vector[i] for i in indices]
    
    if x0 in x: # only interpolate if x0 is not in our x vector
        fx0 = fx[x.index(x0)] 
    else:
        fx0 = lagrange(x0,x,fx)
    if x0+h in x: # only interpolate if x0+h isnt in x vector
        fx0h = fx[x.index(x0+h)]
    else:
        fx0h = lagrange((x0+ h), x,fx)
    if x0+(2*h) in x:   # same for x + 2h
        f2x0h = fx[x.index(x0+(2*h))]
    else:
        f2x0h = lagrange(x0+(2*h),x,fx)    
    if x0 - h in x: # same for x - h
        fx0minh = fx[x.index(x0-h)]
    else:
        fx0minh = lagrange((x0 - h), x,fx)

    if flag == 'a': # flag a uses formula for 2 points forward difference
        derivative = (fx0h - fx0)/h
    elif flag == 'b': # formula for 3 points forward difference
        derivative = ((-1*f2x0h) + (4*fx0h) - (3*fx0))/(2*h)
    elif flag == 'c': # formula for 3 points centered difference
        derivative = (fx0h - fx0minh)/(2*h)
    else: 
        print("Invalid flag: need a, b, or c")
        return None
    
    return derivative
        
def main():
    x_vector = [0.15, 0.21, 0.23, 0.27, 0.32, 0.35]
    y_vector = [0.1761, 0.3222, 0.3617, 0.4314, 0.5051, 0.5441]
    flags = ['a','b','c']
    x0 = 0.26
    for i in flags: #print results
        for j in [1,2]:
            print(f"Result for difference formula {i} interpolation type {j} f'({x0}) = {num_diff(0.26,x_vector, y_vector, 0.01,i,j)}")
    
if __name__ == "__main__":
    main()
    