import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer

class Document:
    def __init__(self, title, text):
        self.title = title
        self.text = text
        self.sentences = text.split('.')

class TFMetric:
    def __init__(self):
        self.vectorizer = TfidfVectorizer()

    def compute(self, document: Document = None):
        sentences = document.sentences

if __name__ == '__main__':
    document = Document(title='Example', text='This This This is a test document. It contains some sentences.')
    tf_metric = TFMetric()
    tf_sums = tf_metric.compute(document=document)
    for i, sentence in enumerate(document.sentences):
        print(f"TF sum for sentence {i + 1}: {tf_sums[i]}")
