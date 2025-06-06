# usuarios/urls_api.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .api_views import (
    UserViewSet, PerfilViewSet, PostViewSet, CarreraViewSet, 
    DisciplinaViewSet, EquipoViewSet, JuezViewSet
)

# Creamos un router para los ViewSets
router = DefaultRouter()
router.register(r'usuarios', UserViewSet)
router.register(r'perfiles', PerfilViewSet)
router.register(r'posts', PostViewSet)
router.register(r'carreras', CarreraViewSet)
router.register(r'disciplinas', DisciplinaViewSet)
router.register(r'equipos', EquipoViewSet)
router.register(r'jueces', JuezViewSet)

# Paths de la API usando los ViewSets
urlpatterns = router.urls
