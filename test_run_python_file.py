# test_run_python_file.py
from functions.run_python_file import run_python_file
from typing import Tuple


test_cases: list[Tuple] = [
    ("calculator", "main.py"),
    ("calculator", "main.py", ["3 + 5"]),
    ("calculator", "tests.py"),
    ("calculator", "../main.py"),
    ("calculator", "nonexistent.py"),
    ("calculator", "lorem.txt"),
]


def test(test_case: tuple):
    result = run_python_file(*test_case)
    print("====================")
    print(f"{result}")
    print("====================\n")


for test_case in test_cases:
    test(test_case)
