import numpy as np
def lagrange_function(z, x, f):
    n = len(x)
    interpolated_value = 0
    
    for i in range (n):
        lagrangian = 1
        for j in range(n):
            if(j != i):
                lagrangian = lagrangian * (z - x[j]) / (x[i] - x[j]) 
        interpolated_value = interpolated_value + lagrangian * f[i]
    
    return interpolated_value
    
def numerical_differentation(x, f, h, method, type_of_interpolation): 
    data_points_used = None
    values_used = None
    
    data_point = float(input("\nWhat is the data point you want to find the derivative value of: "))
    
    if(type_of_interpolation == 1):
        data_points_used = x[0:3]
        values_used = f[0:3]
    else:
        data_points_used = x[0:]
        values_used = f[0:]
        
    data_point_value = None
    
    if(data_point in x):
        data_point_value = f[np.where(x == data_point)[0][0]]
    else:
        data_point_value = lagrange_function(data_point, data_points_used, values_used)
        
    if(method == "a"):
        method_a_data_point = data_point + h
        method_a_data_point_value = None
        
        if(method_a_data_point in x):
            method_a_data_point_value = f[np.where(x == method_a_data_point)[0][0]]
        else:
            method_a_data_point_value = lagrange_function(method_a_data_point, data_points_used, values_used)
        
        return ((method_a_data_point_value - data_point_value) / h)
    
    elif(method == "b"):
        method_b_data_point = data_point + (2 * h)
        method_b_data_point_value = None
        
        if(method_b_data_point in x):
            method_b_data_point_value = f[np.where(x == method_b_data_point)[0][0]]
        else:
            method_b_data_point_value = lagrange_function(method_b_data_point, data_points_used, values_used)
        
        method_b_data_point2 = data_point + h
        method_b_data_point_value2 = None
        
        if(method_b_data_point2 in x):
            method_b_data_point_value2 = f[np.where(x == method_b_data_point2)[0][0]]
        else:
            method_b_data_point_value2 = lagrange_function(method_b_data_point2, data_points_used, values_used)
        
        return (((-1 * method_b_data_point_value) + (4 * method_b_data_point_value2) + (-3 * data_point_value)) / (2 * h))
    
    else:
        method_c_data_point = data_point + h
        method_c_data_point2 = data_point - h
        
        method_c_data_point_value = None
        method_c_data_point_value2 = None
        
        if(method_c_data_point in x):
            method_c_data_point_value = f[np.where(x == method_c_data_point)[0][0]]
        else:
            method_c_data_point_value = lagrange_function(method_c_data_point, data_points_used, values_used)
            
        if(method_c_data_point2 in x):
            method_c_data_point_value2 = f[np.where(x == method_c_data_point2)[0][0]]
        else:
            method_c_data_point_value2 = lagrange_function(method_c_data_point2, data_points_used, values_used)
            
        return ((method_c_data_point_value - method_c_data_point_value2) / (2 * h))
