# test_get_file_content.py

from typing import List
from functions.get_file_content import get_file_content
from config import MAX_CHARS


def test_lorem_truncation():
    content = get_file_content("calculator", "lorem.txt")

    # Make sure we didn’t read past the limit + message
    assert len(content) >= MAX_CHARS  # should be long
    assert f"truncated at {MAX_CHARS} characters]" in content
    assert content.endswith(
        f'[...File "lorem.txt" truncated at {MAX_CHARS} characters]'
    )


file_paths: list[str] = [
    "main.py",
    "pkg/calculator.py",
    "/bin/cat",
    "pkg/does_not_exist.py",
]

for file_path in file_paths:
    content: str = get_file_content("calculator", file_path=file_path)

    print(content)
