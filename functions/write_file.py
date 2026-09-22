import os


def write_file(working_directory: str, file_path: str, content: str) -> str:
    try:
        abs_wd: str = os.path.abspath(working_directory)
        abs_file: str = os.path.join(abs_wd, file_path)
        abs_file = os.path.normpath(abs_file)

        if os.path.commonpath([abs_wd, abs_file]) != abs_wd:
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        if os.path.isdir(abs_file):
            return f'Error: Cannot write to "{file_path}" as it is a directory'
        os.makedirs(os.path.dirname(abs_file), exist_ok=True)

        with open(abs_file, "w") as f:
            f.write(content)

        return (
            f'Successfully wrote to "{file_path}" ({len(content)} characters written)'
        )
    except Exception as e:
        return f"Error: {e}"
