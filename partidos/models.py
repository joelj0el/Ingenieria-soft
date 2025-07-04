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
    def resultado_actual(self):
        """Devuelve el resultado actual basado en eventos registrados"""
        # Si el partido está finalizado, usar los goles oficiales
        if self.estado == 'finalizado' and self.goles_equipo_a is not None and self.goles_equipo_b is not None:
            return f"{self.goles_equipo_a} - {self.goles_equipo_b}"
          # Si está en vivo, calcular desde los eventos
        puntos_a = self.calcular_puntos_equipo(self.equipo_a)
        puntos_b = self.calcular_puntos_equipo(self.equipo_b)
        return f"{puntos_a} - {puntos_b}"    
    def calcular_puntos_equipo(self, equipo):
        """Calcula los puntos actuales de un equipo basándose en los eventos"""
        eventos_equipo = self.eventos.filter(
            equipo=equipo, 
            activo=True,
            tipo_evento__in=['gol', 'punto']
        )
        total_puntos = sum(evento.valor for evento in eventos_equipo)
        print(f"DEBUG: Equipo {equipo.nombre} - Eventos encontrados: {eventos_equipo.count()}, Total puntos: {total_puntos}")
        return total_puntos
    
    def actualizar_resultado_final(self):
        """Actualiza los campos goles_equipo_a/b basándose en los eventos registrados"""
        if self.estado == 'finalizado':
            # SIEMPRE usar los eventos como fuente de verdad al finalizar
            goles_eventos_a = self.calcular_puntos_equipo(self.equipo_a)
            goles_eventos_b = self.calcular_puntos_equipo(self.equipo_b)
            
            print(f"DEBUG: Finalizando partido - Goles de eventos: {goles_eventos_a} - {goles_eventos_b}")
            
            self.goles_equipo_a = goles_eventos_a
            self.goles_equipo_b = goles_eventos_b
            self.save()
            
            # Actualizar puntos de las carreras automáticamente
            self.actualizar_puntos_carreras()
    
    def actualizar_puntos_carreras(self):
        """Actualiza los puntos de olimpiada de las carreras de ambos equipos"""
        try:
            # Actualizar carrera del equipo A
            if self.equipo_a.carrera:
                self.equipo_a.carrera.actualizar_puntos_olimpiada()
                print(f"DEBUG: Puntos actualizados para carrera {self.equipo_a.carrera.nombre}")
            
            # Actualizar carrera del equipo B
            if self.equipo_b.carrera:
                self.equipo_b.carrera.actualizar_puntos_olimpiada()
                print(f"DEBUG: Puntos actualizados para carrera {self.equipo_b.carrera.nombre}")
                
        except Exception as e:
            print(f"ERROR: No se pudieron actualizar puntos de carreras: {str(e)}")
    
    def sincronizar_goles_con_eventos(self):
        """Sincroniza los goles directos con los eventos existentes"""        
        # Obtener goles actuales de los campos directos
        goles_directos_a = self.goles_equipo_a or 0
        goles_directos_b = self.goles_equipo_b or 0
        
        # Obtener goles de eventos
        goles_eventos_a = self.calcular_puntos_equipo(self.equipo_a)
        goles_eventos_b = self.calcular_puntos_equipo(self.equipo_b)
        
        # Si hay diferencia, crear eventos para compensar
        if goles_directos_a > goles_eventos_a:
            diferencia = goles_directos_a - goles_eventos_a
            for _ in range(diferencia):
                # Usar apps.get_model para evitar importación circular
                from django.apps import apps
                EventoPartido = apps.get_model('partidos', 'EventoPartido')
                EventoPartido.objects.create(
                    partido=self,
                    equipo=self.equipo_a,
                    tipo_evento='gol',
                    valor=1,
                    descripcion='Gol registrado manualmente - sincronización',
                    registrado_por_id=self.creado_por_id
                )
        
        if goles_directos_b > goles_eventos_b:
            diferencia = goles_directos_b - goles_eventos_b
            for _ in range(diferencia):
                # Usar apps.get_model para evitar importación circular
                from django.apps import apps
                EventoPartido = apps.get_model('partidos', 'EventoPartido')
                EventoPartido.objects.create(
                    partido=self,
                    equipo=self.equipo_b,
                    tipo_evento='gol',
                    valor=1,
                    descripcion='Gol registrado manualmente - sincronización',
                    registrado_por_id=self.creado_por_id
                )
    
    @property
    def puede_registrar_eventos(self):
        """Indica si se pueden registrar eventos en este partido"""
        return self.estado == 'en_vivo'
    
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

    def limpiar_eventos_duplicados(self):
        """Elimina eventos duplicados basándose en equipo, tipo_evento y timestamp cercano"""
        from django.db.models import Count
        from datetime import timedelta
        
        # Obtener eventos del partido ordenados por timestamp
        eventos = self.eventos.filter(activo=True).order_by('timestamp')
        
        eventos_a_eliminar = []
        eventos_procesados = []
        
        for evento in eventos:
            # Buscar eventos similares en un rango de 5 segundos
            timestamp_inicio = evento.timestamp - timedelta(seconds=5)
            timestamp_fin = evento.timestamp + timedelta(seconds=5)
            
            eventos_similares = [
                e for e in eventos_procesados 
                if (e.equipo == evento.equipo and 
                    e.tipo_evento == evento.tipo_evento and
                    timestamp_inicio <= e.timestamp <= timestamp_fin)
            ]
            
            if eventos_similares:
                # Es un duplicado, marcarlo para eliminación
                eventos_a_eliminar.append(evento.id)
            else:
                # Es único, agregarlo a procesados
                eventos_procesados.append(evento)
        
        # Eliminar eventos duplicados
        if eventos_a_eliminar:
            self.eventos.filter(id__in=eventos_a_eliminar).update(activo=False)
            print(f"DEBUG: Eliminados {len(eventos_a_eliminar)} eventos duplicados")
        
        return len(eventos_a_eliminar)

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

