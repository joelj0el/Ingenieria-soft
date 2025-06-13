# partidos/urls.py
from django.urls import path
from . import views

app_name = 'partidos'

urlpatterns = [
    # Vista principal
    path('', views.partidos_view, name='partidos'),
    
    # URLs de la API
    path('api/partidos/', views.PartidosAPIView.as_view(), name='partidos_api'),
    path('api/partidos/<int:partido_id>/', views.PartidoDetailAPIView.as_view(), name='partido_detail_api'),
    path('api/generar-fixture/', views.GenerarFixtureAPIView.as_view(), name='generar_fixture_api'),
    path('api/estado-fixture/', views.EstadoFixtureAPIView.as_view(), name='estado_fixture_api'),
    path('api/equipos-disciplina/<int:disciplina_id>/', views.EquiposPorDisciplinaAPIView.as_view(), name='equipos_disciplina_api'),
]
