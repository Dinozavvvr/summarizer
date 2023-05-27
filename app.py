# Приложение для генерации Суммаризированного текста для научных статей в формате pdf

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
# Импорт утилиты для парсинга текста
from utils.parser import *
from utils.preprocessor import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    file = get_path(data_dir, 'karl_marks.txt')

    document = read(file)
    log(document, True)

    text = document
    preprocessor = Preprocessor('russian')
    data = preprocessor.preprocess(text)
    log(data.json(), True)
