import os
import json
import wget

from pathlib import Path
from os.path import dirname, abspath


BASE_DIR = dirname(abspath(__file__))
WOKRSPACE_FOLDER = "workspaces"
PROJECTS_FOLDER = "projects"
TASKS_FOLDER = "tasks"
ATTCHMENTS_FOLDER = "attachments"
COMMENTS_FOLDER = "comments"


def make_file_path(*parts):
    return os.path.join(BASE_DIR, *parts)


def make_folder_path(*parts):
    folder_path = os.path.join(BASE_DIR, *parts)
    make_missing_directories(folder_path)
    return folder_path


def make_missing_directories(full_path):
    Path(full_path).mkdir(parents=True, exist_ok=True)


def initialize_folders():

    for _folder in [WOKRSPACE_FOLDER, PROJECTS_FOLDER, TASKS_FOLDER, ATTCHMENTS_FOLDER, COMMENTS_FOLDER]:
        _folder_path = make_file_path(_folder)
        make_missing_directories(_folder_path)


def save_to_json(filepath, data):
    with open(filepath, "w") as outfile:
        json.dump(data, outfile, indent=4)


def download_file(url, filepath):
    response = wget.download(url, filepath)
