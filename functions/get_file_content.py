import os

from config import MAX_CHARS


def get_file_content(working_directory: str, file_path: str) -> str:
    try:
        abs_wd: str = os.path.abspath(working_directory)
        abs_file: str = os.path.join(abs_wd, file_path)
        abs_file = os.path.normpath(abs_file)

        if os.path.commonpath([abs_wd, abs_file]) != abs_wd:
            return f'Error: Cannot read "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        file_content: str
        with open(abs_file) as f:
            file_content = f.read(MAX_CHARS)

            if f.read(1):
                file_content += (
                    f'[...File "{file_path}" truncated at {MAX_CHARS} characters]'
                )

        return file_content
    except Exception as e:
        return f"Error: {e}"
