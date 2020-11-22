import os
import shutil
import re

from .args import parse_args
from .parser import parse_script
from .write_setup import write_setup


def launcher():
    args = parse_args()
    input_path = re.sub('/$', '', args.input_path)
    output_path = re.sub('/$', '', args.output_path)
    if not output_path:
        output_path = input_path + '_PACKAGE'
    if not args.package_name:
        args.package_name = input_path.split('/')[-1]

    src_path = os.path.join(output_path, 'src')
    package_path = os.path.join(src_path, args.package_name)
    if os.path.exists(package_path):
        option = input('[WARNING]: Output path already exists. Remove? (Y/n): ')
        if not option or re.match('(?i)y(es)?$', option):
            shutil.rmtree(package_path)
        else:
            raise(FileExistsError)

    os.makedirs(package_path)
    write_setup(os.path.join(src_path, 'setup.py'), args)

    for curdir, subdirs, files in os.walk(input_path):
        if '__pycache__' in curdir:
            continue
        output_curdir = os.path.join(package_path, curdir[len(input_path)+1:])
        for subdir in subdirs:
            if '__pycache__' in subdir:
                continue
            os.makedirs(os.path.join(output_curdir, subdir))
        for script in files:
            parse_script(args, curdir, script, output_curdir)
        if '__init__.py' not in files:
            open(os.path.join(output_curdir, '__init__.py'), 'w')

if __name__ == "__main__":
    launcher()
