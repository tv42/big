import os
import errno


def maybe_mkdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


def get_umask():
    mask = os.umask(0)
    os.umask(mask)
    return mask


def get_hash_from_path(path):
    (prefix, filename) = os.path.split(path)
    (big, h2) = os.path.split(prefix)
    if big != '.big':
        return None
    assert len(h2) == 2
    (base, ext) = os.path.splitext(filename)
    assert ext == '.data'
    return h2 + base
