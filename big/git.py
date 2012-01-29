import subprocess


def cdup(path=None):
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


def remote_url(remote):
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
