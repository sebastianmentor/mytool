from __future__ import annotations
import argparse
import logging
from typing import Sequence


from . import __version__
from .core import greet, sum_numbers
from .logging_conf import setup_logging




logger = logging.getLogger("mytool")




def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
    prog="mytool",
    description="Exempelpå ett CLI-verktyg med argparse och logging.",
    formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    allow_abbrev=False,
    )


    # Globala flaggor
    parser.add_argument(
    "-v", "--verbose",
    action="count",
    default=0,
    help="Öka loggnivån: -v (INFO), -vv (DEBUG)",
    )
    parser.add_argument(
    "--version",
    action="version",
    version=f"mytool {__version__}",
    )


    sub = parser.add_subparsers(dest="command", required=True)


    # greet
    p_greet = sub.add_parser("greet", help="Hälsa på någon")
    p_greet.add_argument("name", help="Namn att hälsa på")
    p_greet.add_argument("-t", "--times", type=int, default=1, help="Antal gånger")
    p_greet.set_defaults(func=cmd_greet)


    # sum
    p_sum = sub.add_parser("sum", help="Summera tal")
    p_sum.add_argument("numbers", nargs="+", help="Tal att summera")
    p_sum.set_defaults(func=cmd_sum)


    return parser




def cmd_greet(args: argparse.Namespace) -> int:
    lines = greet(args.name, args.times)
    for line in lines:
        print(line)
    logger.info("Hälsning klar")
    return 0


def cmd_sum(args: argparse.Namespace) -> int:
    total = sum_numbers(args.numbers)
    print(total)
    logger.debug("Summerade %d värden", len(args.numbers))
    return 0


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = build_parser()
    return parser.parse_args(argv)


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    setup_logging(args.verbose)
    # Kör vald subkommandos-funktion
    return args.func(args)


if __name__ == "__main__": # pragma: no cover
    raise SystemExit(main())