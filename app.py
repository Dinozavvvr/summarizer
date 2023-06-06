# Приложение для генерации Суммаризированного текста для научных статей в формате pdf
import numpy as np

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
from core.scoring import *
from core.summarizer import Summarizer, Article
from utils.parser import parse_pdf
from core.genetic import SummarizationGeneticAlgoritm
# Импорт утилиты для парсинга текста
from utils.preprocessor import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    # скачивание
    file = get_path(data_dir, '1.txt')
    # file = get_path(data_dir, '1.pdf')
    # text = parse_pdf(file)
    text = read(file)
    # log(document)

    # предобработка
    # preprocessor = Preprocessor('russian')
    # title = 'Философия Карла Маркса и Энгельса'
    # # title = 'ТЕОРЕТИКО-ГРУППОВАЯ ФУНКЦИЯ МЕБИУСА ДЕЛЬСАРТА И ТЕОРИЯ ЛИНЕЙНЫХ ПРЕДСТАВЛЕНИЙ КОНЕЧНЫХ ГРУПП'.lower()
    summarizer = Summarizer([
        TF(), TF_ISF(), POS_F(),
        POS_L(), POS_B(), COV(),
        KEY(), LUHN(), LEN_CH(),
        LEN_W(), SVD(), TITLE_O(),
        TITLE_J(), TITLE_C(), TEXT_RANK()
    ])
    #
    # summary = summarizer.summarize(300, Article(title, text), verbose=True)
    # log(summary.text)

    article = Article('ОТСУТСТВИЕ ПЕРИОДИЧЕСКИХ ОРБИТ У ОДНОГО КЛАССАДВУМЕРНЫХ СИСТЕМ КОЛМОГОРОВА', text, """
    Для двумерной системы Колмогорова, где R (x, y), S (x, y), P (x, y), Q (x, y),
M (x, y), N (x, y) — однородные многочлены степеней m, a, n, n, b, b соответственно, получено
явное выражение первого интеграла. Затем на его основе доказано отсутствие периодических
орбит и предельных циклов. Приведен пример применения этих результатов""")
#     article = Article('ОБЩЕСТВО ОБЩЕСТВА НИКЛАС ЛУМАН ЭВОЛЮЦИЯ', text, """
# Эволюция. Пер. с нем./ А. Антоновский. М: Издательство "Логос". 2005.-256 с.
# "Общество общества" Никласа Лумана - всеобъемлющее социологическое исследование
# общества как системы. Выработанная этим классиком современной социологии теория
# всесторонне и обоснованно описывает процесс возникновения Мирового Общества в качестве
# осевого для социального развития западной цивилизации как таковой. Используя такие
# универсальные - как для естественных, так и для социальных наук - ключевые понятия как
# аутопойесис, бифуркация, биологическая эволюция, хаос, система и функция, информация и
# коммуникация, Луман описывает динамику эволюционирования всех важнейших сфер
# социальности: Право и Политику, Науку и Образование, Религию и Искусство, Экономику и
# Любовьв""")
    genetic_algoritm = SummarizationGeneticAlgoritm(6, [article], summarizer)
    preprocessor = Preprocessor("russian")
    # preprocessor.preprocess(article.text, article.title)
    weights, score = genetic_algoritm.start(1000)
    print('Best weights:', weights)
    print('Best score:', score)

    genetic_algoritm.summarizer.weights = weights
    print('Final abstract:\n', genetic_algoritm.summarizer.summarize(article, len(article.annotation)).text)


