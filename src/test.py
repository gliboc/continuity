from model import *
from subprocess import call

call("python", "../munge/animation.py -s")
m = deep_network()
train_model(m, 1)
