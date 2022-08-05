import uuid
from os import listdir
from os.path import isfile, join
from typing import List


def list_all_files(path) -> List[str]:
    files = [f for f in listdir(path) if isfile(join(path, f))]
    return files


def generate_unique_filename(path) -> str:
    all_files = list_all_files(path)
    while True:
        filename = uuid.uuid4().hex
        if filename not in all_files:
            return filename
