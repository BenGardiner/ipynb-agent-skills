import json
import sys
import os

def clear_outputs(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            nb = json.load(f)
        
        for cell in nb.get('cells', []):
            if 'outputs' in cell:
                cell['outputs'] = []
            if 'execution_count' in cell:
                cell['execution_count'] = None
        
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(nb, f, indent=1, ensure_ascii=False)
            f.write('\n')
        print(f"Cleared outputs for {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python clear_notebooks.py <notebook1.ipynb> [notebook2.ipynb ...]")
        sys.exit(1)
        
    files = sys.argv[1:]
    for f in files:
        if os.path.exists(f):
            clear_outputs(f)
        else:
            print(f"File not found: {f}")
