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
from usuarios.models import Perfil, Disciplina, Equipo
from partidos.models import Partido, EventoPartido
from datetime import datetime, date, time

def probar_funcionalidad_partidos():
    """Probar que la funcionalidad de partidos esté funcionando correctamente"""
    
    print("🏃‍♂️ Probando funcionalidad de partidos...")
    
    # Verificar que hay disciplinas y equipos
    disciplinas = Disciplina.objects.all()
    equipos = Equipo.objects.all()
    
    print(f"📊 Disciplinas disponibles: {disciplinas.count()}")
    print(f"⚽ Equipos disponibles: {equipos.count()}")
    
    if disciplinas.count() == 0:
        print("❌ No hay disciplinas. Creando una disciplina de prueba...")
        disciplina = Disciplina.objects.create(
            nombre="Fútbol",
            descripcion="Deporte de equipo",
            activo=True
        )
        print(f"✅ Disciplina creada: {disciplina.nombre}")
    else:
        disciplina = disciplinas.first()
        print(f"✅ Usando disciplina: {disciplina.nombre}")
    
    if equipos.count() < 2:
        print("❌ Necesitamos al menos 2 equipos. Creando equipos de prueba...")
        
        equipo1 = Equipo.objects.create(
            nombre="Equipo Alfa",
            disciplina=disciplina,
            descripcion="Equipo de prueba 1"
        )
        
        equipo2 = Equipo.objects.create(
            nombre="Equipo Beta", 
            disciplina=disciplina,
            descripcion="Equipo de prueba 2"
        )
        
        print(f"✅ Equipos creados: {equipo1.nombre}, {equipo2.nombre}")
    else:
        equipos_list = list(equipos[:2])
        equipo1, equipo2 = equipos_list[0], equipos_list[1]
        print(f"✅ Usando equipos: {equipo1.nombre}, {equipo2.nombre}")
    
    # Verificar que hay un usuario administrativo
    admin_user = User.objects.filter(is_superuser=True).first()
    if not admin_user:
        print("❌ No hay superusuario. Creando uno...")
        admin_user = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='admin123'
        )
        print("✅ Superusuario creado")
    
    # Crear un partido de prueba
    partido_existente = Partido.objects.filter(
        equipo_a=equipo1,
        equipo_b=equipo2,
        estado='en_vivo'
    ).first()
    
    if partido_existente:
        partido = partido_existente
        print(f"✅ Usando partido existente: {partido}")
    else:
        partido = Partido.objects.create(
            equipo_a=equipo1,
            equipo_b=equipo2,
            disciplina=disciplina,
            categoria='masculino',
            fecha=date.today(),
            hora=time(15, 0),
            lugar="Cancha Principal",
            estado='en_vivo',
            creado_por=admin_user
        )
        print(f"✅ Partido creado: {partido}")
    
    # Probar el cálculo de puntos
    print(f"\n📊 Probando cálculo de puntos...")
    print(f"Puntos {equipo1.nombre}: {partido.calcular_puntos_equipo(equipo1)}")
    print(f"Puntos {equipo2.nombre}: {partido.calcular_puntos_equipo(equipo2)}")
    print(f"Resultado actual: {partido.resultado_actual}")
    
    # Agregar algunos eventos de prueba
    print(f"\n⚽ Agregando eventos de prueba...")
    
    # Gol para equipo1
    evento1 = EventoPartido.objects.create(
        partido=partido,
        equipo=equipo1,
        tipo_evento='gol',
        valor=1,
        activo=True
    )
    
    # Gol para equipo2
    evento2 = EventoPartido.objects.create(
        partido=partido,
        equipo=equipo2,
        tipo_evento='gol',
        valor=1,
        activo=True
    )
    
    print(f"✅ Eventos creados")
    print(f"Puntos {equipo1.nombre}: {partido.calcular_puntos_equipo(equipo1)}")
    print(f"Puntos {equipo2.nombre}: {partido.calcular_puntos_equipo(equipo2)}")
    print(f"Resultado actual: {partido.resultado_actual}")
    
    # Probar finalización de partido
    print(f"\n🏁 Probando finalización de partido...")
    partido.estado = 'finalizado'
    partido.actualizar_resultado_final()
    
    print(f"Goles finales {equipo1.nombre}: {partido.goles_equipo_a}")
    print(f"Goles finales {equipo2.nombre}: {partido.goles_equipo_b}")
    print(f"Resultado final: {partido.resultado}")
    
    print(f"\n✅ ¡Todas las pruebas completadas!")
    print(f"🎯 ID del partido para probar en el navegador: {partido.id}")

if __name__ == '__main__':
    probar_funcionalidad_partidos()
