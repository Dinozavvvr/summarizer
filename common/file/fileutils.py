# Методы для чтения и записи различных файлов
from pathlib import Path
import codecs


def get_path(directory, filename):
    return Path(directory, filename).resolve()


def save(dir_, file, format_, content):
    with open(str(dir_) + str(file) + format_, 'wb') as writer:
        writer.write(content)


def read(path):
    return codecs.open(path, "r", "utf_8_sig").read()
