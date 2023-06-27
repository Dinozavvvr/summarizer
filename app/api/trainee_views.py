from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import permissions
from knox.auth import TokenAuthentication

from api.serializers import DocumentCollectionTraineResultSerializer
from base.models import DocumentCollectionTraineResult, Document
from base.services.summarization import SummarizationService


class IsUserOrPasswordMatch(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        collection = obj.collection
        password = request.data.get('password')
        return (request.user == collection.user) or (password and collection.password == password)


class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return IsUserOrPasswordMatch().has_object_permission(request, view, obj)


class TraineeViewSet(viewsets.ModelViewSet):
    queryset = DocumentCollectionTraineResult.objects.all()
    serializer_class = DocumentCollectionTraineResultSerializer
    summarization_service = SummarizationService()
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    def get_permissions(self):
        if self.action == 'summarize':
            return [permissions.IsAuthenticated(), IsUserOrPasswordMatch()]
        else:
            return [permissions.IsAuthenticated()]

    @action(detail=True, methods=['post'])
    def summarize(self, request, pk=None):
        # Получаем данные из запроса
        trainee_id = pk
        password = request.data.get('password')
        document_id = request.data.get('document_id')
        max_len = int(request.data.get('max_len'))

        try:
            trainee = DocumentCollectionTraineResult.objects.get(id=trainee_id)
        except DocumentCollectionTraineResult.DoesNotExist:
            return Response({'error': 'Модель не найдена'}, status=status.HTTP_404_NOT_FOUND)

        # Проверяем доступ
        if not IsUserOrPasswordMatch().has_object_permission(request, self, trainee):
            return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)

        try:
            # Получаем документ по id
            document = Document.objects.get(id=document_id)
        except Document.DoesNotExist:
            return Response({'error': 'Документ не найден'}, status=status.HTTP_404_NOT_FOUND)

        # Получаем аннотацию
        summary = self.summarization_service.summarize(trainee, document, max_len)

        return Response({
            'sentences': summary.sentences,
            'text': summary.text
        })

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        if not IsUserOrPasswordMatch().has_object_permission(request, self, instance):
            return Response({'error': 'Доступ запрещен'}, status=status.HTTP_403_FORBIDDEN)
        serializer = self.get_serializer(instance)
        return Response(serializer.data)

