"""Definition of my CNN model
Training function
Evaluation function
"""

import settings
import sys

from keras.callbacks import TensorBoard

from keras.models import Sequential   # sequential model type: simple linear stack of neural network layers
from keras.layers import Dense, Dropout, Activation, Flatten   # core layers (most used)
from keras.layers import Convolution2D, MaxPooling2D   # cnn layers
from keras.utils import np_utils
from keras.datasets import mnist

import load_dataset as ld

def deep_network():
    settings.init()

    model = Sequential()

    # input layer
    model.add(Convolution2D(filters, kernel_size,
                            activation='relu', input_shape=(settings.a, settings.b, settings.c)))
    model.add(Convolution2D(settings.filters, settings.kernel_size, activation='relu'))
    model.add(MaxPooling2D(pool_size=(2, 2)))    # reduce the number of parameters

    # additionnal random layer...
    #model.add(Convolution2D(128, (3, 3), activation='relu', padding='same'))
    # model.add(Dropout(0.2))
    #model.add(MaxPooling2D(pool_size=(2, 2)))

    model.add(Dropout(0.25))   # important to regularize the model and prevent overfitting
    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    # +1 because of interactivity detection
    # enlever pour le test
    #model.add(Dense(nb_obj, activation='softmax'))

    model.add(Dense(5, activation='sigmoid'))

    loss_type = "mean_squared_error"    # other loss : categorical_crossentropy

    model.compile(loss=loss_type,
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

def train_model(model, nb_epochs, data=None):
    settings.init()

    (xtr, ytr) = ld.ld_trnset()

    xtr = xtr.astype('float32')
    xtr /= 255

    # fit model
    tbCallBack = TensorBoard(log_dir='../logs', histogram_freq=1, write_graph=True,
                             write_images=True,
                             embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)

    model.fit(xtr, ytr, batch_size=settings.batch_size, epochs=settings.nb_epochs, verbose=1, callbacks=[tbCallBack],)


def eval_model(model):
    settings.init()

    (xts, yts) = ld.ld_tstset() 

    xts /= 255
    xts = xts.astype('float32')
    print("Evaluating model")
    score = model.evaluate(xts, yts, verbose=1)
    print(score)

    if "save" in sys.argv:
        print("Saving model")
        # serialize model to JSON
        model_json = model.to_json()
        with open("model.json", "w") as json_file:
            json_file.write(model_json)

        # serialize weights to HDF5
        model.save_weights("model.h5")
        print("Saved model to disk")

    return score
