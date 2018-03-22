"""Module capable of generating an animation made of 
geometrical shapes moving around randomly on a screen.
"""

import pygame
import random as rd
import numpy as np

import os
import sys
CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.dirname(CURRENT_DIR))

from constants import nb_images_train, nb_images_test, nb_obj, a, b, c
from utils import normalized_sigmoid_fkt as sig_moid
sigmoid = lambda x: sig_moid(x, a=0.2, b=14)

np.random.seed(123)

dflt_dir = "../data/"
if not os.path.exists(dflt_dir):
    os.makedirs(dflt_dir)
    print("Created cached directory to store the generated files")

py_sv = dflt_dir + "pyobj_dir/"
if not os.path.exists(py_sv):
    os.makedirs(py_sv)

trnset_arr = "y_trn.npy"
tstset_arr = "y_tst.npy"

trnset_sv = py_sv + trnset_arr
tstset_sv = py_sv + tstset_arr

anim_dir = dflt_dir + "anim/"
if not os.path.exists(anim_dir):
    os.makedirs(anim_dir)


black = 0, 0, 0
white = 255, 255, 255
red = 80, 80, 80
green = 150, 150, 150
blue = 0, 0, 0
blue = green = red = white  # might be temporary
colors = [red, green, blue]
incr = -400
nb_images = nb_images_train + nb_images_test

square_size = 20
circle_radius = 20
size = width, height = 300, 200

x = 50
left_edge = x
right_edge = x + a
top_edge = 0
bottom_edge = b

pygame.init()
screen = pygame.display.set_mode(size)


def random_color():
    i = rd.randrange(len(colors))
    return colors[i]


def random_speed():
    """Produces a random speed when called
    	:return [a, b]
    	:a : float in [-2; -1] or [1; 2]
    	:b : same
    """
    dirx, diry = rd.randint(0, 1), rd.randint(0, 1)
    return [rd.uniform(1, 2) * (-1) ** dirx, rd.uniform(1, 2) * (-1) ** diry]


class Obj():
    """ Objects that will pass through the screen """

    def __init__(self, rect, img=None, shape=None, color=None):
        self.rect = rect
        self.speed = random_speed()
        self.img = img
        self.color = random_color() if color is None else color
        self.shape = shape


obj_patterns = []
li_obj = []

ball = pygame.image.load("ball.bmp")
ballrect = ball.get_rect()


def new_square():
    """Pops a new square either on the right or the left of the screen
    (chosen randomly)
    """
   
    choice = rd.randint(0, 1)
    squarect = pygame.Rect(0 if choice else width - x, rd.randrange(height - x),
                           square_size, square_size)
    return squarect, None, "square"


def new_circle():
    """Pops a new circle"""

    choice = rd.randint(0, 1)
    circle_rect = pygame.Rect(0 if choice else width - 2 * circle_radius,
                              rd.randrange(
                                  height - 2 * circle_radius), 2 * circle_radius,
                              2 * circle_radius)
    return circle_rect, None, "circle"


def new_ball():
    return ball.get_rect(), ball

obj_patterns.append(new_square)
obj_patterns.append(new_circle)
# obj_patterns.append(new_ball)


def add_obj():
    """ Génère un objet pris au hasard parmi les types possibles """
    i = rd.randrange(len(obj_patterns))
    r, img, shape = obj_patterns[i]()
    li_obj.append(Obj(r, img, shape=shape))

# Génère les objets de l'animation
#r, img = new_ball()
#li_obj.append(Obj(r, img))
r, img, _ = new_circle()
li_obj.append(Obj(r, img, shape="circle"))
r, img, _ = new_square()
li_obj.append(Obj(r, img, shape="square"))


# Already added 2 objs
for _ in range(nb_obj - 2):
    add_obj()


def bounce(obj):
    rect, speed = obj.rect, obj.speed
    obj.rect = rect.move(speed)
    if obj.rect.left < 0 or obj.rect.right > width:
        obj.speed[0] *= -1
        r = rd.random()
        if r > 0.5:
            obj.speed[1] *= -1
    if obj.rect.top < 0 or obj.rect.bottom > height:
        obj.speed[1] *= -1
        r = rd.random()
        if r > 0.5:
            obj.speed[0] *= -1


def in_screen(obj):
    if obj.rect.left > left_edge and obj.rect.right < right_edge and \
       obj.rect.top > top_edge and obj.rect.bottom < bottom_edge:
        return 1.
    else:
        return abs(sigmoid(portion_in_screen(obj)))
        # return 0


def portion_in_screen(obj):
    w_prop = 0.
    h_prop = 0.
    if obj.rect.right < left_edge or obj.rect.left > right_edge or \
       obj.rect.top > bottom_edge:
        return 0.
    if obj.rect.right >= left_edge and obj.rect.left <= left_edge:
        w_prop = (obj.rect.right - left_edge) / obj.rect.width
    elif obj.rect.left <= right_edge and obj.rect.right >= right_edge:
        w_prop = (right_edge - obj.rect.left) / obj.rect.width
    if obj.rect.bottom >= top_edge and obj.rect.top < top_edge:
        h_prop = (obj.rect.bottom - top_edge) / obj.rect.height
    elif obj.rect.top <= bottom_edge and obj.rect.bottom >= bottom_edge:
        h_prop = (bottom_edge - obj.rect.top) / obj.rect.height
    return (w_prop if h_prop == 0. else (h_prop if w_prop == 0. else (w_prop + h_prop) / 2))


