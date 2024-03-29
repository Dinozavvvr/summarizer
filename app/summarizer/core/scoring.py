# Нахождение SCORE-матрицы
import math

import nltk
import numpy as np
import pandas as pd
import yake
from nltk.cluster.util import cosine_distance
from sklearn.metrics.pairwise import cosine_similarity

from summarizer.utils.preprocessor import Document


class Metric:
    """
    Базовый интерфейс для классов реализующих функционал метрик
    """

    def compute(self, document: Document):
        raise NotImplementedError

    def get(self, sentence_index):
        raise NotImplementedError

    def json(self):
        return {
            'name': self.name,
            'description': self.description,
        }


class TF(Metric):
    """
    TF - метрика средней по всем словам, включенных в предложения,
    частоты появляения в тексте
    """
    name = 'TF'
    description = 'Term frequency metric'

    def __init__(self):
        self.tf_per_sentence = []
        self.tf_per_token = {}

    def compute(self, document: Document):
        self.tf_per_sentence = []

        # токены со всех предложений
        tokens = {}
        # общее количество токенов в тексте
        tokens_count = 0
        # токенизированные предложения
        tokenized_sentences = []

        for sentence in document.processed.sentences:
            for word in sentence.words:
                tokens.setdefault(word.value, 0)
                tokens[word.value] += 1
                tokens_count += 1
            tokenized_sentences.append([word.value for word in sentence.words])
        # значение tf для отдельно взятых токенов
        self.tf_per_token = {token_value: token_count / tokens_count for token_value, token_count in tokens.items()}

        # подстчитываем TF
        for sentence in document.processed.sentences:
            sentence_tf = 0
            for word in sentence.words:
                sentence_tf += self.tf_per_token[word.value]

            sentence_tf /= len(sentence.words)
            self.tf_per_sentence.append(sentence_tf)

    def get(self, sentence_index):
        return self.tf_per_sentence[sentence_index]


class POS_F(Metric):
    """
    POS_F - метрика придает предложениям, которые находятся ближе к началу больше значения
    """
    name = 'POS_F'
    description = 'Closeness of sentence to the beginning of the document'

    def __init__(self):
        self.pos_f_per_sentece = []

    def compute(self, document: Document):
        self.pos_f_per_sentece = []

        for i in range(1, len(document.processed.sentences) + 1):
            self.pos_f_per_sentece.append(1 / i)

    def get(self, sentence_index):
        return self.pos_f_per_sentece[sentence_index]


class POS_L(Metric):
    """
    POS_L - метрика придает предложениям, которые находятся ближе к концу больше значения
    """
    name = 'POS_L'
    description = 'Closeness of sentence to the ending of the document'

    def __init__(self):
        self.pos_l_per_sentece = []

    def compute(self, document: Document):
        self.pos_l_per_sentece = np.zeros(len(document.processed.sentences))

        for i in range(len(document.processed.sentences)):
            self.pos_l_per_sentece[i] = (1 / (len(document.processed.sentences) - i))

    def get(self, sentence_index):
        return self.pos_l_per_sentece[sentence_index]


class POS_B(Metric):
    """
    POS_B - метрика придает предложениям, которые находятся ближе к концу или началу больше значения
    """
    name = 'POS_B'
    description = 'Closeness of sentence to the borders of the document'

    def __init__(self):
        self.pos_b_per_sentece = []

    def compute(self, document: Document):
        self.pos_b_per_sentece = np.zeros(len(document.processed.sentences))

        for i in range(1, len(document.processed.sentences) + 1):
            self.pos_b_per_sentece[i - 1] = max(1 / (len(document.processed.sentences) - i + 1), 1 / i)

    def get(self, sentence_index):
        return self.pos_b_per_sentece[sentence_index]


class COV(Metric):
    """
    COV - Отношения количества ключевых слов в предложении
    к общему количеству ключевых слов в тексте (количество ключевых слов задается вручную)
    """
    name = 'COV'
    description = 'Ratio of keywords number in sentece to keywords count'

    def __init__(self, count=30, language='ru', ngram_max_size=1, deduplication_threshold=0.9):
        # optional
        self.count = count
        self.language = language
        self.ngram_max_size = ngram_max_size
        self.deduplication_threshold = deduplication_threshold

        self.extractor = yake.KeywordExtractor(lan=self.language, n=self.ngram_max_size,
                                               dedupLim=self.deduplication_threshold,
                                               top=self.count, features=None)
        self.cov_per_sentence = []

    def compute(self, document: Document):
        self.cov_per_sentence = []

        extraction = self.extractor.extract_keywords(document.processed.value)
        keywords = [keyword[0] for keyword in extraction]

        for sentence in document.processed.sentences:
            keywords_per_sentence = set()
            for word in sentence.words:
                if word.value in keywords:
                    keywords_per_sentence.add(word.value)
            self.cov_per_sentence.append(0 if len(keywords_per_sentence) == 0
                                         else len(keywords_per_sentence) / len(keywords))

    def get(self, sentence_index):
        return self.cov_per_sentence[sentence_index]


