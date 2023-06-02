from django.db import models
from django.urls import reverse


class Document(models.Model):
    """
    Модель документа
    """
    title = models.CharField(max_length=1000)
    file = models.FileField(upload_to='documents/%Y/%m/%d/', null=True)
    created = models.DateTimeField(auto_now_add=True)

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

    def add_document(self, document):
        self.documents.add(document)

    def remove_document(self, document):
        self.documents.remove(document)
