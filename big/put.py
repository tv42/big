def put(args):
    raise NotImplementedError('TODO WIP')


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
