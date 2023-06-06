# Извлечение статей с сайта lobachevskii-dml.ru
import uuid

from bs4 import BeautifulSoup as bs

from common.file.fileutils import save, saveb
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
            saveb(save_dir, uuid.uuid4(), '.pdf', document)
            return document


def get_all_abstracts(collection_count):
    link = 'https://lobachevskii-dml.ru/journal/ivm/'
    abstracts = []
    k = 1
    while netutils.is_accesable(link + str(k)) and k <= collection_count:
        abstracts.extend(get_collection_abstracts(link + str(k)))
        k += 1
    return abstracts


def get_collection_abstracts(ref):
    html = netutils.get_content(ref)
    soup = bs(html, bs_parser)

    articles = []
    abstracts = []

    articles_holder = soup.select_one('div .table')
    for a_tag in articles_holder.find_all('a'):
        href = a_tag.get('href')
        articles.append(href)

    for article in articles:
        abstracts.append(get_single_abstract(article))

    return abstracts


def get_single_abstract(ref):
    html = netutils.get_content(ref)
    soup = bs(html, bs_parser)

    abstract = soup.find('div', {'id': 'abstract'})
    if abstract is None:
        return None
    else:
        return abstract.text


def matches_sources(ref):
    for source in source_list:
        if ref.startswith(source):
            return True
    return False


if __name__ == '__main__':
    abstracts = get_all_abstracts(1000)
    save(save_dir, 'abstracts', '.txt', ' '.join(filter(lambda abstract: abstract is not None, abstracts)))
