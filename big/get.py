import errno
import os
import shutil
import socket
import subprocess
import sys

from .util import maybe_mkdir


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


def get_hash_from_path(path):
    (prefix, filename) = os.path.split(path)
    (big, h2) = os.path.split(prefix)
    if big != '.big':
        return None
    assert len(h2) == 2
    (base, ext) = os.path.splitext(filename)
    assert ext == '.data'
    return h2 + base


def git_list_remotes():
    p = subprocess.Popen(
        args=[
            'git',
            'remote',
            ],
        stdout=subprocess.PIPE,
        )
    (out, err) = p.communicate()
    assert err is None
    return out.rstrip('\n').split('\n')


def git_remote_url(remote):
    p = subprocess.Popen(
        args=[
            'git',
            'config',
            '--',
            'remote.{remote}.url'.format(remote=remote),
            ],
        stdout=subprocess.PIPE,
        )
    (out, err) = p.communicate()
    assert err is None
    return out.rstrip('\n')


def get_fetcher(url):
    # TODO support remote urls
    if not url.startswith('/'):
        return None

    def fetch(hash_):
        path = os.path.join(
            url,
            '.git',
            'big',
            hash_[:2],
            '{h}.data'.format(h=hash_[2:]),
            )
        try:
            f = file(path, 'rb')
        except IOError as e:
            if e.errno == errno.ENOENT:
                return None
            else:
                raise
        else:
            return f

    return fetch


def get(args):
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

        if os.path.exists(path):
            # nothing to do
            continue

        # TODO prioritize remotes better
        acceptable = False
        found = False
        for remote in git_list_remotes():
            url = git_remote_url(remote)

            assert url != ''
            fetcher = get_fetcher(url)
            if fetcher is None:
                continue
            acceptable = True
            f_in = fetcher(hash_=hash_)
            if f_in is None:
                continue
            found = True

            assert ':' not in url, 'TODO'

            # TODO not always in inited git repo
            cdup = git_cdup()
            big_dir = os.path.join(cdup, '.git/big')
            maybe_mkdir(big_dir)

            path_parent = os.path.dirname(path)
            cdup_from_subdir = git_cdup(path_parent)
            git_big_from_subdir = os.path.join(cdup_from_subdir, '.git/big')
            local_big_dir = os.path.join(path_parent, '.big')
            os.symlink(git_big_from_subdir, local_big_dir)

            parent = os.path.join(big_dir, hash_[:2])
            maybe_mkdir(parent)
            base = hash_[2:] + '.data'
            full = os.path.join(parent, base)
            tmp = os.path.join(
                parent,
                '{hrest}.{host}_{pid}.tmp'.format(
                    hrest=hash_[2:],
                    host=socket.gethostname(),
                    pid=os.getpid(),
                    ),
                )
            umask = get_umask()
            with file(tmp, 'wb') as f_out:
                os.fchmod(f_out.fileno(), 0444 & ~umask)
                shutil.copyfileobj(f_in, f_out)
            os.rename(tmp, full)

        if not acceptable:
            print >>sys.stderr, "{prog}: {msg}".format(
                prog=args.prog,
                msg='No remotes with supported schemes',
                )
            fail = True
            continue

        if not found:
            print >>sys.stderr, "{prog}: {path}: {msg}".format(
                prog=args.prog,
                path=path,
                msg='No remote has big file',
                )
            fail = True
            continue

    if fail:
        return 1


def make(parser):
    """
    Get big file from other storage
    """
    parser.add_argument(
        'paths',
        metavar='PATH..',
        help='Paths to get',
        action='append',
        # not using nargs='+' because argparse makes the usage so ugly
        )
    parser.set_defaults(func=get)
