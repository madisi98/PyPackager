import os
import shutil
import re


def add_script_support(lines, new_script, args, script_dir):
    indents = set([len(re.search(' *', x).group()) for x in lines]) - {0}
    for indent in sorted(indents, reverse=True):
        if all([not x % indent for x in indents]):
            break
    indent = ' '*indent

    root_relative_path = '\'..\''
    package_name = args.package_name

    if args.input_path != script_dir:
        root_relative_path = f'\'{os.path.join(os.path.relpath(args.input_path, script_dir), "..")}\''
        package_name += ''.join([f'.{x}' for x in os.path.relpath(script_dir, args.input_path).split('/')])

    new_script.write(f'\n')
    new_script.write(f'import os\n')
    new_script.write(f'import sys\n')
    new_script.write(f'# Allow relative imports when being executed as script.\n')
    new_script.write(f'if __name__ == "__main__" and __package__ is None:\n')
    new_script.write(f'{indent}sys.path.insert(0, os.path.join(os.path.dirname(__file__), {root_relative_path}))\n')
    new_script.write(f'{indent}import {package_name}\n')
    new_script.write(f'{indent}__package__ = "{package_name}"\n')
    new_script.write(f'\n')

def search_import(input_path, line):
    indents = re.search(r'^ *', line).group()

    import_chain = re.sub(r'^ +', '', line)
    import_chain = re.sub(r' as \w+$', '', import_chain)
    import_chain = re.sub(r' import ', '.', import_chain)
    import_chain = re.sub(r'(from|import) ', '', import_chain)
    import_chain = import_chain.split('.')
    function_import = []

    while import_chain:
        script_path = os.path.join(input_path, '/'.join(import_chain)+'.py')
        if os.path.isfile(script_path):
            return script_path, function_import, indents
        function_import += import_chain[-1:]
        import_chain = import_chain[:-1]

    return '', [], indents

def get_relative_path(script_path, import_path):
    # script_name = script_path.split('/')[-1]
    script_path = '/'.join(script_path.split('/')[:-1])
    import_name = re.sub(r'\.py$', '', import_path.split('/')[-1])
    import_path = '/'.join(import_path.split('/')[:-1])
    
    return os.path.join(os.path.relpath(import_path, script_path), import_name)

def parse_script(args, script_dir, script_name, destiny):
    comment_header = True

    script_path = os.path.join(script_dir, script_name)
    shutil.copy(script_path, destiny)
    if re.search(r'\.py$', script_name):
        script_lines = open(script_path).readlines()
        script_lines = [re.sub('\n', '', x) for x in script_lines]
        new_script = open(os.path.join(destiny, script_name), 'w')
        for line in script_lines:
            new_line = line
            if not re.search('^\s*(#|"""|\'\'\')', line) and comment_header:
                comment_header = False
                if args.keep_script_execution and any([re.search('if +__name__ *== *["\']__main__["\']:', x) for x in script_lines]):
                    add_script_support(script_lines, new_script, args, script_dir)

            if re.search(r'(from [\w.]+ )?import [\w.]+', line):
                import_path, function_import, indents = search_import(args.input_path, line)
                if import_path:
                    relative_path = get_relative_path(script_path, import_path)
                    dots = '.' * max(1, relative_path.count('.')//2 + 1)
                    relative_path = re.sub('^[./]+', '', relative_path)
                    relative_path = relative_path.split('/') + function_import
                    as_clause = re.search(r'(| as \w+)$', line).group()
                    new_line = f'{indents}from {dots}{".".join(relative_path[:-1])} import {relative_path[-1]}{as_clause}'

            new_script.write(new_line + '\n')
        new_script.close()
