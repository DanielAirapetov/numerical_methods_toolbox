import numpy as np


def lagrangeInterpolation(z, x, f, m) :

    # if z is already a point where the function is defined, then we should find its index and return the value of f at that index instead of interpolating
    if z in x:
        index = np.where(z == x)[0]
        return f[index][0]

    # np.argpartition sorts the indices based on how close they are to z and takes the first m nearest indices into the array, points
    points = np.argpartition(np.abs(x - z), m)[:m]
    
    # the variable is used to store the result
    interpolated_value = 0;


    # step through the array of indices
    # the outer loop is the sum of products of the weighting function L at each point and the values of f at each point
    for i in points:

        # the weighting function L_n(z): the lagrangian term of order i
        # this term is initialized as 1 in the outer loop so that it can be computed for each element in the points array
        lagrangian = 1
        
        # inner loop computes the lagrangian term of order i
        for j in points:

            # if the indices i and j are equivalent this will result in a zero division since the difference between x at the same index will be zero and this difference is in the denominator of the lagrangian expression.
            if j == i: continue

            # the lagrangian term is the product of (z - x_j]) / (x_i - x_j) for all elements in the range of points
            lagrangian *= ((z - x[j]) / (x[i] - x[j]))

        # the lagrangian polynomial is the sum of products between the lagrangian term of order i and the value of the function at the point x_i
        interpolated_value += lagrangian * f[i]
    
    return interpolated_value


# Trapezoidal Rule: [f(a) + 2 * SUM(f(x_i)) + f(b)] * h/2
def newtonCotesTrapezoidalRuleMethod(x, f, h):

    # m is the number of points used for interpolation, here it is 3 so the interpolating polynomial will be quadratic
    m = 3

    # n is the number of subintervals, found by the length of the entire interval divided by the step
    n = int((x[-1] - x[0]) / h)


    # first add the first and last elements, which are the bounds of the integral
    integral = (f[0] + f[-1]) / 2

    # the summation of values of function at each subinterval, not including the bounds
    for i in range (1, n):

        # I round z to the nearest 8 decimal places to avoid a floaing point error that was occuring
        z = round(x[0] + (i * h), 8)

        # if z is already defined: lagrangeInterpolation will return the value of the function at z
        # if z is not defined: lagrangeInterpolation interpolates the value of the function using quadratic interpolation
        integral += lagrangeInterpolation(z, x, f, m)
    
    # multiply by h
    return integral * h
