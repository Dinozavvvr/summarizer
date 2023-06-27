from rest_framework.viewsets import ModelViewSet

from base.models import Metric
from .serializers import MetricSerializer


class MetricViewSet(ModelViewSet):
    queryset = Metric.objects.all()
    serializer_class = MetricSerializer