class KEY(Metric):
    """
    KEY - сумма частот ключевых слов в предложении
    """
    name = 'KEY'
    description = 'Sum of the keyword frequencies'

    def __init__(self, count=30, language='ru', ngram_max_size=1, deduplication_threshold=0.9):
        # optional
        self.count = count
        self.language = language
        self.ngram_max_size = ngram_max_size
        self.deduplication_threshold = deduplication_threshold

        self.extractor = yake.KeywordExtractor(lan=self.language, n=self.ngram_max_size,
                                               dedupLim=self.deduplication_threshold,
                                               top=self.count, features=None)
        self.key_per_sentence = []

    def compute(self, document: Document):
        self.key_per_sentence = []

        extraction = self.extractor.extract_keywords(document.processed.value)
        keywords = [keyword[0] for keyword in extraction]
        probabilities = [keyword[1] for keyword in extraction]

        keywords_ = {}
        # общее количество ключевых слов в тексте
        keywords_total_count = 0
        # токенизированные предложения
        tokenized_sentences = []

        for sentence in document.processed.sentences:
            for word in sentence.words:
                if word.value in keywords:
                    keywords_.setdefault(word.value, 0)
                    keywords_[word.value] += 1
                    keywords_total_count += 1
            tokenized_sentences.append([word.value for word in sentence.words])
        # значение tf для отдельно взятых ключевых слов
        keyword_probs = {keyword_value: keyword_count / keywords_total_count
                         for keyword_value, keyword_count in keywords_.items()}

        for sentence in tokenized_sentences:
            sentence_key = 0
            for word in sentence:
                if word in keyword_probs:
                    sentence_key += keyword_probs[word]

            self.key_per_sentence.append(sentence_key)

    def get(self, sentence_index):
        return self.key_per_sentence[sentence_index]


class LUHN(Metric):
    """
    LUHN - частотная метрика по алгоритму Луна
    """
    name = 'LUHN'
    description = 'The LUHN summarization algoritm based on selecting ' \
                  'the most important sentences from a text based on the ' \
                  'frequency of significant keywords'

    def __init__(self, count=30):
        self.count = count
        self.luhn_for_sentence = []

    def compute(self, document: Document):
        self.luhn_for_sentence = []

        tokens = [word.value for sentence in document.processed.sentences for word in sentence.words]
        token_frequence = nltk.FreqDist(tokens)
        keywords = [token[0] for token in token_frequence.most_common(self.count)]

        for sentence in document.processed.sentences:
            self.luhn_for_sentence.append(self.get_sentence_weight(sentence, keywords))

    @staticmethod
    def get_sentence_weight(sentence, keywords):
        sen_list = [word.value for word in sentence.words]
        window_start = 0
        window_end = -1

        for i in range(len(sen_list)):
            if sen_list[i] in keywords:
                window_start = i
                break

        for i in range(len(sen_list) - 1, 0, -1):
            if sen_list[i] in keywords:
                window_end = i
                break

        if window_start > window_end:
            return 0

        window_size = window_end - window_start + 1

        keywords_cnt = 0
        for w in sen_list:
            if w in keywords:
                keywords_cnt += 1

        return keywords_cnt * keywords_cnt * 1.0 / window_size

    def get(self, sentence_index):
        return self.luhn_for_sentence[sentence_index]


class LEN_CH(Metric):
    """
    LEN_CH - чем предложение длиннее чем оно более значимое
    """
    name = 'LEN_CH'
    description = 'Normalized number of characters in the sentence'

    def __init__(self):
        self.len_ch_per_sentence = []

    def compute(self, document: Document):
        self.len_ch_per_sentence = []

        for sentence in document.processed.sentences:
            self.len_ch_per_sentence.append(len(sentence.value))

        # нормализуем
        self.len_ch_per_sentence = [score / max(self.len_ch_per_sentence) for score in self.len_ch_per_sentence]

    def get(self, sentence_index):
        return self.len_ch_per_sentence[sentence_index]


class LEN_W(Metric):
    """
    LEN_W - чем предложение длиннее чем оно более значимое
    """
    name = 'LEN_W'
    description = 'Normalized number of words in the sentence'

    def __init__(self):
        self.len_w_per_sentence = []

    def compute(self, document: Document):
        self.len_w_per_sentence = []

        for sentence in document.processed.sentences:
            self.len_w_per_sentence.append(len(sentence.words))

        # нормализуем
        self.len_w_per_sentence = [score / max(self.len_w_per_sentence) for score in self.len_w_per_sentence]

    def get(self, sentence_index):
        return self.len_w_per_sentence[sentence_index]


