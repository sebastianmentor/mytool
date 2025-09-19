import logging
from typing import Optional


_LEVELS = [logging.WARNING, logging.INFO, logging.DEBUG]




def setup_logging(verbosity: int = 0, *, log_format: Optional[str] = None) -> None:
    """Initiera loggning baserat på -v nivåer.


    - 0 (default) -> WARNING
    - 1 (-v) -> INFO
    - 2 eller mer -> DEBUG
    """
    level_index = min(max(verbosity, 0), len(_LEVELS) - 1)
    level = _LEVELS[level_index]


    fmt = log_format or "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    datefmt = "%H:%M:%S"
    logging.basicConfig(level=level, format=fmt, datefmt=datefmt)