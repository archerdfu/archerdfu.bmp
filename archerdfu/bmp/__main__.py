import argparse
from pathlib import Path

from archerdfu.bmp import CaliberIcon, matrix_to_bmp

__version__ = '1.0.1'


def get_argparser():
    parser = argparse.ArgumentParser(
        prog='archerdfu bmp processor',
        epilog='Text at the bottom of help',
        conflict_handler='resolve',
        exit_on_error=False,
    )

    parser.add_argument('-v', '--version', action='version', version=f'{parser.prog} v{__version__}')
    parser.add_argument('-d', '--debug', action='store_true', help="run in debug mode")

    icon_parser_group = parser.add_argument_group("Create icon")
    icon_parser_group.add_argument('-c', '--caliber', action='store', metavar='<str>',
                                   help="Caliber name")
    icon_parser_group.add_argument('-w', '--weight', action='store', metavar='<float>', type=float,
                                   help="Bullet weight")
    icon_parser_group.add_argument('-o', '--output', action='store', metavar='<output dir>',
                                   default='./',
                                   help='output directory')
    return parser


COMMANDLINE_PARSER = get_argparser()

try:
    COMMANDLINE_ARGS, UNKNOWN = COMMANDLINE_PARSER.parse_known_args()
except Exception as exc:
    COMMANDLINE_PARSER.parse_known_args(('-h',))


def create_caliber_icon():
    output = COMMANDLINE_ARGS.output

    dest = Path(output).absolute()
    if not dest.is_dir():
        raise TypeError('Destination must be a directory')

    if not COMMANDLINE_ARGS.weight:
        raise TypeError('Weight required must be a number')

    if not COMMANDLINE_ARGS.caliber:
        raise TypeError('Caliber required must be a string')

    filename = f"{COMMANDLINE_ARGS.caliber}-{COMMANDLINE_ARGS.weight}gr.bmp"
    matrix = CaliberIcon.create_icon_matrix(COMMANDLINE_ARGS.caliber, COMMANDLINE_ARGS.weight)
    matrix_to_bmp(matrix, dest / filename)


def main():
    create_caliber_icon()


if __name__ == "__main__":
    main()
