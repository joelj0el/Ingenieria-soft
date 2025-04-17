# usuarios/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    RegistroView, LoginView, 
    UserAPIView, RegistroAPIView, LoginAPIView, LogoutAPIView, PerfilAPIView,
    PostAPIView
)

urlpatterns = [
    # URLs para vistas basadas en plantillas
    path('registro/', RegistroView.as_view(), name='registro'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    
    # URLs para la API REST de usuarios
    path('api/usuarios/', UserAPIView.as_view(), name='api-usuarios'),
    path('api/registro/', RegistroAPIView.as_view(), name='api-registro'),
    path('api/login/', LoginAPIView.as_view(), name='api-login'),
    path('api/logout/', LogoutAPIView.as_view(), name='api-logout'),
    path('api/perfil/', PerfilAPIView.as_view(), name='api-perfil'),
    
    # URLs para la API REST de posts
    path('api/posts/', PostAPIView.as_view(), name='api-posts-list'),
    path('api/posts/<int:post_id>/', PostAPIView.as_view(), name='api-posts-detail'),
]