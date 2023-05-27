# Извлечение статей с сайта lobachevskii-dml.ru
import uuid

from bs4 import BeautifulSoup as bs

from common.file.fileutils import save
from common.net import netutils

bs_parser = 'html.parser'
save_dir = '../data/'
source_list = [
    'http://mathnet.ru',
    'https://mathnet.ru'
]


def get_document_collection(ref):
    html = netutils.get_content(ref)
    soup = bs(html, bs_parser)

    articles = []

    articles_holder = soup.select_one('div .table')
    for a_tag in articles_holder.find_all('a'):
        href = a_tag.get('href')
        articles.append(href)

    for i, article in enumerate(articles):
        articles[i] = get_single_document(article)

    return articles


def get_single_document(ref):
    html = netutils.get_content(ref)
    soup = bs(html, bs_parser)

    a_tags = soup.find_all('a')

    for a_tag in a_tags:
        href = a_tag.get('href')
        if matches_sources(href):
            document = netutils.get_content(href)
            save(save_dir, uuid.uuid4(), '.pdf', document)
            return document


def matches_sources(ref):
    for source in source_list:
        if ref.startswith(source):
            return True
    return False


if __name__ == '__main__':
    url = 'https://lobachevskii-dml.ru/journal/ivm/162'

    get_document_collection(url)
