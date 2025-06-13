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

# Modelo para almacenar disciplinas deportivas
class Disciplina(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    descripcion = models.TextField(blank=True)
    imagen = models.ImageField(upload_to='disciplinas/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Disciplina"
        verbose_name_plural = "Disciplinas"
    
    def __str__(self):
        return self.nombre
    
# Modelo para almacenar equipos
class Equipo(models.Model):
    CATEGORIA_CHOICES = [
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('mixto', 'Mixto'),
    ]
    
    nombre = models.CharField(max_length=100, unique=True)
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, related_name='equipos', null=True, blank=True)
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE, related_name='equipos')
    categoria = models.CharField(max_length=10, choices=CATEGORIA_CHOICES, default='mixto')
    capitan = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='equipos_capitaneados')
    descripcion = models.TextField(blank=True)
    logo = models.ImageField(upload_to='equipos/', blank=True, null=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['nombre']
        verbose_name = "Equipo"
        verbose_name_plural = "Equipos"
    
    def __str__(self):
        return self.nombre

# Modelo para relacionar jugadores con equipos
class JugadorEquipo(models.Model):
    jugador = models.ForeignKey(User, on_delete=models.CASCADE, related_name='equipos')
    equipo = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='jugadores')
    fecha_registro = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('jugador', 'equipo')
        verbose_name = "Jugador de Equipo"
        verbose_name_plural = "Jugadores de Equipo"
    
    def __str__(self):
        return f"{self.jugador.first_name} {self.jugador.last_name} - {self.equipo.nombre}"

# Modelo para almacenar jueces
class Juez(models.Model):
    nombre_completo = models.CharField(max_length=255)
    correo_electronico = models.EmailField(unique=True)
    telefono = models.CharField(max_length=15)
    especialidad = models.CharField(max_length=255)
    disciplinas = models.ManyToManyField('Disciplina', related_name='jueces', verbose_name="Disciplinas especializadas", blank=True)
    fecha_registro = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['nombre_completo']
        verbose_name = "Juez"
        verbose_name_plural = "Jueces"
    
    def __str__(self):
        return self.nombre_completo