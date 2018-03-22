#! /usr/bin/python

# Load a model saved and evaluates it in X_train data (why not X_test ?)

from keras.models import model_from_json

json_file = open("model.json", "r")
load_model_json = json_file.read()
json_file.close()

loaded_model = model_from_json(load_model_json)

loaded_model.load_weights("model.h5")
loaded_model.compile(loss="mean_squared_error", optimizer="adam",
                     metrics=["accuracy"])

from load_dataset import X_train, Y_train

score = loaded_model.evaluate(X_train, Y_train, verbose=1)
print("%s: %.2f%%" % (loaded_model.metrics_names[1], score[1] * 100))
