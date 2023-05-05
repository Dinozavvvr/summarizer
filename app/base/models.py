from django.db import models


class Item(models.Model):
    """
    Тестовая модель
    """
    name = models.CharField(max_length=50)
    created = models.DateTimeField(auto_now_add=True)