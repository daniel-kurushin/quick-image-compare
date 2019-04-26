"""
Created on Tue Apr 23 13:08:33 2019

@author: dan
"""

from PIL import Image

def compare(img1, img2):
    img1 = Image.open(img1)
    img2 = Image.open(img2)
    return 1

if __name__ == '__main__':
    test= ['test/img1.png', 'test/img2.png']
    for img1 in test:
        for img2 in test:
            print("%s <=> %s (%s)" % (img1, img2, compare(img1, img2)))
    