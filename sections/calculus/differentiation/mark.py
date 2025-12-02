import numpy as np


# function takes as arguments a point where we want to interpolate the function
# array of points x where the function is defined
# and an array f of corresponding function values
def lagrangeInterpolation(z, x, f, n):

    # check if the point z is already a defined point
    if np.any(np.isclose(z, x, 1e-12)): 
        # if it is then we should get the index and return the element of f at that index
        index = np.where(np.isclose(z, x, 1e-12))[0][0]
        return f[index]

    # this will return an array of indices of the elements in x closest by magnitude to z
    # based on the user's choice of quadratic or cubic interpolation (here it is stored in n) we take the first n points
    # these 3 or 4 points are the nearest to z and should result in a lower error
    # np.argsort sorts the indices of the elements based on the comparison np.abs(x - z) and then takes the first n points [:n]

    points = np.argsort(np.abs(x - z))[:n]

    # this variable will store the result
    interpolated_value = 0

    # iterate through the array of indices 
    # the outer loop is the sum of products of the weighting function L at each point and the values of f at each point
    for i in points:

        # the weighting function L_n(z): the lagrangian term of order i
        # initialized as 1 in the outer loop so that it can be computer for each i up to n, which is the number of points being used for interpolation
        lagrangian = 1
        

        # inner loop computes the lagrangian term of order i
        for j in points:

            # if the indices i and j are equivalent this will result in a zero division since the elements of x at the same index will cancel each other out in the denominator of the expression below
            if j == i: continue

            # the lagrangian term is the product of (z - x_j) / (x_i - x_j) for all elementsin the range points
            lagrangian *= ((z - x[j]) / (x[i] - x[j]))

        # the lagrangian polynomial is the sum of the lagrangian term of order i, multiplied by the value of the function at the point x_i
        interpolated_value += lagrangian * f[i]
    
    return interpolated_value



# the following functions maintain a similar composition
# they each accept a point, z, at which to evaluate the derivative
# an array, x, of points where the function is defined and an array, f, of corresponding function values
# h, a step
# n, the type of interpolation (the number of points used to interpolate)

def twoPointForwardDifference(z, x, f, h, n):

    # evaluates the two point forward difference
    # calling the interpolation function covers all cases:
    # if the point z or z + h is already defined, then the interpolation function will return the corresponding function value, otherwise it will interpolate the function value
    return (lagrangeInterpolation(z + h, x, f, n) - lagrangeInterpolation(z, x, f, n)) / h


def threePointForwardDifference(z, x, f, h, n):

    # evaluates the three point forward difference
    # here, I again use the interpolation function which covers two cases:
    # the case where the function f(x) is not defined for a point and needs to be interpolated
    # and the case where the function is already defined and we should use that value instead of interpolating
    return ((-1 * lagrangeInterpolation(z + (2 * h), x, f, n)) + (4 * lagrangeInterpolation(z + h, x, f, n)) - (3 * lagrangeInterpolation(z, x, f, n))) / (2 * h)


def threePointCenteredDifference(z, x, f, h, n):

    # evaluates the three point centered difference
    # again I use the interpolation function to cover all cases
    return (lagrangeInterpolation(z + h, x, f, n) - lagrangeInterpolation(z - h, x, f, n)) / (2 * h)


# this function calls takes a point z, at which to evaluate the derivative
# an array, x, of points where the function is defined and an array, f, of the corresponding function values
# h, a step
# method, which is either a, b, or c, and determines which method of differentiation should be used
# n is the interpolation type which is the number of points to use for interpolation
def differentiate(z, x, f, h, method, n):

    # first we should check if there are enough points defined for the type of interpolation we want to use
    # there should be at least 3 points or at least 4 points where the function is defined to use quadratic or cubic interpolation, respectively
    if len(x) < n:
        print("Not enough points for interpolation")
        return 0


    # if-else statement to determine which type of differntiation to use as determined by the value of the method variable
    if method == 'a':
        return twoPointForwardDifference(z, x, f, h, n)
    elif method == 'b':
        return threePointForwardDifference(z, x, f, h, n)
    elif method == 'c':
        return threePointCenteredDifference(z, x, f, h, n)
