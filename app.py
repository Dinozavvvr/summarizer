# Приложение для генерации Суммаризированного текста для научных статей в формате pdf

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
# Импорт утилиты для парсинга текста
from utils.parser import *
from utils.preprocessor import *
from core.scoring import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    # скачивание
    file = get_path(data_dir, 'karl_marks.txt')
    # file = get_path(data_dir, 'math-text.txt')
    document = read(file)
    # log(document)

    # предобработка
    preprocessor = Preprocessor('russian')
    title = 'Философия Карла Маркса'
    document = preprocessor.preprocess(document, title)
    jlog(document.json())

    # нахождение Score-матрицы
    score_matrix = ScoreMatrix(document)
    score_matrix.add_metric(TF())
    score_matrix.add_metric(TF_ISF())
    score_matrix.add_metric(POS_F())
    score_matrix.add_metric(POS_L())
    score_matrix.add_metric(POS_B())
    score_matrix.add_metric(COV())
    score_matrix.add_metric(KEY())
    score_matrix.add_metric(LUHN())
    score_matrix.add_metric(LEN_CH())
    score_matrix.add_metric(LEN_W())
    score_matrix.add_metric(SVD())
    jlog(score_matrix.json())

    matrix_df = score_matrix.compute()
    dflog(matrix_df)


