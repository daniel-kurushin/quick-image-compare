"""
Created on Tue Apr 23 13:08:33 2019

@author: dan
"""

from PIL import Image, ImageOps
from copy import deepcopy

SIZE = 24
e = 2.78
W = [[0]*24]*24

def σ(x):
    return 1 / (1 + e**(-x))

def train(img1, img2, y):
    w = deepcopy(W)
    for x in range(SIZE):
        for y in range(SIZE):
            w[x][y] += a * (compare(img1, img2) - y)'
    return w

def compare(img1, img2):
    img1 = ImageOps.grayscale(Image.open(img1).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
    img2 = ImageOps.grayscale(Image.open(img2).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            a = σ(img1.getpixel((x,y)) / 255)
            b = σ(img2.getpixel((x,y)) / 255)
            D += [(a-b)**2] * W[x][y]
#    print(D)
    return sum(D)**1/2

if __name__ == '__main__':
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