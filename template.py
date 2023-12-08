import os
import argparse
import logging
from pathlib import Path



#logging start
logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s')
project_name = "DLProject"

list_of_dir=[
    ".github/workflows/.gitkeep",
    f"src/{project_name}/__init__.py",
    f"src/{project_name}/components/__init__.py",
    f"src/{project_name}/utils/__init__.py",
    f"src/{project_name}/config/__init__.py",
    f"src/{project_name}/config/configuration.py",
    f"src/{project_name}/pipeline/__init__.py",
    f"src/{project_name}/entity/__init__.py",
    f"src/{project_name}/constants/__init__.py",
    "config/config.yaml",
    "dvc.yaml",
    "params.yaml",
    "requirements.txt",
    "setup.py",
    "research/trials.ipynb",
    "templates/index.html"
]

if __name__ == '__main__':

    args = argparse.ArgumentParser()

    args.add_argument('-n', '--project_name', default='DLProject', help='Project Name')
    args.add_argument('--author', default='Sadhin', help='Author Name')

    parsed_args = args.parse_args()

    logging.info("Creating the directory structure")

    for dir_ in list_of_dir:

        filepath = Path(dir_)
        filedir, filename = os.path.split(filepath)

        if filedir:
            os.makedirs(filedir, exist_ok=True)
            logging.info(f"Created the directory {filedir} for the file --> {filename}")

        if (not os.path.exists(filepath) or (os.path.getsize(filepath) == 0)):
            with open(filepath, 'w') as f:
                pass
            logging.info(f"Created the file {filename} in {filedir}")
        else:
            logging.info(f"File {filename} already exists in {filedir}")
