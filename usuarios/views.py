# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from django.contrib import messages
from .forms import FormularioRegistro, FormularioLogin

# Imports para Django REST Framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from .serializers import UserSerializer, PerfilSerializer, LoginSerializer, PostSerializer
from django.contrib.auth.models import User
from .models import Perfil, Post, Carrera

# Vistas tradicionales basadas en plantillas
class RegistroView(View):
    def get(self, request):
        form = FormularioRegistro()
        return render(request, 'usuarios/registro.html', {'form': form})
    
    def post(self, request):
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            rol = form.cleaned_data.get('rol')
            
            if rol == 'administrativo':
                messages.info(request, 'Tu cuenta ha sido creada pero necesita aprobación de un administrador. Te notificaremos cuando sea aprobada.')
                return redirect('login')
            else:
                # Para estudiantes, inicio de sesión automático
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password1')
                user = authenticate(username=username, password=password)
                login(request, user)
                messages.success(request, 'Te has registrado correctamente.')
                return redirect('home')
        return render(request, 'usuarios/registro.html', {'form': form})

class LoginView(View):
    def get(self, request):
        form = FormularioLogin()
        return render(request, 'usuarios/login.html', {'form': form})
    
    def post(self, request):
        form = FormularioLogin(data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                # Verificar si el usuario administrativo está aprobado
                try:
                    perfil = Perfil.objects.get(usuario=user)
                    if perfil.rol == 'administrativo' and perfil.estado_verificacion != 'aprobado':
                        messages.error(request, 'Tu cuenta administrativa aún no ha sido aprobada. Por favor, espera la confirmación.')
                        return render(request, 'usuarios/login.html', {'form': form})
                except Perfil.DoesNotExist:
                    pass  # Si no hay perfil, continúa con el login normal
                
                login(request, user)
                return redirect('home')
            else:
                messages.error(request, 'Nombre de usuario o contraseña incorrectos.')
        return render(request, 'usuarios/login.html', {'form': form})

# Vistas API basadas en DRF
class UserAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener información del usuario actual"""
        user = request.user
        serializer = UserSerializer(user)
        return Response(serializer.data)
    
    def put(self, request):
        """Actualizar información del usuario actual"""
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RegistroAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Registrar un nuevo usuario a través de la API"""
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Obtener el perfil recién creado
            perfil = Perfil.objects.get(usuario=user)
            
            # Mensaje específico según el rol
            message = "Registro exitoso. Ya puedes iniciar sesión."
            if perfil.rol == 'administrativo':
                message = "Registro exitoso. Tu cuenta necesita aprobación de un administrador."
            
            return Response({
                'success': True,
                'message': message,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginAPIView(APIView):
    permission_classes = [AllowAny]
    
    def post(self, request):
        """Iniciar sesión a través de la API"""
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')
            user = authenticate(request, username=username, password=password)
            
            if user is not None:
                # Verificar si el usuario administrativo está aprobado
                try:
                    perfil = Perfil.objects.get(usuario=user)
                    if perfil.rol == 'administrativo' and perfil.estado_verificacion != 'aprobado':
                        return Response({
                            'error': 'Tu cuenta administrativa aún no ha sido aprobada.'
                        }, status=status.HTTP_403_FORBIDDEN)
                except Perfil.DoesNotExist:
                    pass  # Si no hay perfil, continúa con el login normal
                
                login(request, user)
                return Response({
                    'success': True,
                    'message': 'Has iniciado sesión correctamente',
                    'id': user.id,
                    'username': user.username
                })
            else:
                return Response({
                    'error': 'Credenciales inválidas'
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    def delete(self, request):
        """Cerrar sesión"""
        logout(request)
        return Response({'message': 'Sesión cerrada exitosamente'})

class PerfilAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request):
        """Obtener el perfil del usuario actual"""
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            serializer = PerfilSerializer(perfil)
            return Response(serializer.data)
        except Perfil.DoesNotExist:
            return Response(
                {'error': 'Perfil no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def put(self, request):
        """Actualizar el perfil del usuario actual"""
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            serializer = PerfilSerializer(perfil, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Perfil.DoesNotExist:
            return Response(
                {'error': 'Perfil no encontrado'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Vistas API para Posts
class PostAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, post_id=None):
        """Obtener una publicación específica o todas las publicaciones"""
        if post_id:
            try:
                post = Post.objects.get(id=post_id)
                serializer = PostSerializer(post)
                return Response(serializer.data)
            except Post.DoesNotExist:
                return Response(
                    {'error': 'Publicación no encontrada'}, 
                    status=status.HTTP_404_NOT_FOUND
                )
        else:
            # Por defecto mostrar todas las publicaciones activas
            posts = Post.objects.filter(activo=True)
            serializer = PostSerializer(posts, many=True)
            return Response(serializer.data)
    
    def post(self, request):
        """Crear una nueva publicación"""
        # Asignamos automáticamente el autor actual
        data = request.data.copy()
        data['autor'] = request.user.id
        
        serializer = PostSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    def put(self, request, post_id):
        """Actualizar una publicación existente"""
        try:
            post = Post.objects.get(id=post_id)
            
            # Verificar que el usuario actual sea el autor
            if post.autor != request.user:
                return Response(
                    {'error': 'No tienes permiso para editar esta publicación'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            data = request.data.copy()
            data['autor'] = request.user.id
            
            serializer = PostSerializer(post, data=data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Publicación no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )
    
    def delete(self, request, post_id):
        """Eliminar una publicación"""
        try:
            post = Post.objects.get(id=post_id)
            
            # Verificar que el usuario actual sea el autor
            if post.autor != request.user:
                return Response(
                    {'error': 'No tienes permiso para eliminar esta publicación'},
                    status=status.HTTP_403_FORBIDDEN
                )
                
            post.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Publicación no encontrada'}, 
                status=status.HTTP_404_NOT_FOUND
            )

# Vista para administrar solicitudes de administrativos (para superadmins)
class AdministrativosView(APIView):
    permission_classes = [IsAdminUser]
    
    def get(self, request):
        """Listar solicitudes pendientes de administrativos"""
        perfiles = Perfil.objects.filter(rol='administrativo', estado_verificacion='pendiente')
        serializer = PerfilSerializer(perfiles, many=True)
        return Response(serializer.data)
    
    def put(self, request, pk):
        """Aprobar o rechazar solicitud"""
        try:
            perfil = Perfil.objects.get(pk=pk, rol='administrativo')
            accion = request.data.get('accion')
            
            if accion not in ['aprobar', 'rechazar']:
                return Response({'error': 'Acción no válida'}, status=status.HTTP_400_BAD_REQUEST)
            
            perfil.estado_verificacion = 'aprobado' if accion == 'aprobar' else 'rechazado'
            perfil.save()
            
            return Response({'success': True, 'message': f'Solicitud {perfil.estado_verificacion} correctamente'})
            
        except Perfil.DoesNotExist:
            return Response({'error': 'Perfil no encontrado'}, status=status.HTTP_404_NOT_FOUND)

# Vista para obtener carreras
class CarreraAPIView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        """Obtener lista de carreras activas"""
        carreras = Carrera.objects.filter(activo=True)
        from .serializers import CarreraSerializer
        serializer = CarreraSerializer(carreras, many=True)
        return Response(serializer.data)