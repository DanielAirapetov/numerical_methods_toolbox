def lagrange(x, vector_x, vector_y): #lagrangian interpolation function 
    if x in vector_x:
        return vector_y[vector_x.index(x)]
    else:
        result = 0 # initalize result which will be added to later
        n = len(vector_x) #set n as the length of the vectors
        for i in range(n): #iteration for the length of the vectors 
            L_x = 1 #initializing L_x as one because we will multiply in nested loop, also resest for each iteration
            for j in range(n): # nested loop for L_x calculation
                if i != j: # only do it on seperate iterations so no division by zero
                    L_x *= (x - vector_x[j])/(vector_x[i] - vector_x[j]) #peform formula for weighting function L(x)
            result += L_x*vector_y[i] #multiply L_x by output at current iteration and add for each iteration based on lagranges formula, 
    
        return result #return result

def simpsons_rule(x_points, fx_points, h):
    a = x_points[0]
    b = x_points[-1]
    n = int((b - a)/h) #define n
    I = fx_points[0] # get first point in f_x
    for k in range(2,n,2): # add and multiply each even point by 2
        I += 2 * fx_points[k]
    for k in range(1,n,2): # add and multiply each odd point by 4
        I += 4 * fx_points[k]
    I += fx_points[-1] # add last point in f_x
    I *= h/3 # finally multiply by h/3
    return I 