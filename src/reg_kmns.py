#! /usr/bin/python
import numpy as np


def dist(a, b):
    return np.linalg.norm(a - b)


def naive_reg(nb_values, given_v, select, X_train):

    Y_tr = []
    k = 0
    for (i, j) in enumerate(select):
        while k < j:
            img = X_train[k]
            m = 0
            d_m = dist(img, X_train[m])
            for (r, s) in enumerate(select):
                if r != i:
                    d = dist(img, X_train[s])
                    if d < d_m:
                        d_m = d
                        m = r
            # m is the closest image that has supervision
            Y_tr.append(given_v[r])
            k += 1

        Y_tr.append(given_v[i])
        k += 1

    assert(len(Y_tr) == nb_values)

    return np.array(Y_tr)
# Now we want to do a better selection of the select array
# Instead of random, we use k-means to identify points of interest, and therefore take the images
# Then, we take an equal number of supervisions for each partition identified
# At first, we take them at random.
# Later, we can choose them because they are temporarly regularly spaced

from scipy.cluster.vq import kmeans2
from sklearn.cluster import KMeans


def kmean_reg(nb_values, given_v, given_i, X_train):
    kmeans = KMeans().fit(X_train)
    return kmeans


if __name__ == "__main__":
   # stuff only to run when not called via 'import' here
    import numpy as np
    from bokeh.plotting import figure, show, output_file
    import os
    import sys
    CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
    sys.path.append(os.path.dirname(CURRENT_DIR))
    from constants import nb_epochs
    from load_dataset import *
    import random as rd
    nb_values = len(X_train)

    # First : naive method with L^2 distance

    p = 0.5

    if p < 1.:
        select = rd.sample(list(range(1, nb_values - 1)), int(nb_values * p))
    else:
        select = list(range(1, nb_values - 1))

        select.sort()
        select = [0] + select + [nb_values - 1]

    given_v = Y_train[select]
