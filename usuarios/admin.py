from django.contrib import admin
from .models import Perfil, Post, Carrera

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
