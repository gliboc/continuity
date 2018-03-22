"""
Function used for manually labelling a video
"""

import sys 
import numpy as np

m = input("Hello, type S to start, E to end\n")

animals = ["l", "g", "e"]
inter = {x : [] for x in animals}
count = {x : 0 for x in animals}
save = {x : None for x in animals}

while m != "end":
    m = sys.stdin.readline().strip()
    if m == "":
        break
    if m[0] not in animals:
        print("Ignoring", m)
        continue

    if m[0] == "end":
        print("Fin")
        break
    elif m[0] not in animals:
        print("Erreur d'entrée")
    else:
        x = m[0]
        if count[x] == 0:
            mi, se = map(int, m[1:].split(":"))
            time = mi*60+se
            save[x] = time
            count[x] = 1
        else:
            mi, se = map(int, m[1:].split(":"))
            time = mi*60+se
            inter[x].append((save[x], time))
            count[x] = 0
            print("Saved ({}, {}) intervals to {}".format(save[x], time, x))

import pickle

pickle.dump(inter, open("labels.save", "wb"))
