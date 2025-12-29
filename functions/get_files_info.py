# functions/get_file_info.py


import os
from google.genai import types

schema_get_files_info = types.FunctionDeclaration(
    name="get_files_info",
    description="Lists files in a specified directory relative to the working directory, providing file size and directory status",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "directory": types.Schema(
                type=types.Type.STRING,
                description="Directory path to list files from, relative to the working directory (default is the working directory itself)",
            ),
        },
    ),
)


def get_files_info(working_directory, directory=".") -> str:
    """List files and directories within a specified directory with security validation and traversal protection.

    Args:
        working_directory (str): The base directory within which the target directory must reside.
        directory (str): The relative path to the directory to list. Defaults to ".".

    Returns:
        str: A formatted string containing file information (name, size, is_dir), one per line. Returned string is an error message if validation fails or target is not a direcrtory.
    """
    try:
        working_dir_abs: str = os.path.abspath(working_directory)

        target_directory: str = os.path.normpath(
            os.path.join(working_dir_abs, directory)
        )

        valid_target_dir: bool = (
            os.path.commonpath([target_directory, working_dir_abs]) == working_dir_abs
        )

        if not valid_target_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(target_directory):
            return f'Error: "{target_directory}" is not a directory'

        files_info: list[str] = []

        for item in os.listdir(target_directory):
            joined_path = os.path.join(target_directory, item)
            name: str = os.path.basename(joined_path)
            size: int = os.path.getsize(joined_path)
            is_a_dir: bool = os.path.isdir(joined_path)

            files_info.append(f"- {name}: file_size={size} bytes, is_dir={is_a_dir}")

        files_str = "\n".join(files_info)

    except Exception as e:
        return f"Error: {str(e)}"

    return files_str
