from django.contrib import admin
from .models import Perfil, Post, Carrera, Disciplina, Equipo, JugadorEquipo, Juez

# Registrar los modelos en el panel de administración
@admin.register(Perfil)
class PerfilAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'rol', 'estado_verificacion', 'fecha_registro')
    list_filter = ('rol', 'estado_verificacion', 'carrera')
    search_fields = ('usuario__username', 'usuario__email')
    actions = ['aprobar_administrativos', 'rechazar_administrativos']
    
    def aprobar_administrativos(self, request, queryset):
        queryset.filter(rol='administrativo').update(estado_verificacion='aprobado')
        self.message_user(request, f'Se han aprobado {queryset.count()} cuentas administrativas')
    aprobar_administrativos.short_description = "Aprobar cuentas administrativas seleccionadas"
    
    def rechazar_administrativos(self, request, queryset):
        queryset.filter(rol='administrativo').update(estado_verificacion='rechazado')
        self.message_user(request, f'Se han rechazado {queryset.count()} cuentas administrativas')
    rechazar_administrativos.short_description = "Rechazar cuentas administrativas seleccionadas"

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'autor', 'fecha_creacion', 'activo')
    list_filter = ('activo', 'fecha_creacion')
    search_fields = ('titulo', 'contenido')

@admin.register(Carrera)
class CarreraAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'abreviatura', 'activo')
    list_filter = ('activo',)
    search_fields = ('nombre',)

@admin.register(Disciplina)
class DisciplinaAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'fecha_registro')
    search_fields = ('nombre',)

@admin.register(Equipo)
class EquipoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'disciplina', 'fecha_registro')
    list_filter = ('disciplina',)
    search_fields = ('nombre',)

@admin.register(JugadorEquipo)
class JugadorEquipoAdmin(admin.ModelAdmin):
    list_display = ('jugador', 'equipo', 'fecha_registro')
    list_filter = ('equipo',)
    search_fields = ('jugador__username', 'equipo__nombre')

@admin.register(Juez)
class JuezAdmin(admin.ModelAdmin):
    list_display = ('nombre_completo', 'especialidad', 'correo_electronico', 'fecha_registro')
    list_filter = ('especialidad',)
    search_fields = ('nombre_completo', 'correo_electronico')
