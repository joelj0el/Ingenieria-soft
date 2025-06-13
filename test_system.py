#!/usr/bin/env python3
"""
Script de prueba para verificar el funcionamiento del sistema de equipos.
"""

import os
import sys
import django

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil, Disciplina, Equipo, JugadorEquipo, Carrera

def test_system():
    """Prueba básica del sistema"""
    print("=== VERIFICACIÓN DEL SISTEMA DE EQUIPOS ===")
    
    # Verificar usuarios
    print(f"Usuarios registrados: {User.objects.count()}")
    
    # Verificar perfiles
    print(f"Perfiles creados: {Perfil.objects.count()}")
    
    # Verificar carreras
    print(f"Carreras disponibles: {Carrera.objects.count()}")
    for carrera in Carrera.objects.all():
        print(f"  - {carrera.nombre}")
    
    # Verificar disciplinas
    print(f"Disciplinas disponibles: {Disciplina.objects.count()}")
    for disciplina in Disciplina.objects.all():
        print(f"  - {disciplina.nombre}")
    
    # Verificar equipos
    print(f"Equipos registrados: {Equipo.objects.count()}")
    for equipo in Equipo.objects.all():
        jugadores_count = JugadorEquipo.objects.filter(equipo=equipo).count()
        print(f"  - {equipo.nombre} ({equipo.disciplina.nombre}) - {jugadores_count} jugadores")
    
    # Verificar administradores
    admins = Perfil.objects.filter(rol='administrativo', estado_verificacion='aprobado')
    print(f"Administradores activos: {admins.count()}")
    for admin in admins:
        print(f"  - {admin.usuario.username}")
    
    print("\n=== PRUEBA COMPLETADA ===")

if __name__ == "__main__":
    test_system()
