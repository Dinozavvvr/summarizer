from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response

from api.serializers import DocumentCollectionSerializer, DocumentCollectionCreateSerializer
from base.models import DocumentCollection, Document
from base.services.summarization import SummarizationService


class DocumentCollectionViewSet(viewsets.ModelViewSet):
    queryset = DocumentCollection.objects.all()
    serializer_class = DocumentCollectionSerializer
    summarization_service = SummarizationService()

    @action(detail=True, methods=['post'])
    def summarize(self, request, pk=None):
        # Получаем данные из запроса
        collection_id = pk
        password = request.data.get('password')
        document_id = request.data.get('document_id')
        max_len = request.data.get('max_len')

        try:
            # Получаем коллекцию документов по id
            collection = DocumentCollection.objects.get(id=collection_id)
        except DocumentCollection.DoesNotExist:
            return Response({'error': 'Коллекция документов не найдена'}, status=status.HTTP_404_NOT_FOUND)

        try:
            # Получаем документ по id
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({'error': 'Документ не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем пароль
        if collection.password != password:
            return Response({'error': 'Неверный пароль для доступа к коллекции'}, status=status.HTTP_401_UNAUTHORIZED)

        # Получаем аннотацию
        summary = self.summarization_service.summarize(collection, document, max_len)
        # Возвращаем успешный ответ со списком файлов

        return Response({
            'sentences': summary.sentences,
            'text': summary.text
        })

    @action(detail=True, methods=['post'])
    def traine(self, request, pk=None):
        # Получаем данные из запроса
        collection_id = pk
        password = request.data.get('password')

        try:
            # Получаем коллекцию документов по id
            collection = DocumentCollection.objects.get(id=collection_id)
        except DocumentCollection.DoesNotExist:
            return Response({'error': 'Коллекция документов не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем пароль
        if collection.password != password:
            return Response({'error': 'Неверный пароль для доступа к коллекции'}, status=status.HTTP_401_UNAUTHORIZED)

        # Обучаем
        weights, score = self.summarization_service.traine(collection.documents.all())
        # Возвращаем успешный ответ со списком файлов

        collection.score = score
        collection.weights = ', '.join([str(w) for w in weights])
        collection.save()

        return Response({
            'score': score,
            'weights': weights
        })

    def create(self, request, *args, **kwargs):
        serializer = DocumentCollectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()

        # Проверяем пароль только при обновлении коллекции
        password = request.data.get('password')
        if password and password != instance.password:
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)

        if getattr(instance, '_prefetched_objects_cache', None):
            # Если у объекта есть предварительно загруженные объекты, их нужно обновить
            instance._prefetched_objects_cache = {}

        return Response(serializer.data)

    @action(detail=True, methods=['post'])
    def add_document(self, request, pk=None):
        collection = self.get_object()
        password = request.data.get('password')

        # Проверяем пароль перед добавлением документа
        if password and password != collection.password:
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        document_id = request.data.get('document_id')
        document = Document.objects.get(id=document_id)
        collection.documents.add(document)
        return Response({'detail': 'Документ успешно добавлен в коллекцию'})

    @action(detail=True, methods=['post'])
    def remove_document(self, request, pk=None):
        collection = self.get_object()
        password = request.data.get('password')

        # Проверяем пароль перед удалением документа
        if password and password != collection.password:
            return Response({'error': 'Неверный пароль'}, status=status.HTTP_401_UNAUTHORIZED)

        document_id = request.data.get('document_id')
        document = Document.objects.get(id=document_id)
        collection.documents.remove(document)
        return Response({'detail': 'Документ успешно удален из коллекции'})
