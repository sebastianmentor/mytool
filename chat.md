# Argparse-CLI – komplett skelettprojekt (Python)

Nedan finns en färdig projektstruktur med fungerande CLI via `argparse`, loggning med `logging`, tester med `pytest`, samt `pyproject.toml` för paketbygge/installering. Kopiera innehållet till en mapp (t.ex. `mytool/`) och följ instruktionerna under **Kom igång**.

---

## Trädstruktur

```
mytool/
├─ pyproject.toml
├─ README.md
├─ LICENSE
├─ .gitignore
├─ src/
│  └─ mytool/
│     ├─ __init__.py
│     ├─ __main__.py
│     ├─ cli.py
│     ├─ logging_conf.py
│     └─ core.py
└─ tests/
   ├─ test_core.py
   └─ test_cli.py
```

---

## `pyproject.toml`

```toml
[build-system]
requires = ["hatchling>=1.18"]
build-backend = "hatchling.build"

[project]
name = "mytool"
version = "0.1.0"
description = "Exempelpå ett CLI-verktyg med argparse och logging"
readme = "README.md"
authors = [{ name = "Ditt Namn" }]
requires-python = ">=3.8"
license = { text = "MIT" }
keywords = ["cli", "argparse", "example"]

# Inga obligatoriska beroenden behövs för exemplen.
dependencies = []

# Utvecklingsberoenden (installera via: `pip install -e .[dev]`)
[project.optional-dependencies]
dev = [
  "pytest>=7",
  "pytest-cov>=4",
  "ruff>=0.4",
]

[project.scripts]
# Skapar ett konsolkommando `mytool`
mytool = "mytool.cli:main"

[tool.hatch.build]
packages = ["src/mytool"]
```

---

## `README.md`

````markdown
# mytool

Ett minimalt men komplett exempel på ett Python-CLI med `argparse` och `logging`.

## Kom igång

```bash
# 1) (valfritt) skapa och aktivera virtuell miljö
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 2) Installera i utvecklingsläge
pip install -e .[dev]

# 3) Kör verktyget
mytool greet Ada --times 2 -vv
mytool sum 1 2 3 4

# 4) Kör tester
pytest -q
````

## Användning

```bash
mytool -h
mytool greet -h
mytool sum -h
```

## Kodstil

Kör `ruff` för snabb lintning:

```bash
ruff check src tests
```

````

---

## `LICENSE` (MIT)

```text
MIT License

Copyright (c) 2025

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
````

---

## `.gitignore`

```gitignore
# Python
__pycache__/
*.py[cod]
*.pyo
*.pyd

# Virtual environments
.venv/
venv/

# Packaging
*.egg-info/
dist/
build/

# OS
.DS_Store
Thumbs.db

# Test & coverage
.pytest_cache/
.coverage
htmlcov/
```

---

## `src/mytool/__init__.py`

```python
__all__ = ["__version__"]
__version__ = "0.1.0"
```

---

## `src/mytool/__main__.py`

```python
from .cli import main

if __name__ == "__main__":
    main()
```

---

## `src/mytool/logging_conf.py`

```python
import logging
from typing import Optional

_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]


def setup_logging(verbosity: int = 0, *, log_format: Optional[str] = None) -> None:
    """Initiera loggning baserat på -v nivåer.

    - 0 (default)  -> WARNING
    - 1 (-v)       -> INFO
    - 2 eller mer  -> DEBUG
    """
    level_index = min(max(verbosity, 0), len(_LEVELS) - 1)
    level = _LEVELS[level_index]

    fmt = log_format or "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)
```

---

## `src/mytool/core.py`

```python
from __future__ import annotations
from typing import Iterable, List


def greet(name: str, times: int = 1) -> List[str]:
    """Generera hälsningsrader.

    >>> greet("Ada", 2)
    ['Hej Ada!', 'Hej Ada!']
    """
    times = max(1, int(times))
    return [f"Hej {name}!" for _ in range(times)]


def sum_numbers(values: Iterable[float]) -> float:
    """Summera värden som float.

    >>> sum_numbers([1, 2, 3])
    6.0
    """
    total = 0.0
    for v in values:
        total += float(v)
    return total
```

---

## `src/mytool/cli.py`

```python
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


if __name__ == "__main__":  # pragma: no cover
    raise SystemExit(main())
```

---

## `tests/test_core.py`

```python
from mytool.core import greet, sum_numbers


def test_greet_repeats():
    assert greet("Ada", 2) == ["Hej Ada!", "Hej Ada!"]


def test_sum_numbers():
    assert sum_numbers([1, 2, 3, 4]) == 10.0
```

---

## `tests/test_cli.py`

```python
import sys
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
    args = parse_args(["-vv", "sum", "1"])  # två v -> DEBUG
    assert args.verbose == 2
```

---

## Snabbguide – vanliga kommandon

```bash
# Installera i utvecklingsläge (inkl test & lint)
pip install -e .[dev]

# Hjälp
mytool -h
mytool greet -h
mytool sum -h

# Exempel
mytool greet "Sebastian" --times 3 -v
mytool sum 1 2 3 4 -vv

# Testa
pytest -q

# Linta
ruff check src tests
```

---

## Vidareutveckling (idéer)

* Lägg till `fromfile_prefix_chars='@'` om du vill läsa argument från fil.
* Lägg till fler underkommandon, t.ex. `convert`, `report`.
* Skapa en `config`-flagga och mönster för tvåstegs-parsning (läs defaults från JSON/YAML, CLI vinner alltid).
* Paketera till wheel: `python -m build` (kräver `build`-paketet) eller fortsätt med Hatch/Poetry om du föredrar det.


Klart! Jag har lagt hela skelettprojektet i canvasen här bredvid (struktur, filer och kod).

Snabbstart:

1. skapa venv och installera i utvecklingsläge:

```bash
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
```

2. kör:

```bash
mytool greet Ada --times 2 -vv
mytool sum 1 2 3 4
```

3. testa & linta:

```bash
pytest -q
ruff check src tests
```

Vill du att jag lägger till:

* ett `config`-flöde (tvåstegs-parsning via JSON/YAML),
* färdigt `logging`-stöd med filhandler + roterande loggar,
* GitHub Actions för test/lint,
* eller ett extra underkommando (t.ex. `report`)?

Säg bara till så bygger jag vidare.
