# partidos/urls.py
from django.urls import path
from . import views

app_name = 'partidos'

urlpatterns = [
    # Vistas principales
    path('', views.partidos_view, name='partidos'),
    path('resultados/', views.resultados_view, name='resultados'),
    
    # URLs de la API
    path('api/partidos/', views.PartidosAPIView.as_view(), name='partidos_api'),
    path('api/partidos/<int:partido_id>/', views.PartidoDetailAPIView.as_view(), name='partido_detail_api'),
    path('api/generar-fixture/', views.GenerarFixtureAPIView.as_view(), name='generar_fixture_api'),
    path('api/estado-fixture/', views.EstadoFixtureAPIView.as_view(), name='estado_fixture_api'),
    path('api/equipos-disciplina/<int:disciplina_id>/', views.EquiposPorDisciplinaAPIView.as_view(), name='equipos_disciplina_api'),
      # APIs para gestión de resultados
    path('api/partidos/<int:partido_id>/cambiar-estado/', views.CambiarEstadoPartidoAPIView.as_view(), name='cambiar_estado_partido'),
    path('api/partidos/<int:partido_id>/registrar-evento/', views.RegistrarEventoAPIView.as_view(), name='registrar_evento'),
    path('api/partidos/<int:partido_id>/eventos/', views.EventosPartidoAPIView.as_view(), name='eventos_partido'),
    path('api/partidos-en-vivo/', views.PartidosEnVivoAPIView.as_view(), name='partidos_en_vivo'),    # APIs para dashboard
    path('api/dashboard/stats/', views.DashboardStatsAPIView.as_view(), name='dashboard_stats'),
    path('api/dashboard/partidos-recientes/', views.PartidosRecientesAPIView.as_view(), name='partidos_recientes'),
    path('api/dashboard/tabla-posiciones/', views.TablaPosicionesAPIView.as_view(), name='tabla_posiciones'),
    path('api/tabla-posiciones/', views.TablaPosicionesAPIView.as_view(), name='tabla_posiciones_alt'),
    path('api/tabla-general-carreras/', views.TablaGeneralCarrerasAPIView.as_view(), name='tabla_general_carreras'),
    
    # API para limpiar jornadas
    path('api/limpiar-jornadas/', views.LimpiarJornadasAPIView.as_view(), name='limpiar_jornadas'),
]
