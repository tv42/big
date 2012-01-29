import errno
import os
import sys

from .util import (
    get_hash_from_path,
    )


def put(args):
    fail = False
    for path in args.paths:
        try:
            dest = os.readlink(path)
        except OSError as e:
            if e.errno == errno.ENOENT:
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg=os.strerror(e.errno),
                    )
                fail = True
                continue
            elif e.errno == errno.EINVAL:
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg='Not a big file (not a symlink)',
                    )
                fail = True
                continue
            else:
                raise

        hash_ = get_hash_from_path(dest)
        if hash_ is None:
            print >>sys.stderr, "{prog}: {path}: {msg}".format(
                prog=args.prog,
                path=path,
                msg='Not a big file',
                )
            fail = True
            continue

        raise NotImplementedError('TODO WIP')

    if fail:
        return 1


def make(parser):
    """
    Put a copy of big file to other storage
    """
    parser.add_argument(
        'remote',
        help='Remote to put content on',
        metavar='REMOTE',
        )
    parser.add_argument(
        'paths',
        help='Paths to get',
        metavar='PATH',
        nargs='+',
        )
    parser.set_defaults(func=put)
