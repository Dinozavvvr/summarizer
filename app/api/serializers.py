from rest_framework import serializers
from base.models import Document, DocumentCollection


class DocumentSerializer(serializers.ModelSerializer):
    file = serializers.SerializerMethodField()

    def get_file(self, obj):
        request = self.context.get('request')
        if request is not None:
            return request.build_absolute_uri(obj.get_download_url())
        return None

    class Meta:
        model = Document
        fields = '__all__'


class DocumentCollectionCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCollection
        fields = ['name', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class DocumentCollectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = DocumentCollection
        fields = ['id', 'name', 'documents']
        read_only_fields = ['id']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def validate(self, attrs):
        # Check uniqueness of the collection name
        name = attrs.get('name')
        if DocumentCollection.objects.filter(name=name).exists():
            raise serializers.ValidationError('A collection with this name already exists.')
        return attrs