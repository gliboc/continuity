#! /usr/bin/python

from load_modules import *
from kMeans import dist

from regressionConstants import reg_lin


if __main__ == "__main__":

    from load_dataset import X_train, Y_train

    p = 0.5
    nb_values = len(X_train)

    select = np.linspace(0, nb_values - 1, int(p * nb_values), dtype=int)
    given_v = Y_train[select]

    Y_tr = reg_lin(nb_values, given_v, select)

    d = dist(Y_tr, Y_train)

    print(d)
