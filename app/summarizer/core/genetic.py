import random

from nltk.translate.bleu_score import sentence_bleu, SmoothingFunction

from summarizer.core.summarizer import Article, Summarizer
from summarizer.utils.preprocessor import *


class PreprocessedArticle:

    def __init__(self, score_matrix, document):
        self.score_matrix = score_matrix
        self.document = document


class SummarizationGeneticAlgoritm:

    def __init__(self, population_size, articles: [Article],
                 summarizer: Summarizer, language="russian"):
        self.language = language
        # количество хромосом в популяции
        self.population_size = population_size
        # количество генов в хромосоме
        self.chromosome_size = len(summarizer.metrics)
        # полуляция - двумерный массив в котором каждый элемент относится к i-ой хромосоме
        self.population = self.__generate_first_population()
        # коллекция статей используемых в фитнесс функции для обучения
        self.articles = articles
        # суммаризатор
        self.summarizer = summarizer
        # препроцессор
        self.preprocessor = Preprocessor(language)
        # кэш
        self.article_caches = {}
        # предобрабатываем документы
        self.__prepare_data()

    def __prepare_data(self):
        for article in self.articles:
            document = self.preprocessor.preprocess(article.text, article.title)

            matrix, dataframe = self.summarizer.score_matrix.compute(document)
            self.article_caches[article] = PreprocessedArticle(matrix, document)

    # функция для определния начальной популяции
    def __generate_first_population(self):
        population = []
        for _ in range(self.population_size):
            chromosome = []
            while True:
                genes = [random.uniform(0, 100) for _ in range(self.chromosome_size)]
                sum_genes = sum(genes)
                if sum_genes != 0:
                    self.__normalize(genes)
                    chromosome = genes
                    break
            population.append(chromosome)
        return population

    # стоп функция
    @staticmethod
    def __stop_condition(iteration, limit):
        return iteration == limit

    # фитнесс функция
    def __fitness(self):
        fitness_result = []

        for chomosome in self.population:
            # получаем значение фитнесс функции
            value = 0

            for article in self.articles:
                article_cache: PreprocessedArticle = self.article_caches[article]

                original_summary = article.annotation
                generated_summary = self.summarizer.summarize_(article_cache.document, article_cache.score_matrix,
                                                               chomosome, max_len=len(original_summary)).text

                value += self.__closest(original_summary, generated_summary)

            fitness_result.append(float(value) / len(self.articles))

        return fitness_result

    def __closest(self, original_summary: str, generated_summary: str):
        original_summary_ = self.__clear_annotations(original_summary.lower())
        generated_summary_ = self.__clear_annotations(generated_summary.lower())

        smoothing = SmoothingFunction()
        return sentence_bleu([original_summary_.split()], generated_summary_.split(),
                             smoothing_function=smoothing.method1)

    def __clear_annotations(self, text):
        text = self.preprocessor.clear(text)
        words = []
        for token in [token for token in self.preprocessor.tokenize(text, self.language)
                      if token not in self.preprocessor.stops]:
            word = self.preprocessor.clear(token, True)
            if word != '':
                words.append(self.preprocessor.lemmatize(word.lower()))

        return ' '.join(words)

    # функция для нахождения интервалов для выборки хромосом
    @staticmethod
    def __get_suitability_intervals(fitness_result):
        suitability = []
        coefs_sum = 0
        for i in range(len(fitness_result)):
            if fitness_result[i] != 0:
                fitness_result[i] = 1 / fitness_result[i]
            coefs_sum += fitness_result[i]
        for coef in fitness_result:
            suitability.append(coef / coefs_sum)
        for i in range(1, len(suitability)):
            suitability[i] += suitability[i - 1]

        return suitability

    # функция для выбора родительского элемента на основании вероятностного интервала
    @staticmethod
    def __get_parent(suitability_intervals, exclude=-1):
        while True:
            r = random.uniform(0, 1)
            left = 0
            for i, s in enumerate(suitability_intervals):
                if left <= r < s:
                    if i != exclude:
                        return i
                left = s

    # функция получения следующего поколения
    def __next_population(self, fitness_result):
        suitability_intervals = self.__get_suitability_intervals(fitness_result)

        next_population = []
        # получение элементов нового поколения путем выбора родительских
        # элементов на основе вероятностных интервалов и скрещивания
        for _ in range(self.population_size):
            # первый родитель (index)
            parent_i1 = self.__get_parent(suitability_intervals)
            # второй родитель (index)
            parent_i2 = self.__get_parent(suitability_intervals, parent_i1)
            # скрещивание
            next_population.append(self.__crossover(parent_i1, parent_i2))

        return next_population

    # функция скрещивания
    def __crossover(self, parent_i1, parent_i2):
        # первый родитель
        parent_1 = self.population[parent_i1]
        # второй родитель
        parent_2 = self.population[parent_i2]

        # выбор точки кроссовера
        crossover_point = random.randint(0, self.chromosome_size - 1)

        child = parent_1[:crossover_point] + parent_2[crossover_point:]
        self.__normalize(child)

        return child

    # функция нормализации генов внутри хромосомы
    @staticmethod
    def __normalize(chromosome):
        total = sum(chromosome)

        for i in range(len(chromosome)):
            if total != 0:
                chromosome[i] /= total

    # функция мутации
    def __mutation(self):
        for index, chromosome in enumerate(self.population):
            mutated_chromosome = chromosome.copy()

            # случайным образом выбираем ген для мутации
            selected_gen = random.randint(0, self.chromosome_size - 1)

            # изменяем значение гена на случайное значение из промежутка [-0.1, 0.1]
            mutated_chromosome[selected_gen] += random.uniform(-5, 5)
            mutated_chromosome[selected_gen] = max(min(mutated_chromosome[selected_gen], 1), 0.1)

            # нормализуем
            self.__normalize(mutated_chromosome)
            self.population[index] = mutated_chromosome

    # функция для запуска генетического алгоритма
    def start(self, limit=-1, debug=False):
        iteration = 0
        # пока имеется смысл продолжать
        best_weights = []
        best_fitness_score = 0
        while not self.__stop_condition(iteration, limit):
            iteration += 1
            # фитнесс функция
            fitness_result = self.__fitness()

            for i, fitness_score in enumerate(fitness_result):
                if fitness_score > best_fitness_score:
                    best_fitness_score = fitness_score
                    best_weights = self.population[i]

            # выводим информацию
            if debug:
                self.log(iteration, self.population, fitness_result)
            # эволюция
            self.population = self.__next_population(fitness_result)
            # мутация
            self.__mutation()

        # возвращаем наилучшее поколение и наилучшую хромосому
        return best_weights, best_fitness_score

    @staticmethod
    def log(iteration, population, fitness_result):
        print('\nIteration num:', iteration)
        print('\nAverage fitness:', sum(fitness_result))

        for i, choromose in enumerate(population):
            print('Chromosome num:', i, 'Fitness:', fitness_result[i], 'Genes:', choromose)
