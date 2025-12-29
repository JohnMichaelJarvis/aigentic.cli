# functions/write_file.py
from genericpath import isdir
import os
from google.genai import types


schema_write_file = types.FunctionDeclaration(
    name="write_file",
    description="Writes content to a file at a path reletive to the working directory.",
    parameters=types.Schema(
        type=types.Type.OBJECT,
        properties={
            "file_path": types.Schema(
                type=types.Type.STRING,
                description="Path of the file to be written, relative to the working directory.",
            ),
            "content": types.Schema(
                type=types.Type.STRING,
                description="The content being written to the file.",
            ),
        },
    ),
)


def write_file(working_directory, file_path, content) -> str:
    try:
        working_directory_abs: str = os.path.abspath(working_directory)

        safe_file_path: str = os.path.normpath(
            os.path.join(working_directory_abs, file_path)
        )

        valid_safe_path: bool = (
            os.path.commonpath([working_directory_abs, safe_file_path])
            == working_directory_abs
        )

        if not valid_safe_path:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(safe_file_path):
            print(f"PATH::::{safe_file_path}")
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        dir_path = safe_file_path.rstrip(os.path.basename(safe_file_path))
        os.makedirs(dir_path, exist_ok=True)

        with open(safe_file_path, "w", encoding="utf-8") as f:
            f.write(content)
    except Exception as e:
        return f"Error: {str(e)}"

    return f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
