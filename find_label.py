from pathlib import Path

def find_dialect(target_line: str, target_file: str, source_dir: Path) -> str:

    '''
    This is a script that can be used to find out which file a line comes from:
    It goes through every file in the source directory and locates the source file.
    The name of the source file provides the dialect name.
    If source file is not located, returns 'uk'
    '''

    for file in source_dir.iterdir():
        if file.is_file() and file != Path(target_file): #so it doesn't look in the file that the source line comes from, i.e. test set
            with open(file, 'r', encoding='utf-8') as f:
                if target_line in f.read():
                    return f'uk_{file.stem[:5]}'
                
    return 'uk'

