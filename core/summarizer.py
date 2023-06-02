# функция для построения итогового текста длинной от min до max на основании Score метрики приделожений из текста
from common.log.logutils import *
from core.scoring import *
from utils.preprocessor import *


class Article:

    def __init__(self, title: str, text: str, annotation: str = None):
        self.title = title
        self.text = text
        self.annotation = annotation


class Summary:

    def __init__(self, sentences):
        self.sentences = sentences
        self.text = ' '.join(sentences)


class Summarizer:

    def __init__(self, metrics: [Metric], weights: [float], language='russian', max_len=300):
        self.language = language
        self.metrics = metrics
        self.weights = weights
        self.max_len = max_len

        if len(self.metrics) == 0:
            raise ValueError('Metrics cannot be empty')
        if len(self.metrics) != len(self.weights):
            raise ValueError('Weights len must be the same as metrics len')

        # SCORE - матрица
        self.score_matrix = ScoreMatrix(self.metrics)
        self.preprocessor = Preprocessor(self.language)

    def summarize(self, article: Article, max_len=self.max_len, verbose=False):
        document = self.preprocessor.preprocess(article.text, article.title)
        matrix, dataframe = self.score_matrix.compute(document)

        if verbose:
            jlog(document.json())
            jlog(self.score_matrix.json())
            dflog(dataframe)

        # подсчитываем final score для каждого предложения
        scores = []
        for i in range(len(matrix)):
            sentence_score = 0
            for j in range(len(self.metrics)):
                sentence_score += matrix[i][j] * self.weights[j]
            scores.append(sentence_score)

        return self.build_abstract(max_len, document.original.sentences, scores)

    @staticmethod
    def build_abstract(max_len, sentences, scores):
        sentences = [sentence.value for sentence in sentences]
        sentence_metrics = list(zip(sentences, scores))
        sorted_sentences = sorted(sentence_metrics, key=lambda x: x[1], reverse=True)

        selected_sentences = []
        total_words = 0

        for sentence, metric in sorted_sentences:
            words_count = len(sentence.split())

            if total_words + words_count <= max_len:
                selected_sentences.append(sentence)
                total_words += words_count

        return Summary(selected_sentences)
