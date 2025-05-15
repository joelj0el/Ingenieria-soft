import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from usuarios.models import Perfil, Carrera

def list_users():
    print("==== USUARIOS EN BASE DE DATOS ====")
    users = User.objects.all()
    print(f"Total de usuarios: {users.count()}")
    
    for user in users:
        try:
            perfil = Perfil.objects.get(usuario=user)
            print(f"ID: {user.id}, Username: {user.username}, Nombre: {user.first_name} {user.last_name}, Rol: {perfil.rol}")
        except Perfil.DoesNotExist:
            print(f"ID: {user.id}, Username: {user.username}, Nombre: {user.first_name} {user.last_name}, Sin Perfil")

def list_carreras():
    print("\n==== CARRERAS EN BASE DE DATOS ====")
    carreras = Carrera.objects.all()
    print(f"Total de carreras: {carreras.count()}")
    
    for carrera in carreras:
        print(f"ID: {carrera.id}, Nombre: {carrera.nombre}")

if __name__ == "__main__":
    list_users()
    list_carreras()