class EventoPartido(models.Model):
    """Modelo para registrar eventos durante un partido (goles, puntos, etc.)"""
    TIPO_EVENTO_CHOICES = [
        ('gol', 'Gol'),
        ('punto', 'Punto'),
        ('tarjeta_amarilla', 'Tarjeta Amarilla'),
        ('tarjeta_roja', 'Tarjeta Roja'),
        ('cambio', 'Cambio de Jugador'),
        ('inicio_tiempo', 'Inicio de Tiempo'),
        ('fin_tiempo', 'Fin de Tiempo'),
        ('otro', 'Otro'),
    ]
    
    partido = models.ForeignKey(Partido, on_delete=models.CASCADE, related_name='eventos')
    equipo = models.ForeignKey('usuarios.Equipo', on_delete=models.CASCADE, 
                              help_text="Equipo al que se le asigna el evento")
    tipo_evento = models.CharField(max_length=20, choices=TIPO_EVENTO_CHOICES, default='gol')
    minuto = models.IntegerField(null=True, blank=True, 
                               help_text="Minuto en que ocurrió el evento")
    descripcion = models.TextField(blank=True, 
                                 help_text="Descripción adicional del evento")
    valor = models.IntegerField(default=1, 
                              help_text="Valor del evento (ej: 1 para gol, 2 para punto de 2, etc.)")
    
    # Metadatos
    registrado_por = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    activo = models.BooleanField(default=True, 
                               help_text="Permite 'eliminar' un evento sin borrarlo")
    
    class Meta:
        ordering = ['timestamp']
        verbose_name = 'Evento de Partido'
        verbose_name_plural = 'Eventos de Partido'
    
    def __str__(self):
        minuto_str = f"min {self.minuto}" if self.minuto else "s/min"
        return f"{self.partido} - {self.equipo.nombre}: {self.get_tipo_evento_display()} ({minuto_str})"
    
    def clean(self):
        """Validaciones personalizadas"""
        from django.core.exceptions import ValidationError
        
        # Verificar que el equipo pertenezca al partido
        if self.equipo not in [self.partido.equipo_a, self.partido.equipo_b]:
            raise ValidationError('El equipo debe ser uno de los participantes del partido')
        
        # Verificar que el partido esté en vivo para registrar eventos de juego
        if self.tipo_evento in ['gol', 'punto'] and self.partido.estado != 'en_vivo':
            raise ValidationError('Solo se pueden registrar goles/puntos en partidos en vivo')
        
        # Validar minuto positivo
        if self.minuto is not None and self.minuto < 0:
            raise ValidationError('El minuto no puede ser negativo')
