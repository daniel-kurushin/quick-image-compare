"""
Created on Tue Apr 23 13:08:33 2019

@author: dan
"""

from PIL import Image, ImageOps
from copy import deepcopy
import numpy as np

SIZE = 16
e = 2.78
W = np.zeros((SIZE,SIZE))
a = 0.5
IMG = {}
epoc = 0

def plot(w):
    global epoc
    
    from matplotlib import pyplot as plt
    ww = np.zeros((SIZE*20,SIZE*20))
    for x in range(SIZE * 20):
        for y in range(SIZE * 20):
            ww[x,y] = w[x//20,y//20]
    plt.imshow(ww)
    plt.savefig("%s" % epoc)
    epoc += 1

def get_image(img):
    global IMG

    try:
        return IMG[img]
    except KeyError:
        data = ImageOps.grayscale(Image.open(img).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
        IMG.update({img:data})
        return data
        
def train():
    global W

    from os import listdir
    from os.path import isfile, join
    from json import dumps
    images = [ join('test', f) for f in listdir('test') if isfile(join('test', f))]

    Δ = [1] * len(images) * len(images)
    while sum(Δ) > 3:
        i = 0
        for img1 in images:
            class1 = img1.split('.')[0]
            for img2 in images:
                class2 = img2.split('.')[0]
                y = 0 if class1 == class2 else 1
                W = deepcopy(update_w(img1, img2, y))
                r = compare(img1, img2)
                Δ[i] = abs(y - r)
                print(img1, img2, y, r)
                i += 1
        plot(W)
        print("sum = %s" % sum(Δ))


def update_w(img1, img2, y):
    w = deepcopy(W)
    for x in range(SIZE):
        for y in range(SIZE):
            w[x,y] += a * (y - compare(img1, img2)) * δ(img1, img2, x, y)
    return w


def σ(x):
    return 1 / (1 + e**(-x))


def δ(img1, img2, x, y):
    img1 = get_image(img1)
    img2 = get_image(img2)
    a = σ(img1.getpixel((x,y)) / 255)
    b = σ(img2.getpixel((x,y)) / 255)
    return (a-b)**2


def compare(img1, img2):
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            v = δ(img1, img2, x, y)
            D += [v * W[x,y]]
#    print(D)
    return σ(sum(D)**1/2)-1/2


def test():
    from os import listdir
    from os.path import isfile, join
    from json import dumps
    test = [ join('test', f) for f in listdir('test') if isfile(join('test', f))]
    compared = []
    resylt = []
    for img1 in test:
        for img2 in test:
            to_compare = {img1, img2}
            if img1 != img2 and to_compare not in compared:
                x = compare(img1, img2)
                compared += [to_compare]
                resylt += [{
                        'img1' : img1,
                        'img2' : img2,
                        'q'    : round(x,5),
                        'text' : "да" if x < 0.07 else "похожи" if x < 0.7 else "нет",
                        'col'  : 0 if x < 0.07 else 1 if x < 0.7 else 2,
                }]
    resylt = sorted(resylt, key=lambda x: x['q'])
    print (dumps(resylt, ensure_ascii=0, indent=2))


if __name__ == '__main__':
    train()
    test()