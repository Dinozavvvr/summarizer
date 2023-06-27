import json
from collections import OrderedDict

from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from knox.auth import TokenAuthentication

from api.serializers import DocumentCollectionSerializer, DocumentCollectionCreateSerializer, \
    DocumentCollectionTraineResultSerializer
from base.models import DocumentCollection, Document, DocumentCollectionTraineResult, Metric
from base.services.summarization import SummarizationService


class DocumentCollectionViewSet(viewsets.ModelViewSet):
    queryset = DocumentCollection.objects.all()
    serializer_class = DocumentCollectionSerializer
    summarization_service = SummarizationService()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    @action(detail=True, methods=['post'])
    def traine(self, request, pk=None):
        # Получаем данные из запроса
        collection_id = pk

        try:
            # Получаем коллекцию документов по id
            collection = DocumentCollection.objects.get(id=collection_id)
        except DocumentCollection.DoesNotExist:
            return Response({'error': 'Коллекция документов не найдена'}, status=status.HTTP_404_NOT_FOUND)

        trainee_result = DocumentCollectionTraineResult()
        trainee_result.collection = collection
        trainee_result.population_size = int(request.data.get('population_size'))
        trainee_result.iteration_count = int(request.data.get('iteration_count'))
        trainee_result.save()

        for metric_id in request.data.get('metrics'):
            trainee_result.metrics.add(Metric.objects.get(id=metric_id))

        trainee_result.save()

        # Обучаем
        weights, score = self.summarization_service.traine(trainee_result, collection.documents.all())
        trainee_result.score = score
        metric_weight_map = OrderedDict()

        for i, metric in enumerate(trainee_result.metrics.all()):
            metric_weight_map[metric.id] = weights[i]

        trainee_result.weights = json.dumps(metric_weight_map)
        trainee_result.save()

        serializer = DocumentCollectionTraineResultSerializer(trainee_result)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        serializer = DocumentCollectionCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.validated_data['user'] = request.user
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

        document_id = request.data.get('document_id')
        document = Document.objects.get(id=document_id)
        collection.documents.add(document)
        return Response({'detail': 'Документ успешно добавлен в коллекцию'})

    @action(detail=True, methods=['post'])
    def add_documents(self, request, pk=None):
        try:
            documents = request.data.get('documents', [])
            collection = self.get_object()

            collection.documents.clear()

            for document_data in documents:
                document_id = document_data.get('id')
                document = Document.objects.get(id=document_id)
                collection.documents.add(document)

            return Response({'message': 'Документы успешно добавлены в коллекцию.'})
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Отображаем только коллекции документов, принадлежащие текущему пользователю
        queryset = queryset.filter(user=self.request.user)
        queryset = queryset.prefetch_related('documents')
        return queryset