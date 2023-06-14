from django.urls import include, path
from rest_framework import routers

from api import document_view
from api import downloader_views
from api import document_collection_view
from api.document_view import DocumentViewSet

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi

schema_view = get_schema_view(
   openapi.Info(
      title="Snippets API",
      default_version='v1',
      description="Test description",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="contact@snippets.local"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = routers.DefaultRouter()
router.register(r'document', document_view.DocumentViewSet, basename='document')
router.register(r'collection', document_collection_view.DocumentCollectionViewSet, basename='collection')
router.register(r'downloader', downloader_views.DownloaderViewSet, basename='downloader')

urlpatterns = [
    path('', include(router.urls)),
    path('documents/<int:pk>/download/', document_view.DocumentViewSet.as_view({'get': 'download'}), name='document-download'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
    path('collection/<int:pk>/traine/', document_collection_view.DocumentCollectionViewSet.as_view({'post': 'traine'}),
         name='collection-traine'),
]
