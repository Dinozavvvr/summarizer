from django.http import FileResponse
from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.parsers import JSONParser, MultiPartParser, FormParser

from api.serializers import DocumentSerializer
from base.models import Document


class DocumentViewSet(viewsets.ModelViewSet):
    """
    API для работы с документами
    """
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
    permission_classes = [permissions.AllowAny]
    parser_classes = (JSONParser, MultiPartParser, FormParser)

    @action(methods=['GET'], detail=True, url_path='/download')
    @swagger_auto_schema(responses={200: 'application/pdf'})
    def download(self, request, pk):
        document = get_object_or_404(Document, pk=pk)
        file_path = document.file.path
        return FileResponse(open(file_path, 'rb'), content_type='application/pdf')
