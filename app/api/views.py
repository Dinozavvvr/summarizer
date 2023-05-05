from rest_framework.response import Response
from rest_framework.decorators import api_view


@api_view(['POST'])
def serialize_article(link):
    """
    Метод для получения суммаризации для отдельно взятой статьи

    :param link: ссылка на страницу с документом
    :return: саммари
    """
    data = {"summary": "it's summary"}
    return Response(data)


@api_view(['POST'])
def serialize_article_collection(link):
    """
    Метод для получения суммари для коллекции статей
    :param link:
    :return:
    """
    summary = {}
    return Response(summary)
