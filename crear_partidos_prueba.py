# crear_partidos_prueba.py
import os
import sys
import django
from datetime import date, time, timedelta

# Configurar Django
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from partidos.models import Partido
from usuarios.models import Equipo, Disciplina, User

def crear_partidos_prueba():
    """Crear algunos partidos de prueba"""
    print("Creando partidos de prueba...")
    
    try:
        # Obtener equipos existentes
        equipos = list(Equipo.objects.all())
        
        if len(equipos) < 2:
            print("No hay suficientes equipos para crear partidos. Primero crea algunos equipos.")
            return
        
        # Obtener un usuario administrador para crear los partidos
        admin_user = User.objects.filter(perfil__rol='administrativo').first()
        
        if not admin_user:
            print("No hay usuarios administrativos. Primero crea un usuario administrativo.")
            return
        
        # Crear algunos partidos de ejemplo
        partidos_creados = 0
        
        # Partido 1: Primer equipo vs segundo equipo
        if len(equipos) >= 2:
            equipo_a = equipos[0]
            equipo_b = equipos[1]
            
            # Verificar que sean de la misma disciplina y categoría
            if equipo_a.disciplina == equipo_b.disciplina and equipo_a.categoria == equipo_b.categoria:
                partido1 = Partido.objects.create(
                    equipo_a=equipo_a,
                    equipo_b=equipo_b,
                    disciplina=equipo_a.disciplina,
                    categoria=equipo_a.categoria,
                    fecha=date.today() + timedelta(days=7),
                    hora=time(15, 0),
                    lugar="Campo Principal",
                    estado='programado',
                    creado_por=admin_user
                )
                print(f"✓ Partido creado: {partido1}")
                partidos_creados += 1
        
        # Si hay más equipos, crear más partidos
        if len(equipos) >= 4:
            equipo_c = equipos[2]
            equipo_d = equipos[3]
            
            if equipo_c.disciplina == equipo_d.disciplina and equipo_c.categoria == equipo_d.categoria:
                # Partido finalizado con resultado
                partido2 = Partido.objects.create(
                    equipo_a=equipo_c,
                    equipo_b=equipo_d,
                    disciplina=equipo_c.disciplina,
                    categoria=equipo_c.categoria,
                    fecha=date.today() - timedelta(days=2),
                    hora=time(16, 30),
                    lugar="Gimnasio Norte",
                    estado='finalizado',
                    goles_equipo_a=2,
                    goles_equipo_b=1,
                    creado_por=admin_user
                )
                print(f"✓ Partido creado: {partido2}")
                partidos_creados += 1
                
                # Partido en vivo
                partido3 = Partido.objects.create(
                    equipo_a=equipo_a,
                    equipo_b=equipo_c,
                    disciplina=equipo_a.disciplina,
                    categoria=equipo_a.categoria,
                    fecha=date.today(),
                    hora=time(18, 0),
                    lugar="Campo Auxiliar",
                    estado='en_vivo',
                    goles_equipo_a=1,
                    goles_equipo_b=0,
                    creado_por=admin_user
                )
                print(f"✓ Partido creado: {partido3}")
                partidos_creados += 1
        
        print(f"\n✅ Se crearon {partidos_creados} partidos de prueba correctamente!")
        print("\nAhora puedes:")
        print("1. Visitar /partidos/ para ver los partidos")
        print("2. Usar los filtros para filtrar por estado y disciplina")
        print("3. Crear nuevos partidos manualmente")
        print("4. Generar fixtures automáticamente")
        
    except Exception as e:
        print(f"❌ Error al crear partidos: {str(e)}")

if __name__ == "__main__":
    crear_partidos_prueba()
