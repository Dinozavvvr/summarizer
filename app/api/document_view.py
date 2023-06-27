from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions, status
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser
from knox.auth import TokenAuthentication
from rest_framework.response import Response

from api.serializers import DocumentSerializer
from base.models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API для работы с документами
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (TokenAuthentication,)

    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @action(methods=['GET'], detail=True, url_path='/download')
    @swagger_auto_schema(responses={200: 'application/pdf'})
    def download(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        file_path = document.file.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())

        queryset = queryset.filter(commited=True)

        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            return self.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def get_queryset(self):
        queryset = super().get_queryset()
        # Отображаем только документы, принадлежащие текущему пользователю
        queryset = queryset.filter(user=self.request.user)
        return queryset