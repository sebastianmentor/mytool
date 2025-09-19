from mytool.core import greet, sum_numbers




def test_greet_repeats():
    assert greet("Ada", 2) == ["Hej Ada!", "Hej Ada!"]




def test_sum_numbers():
    assert sum_numbers([1, 2, 3, 4]) == 10.0