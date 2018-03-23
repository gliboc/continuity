"""Loads the dataset (y_train, y_test)
in the data directory
:return: tuple ((X_train, Y_train), (X_test, Y_test))
"""

import os
import numpy as np
from scipy import misc    # Loading & saving functions

import sys
sys.path.insert(0, "../config")
import settings

# raw data directory
dr = "../data/"
py_dir = dr + "pyobj_dir/"

def ld_ytr():
    print("Loading training targets")
    ytr = np.load(py_dir + "y_trn.npy")
    return ytr

def ld_yts():
    print("Loading testing targets")
    yts = np.load(py_dir + "y_tst.npy")
    return yts

def ld_trnset():
    settings.init()

    ytr = ld_ytr()
    n = len(ytr)

    print("Initiating memory for array of images")
    xtr = np.array([0] * (settings.a * settings.b * n)).reshape(n, settings.a, settings.b, settings.c)

    print("Adding dataset to X_train")
    for i in range(1, n + 1):

        f = dr + "anim/" + str(i) + ".bmp"
        img = misc.imread(f)
        xtr[i - 1] = img[:, :, :1]

    return (xtr, ytr)
 
def ld_tstset():
    settings.init()

    yts = ld_yts()
    m = len(yts)

    print("Initiating memory for array of images")
    xts = np.array([0] * (settings.a * settings.b * m)).reshape(m, settings.a, settings.b, settings.c)

    print("Adding dataset to X_test")
    n = next(i for i in range(m,-1, -1) if os.path.exists(dr + "anim/" + str(i+m) + ".bmp"))

    for i in range(n + 1, n + m + 1):
        f = dr + "anim/" + str(i) + ".bmp"
        img = misc.imread(f)
        xts[i - (n + 1)] = img[:, :, :1]

    print("Shuffling tests")
    idd = np.random.permutation(len(xts))
    xts, yts = xts[idd], yts[idd]

    return (xts, yts)

def ld_dtst():
    return (ld_trnset(), ld_tstset())
