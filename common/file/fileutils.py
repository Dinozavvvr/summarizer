# Методы для чтения и записи различных файлов
from pathlib import Path


def get_path(directory, filename):
    return Path(directory, filename).resolve()
