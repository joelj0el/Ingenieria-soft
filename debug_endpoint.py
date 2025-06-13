#!/usr/bin/env python
import os
import sys
import django
from django.test import Client

# Agregar el directorio del proyecto al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Configurar Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil

def probar_endpoint():
    """Probar el endpoint de administrativos directamente"""
    
    # Crear un superusuario de prueba si no existe
    if not User.objects.filter(is_superuser=True).exists():
        superuser = User.objects.create_superuser(
            username='admin_test',
            email='admin@test.com',
            password='admin123'
        )
        print("✅ Superusuario de prueba creado")
    else:
        superuser = User.objects.filter(is_superuser=True).first()
        print("✅ Usando superusuario existente")

    # Usar el cliente de Django para probar
    client = Client()
    
    # Iniciar sesión como superusuario
    client.force_login(superuser)    # Probar el endpoint
    response = client.get('/api/v2/perfiles/administrativos/')
    
    print(f"📡 Status code: {response.status_code}")
    print(f"📄 Content-Type: {response.get('Content-Type', 'No especificado')}")
    
    if response.status_code == 404:
        print("❌ Endpoint no encontrado. Probando rutas alternativas...")
        
        # Probar rutas alternativas
        endpoints_alternativos = [
            '/api/v2/perfiles/administrativos/',
            '/usuarios/api/perfiles/administrativos/',
            '/api/perfiles/administrativos/',
            '/perfiles/administrativos/'
        ]
        
        for endpoint in endpoints_alternativos:
            print(f"🔍 Probando: {endpoint}")
            resp = client.get(endpoint)
            print(f"   Status: {resp.status_code}")
            if resp.status_code == 200:
                print(f"   ✅ Encontrado en: {endpoint}")
                response = resp
                break
    
    if response.status_code == 200:
        try:
            data = response.json()
            print(f"✅ Respuesta exitosa!")
            print(f"📊 Número de registros: {len(data)}")
            
            if data:
                print("\n📋 Primeros registros:")
                for i, registro in enumerate(data[:3]):  # Mostrar máximo 3 registros
                    usuario = registro.get('usuario', {})
                    print(f"  {i+1}. {usuario.get('first_name', '')} {usuario.get('last_name', '')} ({usuario.get('email', '')})")
                    print(f"     Estado: {registro.get('estado_verificacion', 'No especificado')}")
            else:
                print("ℹ️  No hay usuarios administrativos pendientes")
                
        except Exception as e:
            print(f"❌ Error al parsear JSON: {str(e)}")
            print(f"📄 Contenido raw: {response.content[:500]}")
    else:
        print(f"❌ Error en la respuesta:")
        print(f"📄 Contenido: {response.content}")

    # Información adicional
    pendientes = Perfil.objects.filter(rol='administrativo', estado_verificacion='pendiente').count()
    print(f"\n📈 Total en BD: {pendientes} usuarios administrativos pendientes")

if __name__ == '__main__':
    probar_endpoint()
