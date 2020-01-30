import inline as inline
import matplotlib

matplotlib.use("TkAgg")
from mpl_toolkits import mplot3d
import numpy as np
import matplotlib.pyplot as plt
from functions import *
from math import *
from interface import *


def get_method_names():
    return ["Hooke-Jeeves", "Powell"]


def plot_function_3D(function, a, b, style, title):
    fig = plt.figure()
    ax = plt.axes(projection='3d')

    x = np.linspace(a, b, 30)
    y = x

    X, Y = np.meshgrid(x, y)
    Z = function([X, Y])

    ax.plot_surface(X, Y, Z, rstride=1, cstride=1, cmap=style, edgecolor="none")
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.set_title(title)

    plt.show()


def hooke_jeeves(function, x0, d, d_min, display_info=False, window=None):
    n = x0.size
    e = np.eye(n) * d
    x = x0
    fx = function(x)
    num_iterations = 0

    while e[1, 1] > d_min:
        current_position = x
        for i in range(0, n):
            z = current_position + e[:, i]
            y = function(z)
            num_iterations += 1
            if y < fx:
                current_position = z
                fx = y
                if display_info and num_iterations % 10 == 0:
                    to_write = "Iteration {} -- Current X: {}\nFunction value: {}\n".format(num_iterations, x, fx)
                    window.result_console.append(to_write)
            else:
                z = current_position - e[:, i]
                y = function(z)
                num_iterations += 1
                if y < fx:
                    current_position = z
                    fx = y
                if display_info and num_iterations % 10 == 0:
                    to_write = "Iteration {} -- Current X: {}\nFunction value: {}\n".format(num_iterations, x, fx)
                    window.result_console.append(to_write)

        if np.all(current_position == x):
            e = e * 0.5

        else:
            x1 = current_position + (current_position - x)
            f1 = function(x1)
            num_iterations += 1
            x = current_position
            if display_info and num_iterations % 10 == 0:
                to_write = "Iteration {} -- Current X: {}\nFunction value: {}\n".format(num_iterations, x, fx)
                window.result_console.append(to_write)
            if f1 < fx:
                x = x1
                fx = f1
                for i in range(0, n):
                    z = x1 - e[:, i]
                    y = function(z)
                    num_iterations += 1
                    if y < f1:
                        x = z
                        fx = y
                    if display_info and num_iterations % 10 == 0:
                        to_write = "Iteration {} -- Current X: {}\nFunction value: {}\n".format(num_iterations, x, fx)
                        window.result_console.append(to_write)

    return x, fx, num_iterations


def golden_ratio(function, e, current, a, b, tolerance):
    c = (3 - sqrt(5)) / 2
    x1 = a + (b - a) * c
    x2 = a + b - x1

    fx1 = function(current + x1 * e)
    fx2 = function(current + x2 * e)

    while b - a > tolerance:
        if fx1 <= fx2:
            b = x2
            x2 = x1
            fx2 = fx1
            x1 = a + c * (b - a)
            fx1 = function(current + x1 * e)
            x = x1
        else:
            a = x1
            x1 = x2
            fx1 = fx2
            x2 = b - c * (b - a)
            fx2 = function(current + x2 * e)
            x = x2

    return x


def powell(function, helper_function, starting_position, tolerance, display_info=False, window=None, gda=-5, gdb=5):
    dimension = starting_position.size
    e = np.eye(dimension)
    x = starting_position
    x1 = starting_position + 2 * 10
    num_iterations = 0

    while np.max(np.abs(x - x1)) > tolerance:
        num_iterations += 1
        current = x
        for i in range(dimension):
            theta = helper_function(function, e[:, i], current, gda, gdb, tolerance)
            current = current + theta * e[:, i]

        for i in range(dimension - 1):
            e[:, i] = e[:, i + 1]
        e[:, dimension - 1] = current - x

        x1 = x
        theta = helper_function(function, e[:, dimension - 1], current, gda, gdb, tolerance)
        x = current + theta * e[:, dimension - 1]

        if display_info and num_iterations % 10 == 0:
            to_write = "Iteration {} -- Current X: {}\nFunction value: {}\n".format(num_iterations, x, function(x))
            window.result_console.append(to_write)

    fx = function(x)

    return x, fx, num_iterations


methods = {"Hooke-Jeeves": hooke_jeeves, "Powell": powell}

methods_info = {
    "Hooke-Jeeves": "The Hooke-Jeeves algorithm, also known as “pattern search”, keeps track of the direction of travel as the process moves from point to point, instead of starting over from scratch at each new point.",
    "Powell": "Powell's method, strictly Powell's conjugate direction method, is an algorithm proposed by Michael J. D. Powell for finding a local minimum of a function. The function doesn't need to be differentiable, and no derivatives are taken. The function must be a real-valued function of a fixed number of real-valued inputs."}

if __name__ == '__main__':
    # Testni slucajevi:

    a = np.array([1.0, 4.0]).T
    b = np.array([2, 1, 2, 1, 3, 2, -1, 0, 1, 2]).T
    c = np.array([2, 2, 2, 3]).T
    d = np.array([-1.2, 1]).T

    # Resenja idu redom: X, Y, broj iteracija

    print("SFERA: ")
    print(hooke_jeeves(sphere, b, 1, 0.0001))
    print(powell(sphere, golden_ratio, b, 0.0001))
    print("BANANA: ")
    print(hooke_jeeves(rosenbrock, b, 1, 0.0001))
    print(powell(rosenbrock, golden_ratio, b, 0.0001))
    print("KAMILA: ")
    print(hooke_jeeves(three_hump_camel, d, 1, 0.0001))
    print(powell(three_hump_camel, golden_ratio, d, 0.0001))

    # Odkomentarisati bilo koji poziv funkcije kako bi je iscrtali u 3D

    # plot_function_3D(three_hump_camel, -2, 2, "viridis", "Three Hump Camel")
    # plot_function_3D(sphere, -5, 5, "viridis", "Sphere")
    # plot_function_3D(rosenbrock, -2.048, 2.048, "viridis", "Rosenbrock")
