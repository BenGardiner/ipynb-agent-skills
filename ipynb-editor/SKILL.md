---
name:ipynb-editor
description: Edits, validates, and formats Jupyter Notebook (.ipynb) files. Use when the user wants to safely modify notebook cells, check cell syntax, or verify execution. Do not use for standard Python (.py) scripts.
---

### Purpose
Ensure safe, structurally valid edits to Jupyter Notebook (`.ipynb`) files and verify the syntax and execution of their code cells.

### Inputs / Outputs
* **Input**: Target `.ipynb` file path and the requested code/markdown modifications.
* **Output**: A successfully updated `.ipynb` file with verified JSON structure and validated code cells.

### Constraints
* **MUST** preserve the exact JSON structure of the `.ipynb` file.
* **MUST** ensure every string in a `source` array (except possibly the last) ends with a newline `\n`. Failure to do this causes Python `SyntaxError` or `IndentationError` when cells are loaded.
* **MUST** verify that the final output is completely valid JSON before saving.
* **MUST** check for "double-escaping" (e.g., `\\n` or `\"`) which often occurs when AI agents attempt to nest JSON strings incorrectly.
* **MUST** validate the Python syntax of modified code cells using `scripts/verify_ipynb.py`.
* **MUST NOT** modify standard Python (`.py`) scripts using this skill.

### Workflow
1. **Read and Parse**: Read the `.ipynb` file to analyze its JSON structure, focusing on the `cells` array. 
2. **Edit Safely**: Apply the required modifications to the `source` arrays. 
    * **Crucial**: Ensure each line in the array is a separate string ending in `\n`.
    * **Example**: `"source": ["import os\n", "print(os.name)\n"]`
3. **Validate Structure**: Run `python -m json.tool filename.ipynb` to ensure the file is still valid JSON.
4. **Validate Syntax**: Run `python scripts/verify_ipynb.py --syntax-only filename.ipynb`. 
    * If a `SyntaxError` is reported, check if you missed a `\n` at the end of a line in the `source` array.
    * Check for `\\n` or `\\"` which indicate accidental double-escaping.
5. **Audit the resulting Python code** e.g. to catch "JSON bleeding"-where JSON formatting (like `\n",`) accidentally leaks into code cells and e.g. to verify logical correctness.
    * **Convert to Python**: Run `jupyter nbconvert --to python <filename>.ipynb`.
    * **Audit Logic**: Read the generated `<filename>.py` file to ensure the code matches the intended logic and is free of stray JSON artifacts.
    * **Cleanup**: Delete the temporary `.py` file after verification.
5. **Verify Execution (If requested/expected)**: If the notebook is expected to execute cleanly, run `python scripts/verify_ipynb.py --execute filename.ipynb`.

### Anti-Patterns
* Treating the `.ipynb` file as a standard raw text file instead of a JSON document.
* Forgetting to add `\n` to individual lines within the `source` JSON array.
* Accidentally double-escaping backslashes (e.g., `\\n` instead of `\n`).
* Skipping syntax validation after modifying a code cell.
