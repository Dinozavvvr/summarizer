from rest_framework import serializers
from base.models import Item


class ItemSerializer(serializers.ModelSerializer):

    """
    Простейший пример сериализатора для моделей
    """
    class Meta:
        model = Item
        fields = '__all__'
