# mi_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

# Importar la vista específica
from partidos.views import resultados_view
from usuarios.views import HomeView

# Importaciones para JWT
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
    TokenVerifyView,
)

# Importaciones para Swagger
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from rest_framework import permissions

# Configuración de Swagger
schema_view = get_schema_view(
   openapi.Info(
      title="OLIMPAZ API",
      default_version='v1',
      description="API de OLIMPAZ para gestión de eventos deportivos",
      terms_of_service="https://www.example.com/policies/terms/",
      contact=openapi.Contact(email="contact@olimpaz.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [    path('admin-django/', admin.site.urls),  # Cambiamos la URL del admin de Django
    path('usuarios/', include('usuarios.urls')),
    path('partidos/', include('partidos.urls')),  # URLs de partidos
    path('resultados/', resultados_view, name='resultados'),  # Vista específica para resultados
    path('', HomeView.as_view(), name='home'),
    
    # Nueva API REST usando ViewSets
    path('api/v2/', include('usuarios.urls_api')),
    
    # Endpoints para JWT
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    
    # Endpoints para documentación Swagger
    path('swagger<format>/', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

# Agregar rutas para archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)