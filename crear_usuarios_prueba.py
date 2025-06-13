#!/usr/bin/env python
import os
import sys
import django

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil, Carrera

def crear_usuarios_prueba():
    """Crear usuarios administrativos pendientes de aprobación para pruebas"""
    
    # Crear o obtener una carrera de ejemplo
    carrera, created = Carrera.objects.get_or_create(
        nombre="Ingeniería de Sistemas",
        defaults={'abreviatura': 'IS'}
    )
    
    usuarios_prueba = [
        {
            'username': 'admin_pendiente1',
            'email': 'admin1@test.com',
            'first_name': 'Juan Carlos',
            'last_name': 'López García',
            'telefono': '3001234567'
        },
        {
            'username': 'admin_pendiente2',
            'email': 'admin2@test.com',
            'first_name': 'María José',
            'last_name': 'Rodríguez Silva',
            'telefono': '3009876543'
        },
        {
            'username': 'admin_pendiente3',
            'email': 'admin3@test.com',
            'first_name': 'Carlos Eduardo',
            'last_name': 'Mendoza Torres',
            'telefono': '3005555555'
        }
    ]
    
    print("Creando usuarios administrativos pendientes de aprobación...")
    
    for datos_usuario in usuarios_prueba:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=datos_usuario['username']).exists():
            print(f"❌ Usuario {datos_usuario['username']} ya existe, saltando...")
            continue
            
        # Crear usuario
        try:
            usuario = User.objects.create_user(
                username=datos_usuario['username'],
                email=datos_usuario['email'],
                first_name=datos_usuario['first_name'],
                last_name=datos_usuario['last_name'],
                password='password123' # Contraseña de prueba
            )
            
            # Crear perfil administrativo pendiente
            perfil = Perfil.objects.create(
                usuario=usuario,
                telefono=datos_usuario['telefono'],
                rol='administrativo',
                carrera=carrera,
                estado_verificacion='pendiente'
            )
            
            print(f"✅ Usuario {datos_usuario['username']} creado exitosamente")
            print(f"   - Nombre: {datos_usuario['first_name']} {datos_usuario['last_name']}")
            print(f"   - Email: {datos_usuario['email']}")
            print(f"   - Estado: Pendiente de aprobación")
            print()
            
        except Exception as e:
            print(f"❌ Error creando usuario {datos_usuario['username']}: {str(e)}")
    
    # Mostrar resumen
    pendientes = Perfil.objects.filter(rol='administrativo', estado_verificacion='pendiente').count()
    print(f"📊 Total de usuarios administrativos pendientes: {pendientes}")

if __name__ == '__main__':
    crear_usuarios_prueba()