def dist(u, v):
    (x, y), (z, t) = u, v
    return sqrt((x - z)**2 + (y - t)**2)


def in_obj(x, y, obj):
    """ Is this pixel in the obj or not ? """
    if obj.shape == "square":
        if x >= obj.rect.left and x <= obj.rect.right and y >= obj.rect.top and y <= obj.rect.bottom:
            return 1.
        else:
            return 0.
    elif obj.shape == "circle":
        if dist(obj.rect.center, (x, y)) <= circle_radius:
            return 1.
        else:
            return 0.
    print("Error in in_obj")

if len(sys.argv) <= 2:
    print("Default directory for saving images:", dflt_dir)
    data_dir = dflt_dir
else:
    data_dir = sys.argv[2]

# Gère l'enregistrement des images générées
if len(sys.argv) > 1 and sys.argv[1] == "-s":
    print("Saving animation and monitoring at", dflt_dir)
    eventual_output = lambda: pygame.image.save(
        screen, anim_dir + str(incr) + ".bmp")
else:
    eventual_output = lambda: None
    print("Not saving anything. Use argument -s to save in", dflt_dir)

# Contiennent les "bonnes réponses"
# +1 car on ajoute -1 au début
y_train = np.array([0.] * (nb_images_train * (nb_obj))
                   ).reshape(nb_images_train, nb_obj)
y_test = np.array([0.] * (nb_images_test * (nb_obj))
                  ).reshape(nb_images_test, nb_obj)

# un peu complexe : pour chaque pixel (a*b dans chaque image), on stocke à
# chaque instant (nb_images instants) son appartenance aux différents objets
# sous forme d'une indicatrice (nb_obj objets)
# y_train_temp = np.array([0.] * (a*b * nb_images_train * nb_obj)
#                   ).reshape(a*b, nb_images_train, nb_obj)
# y_test_temp = np.array([0.] * (a*b * nb_images_test * nb_obj)
#                  ).reshape(a*b, nb_images_test, nb_obj)

# Déroulement de l'animation
while incr <= nb_images:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    # drawing the image
    screen.fill(black)
    for o in li_obj:
        bounce(o)
        if o.shape == "square":
            pygame.draw.rect(screen, o.color, o.rect)
        elif o.shape == "circle":
            x_pos, y_pos = o.rect.left + circle_radius, o.rect.top + circle_radius
            pygame.draw.circle(screen, o.color, (x_pos, y_pos), circle_radius)
        else:
            screen.blit(o.img, o.rect)

    # refresh the screen. useless for training, but ok for visualizing thedata
    # being generated
    pygame.display.flip()

    # Remplit les vecteurs de présence des différents objets
    # Taille nb_obj
    if incr <= nb_images_train and incr > 0:
        for i, o in enumerate(li_obj):
            y_train[incr - 1][i] = in_screen(o)

#        for x in range(a):
#            for y in range(b):
#                for (i, o) in enumerate(li_obj):
#                    y_train_temp[g(x,y)][incr-1][i] = in_obj(x,y,o)

    elif incr > nb_images_train:
        for i, o in enumerate(li_obj):
            y_test[incr - (nb_images_train + 1)][i] = in_screen(o)

#        for x in range(a):
#            for y in range(b):
#                for (i, o) in enumerate(li_obj):
#                    y_test_temp[g(x,y)][incr-(nb_images_train+1)][i] = in_obj(x,y,o)

    # Enregistre l'image selon la situation
    if incr > 0:
        eventual_output()

    incr += 1


# Cropping images and drawing score
if 1:
    from PIL import Image, ImageFont, ImageDraw
#    font = ImageFont.truetype("sans-serif.ttf", 16)
    box = (left_edge, top_edge, right_edge, bottom_edge)
    ind_pic = 1
    y_trn_ind = []
    y_tst_ind = []
    for i in range(1, nb_images + 1):
        img_path = anim_dir + str(i) + ".bmp"
        try:
            img = Image.open(img_path)
        except:
            print("Program exiting.")
            print("Maybe you forgot to use -s and have no files saved yet.")
            sys.exit(0)

        area = img.crop(box)
        y = y_train[i - 1] if i <= nb_images_train else y_test[i -
                                                               (nb_images_train + 1)]
        l = [(i + 1) for i in range(nb_obj)]
        if sum(y) == 0.:
            # if sum(y) not in l:
            os.remove(img_path)
            print("Removed", img_path)
        else:
            text = str(y)
            area.save(anim_dir + str(ind_pic) + ".bmp", "BMP")
            draw = ImageDraw.Draw(area)
            draw.text((0, 0), text, (255, 255, 255))
            monit_dir = dflt_dir + "monitor/"
            if not os.path.exists(monit_dir):
                os.makedirs(monit_dir)
            area.save(monit_dir + str(ind_pic) + ".bmp", "BMP")
            ind_pic += 1
            if i <= nb_images_train:
                y_trn_ind.append(i - 1)
            else:
                y_tst_ind.append(i - (nb_images_train + 1))


y_train = y_train[y_trn_ind]
y_test = y_test[y_tst_ind]

print("Saving y_train and y_test to", py_sv)
np.save(trnset_sv, y_train)
np.save(tstset_sv, y_test)

#print("Saving y_train_temp and y_test_temp to", path_train_temp, "and", path_test_temp)
#np.save(py_sv + , y_train_temp)
#np.save(path_test_temp, y_test_temp)
