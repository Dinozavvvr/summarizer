import random

from nltk.translate.bleu_score import sentence_bleu

from summarizer import Article, Summarizer
from utils.preprocessor import *


class SummarizationGeneticAlgoritm:

    def __init__(self, chromosome_size, population_size, articles: [Article],
                 summarizer: Summarizer, language="russian"):
        # количество хромосом в популяции
        self.population_size = population_size
        # количество генов в хромосоме
        self.chromosome_size = chromosome_size
        # полуляция - двумерный массив в котором каждый элемент относится к i-ой хромосоме
        self.population = self.generate_first_population()
        # коллекция статей используемых в фитнесс функции для обучения
        self.articles = articles
        # суммаризатор
        self.summarizer = summarizer
        # препроцессор
        self.preprocessor = Preprocessor(language)
        # длинна анн

    # функция для определния начальной популяции
    def __generate_first_population(self):
        return [1 / self.chromosome_size for _ in range(self.chromosome_size)]

    # стоп функция
    def __stop_condition(self, iteration, limit):
        pass

    # фитнесс функция
    def __fitness(self):
        fitness_result = []

        for chomosome in self.population:
            # применяем веса
            self.summarizer.weights = chomosome

            # получаем значение фитнесс функции
            value = 0

            for article in self.articles:
                generated_summary = self.summarizer.summarize(article, ).text
                original_summary = article.annotation

                value += self.__closest(generated_summary, original_summary)

            fitness_result.append(float(value) / len(self.articles))

        return fitness_result

    def __closest(self, original_summary: str, generated_summary: str):
        original_summary = self.preprocessor.clear(original_summary.lower())
        generated_summary = self.preprocessor.clear(generated_summary.lower())

        return sentence_bleu([original_summary.split()], generated_summary.split(),
                             smoothing_function=smoothing.method1)

    # функция для нахождения интервалов для выборки хромосом
    @staticmethod
    def __get_suitability_intervals(fitness_result):
        suitability = []
        coefs_sum = 0
        for i in range(len(fitness_result)):
            fitness_result[i] = 1 / fitness_result[i]
            coefs_sum += fitness_result[i]
        for coef in coefs:
            suitability.append(coef / fitness_result)
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
        crossover_point = random.randint(1, self.chromosome_size - 1)

        return self.__normalize(parent_1[:crossover_point] + parent_2[crossover_point:])

    # функция нормализации генов внутри хромосомы
    @staticmethod
    def __normalize(chromosome):
        total = sum(chromosome)

        for i in range(len(chromosome)):
            chromosome[i] /= total

    # функция мутации
    def __mutation(self):
        for index, chromosome in enumerate(self.population):
            mutated_chromosome = chromosome.copy()

            # случайным образом выбираем ген для мутации
            selected_gen = random.randint(0, self.chromosome_size - 1)

            # изменяем значение гена на случайное значение из промежутка [-0.1, 0.1]
            mutated_chromosome[selected_gen] += random.uniform(-0.1, 0.1)
            mutated_chromosome[selected_gen] = max(min(mutated_chromosome[selected_gen], 1), 0)

            # нормализуем
            self.__normalize(mutated_chromosome)
            self.population[index] = mutated_chromosome

    # функция для запуска генетического алгоритма
    def start(self, limit=-1):
        iteration = 0
        # пока имеется смысл продолжать
        while not self.__stop_condition(iteration, limit):
            iteration += 1
            # фитнесс функция
            fitness_result = self.__fitness()
            # эволюция
            self.population = self.__next_population(fitness_result)
            # мутация
            self.__mutation()

        # возвращаем наилучшее поколение и наилучшую хромосому
        return self.population
