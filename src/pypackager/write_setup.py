import os
import re


def write_requires(setup, args):
    requirements_file = ''
    if not os.path.isfile(args.requirements_file):
        print('[INFO]: Searching for requirements.txt')
        for curdir, _, subfiles in os.walk(args.input_path):
            if 'requirements.txt' in subfiles:
                requirements_file = os.path.join(curdir, 'requirements.txt')
                print(f'[INFO]: Found {requirements_file}')
                break
    else:
       requirements_file = args.requirements_file 

    if requirements_file:
        reqs = open(requirements_file).read().splitlines()
        reqs = [f'        \'{x}\'' for x in reqs] # TODO: Analyse imports and get dependencies; The write becomes common and reqs must be passes or be found in globals.
        setup.write(f'    install_requires = [\n')
        setup.write(f',\n'.join(reqs))
        setup.write(f'\n')
        setup.write(f'    ],\n')
    else:
        print('[WARNING]: Unable to get dependencies. Skipping install_requires')

def write_entrypoints(setup, args):
    entrypoints = []
    if not os.path.isfile(args.entry_points):
        launcher = os.path.join(args.input_path, 'launcher.py')
        main = os.path.join(args.input_path, 'main.py')
        if os.path.isfile(launcher):
            if re.search(r'def launcher\(\):', open(launcher).read()):
                entrypoints = [f'{args.package_name}={args.package_name}.launcher:launcher']
        elif os.path.isfile(main):
            if re.search(r'def main\(\):', open(main).read()):
                entrypoints = [f'{args.package_name}={args.package_name}.main:main']
    else:
        entrypoints = open(args.entry_points).read().splitlines()
        entrypoints = [f'{args.package_name}-{x}' for x in entrypoints if re.search(r'^[\w-]+=(\w+\.?)+:\w+$', x)]

    if entrypoints:
        entrypoints = [f'            \'{x}\'' for x in entrypoints]
        setup.write('    entry_points     = {\n')
        setup.write('        \'console_scripts\': [\n')
        setup.write(f',\n'.join(entrypoints))
        setup.write(f'\n')
        setup.write('        ],\n')
        setup.write('    }\n')
    else:
        print('[WARNING]: Unable to get Entry points. Skipping entry_points')

def write_setup(path, args):
    with open(path, 'w') as setup:
        setup.write(f'import setuptools\n')
        setup.write(f'\n')
        setup.write(f'\n')

        setup.write(f'setuptools.setup(\n')
        setup.write(f'    name             = \'{args.package_name}\',\n')
        setup.write(f'    version          = \'0.0.0\',\n')
        setup.write(f'    description      = \'\',\n')
        setup.write(f'    url              = \'\',\n')
        setup.write(f'    author           = \'PyPackager\',\n')
        setup.write(f'    author_email     = \'\',\n')
        setup.write(f'    maintainer       = \'\',\n')
        setup.write(f'    maintainer_email = \'\',\n')
        setup.write(f'    packages         = setuptools.find_packages(),\n')

        write_requires(setup, args)
        write_entrypoints(setup, args)

        setup.write(')\n')

