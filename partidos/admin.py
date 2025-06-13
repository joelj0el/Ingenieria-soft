# partidos/admin.py
from django.contrib import admin
from .models import Partido, FixtureGenerado, EventoPartido

@admin.register(Partido)
class PartidoAdmin(admin.ModelAdmin):
    list_display = ('equipo_a', 'equipo_b', 'disciplina', 'categoria', 'fecha', 'hora', 'estado', 'resultado')
    list_filter = ('disciplina', 'categoria', 'estado', 'fecha', 'es_fixture')
    search_fields = ('equipo_a__nombre', 'equipo_b__nombre', 'disciplina__nombre', 'lugar')
    date_hierarchy = 'fecha'
    ordering = ['-fecha', '-hora']
    
    fieldsets = (
        ('Equipos', {
            'fields': ('equipo_a', 'equipo_b')
        }),
        ('Información del Partido', {
            'fields': ('disciplina', 'categoria', 'fecha', 'hora', 'lugar')
        }),
        ('Estado y Resultado', {
            'fields': ('estado', 'goles_equipo_a', 'goles_equipo_b')
        }),
        ('Metadatos', {
            'fields': ('jornada', 'es_fixture', 'creado_por'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un objeto nuevo
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(FixtureGenerado)
class FixtureGeneradoAdmin(admin.ModelAdmin):
    list_display = ('disciplina', 'categoria', 'total_partidos', 'total_jornadas', 'fecha_inicio', 'fecha_fin', 'fecha_creacion')
    list_filter = ('disciplina', 'categoria', 'fecha_creacion')
    search_fields = ('disciplina__nombre',)
    date_hierarchy = 'fecha_creacion'
    ordering = ['-fecha_creacion']
    readonly_fields = ('fecha_creacion',)
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un objeto nuevo
            obj.creado_por = request.user
        super().save_model(request, obj, form, change)

@admin.register(EventoPartido)
class EventoPartidoAdmin(admin.ModelAdmin):
    list_display = ('partido', 'equipo', 'tipo_evento', 'valor', 'minuto', 'timestamp', 'registrado_por', 'activo')
    list_filter = ('tipo_evento', 'equipo__disciplina', 'timestamp', 'activo')
    search_fields = ('partido__equipo_a__nombre', 'partido__equipo_b__nombre', 'equipo__nombre', 'descripcion')
    date_hierarchy = 'timestamp'
    ordering = ['-timestamp']
    readonly_fields = ('timestamp',)
    
    fieldsets = (
        ('Información del Evento', {
            'fields': ('partido', 'equipo', 'tipo_evento', 'valor')
        }),
        ('Detalles', {
            'fields': ('minuto', 'descripcion', 'activo')
        }),
        ('Metadatos', {
            'fields': ('registrado_por', 'timestamp'),
            'classes': ('collapse',)
        })
    )
    
    def save_model(self, request, obj, form, change):
        if not change:  # Si es un objeto nuevo
            obj.registrado_por = request.user
        super().save_model(request, obj, form, change)
    
    def get_queryset(self, request):
        return super().get_queryset(request).select_related(
            'partido', 'equipo', 'registrado_por'
        )
