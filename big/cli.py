import argparse


def get_parser():
    parser = argparse.ArgumentParser(
        description='Large file storage with Git',
        )
    return parser


def main():
    parser = get_parser()
    args = parser.parse_args()
    del args  # please pyflakes, for now