class TF_ISF(Metric):
    """
    TF-ISF - тот же TF-IDF только вместо документов предолжения
    """
    name = 'TF_ISF'
    description = 'Term frequency–inverse sentence frequency'

    def __init__(self):
        self.tf_isf_per_sentence = []
        self.tf_isf_per_token = {}
        self.tf = TF()

    def compute(self, document: Document):
        self.tf_isf_per_sentence = []

        self.tf.compute(document)

        # находим ISF
        tokens_isf = {}
        for sentence in document.processed.sentences:
            sentence_words = []
            for word in sentence.words:
                if word.value not in sentence_words:
                    tokens_isf.setdefault(word.value, 0)
                    tokens_isf[word.value] += 1

                    sentence_words.append(word.value)

        sentence_count = len(document.processed.sentences)
        for sentence in document.processed.sentences:
            sentence_tf_isf = 0
            for word in sentence.words:
                word_tf_isf = self.tf.tf_per_token[word.value] \
                              * (1 - (math.log(tokens_isf[word.value], 10) / math.log(sentence_count, 10)))
                if word not in self.tf_isf_per_token:
                    self.tf_isf_per_token[word.value] = word_tf_isf

                sentence_tf_isf += word_tf_isf

            self.tf_isf_per_sentence.append(sentence_tf_isf)

    def get(self, sentence_index):
        return self.tf_isf_per_sentence[sentence_index]


class SVD(Metric):
    """
    SVD - длинна вектора предложений после SVD разложения
    """
    name = 'SVD'
    description = 'Length of a sentence vector in ∑^2 * Vt'

    def __init__(self):
        self.svd_per_sentence = []
        self.tf_isf = TF_ISF()

    def compute(self, document: Document):
        self.svd_per_sentence = []
        self.tf_isf.compute(document)
        # количество предложений
        m = len(self.tf_isf.tf_isf_per_sentence)
        # количество токенов
        n = len(self.tf_isf.tf_isf_per_token)

        # построение матрицы Sentence x Token
        matrix = np.zeros((n, m))
        i = 0
        for token, value in self.tf_isf.tf_isf_per_token.items():
            for j, sentence in enumerate(document.processed.sentences):
                words = [word.value for word in sentence.words]
                if token in words:
                    matrix[i][j] = value * 100
            i += 1

        u, s, vt = np.linalg.svd(matrix, False, True)
        self.svd_per_sentence = np.linalg.norm(np.dot(np.diag(s), vt), axis=0)

    def get(self, sentence_index):
        return self.svd_per_sentence[sentence_index]


class TITLE_O(Metric):
    """
    TITLE_O - Большее значение придается предложениям схожим с заголовком
    """
    name = 'TITLE_O'
    description = 'Overlap similarity between title and sentence'

    def __init__(self):
        self.title_o_per_sentence = []

    def compute(self, document: Document):
        self.title_o_per_sentence = []

        title_tokens = set([word.value for word in document.processed.title.words])

        for sentence in document.processed.sentences:
            sentence_tokens = set([word.value for word in sentence.words])
            sentence_title_o = len(sentence_tokens.intersection(title_tokens)) / min(len(title_tokens),
                                                                                     len(sentence_tokens))

            self.title_o_per_sentence.append(sentence_title_o)

    def get(self, sentence_index):
        return self.title_o_per_sentence[sentence_index]


class TITLE_J(Metric):
    """
    TITLE_J - Большее значение придается предложениям схожим с заголовком (по Жаккару)
    """
    name = 'TITLE_J'
    description = 'Jaccard similarity between title and sentence'

    def __init__(self):
        self.title_j_per_sentence = []

    def compute(self, document: Document):
        self.title_j_per_sentence = []

        title_tokens = set([word.value for word in document.processed.title.words])

        for sentence in document.processed.sentences:
            sentence_tokens = set([word.value for word in sentence.words])
            intersection = len(sentence_tokens.intersection(title_tokens))
            union = len(sentence_tokens) + len(title_tokens) - intersection

            self.title_j_per_sentence.append(float(intersection) / union)

    def get(self, sentence_index):
        return self.title_j_per_sentence[sentence_index]


