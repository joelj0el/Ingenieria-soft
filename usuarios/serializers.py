# usuarios/serializers.py

from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Perfil, Post, Carrera

class CarreraSerializer(serializers.ModelSerializer):
    class Meta:
        model = Carrera
        fields = ['id', 'nombre']

class UserSerializer(serializers.ModelSerializer):
    rol = serializers.CharField(write_only=True)
    carrera = serializers.PrimaryKeyRelatedField(queryset=Carrera.objects.all(), write_only=True, required=False)
    
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'password', 'rol', 'carrera']
        extra_kwargs = {'password': {'write_only': True}}
    
    def validate_email(self, value):
        """
        Validar que el correo electrónico tenga el dominio @uab.edu.bo
        """
        if not value.endswith('@uab.edu.bo'):
            raise serializers.ValidationError("Solo se permiten correos con dominio @uab.edu.bo")
        return value
    
    def validate(self, data):
        """
        Validar que los estudiantes seleccionen una carrera
        """
        rol = data.get('rol')
        carrera = data.get('carrera')
        
        if rol == 'estudiante' and not carrera:
            raise serializers.ValidationError({"carrera": "Este campo es obligatorio para estudiantes"})
        
        return data
    
    def create(self, validated_data):
        # Extraemos campos adicionales
        password = validated_data.pop('password', None)
        rol = validated_data.pop('rol', 'estudiante')
        carrera = validated_data.pop('carrera', None)
        
        # Creamos el usuario
        user = User.objects.create(**validated_data)
        if password:
            user.set_password(password)
            user.save()
        
        # Creamos el perfil asociado
        perfil = Perfil.objects.create(
            usuario=user,
            rol=rol,
            carrera=carrera if rol == 'estudiante' else None,
            estado_verificacion='pendiente' if rol == 'administrativo' else 'aprobado'
        )
        
        return user

class PerfilSerializer(serializers.ModelSerializer):
    usuario = UserSerializer(read_only=True)
    carrera = CarreraSerializer(read_only=True)
    
    class Meta:
        model = Perfil
        fields = ['id', 'usuario', 'telefono', 'direccion', 'fecha_registro', 'rol', 'carrera', 'estado_verificacion']

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