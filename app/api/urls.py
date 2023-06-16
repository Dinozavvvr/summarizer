from django.urls import include, path
from rest_framework import routers

from api import document_view
from api import downloader_views
from api import document_collection_view
from api.user_view import RegisterAPI, LoginAPI, UserAPI
from api.document_view import DocumentViewSet

from rest_framework import permissions

router = routers.DefaultRouter()
router.register(r'document', document_view.DocumentViewSet, basename='document')
router.register(r'collection', document_collection_view.DocumentCollectionViewSet, basename='collection')
router.register(r'downloader', downloader_views.UploaderViewSet, basename='downloader')

urlpatterns = [
    path('', include(router.urls)),
    path('documents/<int:pk>/download/', document_view.DocumentViewSet.as_view({'get': 'download'}), name='document-download'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('collection/<int:pk>/traine/', document_collection_view.DocumentCollectionViewSet.as_view({'post': 'traine'}),
         name='collection-traine'),
    path('user/register/', RegisterAPI.as_view(), name='user-register'),
    path('user/login/', LoginAPI.as_view(), name='user-login'),
    path('user/me/', UserAPI.as_view(), name='user-info'),
]
