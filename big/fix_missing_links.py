import errno
import os
import sys

from . import git
from .util import (
    get_hash_from_path,
    maybe_symlink,
    )


def fix_missing_links(args):
    fail = False
    for path in args.paths:
        try:
            dest = os.readlink(path)
        except OSError as e:
            if e.errno == errno.EINVAL:
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg='Not a big file (not a symlink)',
                    )
                fail = True
                continue
            else:
                print >>sys.stderr, "{prog}: {path}: {msg}".format(
                    prog=args.prog,
                    path=path,
                    msg=os.strerror(e.errno),
                    )
                fail = True
                continue

        hash_ = get_hash_from_path(dest)
        if hash_ is None:
            print >>sys.stderr, "{prog}: {path}: {msg}".format(
                prog=args.prog,
                path=path,
                msg='Not a big file',
                )
            fail = True
            continue

        # TODO fastpath via cache so we don't do this too much on big
        # trees

        # TODO not always in inited git repo

        path_parent = os.path.dirname(path)
        cdup_from_subdir = git.cdup(path_parent)
        git_big_from_subdir = os.path.join(cdup_from_subdir, '.git/big')
        local_big_dir = os.path.join(path_parent, '.big')
        maybe_symlink(git_big_from_subdir, local_big_dir)

    if fail:
        return 1


def make(parser):
    """
    Fix missing .big links
    """
    parser.add_argument(
        'paths',
        help='Paths to fix',
        metavar='PATH',
        nargs='+',
        )
    parser.set_defaults(func=fix_missing_links)
