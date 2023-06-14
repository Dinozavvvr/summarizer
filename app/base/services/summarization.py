from base.models import DocumentCollection
from summarizer.common.file.fileutils import *
from summarizer.core.genetic import SummarizationGeneticAlgoritm
from summarizer.core.scoring import *
from summarizer.core.summarizer import Summarizer, Article
from summarizer.utils.parser import parse_pdf

import logging

logger = logging.getLogger(__name__)


class SummarizationService:

    def __init__(self, pop_size=6, iterations_limit=1000, language="russian"):
        self.pop_size = pop_size
        self.language = language
        self.interations_limit = iterations_limit
        self.keywords = self.__get_keywords()

    def summarize(self, collection: DocumentCollection, document, max_len=300):
        article = self.__prepare_articles([document])[0]
        weights = [float(w) for w in collection.weights.split(', ')]

        summarizer = Summarizer([
            TF(), TF_ISF(), POS_F(),
            POS_L(), POS_B(), COV(),
            KEY(), LUHN(), LEN_CH(),
            LEN_W(), SVD(), TITLE_O(),
            TITLE_J(), TITLE_C(), TEXT_RANK()
        ], weights, max_len=max_len, keywords=self.keywords)

        return summarizer.summarize(article)

    def traine(self, documents):
        summarizer = Summarizer([
            TF(), TF_ISF(), POS_F(),
            POS_L(), POS_B(), COV(),
            KEY(), LUHN(), LEN_CH(),
            LEN_W(), SVD(), TITLE_O(),
            TITLE_J(), TITLE_C(), TEXT_RANK()
        ])
        ga = SummarizationGeneticAlgoritm(self.pop_size, self.__prepare_articles(documents), summarizer,
                                          self.language)

        return ga.start(self.interations_limit)

    @staticmethod
    def __prepare_articles(documents):
        articles = []
        for document in documents:
            base_path = Path('D:/Study/PythonProjects/summarizer/app/')
            file_path = base_path.joinpath(document.file.name)
            logger.debug(document.file.name)
            text = parse_pdf(file_path.resolve())
            title = document.title

            articles.append(Article(title, text, document.annotation))

        return articles

    @staticmethod
    def __get_keywords():
        with open('keywords.txt', 'r') as f:
            return f.read().replace('\n', ' ')
