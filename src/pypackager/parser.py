import os
import shutil
import re


def search_import(input_path, line):
    import_chain = re.sub(r' as \w+$', '', line)
    import_chain = re.sub(r' import ', '.', import_chain)
    import_chain = re.sub(r'(from|import) ', '', import_chain)
    import_chain = import_chain.split('.')
    function_import = []

    while import_chain:
        script_path = os.path.join(input_path, '/'.join(import_chain)+'.py')
        if os.path.isfile(script_path):
            return script_path, function_import
        function_import += import_chain[-1:]
        import_chain = import_chain[:-1]

    return '', []

def get_relative_path(script_path, import_path):
    # script_name = script_path.split('/')[-1]
    script_path = '/'.join(script_path.split('/')[:-1])
    import_name = re.sub(r'\.py$', '', import_path.split('/')[-1])
    import_path = '/'.join(import_path.split('/')[:-1])
    
    return os.path.join(os.path.relpath(import_path, script_path), import_name)

def parse_script(input_path, script_dir, script_name, destiny):
    script_path = os.path.join(script_dir, script_name)
    if re.search(r'\.py$', script_name):
        script_lines = open(script_path).readlines()
        script_lines = [re.sub('\n', '', x) for x in script_lines]
        with open(os.path.join(destiny, script_name), 'w') as new_script:
            for line in script_lines:
                if re.search(r'(from [\w.]+ )?import [\w.]+', line):
                    import_path, function_import = search_import(input_path, line)
                    if import_path:
                        relative_path = get_relative_path(script_path, import_path)
                        dots = '.' * max(1, relative_path.count('.')//2 + 1)
                        relative_path = re.sub('^[./]+', '', relative_path)
                        relative_path = relative_path.split('/') + function_import
                        new_line = f'from {dots}{".".join(relative_path[:-1])} import {relative_path[-1]}'
                        new_line += re.search(r' as \w+$', line) or ''
                        new_script.write(new_line)
                    else:
                        new_script.write(line)
                else:
                    new_script.write(line)
                new_script.write('\n')
    else:
        shutil.copy(script_path, destiny)
    
