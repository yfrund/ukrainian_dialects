import random
from pathlib import Path
from collections import defaultdict

random.seed(42)

def create_reference(input_root=Path('.'), output_dir=Path('reference')):
    '''
    picks a roughly even number of lines per class from every model
    '''
    models = [d for d in input_root.iterdir() if d.is_dir()]
    num_models = len(models)
    files_by_name = defaultdict(list)

    #collect classes and ensure that the classes are represented in all models
    for model in models:
        for file_path in model.iterdir():
            if file_path.is_file():
                files_by_name[file_path.name].append(file_path)

    output_dir.mkdir(exist_ok=True)

    shared_files = {fname: paths for fname, paths in files_by_name.items() if len(paths) == num_models}

    for file_name, file_paths in shared_files.items():
        contents = [p.read_text(encoding='utf-8').splitlines() for p in file_paths]
        num_lines = len(contents[0])

        line_indeces = list(range(num_lines))
        random.shuffle(line_indeces)
        model_assignments = [None] * num_lines

        for i, idx in enumerate(line_indeces):
            model_assignments[idx] = i % num_models
        
        reference_lines = [
            contents[model_assignments[i]][i] for i in range(num_lines)
        ]

        
        (output_dir / file_name).write_text('\n'.join(reference_lines), encoding='utf-8')

if __name__ == '__main__':
    create_reference(input_root=Path('./path/to/source/files'), output_dir=Path('./path/to/save/references'))