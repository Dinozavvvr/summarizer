# Приложение для генерации Суммаризированного текста для научных статей в формате pdf

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
# Импорт утилиты для парсинга текста
from process_utils.parser import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    file = get_path(data_dir, '2eba0771-3907-4d7a-9fcb-a64a27c7e955.pdf')

    document = parse_pdf(file)
    log(document, True)

    text = document['sections'][0]['text']
    data = tokenize(text)
    log(data, True)
