import argparse


def parse_args():
    parser = argparse.ArgumentParser()

    parser.add_argument('-in', '--input-path', help='Input path pointing to the root of the package', required=True)
    parser.add_argument('-out', '--output-path', help='Output path pointing to where the package will be stored', default='')
    parser.add_argument('-n', '--package-name', help='Package\'s name', default='')
    parser.add_argument('-r', '--requirements-file', help='Path to requirements file. If empty, will be searched inside the package as requirements.txt', default='')
    parser.add_argument('-ep', '--entry-points', help='Path to entry points file. If empty, only root.launcher:launcher will be added if found', default='')
    parser.add_argument('--keep-script-execution', action='store_true', help='Whether or not you want to keep script execution besides entry point execution')

    return parser.parse_args()
