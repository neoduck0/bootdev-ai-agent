import os


def get_files_info(working_directory: str, directory: str = ".") -> str:
    try:
        abs_wd: str = os.path.abspath(working_directory)
        abs_dir: str = os.path.join(abs_wd, directory)
        abs_dir = os.path.normpath(abs_dir)

        valid_dir: bool = abs_wd == os.path.commonpath([abs_dir, abs_wd])

        if not valid_dir:
            return f'Error: Cannot list "{directory}" as it is outside the permitted working directory'

        if not os.path.isdir(abs_dir):
            return f'Error: "{directory}" is not a directory'

        dir_contents: str = ""
        for file_name in os.listdir(abs_dir):
            abs_file_path: str = os.path.join(abs_dir, file_name)
            is_dir: bool = os.path.isdir(abs_file_path)
            file_size: int = os.path.getsize(abs_file_path)

            dir_contents = (
                dir_contents
                + f"- {file_name}: file_size={file_size}, is_dir={is_dir}\n"
            )
        dir_contents = dir_contents[: len(dir_contents) - 1]

        return dir_contents

    except Exception as e:
        return f"Error: {e}"


schema_get_files_info = {
    "type": "function",
    "function": {
        "name": "get_files_info",
        "description": "Lists files in a specified directory relative to the working directory, providing file size and directory status",
        "parameters": {
            "type": "object",
            "properties": {
                "directory": {
                    "type": "string",
                    "description": "Directory path to list files from, relative to the working directory (default is the working directory itself)",
                },
            },
        },
    },
}
