import re
import uuid

from gingerit.gingerit import GingerIt
from nltk.corpus import stopwords
from nltk.stem import SnowballStemmer
from nltk.tokenize import sent_tokenize, word_tokenize
from pymorphy2 import MorphAnalyzer
from pyaspeller import YandexSpeller

morph = MorphAnalyzer()


class Word:

    def __init__(self, word: str, original: str, sentence):
        self.value = word
        self.original = original
        self.sentence = sentence

    def json(self):
        return {
            'value': self.value,
            'original': self.original,
            'sentence': self.sentence.id
        }


class Sentence:

    def __init__(self, sentence: str = None, words: [Word] = None, original=None):
        self.value = sentence
        self.words = words
        # optional
        self.original = original
        # auto
        self.id = uuid.uuid4()

    def json(self):
        return {
            'id': self.id,
            'value': self.value,
            'original': None if self.original is None else self.original.id,
            'words': [word.json() for word in self.words]
        }


class Text:

    def __init__(self, text: str, sentences: [Sentence], title: Sentence = None):
        self.value = text
        self.sentences = sentences
        self.title = title

    def json(self):
        return {
            'title': self.title.json(),
            'value': self.value,
            'sentences': [sentence.json() for sentence in self.sentences]
        }


class Document:
    def __init__(self, original: Text, processed: Text):
        self.original = original
        self.processed = processed

    def json(self):
        return {
            'original': self.original.json(),
            'processed': self.processed.json()
        }


class Preprocessor:

    def __init__(self, language):
        # Общие константы
        self.language = language
        self.stops = set(stopwords.words(language))
        self.speller = YandexSpeller(lang=self.language[0:2])

    @staticmethod
    def lemmatize_many(tokens):
        lemmas = {}

        for token in tokens:
            token_lem = morph.normal_forms(token)[0]
            if token_lem not in lemmas:
                lemmas[token_lem] = [token]
            else:
                lemmas[token_lem].append(token)

        return lemmas

    @staticmethod
    def lemmatize(token):
        return morph.normal_forms(token)[0]

    @staticmethod
    def stem(token, language):
        return SnowballStemmer(language).stem(token)

    @staticmethod
    def clear(value, is_word=False):
        value = value.strip()

        value = re.sub('ё', 'e', value)
        value = re.sub(r'[^А-Яа-яA-Za-z-.ёЁ]', ' ', value)
        value = re.sub('\n-', '', value)
        value = re.sub('\n', ' ', value)
        value = re.sub(r'^-.*', value[1:], value)
        value = re.sub(r'^.*-$', value[:-1], value)
        value = re.sub(r'\s\s+', ' ', value)
        value = re.sub(r'\d', '', value)

        if is_word:
            if len(value) < 3:
                return ''

        return value

    @staticmethod
    def sentenize(text, language):
        sents = sent_tokenize(text, language)

        sents = list(filter(lambda s: len(s) >= 10, sents))
        return sents

    @staticmethod
    def tokenize(sentence, language):
        return word_tokenize(sentence, language)

    def preprocess(self, text, title=None):
        """
        :param text - оригинальный необработанный текст
        :param title - заголовок статьи
        :return PreprocessedText {
            original = Text {
                value: '...'
                sentences: [Sentence {
                    original: None,
                    words: [Word {
                        original: None,
                        value: ''
                    }]
                }, ...]
            },
            processed = Text {
                text: '...'
                sentences: [Sentence {
                    original: Sentence (link),
                    value: '...',
                    words: [Word {
                        original: '',
                        value: ''
                    }, ...]
                }, ... ]
            }
        }
        """

        # Оригинальный текст
        original_sentences = []
        for sent in self.sentenize(text, self.language):
            sentnece = Sentence(sent)
            words = []

            for token in self.tokenize(sent, self.language):
                words.append(Word(token, token, sentnece))
            sentnece.words = words

            original_sentences.append(sentnece)

        # заголовок
        original_title = Sentence(title)
        original_title.words = [Word(token, token, original_title) for token in self.tokenize(title, self.language)]

        original_text = Text(text, original_sentences, original_title)

        # Обработанный текст
        processed_sentences = []
        for i, sent in enumerate(self.sentenize(text, self.language)):
            sentence = Sentence(original=original_sentences[i])
            sent = self.clear(sent)

            words = []
            for token in [token for token in self.tokenize(sent, self.language) if token not in self.stops]:
                word = self.clear(token, True)
                if word != '':
                    word = self.lemmatize(word.lower())
                    words.append(Word(word, token, sentence))

            if len(words) == 0:
                continue

            sentence.value = " ".join([word.value for word in words])
            sentence.words = words
            processed_sentences.append(sentence)

        # заголовок
        processed_title = Sentence(original=original_title)
        processed_title.words = [Word(self.lemmatize(token), token, processed_title)
                                 for token in self.tokenize(self.clear(title), self.language)]
        processed_title.value = " ".join([word.value for word in processed_title.words])

        processed_text = Text(". ".join([sentence.value for sentence in processed_sentences]),
                              processed_sentences, processed_title)

        return Document(original_text, processed_text)
