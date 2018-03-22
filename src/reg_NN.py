#! /usr/bin/python
# faire de la regression temporelle sur un jeu de données tronqué

import tensorflow as tf
from load_modules import *

import seaborn

output_file("RegNeuralNetwork.html")

from math import exp
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
    y_values = np.load(fp)

with open("x_regression_add.data", "rb") as fp:
    x_values = pickle.load(fp)
    nb_imgs = pickle.load(fp)

w_variables = [tf.Variable([0.0], dtype=tf.float32)] + \
    [tf.Variable([rd.uniform(-1, 1)], dtype=tf.float32) for _ in range(5)]
x = tf.placeholder(dtype=tf.float32)
y = tf.placeholder(dtype=tf.float32)

polynomial_model = tf.add_n([w_variables[i] * (x ** i)
                             for i in range(len(w_variables))])
loss = tf.reduce_sum(tf.square(polynomial_model - y)) + \
    tf.reduce_sum(tf.square(w_variables))
annotated_loss = tf.summary.scalar("loss rate", loss, collections=None)
init = tf.global_variables_initializer()
sess = tf.Session()

optimizer = tf.train.GradientDescentOptimizer(0.01)
train = optimizer.minimize(loss)
sess.run(init)

writer = tf.summary.FileWriter("log")

for i in range(10):
    merged = tf.summary.merge_all()
    summary, graph = sess.run([merged, train], {x: x_values, y: y_values})
    writer.add_summary(summary, i)
    writer.add_graph(tf.get_default_graph())

res = sess.run(w_variables)


def eval(p, x):
    s = 0
    for a in p:
        s *= x
        s += a

pl = figure()

#p.vbar(x=x, top=y, width=0.1)
pl.line([i for i in range(nb_imgs)], [eval(w_variables, x)
                                      for x in range(nb_imgs)], line_width=0.5)
show(pl)
