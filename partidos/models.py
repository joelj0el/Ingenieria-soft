# partidos/models.py
from django.db import models
from django.contrib.auth.models import User
from usuarios.models import Equipo, Disciplina

class Partido(models.Model):
    ESTADOS_CHOICES = [
        ('programado', 'Programado'),
        ('en_vivo', 'En Vivo'),
        ('finalizado', 'Finalizado'),
    ]
    
    # Equipos participantes
    equipo_a = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_como_equipo_a')
    equipo_b = models.ForeignKey(Equipo, on_delete=models.CASCADE, related_name='partidos_como_equipo_b')
    
    # Información básica
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=20, choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('mixto', 'Mixto'),
    ])
    
    # Fecha y hora
    fecha = models.DateField()
    hora = models.TimeField()
    
    # Lugar
    lugar = models.CharField(max_length=200, blank=True, null=True)
    
    # Estado del partido
    estado = models.CharField(max_length=20, choices=ESTADOS_CHOICES, default='programado')
    
    # Resultados (solo cuando esté finalizado)
    goles_equipo_a = models.IntegerField(default=0, blank=True, null=True)
    goles_equipo_b = models.IntegerField(default=0, blank=True, null=True)
    
    # Metadatos
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='partidos_creados')
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    # Campos adicionales para el fixture
    jornada = models.IntegerField(blank=True, null=True, help_text="Número de jornada del fixture")
    es_fixture = models.BooleanField(default=False, help_text="Indica si fue generado automáticamente")
    
    class Meta:
        ordering = ['fecha', 'hora']
        verbose_name = 'Partido'
        verbose_name_plural = 'Partidos'
        
        # Evitar que un equipo juegue contra sí mismo
        constraints = [
            models.CheckConstraint(
                check=~models.Q(equipo_a=models.F('equipo_b')),
                name='no_mismo_equipo'
            )
        ]
    
    def __str__(self):
        return f"{self.equipo_a.nombre} vs {self.equipo_b.nombre} - {self.fecha}"
    
    @property
    def resultado(self):
        """Devuelve el resultado del partido si está finalizado"""
        if self.estado == 'finalizado' and self.goles_equipo_a is not None and self.goles_equipo_b is not None:
            return f"{self.goles_equipo_a} - {self.goles_equipo_b}"
        return None
    
    @property
    def ganador(self):
        """Devuelve el equipo ganador si el partido está finalizado"""
        if self.estado == 'finalizado' and self.goles_equipo_a is not None and self.goles_equipo_b is not None:
            if self.goles_equipo_a > self.goles_equipo_b:
                return self.equipo_a
            elif self.goles_equipo_b > self.goles_equipo_a:
                return self.equipo_b
            else:
                return None  # Empate
        return None
    
    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError
        
        # Verificar que los equipos sean de la misma disciplina
        if self.equipo_a.disciplina != self.equipo_b.disciplina:
            raise ValidationError('Los equipos deben ser de la misma disciplina')
        
        # Verificar que los equipos sean de la misma categoría
        if self.equipo_a.categoria != self.equipo_b.categoria:
            raise ValidationError('Los equipos deben ser de la misma categoría')
        
        # Verificar que la disciplina del partido coincida con la de los equipos
        if self.disciplina != self.equipo_a.disciplina:
            raise ValidationError('La disciplina del partido debe coincidir con la de los equipos')
        
        # Verificar que la categoría del partido coincida con la de los equipos
        if self.categoria != self.equipo_a.categoria:
            raise ValidationError('La categoría del partido debe coincidir con la de los equipos')

class FixtureGenerado(models.Model):
    """Modelo para llevar registro de los fixtures generados"""
    disciplina = models.ForeignKey(Disciplina, on_delete=models.CASCADE)
    categoria = models.CharField(max_length=20, choices=[
        ('masculino', 'Masculino'),
        ('femenino', 'Femenino'),
        ('mixto', 'Mixto'),
    ])
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField(null=True, blank=True)  # Puede ser null si no se han completado todas las jornadas
    total_jornadas = models.IntegerField()
    jornadas_generadas = models.IntegerField(default=0)  # Número de jornadas ya generadas
    total_partidos = models.IntegerField(default=0)  # Total de partidos generados hasta ahora
    completado = models.BooleanField(default=False)  # Indica si se han generado todas las jornadas
    creado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    fecha_creacion = models.DateTimeField(auto_now_add=True)
    fecha_actualizacion = models.DateTimeField(auto_now=True)
    
    class Meta:
        ordering = ['-fecha_creacion']
        verbose_name = 'Fixture Generado'
        verbose_name_plural = 'Fixtures Generados'
        # Un fixture por disciplina y categoría
        unique_together = ['disciplina', 'categoria']
    
    def __str__(self):
        estado = "Completado" if self.completado else f"Jornadas {self.jornadas_generadas}/{self.total_jornadas}"
        return f"Fixture {self.disciplina.nombre} {self.categoria} - {estado}"
    
    @property
    def progreso_percentage(self):
        """Devuelve el porcentaje de progreso del fixture"""
        if self.total_jornadas == 0:
            return 0
        return int((self.jornadas_generadas / self.total_jornadas) * 100)
    
    @property
    def siguiente_jornada(self):
        """Devuelve el número de la siguiente jornada a generar"""
        return self.jornadas_generadas + 1 if not self.completado else None
