# функция для построения итогового текста длинной от min до max на основании Score метрики приделожений из текста
import random

from random_word import RandomWords

random_word = RandomWords()


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


def generate_test_text(s_cout, s_min_len, s_max_len):
    sentences = []
    for _ in range(s_cout):
        s_len = random.randint(s_min_len, s_max_len)
        sentence = ""
        word = random_word.get_random_word()
        for _ in range(s_len):
            sentence += f' {word} '
        sentences.append(sentence)

    return sentences


def generate_scores(count, min_val, max_val):
    return [random.uniform(min_val, max_val) for _ in range(count)]


def check_len(sentences):
    sum_ = 0
    for sentence in sentences:
        sum_ += len(sentence.split(' '))

    return sum_


def main():
    s_count = 30
    sentences = generate_test_text(s_count, 10, 20)
    scores = generate_scores(s_count, 0, 10)

    abstract = build_abstract(200, 300, sentences, scores)
    print(abstract)
    print('\n', sum(abstract))



if __name__ == '__main__':
    main()
