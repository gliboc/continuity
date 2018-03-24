"""Just for testing :
    - image generation
    - network import
    - network training
"""

import sys
sys.path.insert(0, "../munge")

from subprocess import call
call(["python", "../munge/animation.py", "-s"])

import model
m = model.deep_network()
model.train_model(m)
