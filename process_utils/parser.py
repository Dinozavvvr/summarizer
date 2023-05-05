# Методы для парсинга научного текста
from nltk.tokenize import sent_tokenize, word_tokenize
from science_parse_api.api import parse_pdf as parser

# Настройки подключения к sciense-parser по умолчанию
host_default = '127.0.0.1'
port_default = 10001

# Общие константы
language='russian'


def parse_pdf(file, hostname=host_default, port=port_default):
    return parser(hostname, file, port=port)


def tokenize(text):
    """
    Стркутура возвращаемого объекта
    data = {
        'sentences': [],
        'words': [],
        'stemmed': []
    }
    """
    data = {}

    data['sentences'] = sent_tokenize(text, language=language)
    data['words'] = word_tokenize(text, language=language)

    return data

