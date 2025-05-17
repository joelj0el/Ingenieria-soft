# usuarios/models.py

from django.db import models
from django.contrib.auth.models import User

# Modelo de Carrera para la selección
class Carrera(models.Model):
    nombre = models.CharField(max_length=100)
    abreviatura = models.CharField(max_length=10, blank=True)
    activo = models.BooleanField(default=True)
    
    def __str__(self):
        return self.nombre

# Modelo de Perfil para extender User
class Perfil(models.Model):
    ROLE_CHOICES = (
        ('estudiante', 'Estudiante'),
        ('administrativo', 'Administrativo'),
    )
    VERIFICATION_STATUS = (
        ('pendiente', 'Pendiente'),
        ('aprobado', 'Aprobado'),
        ('rechazado', 'Rechazado'),
    )
    
    usuario = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15, blank=True)
    direccion = models.TextField(blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    rol = models.CharField(max_length=15, choices=ROLE_CHOICES, default='estudiante')
    carrera = models.ForeignKey(Carrera, on_delete=models.SET_NULL, null=True, blank=True)
    estado_verificacion = models.CharField(max_length=10, choices=VERIFICATION_STATUS, default='pendiente')
    
    def __str__(self):
        return self.usuario.username

# Modelo para manejar publicaciones
class Post(models.Model):
    titulo = models.CharField(max_length=200)
    contenido = models.TextField()
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    imagen = models.ImageField(upload_to='posts/', blank=True, null=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        
    def __str__(self):
        return self.titulo

# Modelo para almacenar jueces
class Juez(models.Model):
    nombre_completo = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=255)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre_completo']
        verbose_name = "Juez"
        verbose_name_plural = "Jueces"
    
    def __str__(self):
        return self.nombre_completo