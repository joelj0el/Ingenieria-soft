# usuarios/urls.py

from django.urls import path
from django.contrib.auth.views import LogoutView
from . import views
from . import jueces_views
from . import equipos_views

urlpatterns = [
    # URLs para vistas basadas en plantillas
    path('registro/', views.RegistroView.as_view(), name='registro'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.CustomLogoutView.as_view(), name='logout'),
    
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
      # URL para obtener carreras (cambiar a equipos_views para consistencia)
    path('api/carreras/', equipos_views.CarrerasAPIView.as_view(), name='api_carreras'),
    
    # URLs para el panel de administración
    path('admin/', views.AdminPanelView.as_view(), name='admin_panel'),
    path('admin/usuarios/listar/', views.AdminUserListView.as_view(), name='admin_user_list'),
    path('admin/usuarios/buscar/', views.AdminUserSearchView.as_view(), name='admin_user_search'),
    path('admin/usuarios/<int:user_id>/', views.AdminUserDetailView.as_view(), name='admin_user_detail'),
    path('admin/usuarios/<int:user_id>/editar/', views.AdminUserDetailView.as_view(), name='admin_user_edit'),
    path('admin/usuarios/<int:user_id>/eliminar/', views.AdminUserDetailView.as_view(), name='admin_user_delete'),
    
    # URLs para la API REST de jueces
    path('api/jueces/', jueces_views.JuecesAPIView.as_view(), name='api_jueces'),
    path('api/jueces/<int:juez_id>/', jueces_views.JuezDetailAPIView.as_view(), name='api_juez_detail'),
    
    # URLs para la API REST de disciplinas
    path('api/disciplinas/', equipos_views.DisciplinasAPIView.as_view(), name='api_disciplinas'),
    path('api/disciplinas/<int:disciplina_id>/', equipos_views.DisciplinaDetailAPIView.as_view(), name='api_disciplina_detail'),    # URLs para la API REST de equipos
    path('api/equipos/', equipos_views.EquiposAPIView.as_view(), name='api_equipos'),
    path('api/equipos/<int:equipo_id>/', equipos_views.EquipoDetailAPIView.as_view(), name='api_equipo_detail'),
    path('api/jugadores-disponibles/<int:disciplina_id>/', equipos_views.JugadoresDisponiblesAPIView.as_view(), name='api_jugadores_disponibles'),
    
    # URLs para búsqueda de usuarios
    path('api/buscar-usuarios/', equipos_views.BuscarUsuariosAPIView.as_view(), name='api_buscar_usuarios'),
    
    # URL para la vista de equipos
    path('teams/', views.TeamsView.as_view(), name='teams'),
]