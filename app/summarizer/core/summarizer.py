# функция для построения итогового текста длинной от min до max на основании Score метрики приделожений из текста
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_distances

from summarizer.common.log.logutils import *
from summarizer.core.scoring import *
from summarizer.utils.preprocessor import *


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

    def __init__(self, metrics: [Metric], weights: [float] = None, language='russian', max_len=300,
                 keywords=None, min_keyword_impact=0.1, max_keyword_impact=0.3):
        # base
        self.language = language
        self.metrics = metrics
        self.max_len = max_len
        self.weights = weights
        # keywords
        self.keywords = keywords
        self.min_keyword_impact = min_keyword_impact
        self.max_keyword_impact = max_keyword_impact

        if self.weights is None:
            self.weights = []
        if self.keywords is None:
            self.keywords = []

        if len(self.metrics) == 0:
            raise ValueError('Metrics cannot be empty')

        # SCORE - матрица
        self.score_matrix = ScoreMatrix(self.metrics)
        self.preprocessor = Preprocessor(self.language)

    def summarize(self, article: Article, max_len=None, verbose=False):
        if max_len is None:
            max_len = self.max_len

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

        # изменяем final score на основе keyword
        self.__keyword_based_classification(scores, document)

        return self.__build_abstract(max_len, document.original.sentences, scores)

    # вариация метода summarize для вызова Генетическим Алгоритмом
    def summarize_(self, document: Document, score_matrix, weights, max_len=None):
        if max_len is None:
            max_len = self.max_len

        # подсчитываем final score для каждого предложения
        scores = []
        for i in range(len(score_matrix)):
            sentence_score = 0
            for j in range(len(self.metrics)):
                sentence_score += score_matrix[i][j] * weights[j]
            scores.append(sentence_score)

        self.__keyword_based_classification(scores, document)

        return self.__build_abstract(max_len, document.original.sentences, scores)

    @staticmethod
    def __build_abstract(max_len, sentences, scores):
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

    def __keyword_based_classification(self, scores, document: Document):
        sentences = document.processed.sentences
        scores_boost = []

        for sentence in sentences:
            distance = self.get_distance(sentence.value, self.keywords)
            if distance != 1.0:
                scores_boost.append((1 - distance) * 5)
            else:
                scores_boost.append(0)

        scores_final_boost = []
        length = len(scores_boost)

        for i in range(length):
            left_sum = 0
            right_sum = 0

            # Суммируем значения слева от текущего элемента
            for j in range(i - 2, i):
                if j >= 0:
                    left_sum += scores_boost[j] / 2

            # Суммируем значения справа от текущего элемента
            for k in range(i + 1, i + 3):
                if k < length:
                    right_sum += scores_boost[k] / 2

            modified_value = (left_sum + right_sum + scores_boost[i])
            scores_final_boost.append(modified_value)

        for i in range(len(scores)):
            scores[i] *= 1 + scores_final_boost[i]

    @staticmethod
    def get_distance(sentence, keywords):
        vectorizer = TfidfVectorizer(lowercase=True)
        tfidf_matrix = vectorizer.fit_transform([sentence, keywords])
        distance = cosine_distances(tfidf_matrix[0], tfidf_matrix[1])

        return distance[0][0]
