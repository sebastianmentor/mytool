from mytool.cli import parse_args


def test_parse_greet_defaults():
    args = parse_args(["greet", "Ada"])
    assert args.command == "greet"
    assert args.name == "Ada"
    assert args.times == 1


def test_parse_sum():
    args = parse_args(["sum", "1", "2", "3"])
    assert args.command == "sum"
    assert args.numbers == ["1", "2", "3"]


def test_verbose_flags():
    args = parse_args(["-vv", "sum", "1"]) # två v -> DEBUG
    assert args.verbose == 2