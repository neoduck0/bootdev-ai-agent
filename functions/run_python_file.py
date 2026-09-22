import os
import subprocess


def run_python_file(
    working_directory: str, file_path: str, args: list[str] | None = None
) -> str:

    try:
        abs_wd: str = os.path.abspath(working_directory)
        abs_file: str = os.path.normpath(os.path.join(abs_wd, file_path))

        if os.path.commonpath([abs_wd, abs_file]) != abs_wd:
            return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(abs_file):
            return f'Error: "{file_path}" does not exist or is not a regular file'

        if abs_file[len(abs_file) - 3 : len(abs_file)] != ".py":
            return f'Error: "{file_path}" is not a Python file'

        command: list[str] = ["python", file_path]
        if args != None:
            command.extend(args)

        status: str = ""
        capturedOutput = subprocess.run(
            command, cwd=abs_wd, capture_output=True, text=True, timeout=30
        )

        if capturedOutput.returncode != 0:
            status += f"Process exited with code {capturedOutput.returncode}\n"

        if not capturedOutput.stdout and not capturedOutput.stderr:
            status += "No output produced\n"
        else:
            if capturedOutput.stdout:
                status += f"STDOUT: {capturedOutput.stdout}\n"

            if capturedOutput.stderr:
                status += f"STDERR: {capturedOutput.stderr}\n"

        return status

    except Exception as e:
        return f"Error: executing Python file: {e}"
