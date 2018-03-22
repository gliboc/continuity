# utilitary functions

import numpy as np
from constants import a, b

def normalized_sigmoid_fkt(x, a=0.2, b=14):
    '''
    Returns array of a horizontal mirrored normalized sigmoid function
    output between 0 and 1
    prefer normalized output between 0 and 1
    Function parameters a = center; b = width
    '''
    f = lambda s: 1. / (1. + np.exp(b * (s - a)))
    return (f(x) - f(0)) / (f(1) - f(0))  # normalize function to 0-1
