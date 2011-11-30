import os
import pkg_resources
import pytest
import subprocess
import sys


def pytest_generate_tests(metafunc):
    if 'cramtest' in metafunc.funcargnames:
        files = os.listdir(os.path.dirname(__file__))
        files = [f for f in files
                 if not f.startswith('.')
                 and not f.startswith('_')
                 and f.endswith('.t')]
        metafunc.parametrize('cramtest', files)


def test_cram(cramtest, tmpdir, monkeypatch):
    # pytest you are too opinionated (or, i just disagree)
    tmpdir = str(tmpdir)

    bindir = os.path.join(tmpdir, 'bin')
    os.mkdir(bindir)

    dist = pkg_resources.get_distribution('big')
    for name in dist.get_entry_map(group='console_scripts'):
        with file(os.path.join(bindir, name), 'w') as f:
            f.write("""\
#!{python}
import sys
from pkg_resources import load_entry_point

if __name__ == '__main__':
    sys.exit(
        load_entry_point('big', 'console_scripts', '{name}')()
    )
    """.format(
                    python=sys.executable,
                    name=name,
                    ))
            os.fchmod(f.fileno(), 0755)

    cramdir = os.path.join(tmpdir, 'cram')
    os.mkdir(cramdir)

    search_path = ':'.join([bindir, os.environ['PATH']])

    with file('/dev/null', 'rb') as f:
        proc = subprocess.Popen(
            args=[
                sys.executable, '-m', 'cram',
                '--verbose',
                '--',
                os.path.join(os.path.dirname(__file__), cramtest),
                ],
            cwd=cramdir,
            env=dict(
                PATH=search_path,
                TMPDIR=cramdir,
                ),
            stdin=f,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            close_fds=True,
            )

    (out, err) = proc.communicate()

    if err:
        pytest.fail('Cram internal error:\n' + err)
    if proc.returncode != 0:
        pytest.fail(out)
