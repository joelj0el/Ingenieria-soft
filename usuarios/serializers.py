# usuarios/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Post

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name']
        extra_kwargs = {'password': {'write_only': True}}
    
    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'telefono', 'direccion', 'fecha_registro']

# Serializador para los Posts
class PostSerializer(serializers.ModelSerializer):
    autor_nombre = serializers.ReadOnlyField(source='autor.username')
    autor_info = UserSerializer(source='autor', read_only=True)
    
    class Meta:
        model = Post
        fields = ['id', 'titulo', 'contenido', 'fecha_creacion', 'fecha_actualizacion', 
                 'autor', 'autor_nombre', 'autor_info', 'imagen', 'activo']
        extra_kwargs = {
            'autor': {'write_only': True},  # Solo se usa para crear/actualizar
            'fecha_creacion': {'read_only': True},
            'fecha_actualizacion': {'read_only': True},
        }

class LoginSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150)
    password = serializers.CharField(max_length=128, write_only=True)