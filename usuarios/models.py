# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User

# Si quieres extender el modelo de User de Django
class Perfil(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.usuario.username