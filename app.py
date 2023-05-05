# Приложение для генерации Суммаризированного текста для научных статей в формате pdf

# импорт утилит для работы с файлами и логами
from common.file.fileutils import *
from common.log.logutils import *
# Импорт утилиты для парсинга текста
from process_utils.parser import *

# константы
data_dir = 'data'

if __name__ == '__main__':
    file = get_path(data_dir, '0c1d21aa-863e-429b-8e91-5db748782651.pdf')

    document = parse_pdf(file)
    log(document, True)

    text = document['sections'][0]['text']
    data = tokenize(text)
    log(data, True)
