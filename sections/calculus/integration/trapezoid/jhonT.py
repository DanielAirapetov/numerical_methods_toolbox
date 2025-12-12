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

def trapezoidal_rule(x_np, f_np, h):
    x = list(x_np)
    f = list(f_np)
    sum = 0
    data_point = round(x[0] + 0.1, 1)
    n = int((x[len(x) - 1] - x[0]) / h)
    max = round(((n / 10) + 1.0) - 0.1, 1)
    
    while data_point <= max: 
        if data_point in x:
            sum += f[x.index(data_point)]
        else:
            left = round(data_point - 0.2, 1)
            right = round(data_point + 0.2, 1)
            x_data_points = x[x.index(left):x.index(right)]
            x_values = f[x.index(left):x.index(right)]
            sum += lagrange_function(data_point, x_data_points, x_values)
        data_point = round(data_point + 0.1, 1)
    result = h * ((f[0] + 2 * sum + f[len(f) - 1]) / 2)
    
    return result

