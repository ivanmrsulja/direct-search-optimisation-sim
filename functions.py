def test_function(x):
    f = x[0] ** 2 + x[0] ** x[1] + 3 * x[1] ** 2
    return f


def three_hump_camel(x):
    f = 2 * x[0] ** 2 - 1.05 * x[0] ** 4 + x[0] ** 6 / 6 + x[0] * x[1] + x[1] ** 2
    return f


def sphere(x):
    sum = 0
    for i in range(len(x)):
        sum += x[i] ** 2

    return sum

def rosenbrock(x):
    sum = 0
    for i in range(0, len(x) - 1):
        sum += (100 * (x[i+1] - x[i]**2)**2 + (x[i]-1)**2)

    return sum

def get_function_names():
    return ["Three Hump Camel", "Sphere", "Rosenbrock"]


functions = {"Three Hump Camel": three_hump_camel, "Sphere" : sphere, "Rosenbrock" : rosenbrock}

function_info = {"Three Hump Camel": "The function has three local minima. Plot it on the interval of [-2, 2] in order to see its key characteristics.\n\nGlobal minimum is in x(0, 0)", "Sphere" : "The Sphere function has d local minima except for the global one. It is continuous, convex and unimodal.\n\nGlobal minimum is in x(0, ... ,0)", "Rosenbrock" : "The Rosenbrock function, also referred to as the Valley or Banana function, is a popular test problem for gradient-based optimization algorithms. The function is unimodal, and the global minimum lies in a narrow, parabolic valley. However, even though this valley is easy to find, convergence to the minimum is difficult.\n\nGlobal minimum is in x(1, ... , 1)"}