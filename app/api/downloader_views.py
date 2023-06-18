import os
import uuid

import requests
from django.core.files.base import ContentFile
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ModelViewSet, ViewSet
from rest_framework import status, serializers

from api.serializers import DocumentSerializer
from base.models import Document


class DownloaderViewSet(ModelViewSet):
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer

    class DownloadFileRequest(serializers.Serializer):
        title = serializers.CharField(max_length=1000)
        link = serializers.CharField(max_length=200000)
        annotation = serializers.CharField(max_length=100000000, allow_null=True)

    @action(detail=False, methods=['post'], serializer_class=DownloadFileRequest)
    def upload(self, request: DownloadFileRequest):
        serializer = self.get_serializer(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        link = serializer.validated_data['link']
        title = serializer.validated_data['title']
        annotation = serializer.validated_data['annotation']

        # Загрузка файла
        response = requests.get(link)
        if response.status_code != 200:
            return Response({'error': 'Не удалось загрузить файл'}, status=status.HTTP_400_BAD_REQUEST)

        # Получение имени файла из ссылки
        file_name = str(uuid.uuid4()) + '.pdf'

        # Создание объекта Document
        document = Document(title=title, annotation=annotation)

        # Сохранение файла в поле file модели Document
        document.file.save(file_name, ContentFile(response.content), save=True)

        serializer = DocumentSerializer(document)
        return Response(serializer.data, status=status.HTTP_201_CREATED)
