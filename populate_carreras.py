#!/usr/bin/env python
"""
Script para poblar la base de datos con las carreras de la UAB
Ejecutar con: python populate_carreras.py
"""

import os
import django

# Configurar el entorno de Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "Olimpaz.settings")
django.setup()

from usuarios.models import Carrera

# Lista de carreras de la UAB
CARRERAS = [
    {'nombre': 'INGENIERIA DE SISTEMAS', 'abreviatura': 'IS'},
    {'nombre': 'COMUNICACION SOCIAL Y MEDIOS DIGITALES', 'abreviatura': 'CSMD'},
    {'nombre': 'CONTADURIA PUBLICA', 'abreviatura': 'CP'},
    {'nombre': 'ADMINISTRACION Y NEGOCIOS INTERNACIONALES', 'abreviatura': 'ANI'},
    {'nombre': 'PSICOLOGIA', 'abreviatura': 'PSI'},
    {'nombre': 'INGENIERIA COMERCIAL', 'abreviatura': 'IC'},
    {'nombre': 'ACTIVIDAD FISICA Y DEPORTES', 'abreviatura': 'AFD'},
    {'nombre': 'PSICOPEDAGOGIA', 'abreviatura': 'PP'},
    {'nombre': 'NUTRICION Y DIETETICA', 'abreviatura': 'ND'},
    {'nombre': 'ENFERMERIA', 'abreviatura': 'ENF'},
    {'nombre': 'BIOQUIMICA', 'abreviatura': 'BQ'},
    {'nombre': 'FISIOTERAPIA Y KINESIOLOGIA', 'abreviatura': 'FK'},
    {'nombre': 'DERECHO', 'abreviatura': 'DER'},
    {'nombre': 'TEOLOGIA', 'abreviatura': 'TEO'},
    {'nombre': 'INGENIERIA CIVIL', 'abreviatura': 'IC'},
    {'nombre': 'ARQUITECTURA Y URBANISMO', 'abreviatura': 'ARQ'},
]

def populate_carreras():
    """
    Función para crear las carreras en la base de datos
    """
    print("Iniciando población de carreras...")
    
    # Contador para nuevas carreras
    nuevas = 0
    
    for carrera_info in CARRERAS:
        # Intentar encontrar la carrera o crearla si no existe
        carrera, created = Carrera.objects.get_or_create(
            nombre=carrera_info['nombre'],
            defaults={'abreviatura': carrera_info['abreviatura'], 'activo': True}
        )
        
        if created:
            nuevas += 1
            print(f"Creada carrera: {carrera.nombre}")
        else:
            print(f"Ya existe carrera: {carrera.nombre}")
    
    print(f"Proceso completado. Se crearon {nuevas} nuevas carreras.")

if __name__ == "__main__":
    print("Ejecutando script de poblamiento de carreras...")
    populate_carreras()
    print("Script finalizado!")