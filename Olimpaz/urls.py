# mi_proyecto/urls.py

from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin-django/', admin.site.urls),  # Cambiamos la URL del admin de Django
    path('usuarios/', include('usuarios.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
]

# Agregar rutas para archivos estáticos y media en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)