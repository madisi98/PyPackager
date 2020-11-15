# PyPackager

## Installation
	cd PyPackager/src
	python setupy.py install

## Usage
	usage: pypackager [-h] -in INPUT_PATH [-out OUTPUT_PATH] [-n PACKAGE_NAME] [-r REQUIREMENTS_FILE] [-ep ENTRY_POINTS]


	optional arguments:
	  -h, --help            show this help message and exit
	  -in INPUT_PATH, --input_path INPUT_PATH
                        Input path pointing to the root of the package
	  -out OUTPUT_PATH, --output_path OUTPUT_PATH
                        Output path pointing to where the package will be stored
	  -n PACKAGE_NAME, --package_name PACKAGE_NAME
                        Package's name
	  -r REQUIREMENTS_FILE, --requirements_file REQUIREMENTS_FILE
                        Path to requirements file. If empty, will be searched inside the package as requirements.txt
	  -ep ENTRY_POINTS, --entry_points ENTRY_POINTS
                        Path to entry points file. If empty, only root.launcher:launcher will be added if found
