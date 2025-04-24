# usuarios/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views

urlpatterns = [
    # URLs para vistas basadas en plantillas
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='/login/'), name='logout'),
    
    # URLs para la API REST de usuarios
    path('api/usuarios/', views.UserAPIView.as_view(), name='api-usuarios'),
    path('api/registro/', views.RegistroAPIView.as_view(), name='api-registro'),
    path('api/login/', views.LoginAPIView.as_view(), name='api-login'),
    # Usamos el método DELETE de LoginAPIView para el logout
    path('api/logout/', views.LoginAPIView.as_view(), name='api-logout'),
    path('api/perfil/', views.PerfilAPIView.as_view(), name='api-perfil'),
    path('api/usuarios/actual/', views.UserAPIView.as_view(), name='api_usuario_actual'),
    
    # URLs para la API REST de posts
    path('api/posts/', views.PostAPIView.as_view(), name='api-posts-list'),
    path('api/posts/<int:post_id>/', views.PostAPIView.as_view(), name='api-posts-detail'),
    
    # URLs para administrar administrativos (solo admins)
    path('api/administrativos/', views.AdministrativosView.as_view(), name='api_administrativos'),
    path('api/administrativos/<int:pk>/', views.AdministrativosView.as_view(), name='api_administrativo_detalle'),
    
    # URL para obtener carreras
    path('api/carreras/', views.CarreraAPIView.as_view(), name='api_carreras'),
]