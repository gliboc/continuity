#! /usr/bin/python

from load_modules import *
from load_dataset import *
from kMeans import naive_reg, dist

output_file("RandomSpatialReg.html")

pl = figure(title="Spatial regression with random samples", tools="save",
            background_fill_color="#E8DDCB")

x = [0.01, 0.02, 0.05, 0.08, 0.1, 0.2, 0.5, 1.]


y = []
for p in x:
    # taking random images for supervision
    if p < 1.:
        given_i = rd.sample(list(range(1, nb_values - 1)), int(nb_values * p))
        given_i.sort()
        given_i = [0] + given_i + [nb_values - 1]
    else:
        given_i = list(range(nb_values))
    given_v = Y_train[given_i]

    Y_tr = naive_reg(nb_values, given_v, given_i, X_train)

    idx = np.random.permutation(len(X_train))
    score = training.main(p, nb_epochs, data=(
        X_train[idx], X_test, Y_tr[idx], Y_test))
    y.append(score[1])



i = 1
name_save = lambda i: 'saves/spatialRandom' + str(i) + '.save'
while os.path.isfile(name_save(i)):
    i += 1

with open(name_save(i), 'wb') as fp:
    pickle.dump(x, fp)
    pickle.dump(y, fp)

pl.xaxis.axis_label = "taux de supervision"
pl.yaxis.axis_label = "accuracy"


pl.line(x, y, line_width=0.5)

show(pl)
