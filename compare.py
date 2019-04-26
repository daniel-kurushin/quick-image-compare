"""
Created on Tue Apr 23 13:08:33 2019

@author: dan
"""

from PIL import Image, ImageOps

SIZE = 16 
e = 2.78

def σ(x):
    return 1 / (1 + e**(-x))

def compare(img1, img2):
    img1 = ImageOps.grayscale(Image.open(img1).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
    img2 = ImageOps.grayscale(Image.open(img2).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            a = σ(img1.getpixel((x,y)) / 255)
            b = σ(img2.getpixel((x,y)) / 255)
            D += [(a-b)**2]
#    print(D)
    return sum(D)**1/2

if __name__ == '__main__':
    test = ['test/img1.png', 'test/img2.png',  'test/img3.png', 'test/sigma1.png', 'test/sigma2.png']
    for img1 in test:
        for img2 in test:
            x = compare(img1, img2)
            print("%s <=> %s (%s) %s" % (img1, img2, round(x,2), "да" if x < 0.02 else "похожи" if x < 0.4 else "нет"))
    test = [ 'test/a%s.png' % i for i in range(1,9) ]
    for img1 in test:
        for img2 in test:
            x = compare(img1, img2)
            print("%s <=> %s (%s) %s" % (img1, img2, round(x,2), "да" if x < 0.02 else "похожи" if x < 0.4 else "нет"))
    test = [ 'test/b%s.png' % i for i in range(1,12) ]
    for img1 in test:
        for img2 in test:
            x = compare(img1, img2)
            print("%s <=> %s (%s) %s" % (img1, img2, round(x,2), "да" if x < 0.02 else "похожи" if x < 0.4 else "нет"))
    