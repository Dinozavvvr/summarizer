# Методы для парсинга научного текста
import re

from nltk.tokenize import sent_tokenize, word_tokenize
from science_parse_api.api import parse_pdf as parser
from pymorphy2 import MorphAnalyzer

# Настройки подключения к sciense-process_utils по умолчанию
host_default = 'http://127.0.0.1'
port_default = 10001

# Общие константы
language = 'russian'
morph = MorphAnalyzer()


def parse_pdf(file, hostname=host_default, port=port_default):
    return parser(hostname, file, port=str(port))


def lemmatize(tokens):
    lemmas = {}

    for token in tokens:
        token_lem = morph.normal_forms(token)[0]
        if token_lem not in lemmas:
            lemmas[token_lem] = [token]
        else:
            lemmas[token_lem].append(token)

    return lemmas


def clear(text, is_word=False):
    text = text.strip()

    text = re.sub(r'[^А-Яа-яA-Za-z-.]', ' ', text)
    text = re.sub('\n-', '', text)
    text = re.sub('\n', ' ', text)
    text = re.sub(r'^-.*', text[1:], text)
    text = re.sub(r'^.*-$', text[:-1], text)
    text = re.sub(r'\s\s+', ' ', text)
    text = re.sub(r'\d', '', text)

    if is_word:
        if len(text) <= 3:
            return ''

    return text


def sentenize(text):
    sents = sent_tokenize(text, language)

    sents = list(filter(lambda s: len(s) >= 10, sents))
    return sents


def tokenize(text):
    """
    Стркутура возвращаемого объекта
    data = {
        'sentences': [],
        'words': [],
    }
    """
    data = {
        'original': {},
        'processed': {}
    }

    sents = sentenize(text)
    data.get('original')['text'] = text
    data.get('original')['sentences'] = sents
    data.get('processed')['sentences'] = [clear(sent) for sent in sents]

    tokens = []
    for i, sent in enumerate(sents):
        words = list(filter(lambda x: x != '', [clear(word, True) for word in word_tokenize(sent, language=language)]))
        for word in words:
            tokens.append([word.lower(), i])

    data.get('processed')['words'] = tokens

    return data
