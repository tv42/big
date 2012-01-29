import errno
import hashlib
import os
import socket
import sys

from . import git
from .util import (
    get_hash_from_path,
    get_umask,
    maybe_link,
    maybe_mkdir,
    maybe_symlink,
    )


def add(args):
    fail = False
    for path in args.paths:

        try:
            dest = os.readlink(path)
        except OSError as e:
            if e.errno == errno.EINVAL:
                # it's not a symlink, that's fine for us
                pass
            else:
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg=os.strerror(e.errno),
                    )
                fail = True
                continue
        else:
            # it is a symlink
            hash_ = get_hash_from_path(dest)
            if hash_ is not None:
                # it's a symlink to a big file already, ignore
                continue
            else:
                # user-controlled symlink
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg='Refusing to add a symlink',
                    )
                fail = True
                continue

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

        with f:
            h = hashlib.sha1()
            while True:
                data = f.read(8192)
                if not data:
                    break
                h.update(data)
        hashed = h.hexdigest()

        # TODO not always in inited git repo
        cdup = git.cdup()
        big_dir = os.path.join(cdup, '.git/big')
        maybe_mkdir(big_dir)

        path_parent = os.path.dirname(path)
        cdup_from_subdir = git.cdup(path_parent)
        git_big_from_subdir = os.path.join(cdup_from_subdir, '.git/big')
        local_big_dir = os.path.join(path_parent, '.big')
        maybe_symlink(git_big_from_subdir, local_big_dir)

        umask = get_umask()
        os.chmod(path, 0444 & ~umask)

        parent = os.path.join(big_dir, hashed[:2])
        maybe_mkdir(parent)
        base = hashed[2:] + '.data'
        full = os.path.join(parent, base)
        maybe_link(path, full)
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
        help='Paths to be added',
        metavar='PATH',
        nargs='+',
        )
    parser.set_defaults(func=add)
