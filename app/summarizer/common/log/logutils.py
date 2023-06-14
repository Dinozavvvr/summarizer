# Методы для логирования
import pprint

# константы
pp = pprint.PrettyPrinter(indent=4)


def jlog(json):
    pp.pprint(json)


def dflog(dataframe):
    print(dataframe.name)
    print(dataframe.to_string())


def log(data):
    print(data)
