from compare import compare, getthumb, MIN, NotAnImage


thumbs = {}

if __name__ == '__main__':
    try:
        import sys
        import os
        assert len(sys.argv) > 1
        _dir = sys.argv[1]
        for path, dirs, files in os.walk(_dir):
            for f in [ "%s%s" % (path, f) for f in files]:
                try:
                    thumbs.update({f:getthumb(f)})
                except NotAnImage:
                    pass
        checked = []
        result = []
        to_delete = []
        for k1, v1 in thumbs.items():
            for k2, v2 in thumbs.items():
                to_check = set([k1,k2])
                if k1 != k2 and to_check not in checked:
                    x = compare(v1, v2)
#                    print('%s, %s <> %s' % (int(round(x,2)*100), k1, k2))
                    if x < MIN:
                        to_delete += [(k2, x)]
                    result += [(round(x,2), k1, k2)]
                    checked += [to_check]
        from shutil import move
        for f, x in to_delete:
            ff = "(%s) %s" % (x, os.path.basename(f))
            print('move(%s, "/tmp/"+%s)' % (f, ff), end=' ... ')
            try:
                move(f, '/tmp/'+ff)
                print('done')
            except OSError:
                print('already moved?')
    except AssertionError:
        print("Usage")