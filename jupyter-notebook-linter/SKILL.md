---
name: jupyter-notebook-linter
description: Tool to format, lint, and validate Jupyter Notebook (.ipynb) files via the command line. Use when you need to resolve syntax errors, style violations, or reformat notebook code cells. Do not use for standard Python (.py) scripts or non-Python notebooks.
---

# Jupyter Notebook Linter and Formatter

## 1. Environment Setup
Install the necessary default packages for Jupyter Notebook formatting and linting. Do not offer alternatives unless the environment strictly prevents these from installing.
Execute:
`pip install "black[jupyter]" nbqa flake8`

## 2. Formatting and Linting Workflow
Follow these steps in strict chronological order to format and validate a target notebook.

### Step 0: Clear Cell Outputs
To clear all cell outputs and execution counts before formatting or committing.
Execute:
`python .gemini/skills/jupyter-notebook-linter/scripts/clear_notebooks.py <target_notebook.ipynb>`

### Step 1: Format Code
Reformat the Python code inside the notebook cells to match PEP 8 style using Black.
Execute:
`black <target_notebook.ipynb>`
If this command outputs errors, you must fix them before proceeding.

### Step 2: Syntax & Style Check
Identify syntax errors, unused imports, or style violations without changing the file using Flake8 via nbQA.
Execute:
`nbqa flake8 <target_notebook.ipynb>`
If this command outputs errors, you must triage and fix the critical violations in the notebook before proceeding to Step 3.

### Step 3: Execution Validation (Optional, If requested)
If requested by the user (or you can ask the user if you feel this execution is warranted):

Verify the notebook is syntactically valid and executes cleanly by running it headlessly.
Execute:
`jupyter nbconvert --to notebook --execute <target_notebook.ipynb>`

Only proceed and mark your task as successfully completed when this execution validation passes without errors.

