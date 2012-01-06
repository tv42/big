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
