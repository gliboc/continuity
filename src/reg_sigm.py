#! /usr/bin/python
# faire de la regression temporelle sur un jeu de données tronqué

from load_modules import *
import seaborn

output_file("sigmoidRegression.html")

from math import exp, tan, pi
from utils import normalized_sigmoid_fkt as sigmoid

# Quatres cas différents pour interpoler entre deux points :
# 0 - 0 : cloche de hauteur a_t
# 1 - 1 : creux de fond a_b
# 0 - 1 et 1 - 0 : sigmoïdes de paramètres

# raw sigmoid is a good function for 1 - 0 normalized situation


#x = np.linspace(0, 1, 500)
#y = sigmoid(x)

# le dataset à traiter est encodée sous la forme :
# - données de supervision (numpy array, il y en a strictement moins que la nombre d'images)
# - identifiants des images pour lesquelles il y a supervision
# - nombre total d'images
with open("x_regression.data", "rb") as fp:
    x = np.load(fp)

with open("x_regression_add.data", "rb") as fp:
    ids = pickle.load(fp)
    nb_imgs = pickle.load(fp)

n = len(ids)
y = np.array([0.] * nb_imgs)

# 4 fonctions pour les 4 cas
# normalisées à [0,1]


def f(x1, x2, x, k=1):
    if x == x2:
        return 1.
    elif x == x1:
        return 0.
    a = pi / (x2 - x1)
    b = pi * (x1 + x2) / (2 * (x1 - x2))
    return 1. / (1. + exp(-k * tan(a * x + b)))


def g(x1, x2, x, k=1):
    return 1. - f(x1, x2, x, k=k)

alpha = 0.5

# décroissante


def h(x1, x2, x):
    return alpha + g(x1, x2, x, k=2)


def w(x1, x2, x):
    return alpha + f(x1, x2, x, k=2)


def regression_function(i, x1, y1, x2, y2):
    x = (i - x1) / (x2 - x1)
    return case_funs[y1, y2](x)


i = 0
# if ids[0] != 0:
#    raise Exception("Première valeur de supervision non connue"
# if ids[-1] != nb_imgs-1:
#    raise Exception("Dernière valeur de supervision non connue"
for j in range(n - 1):
    current_index = ids[j]
    if i == current_index:
        y[i] = x[j]
        i += 1
        continue
    elif i < current_index:
        prev_index = ids[j - 1]
        for k in range(i, current_index):
            y[k] = regression_function(
                k, prev_index, x[j - 1], current_index, x[j])
            i += 1
        y[i] = x[j]
        i += 1
        continue
    else:
        if 0:
            pass
#        if j != n-2:
#            raise Exception("Erreur dans l'algorithme")
        else:
            next_index = ids[j + 1]
        #    if next_index != nb_imgs-1:
        #        raise Exception("Prévisions fausses pour dernière valeur de next_index")
            for k in range(i, next_index):
                y[k] = regression_function(
                    k, current_index, x[j], next_index, x[next_index])
                i += 1
            continue
# if i != nb_imgs:
#    raise Exception("Erreur sur la valeur finale de i")


pl = figure()
#p.vbar(x=x, top=y, width=0.1)
pl.line([i for i in range(nb_imgs)], y, line_width=0.5)
show(pl)
