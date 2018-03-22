#! /usr/bin/python

alpha = 0.75
# between a 0 and a 1, d being the time between those two observations, the apparition time is
# estimated to be after d*alpha time units from 0
# d*(1-alpha) for 1 to 0

import numpy as np


def reg_lin(nb_values, given_v, given_i):
    x = 0
    nb_objs = given_v.shape[1]
    y = np.array([0.] * nb_objs * nb_values).reshape(nb_values, nb_objs)

    for j in range(len(given_i) - 1):
        x1 = given_i[j]
        x2 = given_i[j + 1]

        for i in range(nb_objs):
            x = x1
            y1 = given_v[j, i]
            y2 = given_v[j + 1, i]

            f = lambda z: y1 + (y2 - y1) * (z - x1) / (x2 - x1)
            while x <= x2:
                y[x, i] = f(x)
                x += 1
        x = x2

    return y


def reg(nb_values, given_values, given_values_indexes):
    """ Regression by a constant by pieces function """
    assert(len(given_values) == len(given_values_indexes))
    y = []
    i = 0

    for j in range(len(given_values) - 1):
        x1 = given_values_indexes[j]
        x2 = given_values_indexes[j + 1]
        y1 = given_values[j]
        y2 = given_values[j + 1]

        if y1 == y2 == 0.:
            while i <= x2:
                y.append(0.)
                i += 1

        elif y1 == y2 == 1.:
            while i <= x2:
                y.append(1.)
                i += 1

        elif y1 == 0. and y2 == 1.:
            d = x2 - x1

            while i <= x1 + int(d * alpha):
                y.append(y1)
                i += 1

            while i <= x2:
                y.append(y2)
                i += 1

        elif y1 == 1. and y2 == 0.:
            d = x2 - x1

            while i <= x1 + int(d * (1 - alpha)):
                y.append(y1)
                i += 1

            while i <= x2:
                y.append(y2)
                i += 1

        else:
            assert(0)

    return y

# Example
import sys

if len(sys.argv) > 1 and "test" in sys.argv:
    print("This is an example with alpha = 0.75 (void bias)")
    import matplotlib.pyplot as plt
    nb_values = 50
    given_values = [0, 1, 1, 0, 0, 1]
    given_values_indexes = [0, 9, 19, 29, 39, 49]

    p = plt.figure()
    x_axis = list(range(nb_values))
    x = [0] * nb_values
    for (j, i) in enumerate(given_values_indexes):
        x[i] = given_values[j]
    y = reg(nb_values, given_values, given_values_indexes)
    plt.plot(x_axis, x)
    plt.plot(x_axis, y)
    plt.show()
