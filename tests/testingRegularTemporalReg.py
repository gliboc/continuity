#! /usr/bin/python

from load_modules import *
from load_dataset import *

output_file("RegularTemporalReg.html")


pl = figure(title="Temporal regression with regular samples", tools="save",
            background_fill_color="#E8DDCB")

#x = [0.01*i for i in range(1, 21)] + [0.2 + 0.1*i for i in range(1, 8)] + [1.]
x = [0.01, 0.02, 0.05, 0.08, 0.1, 0.2, 0.5, 1.]

pl.xaxis[0].ticker = FixedTicker(ticks=x)
pl.xaxis.major_label_orientation = pi / 6

y = []
from regressionConstants import reg_lin

for p in x:
    given_i = np.linspace(0, nb_values - 1, int(nb_values * p), dtype=int)
    given_v = Y_train[given_i]

    Y_tr = reg_lin(nb_values, given_v, given_i)

    idx = np.random.permutation(len(X_train))

    score = training.main(p, nb_epochs, data=(
        X_train[idx], X_test, Y_tr[idx], Y_test))
    y.append(score[1])


i = 1
name_save = lambda i: 'saves/regularTemporal' + str(i) + '.save'
while os.path.isfile(name_save(i)):
    i += 1

with open(name_save(i), 'wb') as fp:
    pickle.dump(x, fp)
    pickle.dump(y, fp)

pl.xaxis.axis_label = "taux de supervision"
pl.yaxis.axis_label = "accuracy"


pl.line(x, y, line_width=0.5)

show(pl)
