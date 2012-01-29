import argparse
import operator
import pkg_resources


def get_parser():
    parser = argparse.ArgumentParser(
        description='Large file storage with Git',
        )
    sub = parser.add_subparsers(
        title='commands',
        metavar='COMMAND',
        help='description',
        )
    entrypoints = pkg_resources.iter_entry_points('big.cli')
    for ep in sorted(entrypoints, key=operator.attrgetter('name')):
        fn = ep.load()
        p = sub.add_parser(ep.name, help=fn.__doc__)
        # ugly kludge but i really want to have a nice way to access
        # the program name, with subcommand, later
        p.set_defaults(prog=p.prog)
        fn(p)
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    return args.func(args)
