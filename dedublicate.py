from compare import compare, getthumb, MIN, NotAnImage
from shutil import move

import sys
import os

def scan_dir(_dir):
    for path, dirs, files in os.walk(_dir):
        for f in [ "%s%s" % (path, f) for f in files]:
            try:
                yield (f, getthumb(f))
            except NotAnImage:
                pass
    
def compare_images(scanned, minv):
    checked = []
    for k1, v1 in scanned:
        for k2, v2 in scanned:
            to_check = set([k1,k2])
            if k1 != k2 and to_check not in checked:
                x = compare(v1, v2)
                checked += [to_check]
                if x < minv:
                    yield (k2, x)
    
def move_images(compared, _dir):
    for f, x in compared:
        ff = "(%s) %s" % (x, os.path.basename(f))
        print('move(%s, "/tmp/"%s)' % (f, ff), end=' ... ', file=sys.stderr)
        try:
            move(f, _dir+ff)
            print('done', file=sys.stderr)
        except OSError:
            print('already moved?', file=sys.stderr)
    
if __name__ == '__main__':
    try:
        move_images(compare_images(scan_dir(sys.argv[1]), MIN), '/tmp/')
    except IndexError:
        print(""" USAGE:
dedublicate /path

this will move all dublicates of images in path (incl subdirs)
into /tmp/

files will be renamed as '(x) original_name.ext' where x is
tolerance value for debug purposes.
""")