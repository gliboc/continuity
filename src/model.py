"""Definition of my CNN model
Training function
Evaluation function
"""

import sys
# visualisations with tensorboard
from keras.callbacks import TensorBoard

def deep_network():
    
    # importing hyper-parameters
    from constants import a, b, c, nb_obj, kernel_size, filters, batch_size

    # Sequential model type: simple linear stack of neural network layers
    from keras.models import Sequential

    # core layers (most used)
    from keras.layers import Dense, Dropout, Activation, Flatten

    # cnn layers
    from keras.layers import Convolution2D, MaxPooling2D

    # utilities
    from keras.utils import np_utils

    # just for testing
    from keras.datasets import mnist

    # actual model
    model = Sequential()

    # input layer
    model.add(Convolution2D(filters, kernel_size,
                            activation='relu', input_shape=(a, b, c)))

    # more layers
    model.add(Convolution2D(filters, kernel_size, activation='relu'))
    # reduce the number of parameters
    model.add(MaxPooling2D(pool_size=(2, 2)))

    # additionnal random layer...
    #model.add(Convolution2D(128, (3, 3), activation='relu', padding='same'))
    # model.add(Dropout(0.2))
    #model.add(MaxPooling2D(pool_size=(2, 2)))

    # important to regularize the model and prevent overfitting
    model.add(Dropout(0.25))

    model.add(Flatten())
    model.add(Dense(128, activation='relu'))
    model.add(Dropout(0.5))
    # +1 because of interactivity detection
    # enlever pour le test
    #model.add(Dense(nb_obj, activation='softmax'))

    model.add(Dense(5, activation='sigmoid'))
    # compile model

    loss_type = "mean_squared_error"
    # other loss : categorical_crossentropy
    model.compile(loss=loss_type,
                  optimizer='adam',
                  metrics=['accuracy'])

    return model

def train_model(model, nb_epochs, data=None):

    from constants import a, b, c, nb_obj, kernel_size, filters, batch_size

    # Load self-generated data into train and test sets
    # the images are in format (a, b, c)
    from load_dataset import ld_dtst
    ((xtr, ytr), (xts, yts)) = ld_dtst()

    xtr = xtr.astype('float32')
    xtr /= 255

    # fit model
    tbCallBack = TensorBoard(log_dir='../logs', histogram_freq=1, write_graph=True,
                             write_images=True,
                             embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)

    model.fit(xtr, ytr, batch_size=batch_size, epochs=nb_epochs, verbose=1, callbacks=[tbCallBack],)


def eval_model(model):
    X_test /= 255
    X_test = X_test.astype('float32')
    print("Evaluating model")
    score = model.evaluate(X_test, Y_test, verbose=1)
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
