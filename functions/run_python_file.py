# functions/run_python_file.py
import os
import subprocess as sp


def run_python_file(working_directory, file_path, args=None) -> str:
    try:
        abs_working_dir = os.path.abspath(working_directory)

        safe_file_path = os.path.normpath(os.path.join(abs_working_dir, file_path))

        valid_path = (
            os.path.commonpath([safe_file_path, abs_working_dir]) == abs_working_dir
        )

        if not valid_path:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'
        if not os.path.isfile(safe_file_path):
            return f'Error: "{file_path}" does not exist or is not a regular file'
        if not safe_file_path.endswith(".py"):
            return f'Error: "{file_path}" is not a Python file'

        command = ["python", safe_file_path]

        if args:
            command.extend(args)

        command_process = sp.run(
            command, cwd=abs_working_dir, text=True, capture_output=True, timeout=30
        )

        output_strings = []

        if command_process.returncode != 0:
            output_strings.append(
                f"Process exited with code {command_process.returncode}"
            )

        if not command_process.stdout and not command_process.stderr:
            output_strings.append("No output produced")
        else:
            if command_process.stdout:
                output_strings.append(f"STDOUT:\n{command_process.stdout}")
            if command_process.stderr:
                output_strings.append(f"STDERR:\n{command_process.stderr}")

        return "\n".join(output_strings)
    except Exception as e:
        return f"Error: executing Python file: {str(e)}"
