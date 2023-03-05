# Приложение для генерации Суммаризированного текста для научных статей в формате pdf

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
# Импорт утилиты для парсинга текста
from parser.parser import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    file = get_path(data_dir, 'document-1.pdf')

    # document = parse_pdf(file)
    # log(document, True)

    data = tokenize("Я — к.т.н. Сижу на диван-кровати.")

    log(data, True)