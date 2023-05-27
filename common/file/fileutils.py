# Методы для чтения и записи различных файлов
from pathlib import Path


def get_path(directory, filename):
    return Path(directory, filename).resolve()


def save(dir, file, format, content):
    with open(str(dir) + str(file) + format, 'wb') as writer:
        writer.write(content)


def read(path):
    with open(path, 'r') as reader:
        return reader.read()