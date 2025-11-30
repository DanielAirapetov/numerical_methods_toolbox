import math

# assume that x and y values are passed in the proper order from left to right, assume that x_values are evenly spaced by h, missing points will be interpolated
def trapezoidRule_integration(x_values, y_values, h):
    def lagrangeInterpolation(x_value, x_points, y_points):
        len_points = len(x_points)
        y_value = 0

        for i in range(len_points):
            L = 1
            for j in range(len_points):
                if j != i:
                    L *= (x_value - x_points[j]) / (x_points[i] - x_points[j])
            y_value += L * y_points[i]
        return y_value

    def get_exact_value(x_value, x_points, y_points):
        for i, x in enumerate(x_points):
            if math.isclose(x_value, x, rel_tol = 10**-9, abs_tol = 10**-9):
                return y_points[i]
        return None
    
    # Input validation
    if len(x_values) != len(y_values):
        raise ValueError("x_values and y_values must have the same length.")
    if len(x_values) < 2:
        raise ValueError("At least two points are required for integration.")
    if h <= 0:
        raise ValueError("Step size h must be positive.")
    for i in range(1, len(x_values)):
        if x_values[i] <= x_values[i-1]:
            raise ValueError("x_values must be strictly increasing.")
    sum = 0
    n = (int)(math.ceil((x_values[-1] - x_values[0]) / h)) # n = (b - a) / h 
    for i in range(1, n):
        x = x_values[0] + i*h
        y = get_exact_value(x, x_values, y_values)
        if y is not None: 
            sum += y
        else:
            sum += lagrangeInterpolation(x, x_values, y_values)
    return (h/2) * (y_values[0] + 2*sum + y_values[-1])