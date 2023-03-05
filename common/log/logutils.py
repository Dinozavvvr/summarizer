# Методы для логирования
import pprint

# константы
pp = pprint.PrettyPrinter(indent=4)


def log(data, pretty=False):
    if pretty:
       pp.pprint(data)
    else:
        print(data)
