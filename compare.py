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
    D = []
    for x in range(SIZE):
        for y in range(SIZE):
            a = σ(img1.getpixel((x,y)) / 255)
            b = σ(img2.getpixel((x,y)) / 255)
            D += [(a-b)**2]
#    print(D)
    return sum(D)**1/2

if __name__ == '__main__':
    try:
        import sys
        assert sys.argv[1] and sys.argv[2]
        img1, img2 = sys.argv[1], sys.argv[2]
        i1 = ImageOps.grayscale(Image.open(img1).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
        i2 = ImageOps.grayscale(Image.open(img2).resize(size = (SIZE,SIZE), resample = Image.HAMMING))
        x = compare(i1, i2)
        print("%s <=> %s (%s) %s" % (img1, img2, round(x,2), "да" if x < 0.07 else "похожи" if x < 0.7 else "нет"))
    except AssertionError:
        print("Usage")
    except FileNotFoundError:
        print("FileNotFound", file=sys.stderr)
        exit(2)