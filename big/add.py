import hashlib
import errno
import os
import socket
import subprocess
import sys


def maybe_mkdir(path):
    try:
        os.mkdir(path)
    except OSError as e:
        if e.errno == errno.EEXIST:
            pass
        else:
            raise


def git_cdup(path=None):
    # '' is understood as an alias for current dir, because that's
    # what os.path.dirname etc like to give you
    if path == '':
        path = None
    p = subprocess.Popen(
        args=['git', 'rev-parse', '--show-cdup'],
        cwd=path,
        stdout=subprocess.PIPE,
        )
    (out, err) = p.communicate()
    assert err is None
    return out.rstrip('\n')


def get_umask():
    mask = os.umask(0)
    os.umask(mask)
    return mask


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

        # TODO not always in inited git repo
        cdup = git_cdup()
        big_dir = os.path.join(cdup, '.git/big')
        maybe_mkdir(big_dir)

        path_parent = os.path.dirname(path)
        cdup_from_subdir = git_cdup(path_parent)
        git_big_from_subdir = os.path.join(cdup_from_subdir, '.git/big')
        local_big_dir = os.path.join(path_parent, '.big')
        os.symlink(git_big_from_subdir, local_big_dir)

        umask = get_umask()
        os.chmod(path, 0444 & ~umask)

        parent = os.path.join(big_dir, hashed[:2])
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
