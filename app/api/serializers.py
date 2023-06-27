from django.contrib.auth import get_user_model
from rest_framework import serializers

from base.models import Document, DocumentCollection, Metric, DocumentCollectionTraineResult

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
                                        validated_data['email'], validated_data['password'])

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
        fields = ['id', 'name', 'password', 'description']
        extra_kwargs = {
            'password': {'write_only': True},
        }


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = ['id', 'name']


class DocumentCollectionTraineResultSerializer(serializers.ModelSerializer):
    metrics = MetricSerializer(many=True)

    class Meta:
        model = DocumentCollectionTraineResult
        fields = '__all__'


class DocumentCollectionSerializer(serializers.ModelSerializer):
    documents = DocumentSerializer(many=True)
    trainees = DocumentCollectionTraineResultSerializer(many=True, read_only=True,
                                                        source='documentcollectiontraineresult_set')

    class Meta:
        model = DocumentCollection
        fields = ['id', 'name', 'documents', 'description', 'trainees']
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


class MetricSerializer(serializers.ModelSerializer):
    class Meta:
        model = Metric
        fields = '__all__'
