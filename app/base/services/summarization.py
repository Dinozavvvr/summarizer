import json
import logging
from collections import OrderedDict

from base.models import DocumentCollection
from summarizer.core.genetic import SummarizationGeneticAlgoritm
from summarizer.core.scoring import *
from summarizer.core.summarizer import Summarizer, Article

logger = logging.getLogger(__name__)


class SummarizationService:

    def __init__(self, language="russian"):
        self.language = language
        self.keywords = self.__get_keywords()

    def summarize(self, trainee, document, max_len=300):
        article = self.__prepare_articles([document])[0]
        weights = list(json.loads(trainee.weights, object_pairs_hook=OrderedDict).values())

        summarizer = self.__get_summarizer(trainee.metrics.values_list('id', flat=True), self.keywords)
        summarizer.weights = weights

        return summarizer.summarize(article, max_len)

    def traine(self, trainee, documents):
        summarizer = self.__get_summarizer(trainee.metrics.values_list('id', flat=True), self.keywords)
        ga = SummarizationGeneticAlgoritm(trainee.population_size, self.__prepare_articles(documents), summarizer,
                                          self.language)

        return ga.start(trainee.iteration_count)

    @staticmethod
    def __get_summarizer(metric_ids, keywords=None):
        metrics_mapping = {
            1: TF(),
            2: TF_ISF(),
            3: POS_F(),
            4: POS_L(),
            5: POS_B(),
            6: COV(),
            7: KEY(),
            8: LUHN(),
            9: LEN_CH(),
            10: LEN_W(),
            11: SVD(),
            12: TITLE_O(),
            13: TITLE_J(),
            14: TITLE_C(),
            15: TEXT_RANK(),
        }

        metrics = [metrics_mapping[metric_id] for metric_id in metric_ids]
        summarizer = Summarizer(metrics, keywords=keywords)
        return summarizer

    @staticmethod
    def __prepare_articles(documents):
        articles = []
        for document in documents:
            articles.append(Article(document.title, document.text, document.annotation))

        return articles

    @staticmethod
    def __get_keywords():
        with open('keywords.txt', 'r', encoding='utf-8') as f:
            return f.read().replace('\n', ' ')
