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

def simpson_rule(x_np, f_np, h):
    x = list(x_np)
    f = list(f_np)
    n = int((x[-1] - x[0]) / h) 
    sum_01 = 0
    max_01 = round((((n / 2) / 10) + 1.0) - 0.1, 1) 
      
    data_point = x[1]
    multiplier = 0
    
    while data_point <= max_01:
        multiplier += 1
        even_data_point = round(data_point + (0.1 * multiplier), 1)
        if even_data_point in x:
            sum_01 += f[x.index(even_data_point)]
        else:
            left = round(even_data_point - 0.2, 1)
            right = round(even_data_point + 0.2, 1)
            even_x_data_points = x[x.index(left):x.index(right)]
            even_x_values = f[x.index(left):x.index(right)]
            sum_01 += lagrange_function(even_data_point, even_x_data_points, even_x_values)
        data_point = round(data_point + 0.1, 1)
    
    sum_02 = 0
    max_02 = round((((n / 2) / 10) + 1.0), 1) 
    
    data_point = x[1]
    multiplier = 0
    
    while data_point <= max_02:
        multiplier += 1
        odd_data_point = round((data_point + (0.1 * multiplier)) - 0.1, 1)
        if odd_data_point in x:
            sum_02 += f[x.index(odd_data_point)]
        else:
            left = round(odd_data_point - 0.2, 1)
            right = round(odd_data_point + 0.2, 1)
            odd_x_data_points = x[x.index(left):x.index(right)]
            odd_x_values = f[x.index(left):x.index(right)]
            sum_02 += lagrange_function(odd_data_point, odd_x_data_points, odd_x_values)
        data_point = round(data_point + 0.1, 1)
    
    result = (h / 3) * (f[0] + (2 * sum_01) + (4 * sum_02) + f[len(f) - 1])
    return result
