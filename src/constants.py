# for convolution layers
kernel_size = (3, 3)
filters = 32
batch_size = 8
nb_epochs = 5


# continuity
p = 0.5  # supervision parameter

# img generation
nb_obj = 2
nb_imgs = 6000
test_proportion = 0.5
nb_images_train = int(nb_imgs * (1 - test_proportion))
nb_images_test = int(nb_imgs * test_proportion)

# image size
a, b, c = 300,300, 1  # width, height
