from django.conf import settings
from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class Document(models.Model):
    """
    Модель документа
    """
    title = models.CharField(max_length=1000)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', null=True)
    created = models.DateTimeField(auto_now_add=True)
    annotation = models.CharField(max_length=10000000, null=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True)
    text = models.TextField(null=True)
    commited = models.BooleanField(default=False)

    REQUIRED_FIELDS = ['title']

    def get_download_url(self):
        return reverse('document-download', args=[self.pk])


class DocumentCollection(models.Model):
    """
    Модель коллекции документов
    """
    name = models.CharField(max_length=1000)
    password = models.CharField(max_length=8)
    documents = models.ManyToManyField(Document)
    score = models.FloatField(null=True)
    weights = models.CharField(null=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True)

    def add_document(self, document):
        self.documents.add(document)

    def remove_document(self, document):
        self.documents.remove(document)
