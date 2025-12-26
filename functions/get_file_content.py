import os

from config import MAX_CHARS  # typing: ignore


def get_file_contents(working_directory, file_path) -> str:
    """Read file content from a specified path within a working directory with security validation, traversal protection, and truncation.

    Args:
        working_directory (str): The base directory within which the file must reside.
        file_path (str): The relative or absolute path to the file to read.

    Returns:
        str: The file content (up to MAX_CHARS characters), appended with a truncation notice if content exceeds MAX_CHARS.

    Raises:
        Exception: Error message if validation fails or file not found
    """

    try:
        working_dir_abs: str = os.path.abspath(working_directory)

        target_file: str = os.path.normpath(os.path.join(working_directory, file_path))

        valid_tar_file: bool = (
            os.path.commonpath([working_dir_abs, target_file]) == working_dir_abs
        )

        if not valid_tar_file:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(target_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(target_file) as f:
            file_content = f.read(MAX_CHARS)

            # After reading the first MAX_CHARS...

            if f.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

    except Exception as e:
        return f"Error: {str(e)}"

    return file_content
