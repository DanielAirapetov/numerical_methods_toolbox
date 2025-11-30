import math

# assume that x and y values are passed in the proper order from left to right, assume that x_values are evenly spaced by h, missing points will be interpolated
def simpsonsRule_integration(x_values, y_values, h):
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
    if len(x_values) < 3:
        raise ValueError("At least three points are required for Simpson's rule.")
    if h <= 0:
        raise ValueError("Step size h must be positive.")
    for i in range(1, len(x_values)):
        if x_values[i] <= x_values[i-1]:
            raise ValueError("x_values must be strictly increasing.")
        
    even_sum, odd_sum = 0, 0
    even = True
    n = (int)(math.ceil((x_values[-1] - x_values[0]) / h)) # n = (b - a) / h
    if n % 2 != 0:
        n -= 1
        even = False
    for k in range(2, n - 1, 2): # sum1
        x = x_values[0] + k*h
        y = get_exact_value(x, x_values, y_values)
        if y is not None: 
            even_sum += y
        else:
            even_sum += lagrangeInterpolation(x, x_values, y_values)
    for k in range(1, n, 2): # sum2
        x = x_values[0] + k*h
        y = get_exact_value(x, x_values, y_values)
        if y is not None: 
            odd_sum += y
        else:
            odd_sum += lagrangeInterpolation(x, x_values, y_values)
    integral = (h/3) * (y_values[0] + 2*even_sum + 4*odd_sum + y_values[-1])
    if not even:
        f_a = get_exact_value(x_values[0] + h*n, x_values, y_values)
        if f_a is None:
            f_a = lagrangeInterpolation(x_values[0] + h*n, x_values, y_values)
        f_b = y_values[-1]
        integral += (h/2) * (f_a + f_b)
    return integral