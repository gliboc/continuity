"""This module tests what happens to the
accuracy when training using only a portion of
the training set
"""

import os
import numpy as np

from bokeh.io import output_notebook, output_file
from bokeh.plotting import figure

import sys
sys.path.insert(0, "../config")
import settings

settings.init()

sys.path.insert(0, "../src")
import model
import load_dataset

((xtr, ytr), (xts, yts)) = load_dataset.ld_dtst()

# output_file("../graphs/less_supervision_test.html")
output_notebook()

pl = figure(title="Dataset size impact on accuracy", tools="save",
            background_fill_color="#E8DDCB")

ratios = [0.01, 0.02, 0.05, 0.08, 0.1, 0.2, 0.5, 1.]
accuracies = []
for supervision_ratio in ratios:
    nb_values = len(xts)
    m = model.deep_network()
    select = np.linspace(0, nb_values - 1, int(supervision_ratio * nb_values), dtype=int)
    if len(select) == 0:
        print("Training set is empty !")
        continue
    model.train_model(m, data=(xtr[select], ytr[select]) )
    score = model.eval_model(m, data=(xts, yts))

    accuracies.append(score[1])

sv_dir = "../logs/less_supervision_test/"
if not(os.path.exists("../logs")):
    os.makedirs("../logs")
if not(os.path.exists(sv_dir)):
    os.makedirs(sv_dir)

num = 0
name_save = lambda i: sv_dir + "-" + str(i) + '.save'
while os.path.isfile(name_save(num)):
    num += 1

with open(name_save(num), 'wb') as fp:
    pickle.dump(x, fp)
    pickle.dump(y, fp)

pl.xaxis.axis_label = "taux de supervision"
pl.yaxis.axis_label = "accuracy"
pl.line(x, y, line_width=0.5)
show(pl)
