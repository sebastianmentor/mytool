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