class TITLE_C(Metric):
    """
    TITLE_C - Большее значение придается предложениям схожим с заголовком (Cosine)
    """
    name = 'TITLE_C'
    description = 'Cosine similarity between title and sentence'

    def __init__(self):
        self.title_c_per_sentence = []
        self.tf_isf = TF_ISF()

    def compute(self, document: Document):
        self.title_c_per_sentence = []

        self.tf_isf.compute(document)
        # количество предложений
        m = len(self.tf_isf.tf_isf_per_sentence)
        # количество токенов
        n = len(self.tf_isf.tf_isf_per_token)

        # построение матрицы Sentence x Token
        matrix = np.zeros((n, m + 1))
        i = 0
        for token, value in self.tf_isf.tf_isf_per_token.items():
            for j, sentence in enumerate(document.processed.sentences):
                words = [word.value for word in sentence.words]
                if token in words:
                    matrix[i][j] = value * 100
            i += 1

        title_vector = np.zeros(n)

        j = 0
        for token, value in self.tf_isf.tf_isf_per_token.items():
            words = [word.value for word in document.processed.title.words]
            if token in words:
                title_vector[j] = value * 100
            j += 1

        for sentence_vector in matrix.transpose():
            self.title_c_per_sentence.append(cosine_similarity([title_vector], [sentence_vector])[0][0])

    def get(self, sentence_index):
        return self.title_c_per_sentence[sentence_index]


class TEXT_RANK(Metric):
    name = "TEXT_RANK"
    description = "Page Rank implementation for texts"

    def __init__(self):
        self.text_rank_per_sentence = []

    def compute(self, document: Document):
        self.text_rank_per_sentence = []

        sentences = []
        for sentence in document.processed.sentences:
            sentences.append([word.value for word in sentence.words])

        matrix = self.build_similarity_matrix(sentences)
        self.text_rank_per_sentence = self.page_rank(matrix)

    def get(self, sentence_index):
        return self.text_rank_per_sentence[sentence_index]

    @staticmethod
    def page_rank(similarity_matrix):

        damping = 0.85
        min_diff = 1e-5
        steps = 100

        pr_vector = np.array([1] * len(similarity_matrix))

        previous_pr = 0
        for epoch in range(steps):
            pr_vector = (1 - damping) + damping * np.matmul(similarity_matrix, pr_vector)
            if abs(previous_pr - sum(pr_vector)) < min_diff:
                break
            else:
                previous_pr = sum(pr_vector)

        return pr_vector

    @staticmethod
    def build_similarity_matrix(sentences):
        sm = np.zeros([len(sentences), len(sentences)])

        for idx1 in range(len(sentences)):
            for idx2 in range(len(sentences)):
                if idx1 == idx2:
                    continue

                sm[idx1][idx2] = TEXT_RANK.__sentence_similarity(sentences[idx1], sentences[idx2])

        sm = TEXT_RANK.__get_symmetric_matrix(sm)

        norm = np.sum(sm, axis=0)
        sm_norm = np.divide(sm, norm, where=norm != 0)

        return sm_norm

    @staticmethod
    def __get_symmetric_matrix(matrix):
        return matrix + matrix.T - np.diag(matrix.diagonal())

    @staticmethod
    def __sentence_similarity(sent1, sent2):
        all_words = list(set(sent1 + sent2))

        vector1 = [0] * len(all_words)
        vector2 = [0] * len(all_words)

        for w in sent1:
            vector1[all_words.index(w)] += 1

        for w in sent2:
            vector2[all_words.index(w)] += 1

        return TEXT_RANK.core_cosine_similarity(vector1, vector2)

    @staticmethod
    def core_cosine_similarity(vector1, vector2):
        return 1 - cosine_distance(vector1, vector2)


class ScoreMatrix:

    def __init__(self, metrics: [Metric] = None):
        self.metrics = metrics
        if metrics is None:
            self.metrics = []

    def add_metric(self, metric: Metric):
        self.metrics.append(metric)

    def remove_metric(self, metric: Metric):
        self.metrics.remove(metric)

    def json(self):
        return {
            'metrics_count': len(self.metrics),
            'metrics': [metric.json() for metric in self.metrics]
        }

    def compute(self, document: Document):
        score_matrix = np.zeros((len(document.processed.sentences), len(self.metrics)))

        for i, metric in enumerate(self.metrics):
            metric.compute(document)
            for j, sentence in enumerate(document.processed.sentences):
                score_matrix[j][i] = metric.get(j)

        return score_matrix, self.__build_dataframe(document)

    def __build_dataframe(self, document: Document):
        sentence_count = len(document.processed.sentences)
        processed_sentences = [sentence.value for sentence in document.processed.sentences]
        original_sentences = [sentence.original.value for sentence in document.processed.sentences]

        data_frame = pd.DataFrame({
            'Sentence (Original)': original_sentences,
            'Sentence (Processed)': processed_sentences,
        })
        data_frame.name = 'Score-Matrix'
        for metric in self.metrics:
            data_frame[metric.name] = [metric.get(i) for i in range(sentence_count)]

        return data_frame
