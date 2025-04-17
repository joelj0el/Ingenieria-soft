# usuarios/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.views import View
from .forms import FormularioRegistro, FormularioLogin

# Imports para Django REST Framework
from rest_framework import status, viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer, PerfilSerializer, LoginSerializer, PostSerializer
from django.contrib.auth.models import User
from .models import Perfil, Post

# Vistas tradicionales basadas en plantillas
class RegistroView(View):
    def get(self, request):
        form = FormularioRegistro()
        return render(request, 'usuarios/registro.html', {'form': form})
    
    def post(self, request):
        form = FormularioRegistro(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
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
                login(request, user)
                return redirect('home')
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
            # Crear un perfil para el usuario
            Perfil.objects.create(usuario=user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
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
                login(request, user)
                user_serializer = UserSerializer(user)
                return Response({
                    'message': 'Inicio de sesión exitoso',
                    'user': user_serializer.data
                })
            else:
                return Response(
                    {'error': 'Credenciales inválidas'}, 
                    status=status.HTTP_401_UNAUTHORIZED
                )
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        """Cerrar sesión a través de la API"""
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