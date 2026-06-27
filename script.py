
import json, os
base = 'output/california_housing_project'

nb_path = f'{base}/california_housing_project.ipynb'
with open(nb_path, 'r', encoding='utf-8') as f:
    nb = json.load(f)

# Find and fix the broken cell
for cell in nb['cells']:
    if cell['cell_type'] == 'code':
        src = cell['source']
        if isinstance(src, list):
            src_str = ''.join(src)
        else:
            src_str = src
        if "grid_dt.best_score_:.4f" in src_str:
            fixed = src_str.replace(
                "print('Best F1:', grid_dt.best_score_:.4f)",
                "print(f'Best F1: {grid_dt.best_score_:.4f}')"
            )
            cell['source'] = [fixed]
            print("Fixed cell found and patched.")
            break

with open(nb_path, 'w', encoding='utf-8') as f:
    json.dump(nb, f, ensure_ascii=False, indent=2)

print("Notebook saved.")
