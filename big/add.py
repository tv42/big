import hashlib
import errno
import os
import socket
import sys


def maybe_mkdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


def add(args):
    fail = False
    for path in args.paths:
        try:
            f = file(path, 'rb')
        except IOError as e:
            print >>sys.stderr, "{prog}: {path}: {msg}".format(
                prog=args.prog,
                path=path,
                msg=os.strerror(e.errno),
                )
            fail = True
            continue
        else:
            h = hashlib.sha1()
            while True:
                data = f.read(8192)
                if not data:
                    break
                h.update(data)
        hashed = h.hexdigest()
        # TODO not always at top level of git repo
        # TODO not always in inited git repo
        maybe_mkdir('.git/big')
        # TODO not always at top level of git repo
        os.symlink('.git/big', '.big')
        parent = os.path.join('.git', 'big', hashed[:2])
        maybe_mkdir(parent)
        base = hashed[2:] + '.data'
        full = os.path.join(parent, base)
        os.link(path, full)
        tmp = '{path}.{host}_{pid}.tmp'.format(
            path=path,
            host=socket.gethostname(),
            pid=os.getpid(),
            )
        os.symlink(os.path.join('.big', hashed[:2], base), tmp)
        os.rename(tmp, path)
    if fail:
        return 1


def make(parser):
    """
    Add big file to storage and track in Git
    """
    parser.add_argument(
        'paths',
        metavar='PATH..',
        help='Paths to be added',
        action='append',
        # not using nargs='+' because argparse makes the usage so ugly
        )
    parser.set_defaults(func=add)
