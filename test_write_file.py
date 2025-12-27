# test_write_file.py
from functions.write_file import write_file
from typing import Tuple


test_cases: list[Tuple] = [
    ("calculator", "pkg/lorem.txt", "wait, this isn't lorem ipsum"),
    ("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet"),
    ("calculator", "/tmp/temp.txt", "this should not be allowed"),
]


def test(test_case: tuple):
    result = write_file(*test_case)
    print(result)


for test_case in test_cases:
    test(test_case)
