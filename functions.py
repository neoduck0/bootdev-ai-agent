import os


def get_file_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_wd: str = os.path.abspath(working_directory)
        abs_dir: str = os.path.join(abs_wd, directory)
        abs_dir = os.path.normpath(abs_dir)

        valid_dir: bool = abs_wd == os.path.commonpath([abs_dir, abs_wd])

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'

        return f'Success: "{directory}" is within the working directory'

    except Exception as e:
        return f"Error: {e}"
