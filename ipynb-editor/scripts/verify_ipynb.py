import sys
import json
import ast
import subprocess
import argparse
import re


def check_syntax(file_path):
    """Validates that the file is valid JSON and that code cells contain valid Python syntax."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
            nb = json.loads(content)
    except json.JSONDecodeError as e:
        print(f"JSON Structure Error in {file_path}: {e}")
        # Check for common corruption patterns in the raw text
        if "\\\\" in content:
            print(
                "  HINT: Detected multiple backslashes (\\\\). You might have accidentally double-escaped newlines or quotes."
            )
        return False

    syntax_passed = True
    for i, cell in enumerate(nb.get("cells", [])):
        if cell.get("cell_type") == "code":
            source_array = cell.get("source", [])

            # Check for missing newlines in the source array
            for j, line in enumerate(source_array[:-1]):
                if not line.endswith("\n"):
                    print(
                        f"Format Warning in cell {i+1}, line {j+1}: Line does not end with '\\n'. This often causes SyntaxErrors when Jupyter joins the strings."
                    )
                    syntax_passed = False

            source = "".join(source_array)
            if not source.strip():
                continue
            try:
                # Parse the AST to validate syntax without executing
                ast.parse(source)
            except SyntaxError as e:
                print(f"SyntaxError in cell {i+1}: {e}")
                print(
                    f"  Source fragment: {repr(source[max(0, e.offset-20):e.offset+20])}"
                )
                if "\\n" in source:
                    print(
                        "  HINT: Detected literal '\\n' characters in the joined source. Ensure they are interpreted as newlines by the JSON parser, not literal backslashes followed by 'n'."
                    )
                syntax_passed = False

    if syntax_passed:
        print(
            f"Verification of {file_path} successful: JSON structure and Python syntax passed."
        )
    else:
        print(f"Verification of {file_path} failed.")
    return syntax_passed


def execute_notebook(file_path):
    """Executes the notebook to ensure it runs without throwing exceptions."""
    print(f"Executing {file_path} to verify cell contents...")
    try:
        result = subprocess.run(
            [
                "jupyter",
                "nbconvert",
                "--execute",
                "--to",
                "notebook",
                "--inplace",
                file_path,
            ],
            capture_output=True,
            text=True,
        )
        if result.returncode != 0:
            print("Execution failed. Traceback/Error:\n", result.stderr)
            return False
        print("Execution successful.")
        return True
    except FileNotFoundError:
        print("Error: 'jupyter' command not found. Cannot verify execution.")
        return False


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Verify Jupyter Notebook syntax and execution."
    )
    parser.add_argument("file", help="Path to the .ipynb file")
    parser.add_argument(
        "--syntax-only",
        action="store_true",
        help="Only validate JSON and Python syntax (do not execute)",
    )
    parser.add_argument(
        "--execute", action="store_true", help="Execute the notebook cells sequentially"
    )
    args = parser.parse_args()

    # Always check syntax first
    if not check_syntax(args.file):
        sys.exit(1)

    if args.execute:
        if not execute_notebook(args.file):
            sys.exit(1)

    sys.exit(0)
