#! /usr/bin/python

from load_modules import *
from load_dataset import X_train, Y_train, X_test, Y_test, nb_values

output_file("lessSupervisionRegular.html")


pl = figure(title="Dataset size impact on accuracy", tools="save",
            background_fill_color="#E8DDCB")

#x = [0.01*i for i in range(1, 21)] + [0.2 + 0.1*i for i in range(1, 8)] + [1.]
x = [0.01, 0.02, 0.05, 0.08, 0.1, 0.2, 0.5, 1.]


y = []
for p in x:
    select = np.linspace(0, nb_values - 1, int(p * nb_values), dtype=int)
    
    score = training.main(p, nb_epochs, data=(
        X_train[select], X_test, Y_train[select], Y_test))
    y.append(score[1])



i = 1
name_save = lambda i: 'saves/data-set-size' + str(i) + '.save'
while os.path.isfile(name_save(i)):
    i += 1

with open(name_save(i), 'wb') as fp:
    pickle.dump(x, fp)
    pickle.dump(y, fp)

pl.xaxis.axis_label = "taux de supervision"
pl.yaxis.axis_label = "accuracy"


pl.line(x, y, line_width=0.5)

show(pl)
