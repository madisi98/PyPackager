import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in', '--input_path', help='Input path pointing to the root of the package', required=True)
    parser.add_argument('-out', '--output_path', help='Output path pointing to where the package will be stored', default='')
    parser.add_argument('-n', '--package_name', help='Package\'s name', default='')
    parser.add_argument('-r', '--requirements_file', help='Path to requirements file. If empty, will be searched inside the package as requirements.txt', default='')
    parser.add_argument('-ep', '--entry_points', help='Path to entry points file. If empty, only root.launcher:launcher will be added if found', default='')

    return parser.parse_args()
