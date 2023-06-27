from django.urls import include, path
from rest_framework import routers

from api import document_collection_view
from api import document_view
from api import downloader_views
from api import metric_views
from api import trainee_views
from api.user_view import RegisterAPI, LoginAPI, UserAPI

router = routers.DefaultRouter()
router.register(r'document', document_view.DocumentViewSet, basename='document')
router.register(r'collection', document_collection_view.DocumentCollectionViewSet, basename='collection')
router.register(r'downloader', downloader_views.UploaderViewSet, basename='downloader')
router.register(r'metric', metric_views.MetricViewSet, basename='metric')
router.register(r'trainee', trainee_views.TraineeViewSet, basename='trainee')

urlpatterns = [
    path('', include(router.urls)),
    path('documents/<int:pk>/download/', document_view.DocumentViewSet.as_view({'get': 'download'}), name='document-download'),
    path('collection/<int:pk>/traine/', document_collection_view.DocumentCollectionViewSet.as_view({'post': 'traine'}),
         name='collection-traine'),
    path('user/register/', RegisterAPI.as_view(), name='user-register'),
    path('user/login/', LoginAPI.as_view(), name='user-login'),
    path('user/me/', UserAPI.as_view(), name='user-info'),
]
