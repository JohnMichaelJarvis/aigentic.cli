# functions/get_file_content.py

import os
from config import MAX_CHARS  # typing: ignore
from google.genai import types

schema_get_file_content = types.FunctionDeclaration(
    name="get_file_content",
    description="Reads file content from a specified directory relative to the working dictionary and returns the first 10,000 characters of the file's content. The function also appends a message to file's  returned content if the file was truncated at 10,000 characters.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Directory path to read file from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_file_content(working_directory, file_path) -> str:
    """Read file content from a specified path within a working directory with security validation, traversal protection, and truncation.

    Args:
        working_directory (str): The base directory within which the file must reside.
        file_path (str): The relative or absolute path to the file to read.

    Returns:
        str: The file content (up to MAX_CHARS characters), appended with a truncation notice if content exceeds MAX_CHARS. Returned string is an error message if validation fails or file not found
    """

    try:
        working_dir_abs: str = os.path.abspath(working_directory)

        safe_file_path: str = os.path.normpath(os.path.join(working_dir_abs, file_path))

        valid_target_file: bool = (
            os.path.commonpath([safe_file_path, working_dir_abs]) == working_dir_abs
        )

        if not valid_target_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(safe_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(safe_file_path, "r", encoding="utf-8") as f:
            file_content = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...

            if f.read(1):
                file_content += (
                    f'\n[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

    except Exception as e:
        return f"Error: {str(e)}"

    return file_content
