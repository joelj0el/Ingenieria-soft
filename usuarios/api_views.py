# usuarios/api_views.py

from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.contrib.auth.models import User
from .models import Perfil, Post, Carrera, Disciplina, Equipo, JugadorEquipo, Juez
from .serializers import UserSerializer, PerfilSerializer, PostSerializer, CarreraSerializer
from django.db.models import Q

# Serializers adicionales para los modelos
from rest_framework import serializers

class DisciplinaSerializer(serializers.ModelSerializer):
    class Meta:
        model = Disciplina
        fields = '__all__'

class EquipoSerializer(serializers.ModelSerializer):
    disciplina = DisciplinaSerializer(read_only=True)
    disciplina_id = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(),
        source='disciplina',
        write_only=True
    )
    
    class Meta:
        model = Equipo
        fields = ['id', 'nombre', 'disciplina', 'disciplina_id', 'descripcion', 'logo', 'fecha_registro']

class JugadorEquipoSerializer(serializers.ModelSerializer):
    jugador = UserSerializer(read_only=True)
    jugador_id = serializers.PrimaryKeyRelatedField(
        queryset=User.objects.all(),
        source='jugador',
        write_only=True
    )
    equipo = EquipoSerializer(read_only=True)
    equipo_id = serializers.PrimaryKeyRelatedField(
        queryset=Equipo.objects.all(),
        source='equipo',
        write_only=True
    )
    
    class Meta:
        model = JugadorEquipo
        fields = ['id', 'jugador', 'jugador_id', 'equipo', 'equipo_id', 'fecha_registro']

class JuezSerializer(serializers.ModelSerializer):
    disciplinas = DisciplinaSerializer(many=True, read_only=True)
    disciplinas_ids = serializers.PrimaryKeyRelatedField(
        queryset=Disciplina.objects.all(),
        source='disciplinas',
        write_only=True,
        many=True,
        required=False
    )
    
    class Meta:
        model = Juez
        fields = ['id', 'nombre_completo', 'correo_electronico', 'telefono', 'especialidad', 
                 'disciplinas', 'disciplinas_ids', 'fecha_registro', 'activo']

# ViewSets para los modelos
class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    
    @action(detail=False, methods=['get'])
    def current(self, request):
        """Obtener información del usuario actual"""
        serializer = UserSerializer(request.user)
        return Response(serializer.data)

class PerfilViewSet(viewsets.ModelViewSet):
    queryset = Perfil.objects.all()
    serializer_class = PerfilSerializer
    
    @action(detail=False, methods=['get'])
    def my_profile(self, request):
        """Obtener perfil del usuario actual"""
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            serializer = PerfilSerializer(perfil)
            return Response(serializer.data)
        except Perfil.DoesNotExist:
            return Response({"detail": "Perfil no encontrado"}, status=status.HTTP_404_NOT_FOUND)
    
    @action(detail=False, methods=['get'])
    def administrativos(self, request):
        """Listar perfiles administrativos"""
        if not request.user.is_superuser:
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return Response({"detail": "No tiene permisos"}, status=status.HTTP_403_FORBIDDEN)
            except Perfil.DoesNotExist:
                return Response({"detail": "No tiene permisos"}, status=status.HTTP_403_FORBIDDEN)
        
        perfiles = Perfil.objects.filter(rol='administrativo')
        serializer = PerfilSerializer(perfiles, many=True)
        return Response(serializer.data)

class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def perform_create(self, serializer):
        serializer.save(autor=self.request.user)

class CarreraViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Carrera.objects.all()
    serializer_class = CarreraSerializer
    permission_classes = [permissions.IsAuthenticated]

