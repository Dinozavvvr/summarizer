# функция для построения итогового текста длинной от min до max на основании Score метрики приделожений из текста
from core.scoring import *
from utils.preprocessor import *


class Article:

    def __init__(self, title, text):
        self.title = title,
        self.text = text


class Summarizer:

    def __init__(self, metrics: [Metric], language='russian'):
        self.language = language
        self.metrics = metrics
        if len(self.metrics) == 0:
            raise ValueError('Metrics cannot be empty')

        # SCORE - матрица
        self.score_matrix = ScoreMatrix(self.metrics)
        self.preprocessor = Preprocessor(self.language)

    def summarize(self, article: Article):
        document = self.preprocessor.preprocess(article.text, article.title)
        matrix, dataframe = self.score_matrix.compute(document)


def build_abstract(min_len, max_len, sentences, scores):
    sentence_metrics = list(zip(sentences, scores))
    sorted_sentences = sorted(sentence_metrics, key=lambda x: x[1], reverse=True)

    selected_sentences = []
    total_words = 0

    for sentence, metric in sorted_sentences:
        words_count = len(sentence.split())

        if min_len <= total_words + words_count <= max_len:
            selected_sentences.append(sentence)
            total_words += words_count

    return selected_sentences
