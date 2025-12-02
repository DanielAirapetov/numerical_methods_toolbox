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
    
def numerical_differentation(data_point, x, f, h, method, type_of_interpolation): 
    data_points_used = None
    values_used = None
    
    nums_data_points = None
    
    if type_of_interpolation == 1:
        nums_data_points = 3
    else:
        nums_data_points = 4
        
    distances = np.abs(x - data_point)
    sorted_indices = np.argsort(distances)
    selected_indices = sorted_indices[:nums_data_points]
    
    data_points_used = x[selected_indices]
    values_used = f[selected_indices]
        
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
