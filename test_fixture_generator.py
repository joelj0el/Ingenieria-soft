#!/usr/bin/env python
"""
Script para probar el generador de fixtures round-robin
Este script crea equipos de prueba y genera un fixture para verificar
que ningún equipo juegue más de una vez por jornada.
"""
import os
import sys
import django
from datetime import date, timedelta

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil, Disciplina, Carrera, Equipo
from partidos.models import Partido, FixtureGenerado


def crear_equipos_prueba():
    """Crear equipos de prueba para testing"""
    print("Creando equipos de prueba...")
    
    # Crear un usuario administrativo si no existe
    admin_user, created = User.objects.get_or_create(
        username='admin_fixture',
        defaults={
            'email': 'admin@test.com',
            'first_name': 'Admin',
            'last_name': 'Fixture'
        }
    )
    
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        
        # Crear perfil administrativo
        Perfil.objects.create(
            usuario=admin_user,
            rol='administrativo',
            estado_verificacion='aprobado'
        )
        print(f"Usuario administrativo creado: {admin_user.username}")
    
    # Obtener o crear disciplina
    disciplina, created = Disciplina.objects.get_or_create(
        nombre='Fútbol Test',
        defaults={'descripcion': 'Disciplina de prueba para fixture'}
    )
      # Obtener o crear carrera
    carrera, created = Carrera.objects.get_or_create(
        nombre='Ingeniería Test',
        defaults={'abreviatura': 'ING_T'}
    )
    
    # Crear equipos de prueba
    nombres_equipos = [
        'Equipo Alpha',
        'Equipo Beta', 
        'Equipo Gamma',
        'Equipo Delta',
        'Equipo Epsilon'
    ]
    
    equipos_creados = []
    for nombre in nombres_equipos:
        equipo, created = Equipo.objects.get_or_create(
            nombre=nombre,
            disciplina=disciplina,
            categoria='varones',
            defaults={
                'carrera': carrera,
                'capitan': admin_user,
            }
        )
        equipos_creados.append(equipo)
        if created:
            print(f"Equipo creado: {equipo.nombre}")
    
    return admin_user, disciplina, equipos_creados


def probar_fixture_generator():
    """Probar el generador de fixtures"""
    print("\n" + "="*50)
    print("PROBANDO GENERADOR DE FIXTURES")
    print("="*50)
    
    admin_user, disciplina, equipos = crear_equipos_prueba()
    print(f"\nEquipos disponibles: {len(equipos)}")
    for equipo in equipos:
        print(f"- {equipo.nombre}")
    
    # Limpiar partidos existentes de esta disciplina
    Partido.objects.filter(disciplina=disciplina, categoria='varones').delete()
    FixtureGenerado.objects.filter(disciplina=disciplina, categoria='varones').delete()
    print(f"\nPartidos anteriores eliminados")
    
    # Simular datos para el generador
    from partidos.views import GenerarFixtureAPIView
    from django.http import HttpRequest
    from unittest.mock import Mock
    import json
    
    # Crear mock request
    request = Mock(spec=HttpRequest)
    request.user = admin_user
    request.body = json.dumps({
        'disciplina_id': disciplina.id,
        'categoria': 'varones',
        'fecha_inicio': date.today().strftime('%Y-%m-%d'),
        'fecha_fin': (date.today() + timedelta(days=30)).strftime('%Y-%m-%d'),
        'hora_inicio': '09:00',
        'hora_fin': '18:00',
        'duracion_partido': 90,
        'descanso_partidos': 30,
        'sedes': ['Cancha 1', 'Cancha 2', 'Cancha 3']
    }).encode('utf-8')
    
    # Ejecutar el generador
    view = GenerarFixtureAPIView()
    response = view.post(request)
    
    print(f"\nRespuesta del generador: {response.status_code}")
    if hasattr(response, 'content'):
        import json
        try:
            content = json.loads(response.content.decode('utf-8'))
            print(f"Contenido: {content}")
        except:
            print(f"Contenido (raw): {response.content}")
    
    # Verificar resultados
    partidos = Partido.objects.filter(disciplina=disciplina, categoria='varones', es_fixture=True)
    print(f"\nPartidos generados: {partidos.count()}")
    
    # Agrupar por jornada
    jornadas = {}
    for partido in partidos:
        jornada = partido.jornada
        if jornada not in jornadas:
            jornadas[jornada] = []
        jornadas[jornada].append(partido)
    
    print(f"\nJornadas generadas: {len(jornadas)}")
    
    # Verificar que ningún equipo juegue más de una vez por jornada
    error_encontrado = False
    for jornada_num, partidos_jornada in jornadas.items():
        print(f"\nJornada {jornada_num}: {len(partidos_jornada)} partidos")
        equipos_en_jornada = set()
        
        for partido in partidos_jornada:
            print(f"  {partido.equipo_a.nombre} vs {partido.equipo_b.nombre} - {partido.fecha} {partido.hora}")
            
            # Verificar que ningún equipo esté duplicado
            if partido.equipo_a.id in equipos_en_jornada:
                print(f"  ❌ ERROR: {partido.equipo_a.nombre} juega más de una vez en esta jornada")
                error_encontrado = True
            if partido.equipo_b.id in equipos_en_jornada:
                print(f"  ❌ ERROR: {partido.equipo_b.nombre} juega más de una vez en esta jornada")
                error_encontrado = True
                
            equipos_en_jornada.add(partido.equipo_a.id)
            equipos_en_jornada.add(partido.equipo_b.id)
    
    # Verificar que cada equipo juegue contra todos los demás exactamente una vez
    print(f"\n" + "="*50)
    print("VERIFICACIÓN DE ENFRENTAMIENTOS")
    print("="*50)
    
    total_equipos = len(equipos)
    enfrentamientos_esperados = total_equipos * (total_equipos - 1) // 2
    print(f"Enfrentamientos esperados: {enfrentamientos_esperados}")
    print(f"Partidos generados: {partidos.count()}")
    
    # Crear matriz de enfrentamientos
    enfrentamientos = set()
    for partido in partidos:
        equipo_a_id = min(partido.equipo_a.id, partido.equipo_b.id)
        equipo_b_id = max(partido.equipo_a.id, partido.equipo_b.id)
        enfrentamiento = (equipo_a_id, equipo_b_id)
        
        if enfrentamiento in enfrentamientos:
            print(f"❌ ERROR: Enfrentamiento duplicado entre equipos {equipo_a_id} y {equipo_b_id}")
            error_encontrado = True
        else:
            enfrentamientos.add(enfrentamiento)
    
    print(f"Enfrentamientos únicos encontrados: {len(enfrentamientos)}")
    
    if not error_encontrado and len(enfrentamientos) == enfrentamientos_esperados:
        print(f"\n✅ FIXTURE GENERADO CORRECTAMENTE")
        print(f"✅ Ningún equipo juega más de una vez por jornada")
        print(f"✅ Todos los enfrentamientos están presentes")
    else:
        print(f"\n❌ ERRORES ENCONTRADOS EN EL FIXTURE")
        
    return not error_encontrado


if __name__ == '__main__':
    success = probar_fixture_generator()
    if success:
        print(f"\n🎉 TODAS LAS PRUEBAS PASARON EXITOSAMENTE")
        sys.exit(0)
    else:
        print(f"\n💥 ALGUNAS PRUEBAS FALLARON")
        sys.exit(1)
