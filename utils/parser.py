# Методы для парсинга научного текста
import io

from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.pdfpage import PDFPage
from science_parse_api.api import parse_pdf as parser

# Настройки подключения к sciense-process_utils по умолчанию
host_default = 'http://127.0.0.1'
port_default = 10001


def parse_pdf(file, hostname=host_default, port=port_default):
    pdf = parser(hostname, file, port=str(port))

    return ' '.join([section['text'] for section in pdf['sections']])


# данный парсер применим для не отсканнированных pdf документов
def parse_pdf_2(file):
    input_stream = open(file, 'rb')

    res_manager = PDFResourceManager()
    ret_data = io.StringIO()
    txt_converter = TextConverter(res_manager, ret_data, laparams=LAParams())
    interpreter = PDFPageInterpreter(res_manager, txt_converter)

    for page in PDFPage.get_pages(input_stream):
        interpreter.process_page(page)

    return ret_data.getvalue()

