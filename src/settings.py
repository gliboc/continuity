"""Set of hyperparameters
"""

def init():
  # for convolution layers
  global kernel_size, filters, batch_size, nb_epochs
  kernel_size = (3, 3)
  filters = 32
  batch_size = 8
  nb_epochs = 5

  # img generation
  global nb_obj, nb_imgs, test_proportion, nb_images_train, nb_images_test
  nb_obj = 2
  nb_imgs = 6000
  test_proportion = 0.5
  nb_images_train = int(nb_imgs * (1 - test_proportion))
  nb_images_test = int(nb_imgs * test_proportion)

  # image size
  global a, b, c
  a, b, c = 300,300, 1  # width, height
