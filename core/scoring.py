# Нахождение SCORE-матрицы
import numpy as np


class Document:

    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.sentences = text.slit('.')


class Metric:

    def compute(self, document: Document = None):
        raise NotImplementedError

    def get(self, sentence_index):
        raise NotImplementedError

    def description(self):
        print(self)


class TF(Metric):

    def compute(self, document: Document = None):
        pass

    def get(self, sentence_index):
        pass


class ScoreMatrix:

    def __init__(self):
        self.metrics = []

    def add_metric(self, metric: Metric):
        self.metrics.append(metric)

    def remove_metric(self, metric: Metric):
        self.metrics.remove(metric)

    def description(self):
        # metrics
        print('Metrics count: ', len(self.metrics))
        [metric.description() for metric in self.metrics]

    def compute(self, document: Document):
        matrix = np.zeros((len(document.sentences), len(self.metrics)))

        for i, metric in enumerate(self.metrics):
            metric.compute(document)
            for j, sentence in enumerate(document.sentences):
                matrix[j][i] = metric.compute(sentence, document)

        print(matrix)


if __name__ == '__main__':
    scoreMatrix = ScoreMatrix()

    scoreMatrix.add_metric(MetricImpl1())
    scoreMatrix.add_metric(MetricImpl1())
    scoreMatrix.add_metric(MetricImpl1())
    scoreMatrix.add_metric(MetricImpl1())

    scoreMatrix.description()

    doc = Document('title', 'original text')
    scoreMatrix.compute(doc)