class DisciplinaViewSet(viewsets.ModelViewSet):
    queryset = Disciplina.objects.all()
    serializer_class = DisciplinaSerializer
    
    def get_permissions(self):
        """Solo administrativos pueden crear, editar o eliminar disciplinas"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                raise serializers.ValidationError("No tiene permisos para crear disciplinas")
        except Perfil.DoesNotExist:
            raise serializers.ValidationError("No tiene permisos para crear disciplinas")
        serializer.save()

class EquipoViewSet(viewsets.ModelViewSet):
    queryset = Equipo.objects.all()
    serializer_class = EquipoSerializer
    
    def get_permissions(self):
        """Solo administrativos pueden crear, editar o eliminar equipos"""
        if self.action in ['create', 'update', 'partial_update', 'destroy']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    @action(detail=True, methods=['get', 'post'])
    def jugadores(self, request, pk=None):
        """Obtener o asignar jugadores a un equipo"""
        equipo = self.get_object()
        
        if request.method == 'GET':
            jugadores = JugadorEquipo.objects.filter(equipo=equipo)
            serializer = JugadorEquipoSerializer(jugadores, many=True)
            return Response(serializer.data)
        
        elif request.method == 'POST':
            # Verificar permisos
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return Response({"detail": "No tiene permisos"}, status=status.HTTP_403_FORBIDDEN)
            except Perfil.DoesNotExist:
                return Response({"detail": "No tiene permisos"}, status=status.HTTP_403_FORBIDDEN)
            
            # Procesar la asignación de jugadores
            jugadores_ids = request.data.get('jugadores_ids', [])
            
            # Eliminar jugadores actuales
            JugadorEquipo.objects.filter(equipo=equipo).delete()
            
            # Asignar nuevos jugadores
            for jugador_id in jugadores_ids:
                try:
                    usuario = User.objects.get(id=jugador_id)
                    # Verificar si ya está en otro equipo de la misma disciplina
                    if JugadorEquipo.objects.filter(
                        jugador=usuario, 
                        equipo__disciplina=equipo.disciplina
                    ).exclude(equipo=equipo).exists():
                        return Response({
                            "detail": f"El jugador ya pertenece a otro equipo en esta disciplina"
                        }, status=status.HTTP_400_BAD_REQUEST)
                    
                    JugadorEquipo.objects.create(
                        jugador=usuario,
                        equipo=equipo
                    )
                except User.DoesNotExist:
                    pass
            
            return Response({"detail": "Jugadores asignados correctamente"})
    
    @action(detail=False, methods=['get'])
    def jugadores_disponibles(self, request):
        """Obtener jugadores disponibles para un equipo por disciplina"""
        disciplina_id = request.query_params.get('disciplina_id')
        equipo_id = request.query_params.get('equipo_id')
        
        if not disciplina_id:
            return Response({"detail": "Se requiere el ID de la disciplina"}, 
                          status=status.HTTP_400_BAD_REQUEST)
        
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
        except Disciplina.DoesNotExist:
            return Response({"detail": "Disciplina no encontrada"}, status=status.HTTP_404_NOT_FOUND)
        
        # Obtener todos los usuarios
        usuarios = User.objects.all()
        
        # Jugadores seleccionados del equipo en edición (si aplica)
        jugadores_seleccionados = []
        if equipo_id:
            try:
                equipo = Equipo.objects.get(id=equipo_id)
                jugadores_seleccionados = JugadorEquipo.objects.filter(equipo=equipo).values_list('jugador_id', flat=True)
            except Equipo.DoesNotExist:
                pass
        
        # Filtrar usuarios que ya están en algún equipo de esta disciplina
        jugadores_ocupados = JugadorEquipo.objects.filter(equipo__disciplina=disciplina)
        
        if equipo_id:
            jugadores_ocupados = jugadores_ocupados.exclude(equipo_id=equipo_id)
            
        jugadores_ocupados = jugadores_ocupados.values_list('jugador_id', flat=True)
        
        jugadores_disponibles = []
        for usuario in usuarios:
            if usuario.id not in jugadores_ocupados:
                try:
                    perfil = Perfil.objects.get(usuario=usuario)
                    carrera = perfil.carrera.nombre if perfil.carrera else None
                except Perfil.DoesNotExist:
                    carrera = None
                jugadores_disponibles.append({
                    'id': usuario.id,
                    'nombre': f"{usuario.first_name} {usuario.last_name}" if (usuario.first_name or usuario.last_name) else usuario.username,
                    'email': usuario.email,
                    'carrera': carrera,
                    'seleccionado': usuario.id in jugadores_seleccionados
                })
        
        return Response(jugadores_disponibles)

class JuezViewSet(viewsets.ModelViewSet):
    queryset = Juez.objects.all()
    serializer_class = JuezSerializer
    
    def get_permissions(self):
        """Solo administrativos pueden gestionar jueces"""
        if self.action in ['list', 'retrieve']:
            return [permissions.IsAuthenticated()]
        return [permissions.IsAuthenticated()]
    
    def perform_create(self, serializer):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=self.request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                raise serializers.ValidationError("No tiene permisos para crear jueces")
        except Perfil.DoesNotExist:
            raise serializers.ValidationError("No tiene permisos para crear jueces")
        serializer.save()
