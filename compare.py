"""
Created on Tue Apr 23 13:08:33 2019

@author: dan
"""

from PIL import Image, ImageOps
from copy import deepcopy
import numpy as np

SIZE = 16
e = 2.78
try:
    W = np.loadtxt('W.dat')
except OSError:
    W = np.zeros((SIZE,SIZE))
a = 0.5
IMG = {}

def dump(w, epoc):
    np.savetxt('W.%s.dat' % epoc, w)
    np.savetxt('W.dat', w)
    
    
def plot(w, epoc):
    from matplotlib import pyplot as plt

    ww = np.zeros((SIZE*20,SIZE*20))
    for x in range(SIZE * 20):
        for y in range(SIZE * 20):
            ww[x,y] = w[x//20,y//20]
    plt.imshow(ww, 'gray', vmin = -1, vmax = 30)
    plt.savefig("%s" % epoc)


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
    global a
    
    from os import listdir
    from os.path import isfile, join
    images = [ join('test', f) for f in listdir('test') if isfile(join('test', f))]

    Δ = [1] * len(images) * len(images)
    ΣΔ = 100
    n = 0
    while n < 10: # sum(Δ) - ΣΔ < 0 and 
        ΣΔ = sum(Δ)
        i = 0
        for img1 in images:
            class1 = img1.split('.')[0]
            for img2 in images:
                class2 = img2.split('.')[0]
                y = 1 if class1 == class2 else 0
                W = update_w(W, img1, img2, y)
                r = compare(img1, img2)
                Δ[i] = abs(y - r)
                i += 1
        plot(W, n)
        dump(W, n)
        print(n, sum(Δ))
        a = sum(Δ) - ΣΔ
        n += 1


def update_w(w, img1, img2, y):
    for x in range(SIZE):
        for y in range(SIZE):
            w[x,y] += a * (compare(img1, img2) - y) * δ(img1, img2, x, y)
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
    return (σ(sum(D)**1/2)-1/2)*2


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
                        'text' : "да" if x > 0.9 else "похожи" if x > 0.5 else "нет",
                }]
    resylt = sorted(resylt, key=lambda x: x['q'])
    print (dumps(resylt, ensure_ascii=0, indent=2))


if __name__ == '__main__':
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == 'train':
        train()
    else:
        test()