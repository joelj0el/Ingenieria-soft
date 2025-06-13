#!/usr/bin/env python
"""
Script para crear usuarios de prueba para el sistema de equipos
Ejecutar con: python create_test_users.py
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Olimpaz.settings")
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Carrera, Perfil

# Lista de usuarios de prueba
USUARIOS_PRUEBA = [
    {
        'username': 'estudiante1',
        'email': 'estudiante1@uab.edu.bo',
        'password': '123456',
        'first_name': 'Juan',
        'last_name': 'Pérez',
        'carrera': 'INGENIERIA DE SISTEMAS',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante2',
        'email': 'estudiante2@uab.edu.bo',
        'password': '123456',
        'first_name': 'María',
        'last_name': 'García',
        'carrera': 'COMUNICACION SOCIAL Y MEDIOS DIGITALES',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante3',
        'email': 'estudiante3@uab.edu.bo',
        'password': '123456',
        'first_name': 'Carlos',
        'last_name': 'López',
        'carrera': 'INGENIERIA DE SISTEMAS',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante4',
        'email': 'estudiante4@uab.edu.bo',
        'password': '123456',
        'first_name': 'Ana',
        'last_name': 'Martínez',
        'carrera': 'PSICOLOGIA',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante5',
        'email': 'estudiante5@uab.edu.bo',
        'password': '123456',
        'first_name': 'Diego',
        'last_name': 'Rodríguez',
        'carrera': 'ADMINISTRACION Y NEGOCIOS INTERNACIONALES',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante6',
        'email': 'estudiante6@uab.edu.bo',
        'password': '123456',
        'first_name': 'Sofía',
        'last_name': 'Vargas',
        'carrera': 'DERECHO',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante7',
        'email': 'estudiante7@uab.edu.bo',
        'password': '123456',
        'first_name': 'Luis',
        'last_name': 'Hernández',
        'carrera': 'INGENIERIA DE SISTEMAS',
        'rol': 'estudiante'
    },
    {
        'username': 'estudiante8',
        'email': 'estudiante8@uab.edu.bo',
        'password': '123456',
        'first_name': 'Carmen',
        'last_name': 'Jiménez',
        'carrera': 'ENFERMERIA',
        'rol': 'estudiante'
    }
]

def create_test_users():
    """
    Función para crear usuarios de prueba
    """
    print("Iniciando creación de usuarios de prueba...")
    
    # Contador para nuevos usuarios
    nuevos = 0
    
    for user_info in USUARIOS_PRUEBA:
        # Verificar si el usuario ya existe
        if User.objects.filter(username=user_info['username']).exists():
            print(f"Ya existe usuario: {user_info['username']}")
            continue
            
        # Obtener la carrera
        try:
            carrera = Carrera.objects.get(nombre=user_info['carrera'])
        except Carrera.DoesNotExist:
            print(f"Carrera no encontrada: {user_info['carrera']}")
            continue
            
        # Crear el usuario
        user = User.objects.create_user(
            username=user_info['username'],
            email=user_info['email'],
            password=user_info['password'],
            first_name=user_info['first_name'],
            last_name=user_info['last_name']
        )
        
        # Crear el perfil
        perfil = Perfil.objects.create(
            usuario=user,
            rol=user_info['rol'],
            carrera=carrera,
            estado_verificacion='aprobado'
        )
        
        nuevos += 1
        print(f"Creado usuario: {user_info['username']} - {user_info['first_name']} {user_info['last_name']}")
    
    print(f"Proceso completado. Se crearon {nuevos} nuevos usuarios.")
    print("\nCredenciales de acceso:")
    print("Username: estudiante1, estudiante2, etc.")
    print("Password: 123456")

if __name__ == "__main__":
    print("Ejecutando script de creación de usuarios de prueba...")
    create_test_users()
    print("Script finalizado!")
