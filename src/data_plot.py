from bokeh.plotting import figure, show, output_file
import pickle
from glob import glob
from load_modules import *


output_file("resu-apercu.html")

def interactive_visu1():
    i = input("Quel jeu de données voulez-vous visualiser ?\nAperçu fichiers : " +
              " ".join(glob("semi-sup*.save")) + "\n")

    try:
        w = float(input("Largeur des barres ?\nDefault = 0.5\n"))
    except:
        w = 0.5

    with open("semi-sup" + i + ".save", "rb") as fp:
        x = pickle.load(fp)
        y = pickle.load(fp)

    pl = figure(title="Semi-supervision impact",
                tools="save", background_fill_color="#E8DDCB")

    pl.xaxis.axis_label = "taux de supervision"
    pl.yaxis.axis_label = "accuracy"

    pl.line(x, y, line_width=w)
    #pl.vbar(x=x, top=y, width=w)
    show(pl)

def interactive_visu2():
    i = input("Quel jeu de données voulez-vous visualiser ?\nAperçu fichiers : " +
              " ".join(glob("semi-sup*.save")) + "\n")

    name = input("Nom du fichier à enregister ?\n")
    output_file(name + ".html")
    try:
        w = float(input("Largeur des barres ?\nDefault = 0.5\n"))
    except:
        w = 0.5

    with open("semi-sup" + i + ".save", "rb") as fp:
        x = pickle.load(fp)
        y = pickle.load(fp)

    pl = figure(title="Semi-supervision impact",
                tools="save", background_fill_color="#E8DDCB")

    pl.xaxis.axis_label = "taux de supervision"
    pl.yaxis.axis_label = "accuracy"

    pl.line(x, y, line_width=w)
    #pl.vbar(x=x, top=y, width=w)
    show(pl)
