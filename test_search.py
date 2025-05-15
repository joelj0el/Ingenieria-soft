import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Olimpaz.settings')
django.setup()

from django.contrib.auth.models import User
from django.db.models import Q
from usuarios.models import Perfil, Carrera

def test_user_search(query):
    print(f"Probando búsqueda con término: '{query}'")
    
    # Intentar buscar usuarios con la consulta
    try:
        usuarios = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query)
        ).exclude(is_superuser=True)
        
        print(f"Total de resultados: {usuarios.count()}")
        
        for usuario in usuarios:
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                carrera_nombre = perfil.carrera.nombre if perfil.carrera else "N/A"
                print(f"Usuario: {usuario.username}, Nombre: {usuario.first_name} {usuario.last_name}, Email: {usuario.email}, Rol: {perfil.rol}, Carrera: {carrera_nombre}")
            except Perfil.DoesNotExist:
                print(f"Usuario: {usuario.username}, Nombre: {usuario.first_name} {usuario.last_name}, Email: {usuario.email}, Sin perfil")
    except Exception as e:
        print(f"Error durante la búsqueda: {str(e)}")

if __name__ == "__main__":
    # Probar con algunos términos de búsqueda
    test_user_search("admin")
    print("\n" + "-" * 50 + "\n")
    
    test_user_search("uab.edu.bo")
    print("\n" + "-" * 50 + "\n")
    
    # Mostrar todos los usuarios para referencia
    print("Todos los usuarios en el sistema:")
    for user in User.objects.all():
        print(f"ID: {user.id}, Usuario: {user.username}, Nombre: {user.first_name} {user.last_name}, Email: {user.email}")
