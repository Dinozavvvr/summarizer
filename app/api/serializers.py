from django.contrib.auth import get_user_model
from rest_framework import serializers

from base.models import Document, DocumentCollection

User = get_user_model()

from django.contrib.auth.models import User


# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


# Register Serializer
class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'password', 'email')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = User.objects.create_user(validated_data['username'],
                                        validated_data['email'],  validated_data['password'])

        return user


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
        fields = ['id', 'name', 'password']
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
