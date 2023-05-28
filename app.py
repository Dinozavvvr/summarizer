# Приложение для генерации Суммаризированного текста для научных статей в формате pdf
import numpy as np

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
from core.scoring import *
from core.summarizer import Summarizer, Article
# Импорт утилиты для парсинга текста
from utils.preprocessor import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    # скачивание
    file = get_path(data_dir, 'karl_marks.txt')
    # file = get_path(data_dir, 'math-text.txt')
    text = read(file)
    # log(document)

    # предобработка
    preprocessor = Preprocessor('russian')
    title = 'Философия Карла Маркса и Энгельса'
    # title = 'ТЕОРЕТИКО-ГРУППОВАЯ ФУНКЦИЯ МЕБИУСА ДЕЛЬСАРТА И ТЕОРИЯ ЛИНЕЙНЫХ ПРЕДСТАВЛЕНИЙ КОНЕЧНЫХ ГРУПП'.lower()
    summarizer = Summarizer([
        TF(), TF_ISF(), POS_F(),
        POS_L(), POS_B(), COV(),
        KEY(), LUHN(), LEN_CH(),
        LEN_W(), SVD(), TITLE_O(),
        TITLE_J(), TITLE_C(), TEXT_RANK()
    ], np.ones(15))

    summary = summarizer.summarize(300, Article(title, text), verbose=True)
    log(summary.text)
