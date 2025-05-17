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

# Clase para personalizar el logout
class CustomLogoutView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'Has cerrado sesión correctamente.')
        return redirect('login')

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
        if (post_id):
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

# Vistas para el panel de administración
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import JsonResponse, HttpResponseForbidden, HttpResponseBadRequest
from django.db.models import Q
from django.contrib.auth import authenticate
import json

class AdminPanelView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return HttpResponseForbidden("Acceso denegado")
        except Perfil.DoesNotExist:
            return HttpResponseForbidden("Acceso denegado")
            
        return render(request, 'admin_panel.html')

class AdminUserListView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
        # Obtener todos los usuarios con sus perfiles
        usuarios = User.objects.all().exclude(is_superuser=True)
        resultado = []
        
        for usuario in usuarios:
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                carrera_nombre = perfil.carrera.nombre if perfil.carrera else None
                
                resultado.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'email': usuario.email,
                    'rol': perfil.rol,
                    'carrera_id': perfil.carrera.id if perfil.carrera else None,
                    'carrera_nombre': carrera_nombre,
                    'estado_verificacion': perfil.estado_verificacion
                })
            except Perfil.DoesNotExist:
                # Usuario sin perfil
                resultado.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'email': usuario.email,
                    'rol': 'N/A',
                    'carrera_id': None,
                    'carrera_nombre': None,
                    'estado_verificacion': 'N/A'
                })
        
        return JsonResponse(resultado, safe=False)

class AdminUserSearchView(View):
    @method_decorator(login_required)
    def get(self, request):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
        # Obtener el término de búsqueda
        query = request.GET.get('q', '').strip()
        
        if not query:
            return JsonResponse([], safe=False)
              # Buscar usuarios por nombre, apellido o email
        usuarios = User.objects.filter(
            Q(username__icontains=query) | 
            Q(first_name__icontains=query) | 
            Q(last_name__icontains=query) | 
            Q(email__icontains=query)
        ).exclude(is_superuser=True)
        
        resultado = []
        
        for usuario in usuarios:
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                carrera_nombre = perfil.carrera.nombre if perfil.carrera else None
                
                resultado.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'email': usuario.email,
                    'rol': perfil.rol,
                    'carrera_id': perfil.carrera.id if perfil.carrera else None,
                    'carrera_nombre': carrera_nombre,
                    'estado_verificacion': perfil.estado_verificacion
                })
            except Perfil.DoesNotExist:
                # Usuario sin perfil
                resultado.append({
                    'id': usuario.id,
                    'username': usuario.username,
                    'first_name': usuario.first_name,
                    'last_name': usuario.last_name,
                    'email': usuario.email,
                    'rol': 'N/A',
                    'carrera_id': None,
                    'carrera_nombre': None,
                    'estado_verificacion': 'N/A'
                })
        
        return JsonResponse(resultado, safe=False)

class AdminUserDetailView(View):
    @method_decorator(login_required)
    def get(self, request, user_id):
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
        # Obtener el usuario por ID
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            
        try:
            perfil = Perfil.objects.get(usuario=usuario)
            carrera_nombre = perfil.carrera.nombre if perfil.carrera else None
            
            resultado = {
                'id': usuario.id,
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'rol': perfil.rol,
                'carrera_id': perfil.carrera.id if perfil.carrera else None,
                'carrera_nombre': carrera_nombre,
                'estado_verificacion': perfil.estado_verificacion
            }
        except Perfil.DoesNotExist:
            # Usuario sin perfil
            resultado = {
                'id': usuario.id,
                'username': usuario.username,
                'first_name': usuario.first_name,
                'last_name': usuario.last_name,
                'email': usuario.email,
                'rol': 'N/A',
                'carrera_id': None,
                'carrera_nombre': None,
                'estado_verificacion': 'N/A'
            }
        
        return JsonResponse(resultado)
        
    @method_decorator(login_required)
    def put(self, request, user_id):
        # Verificar si el usuario es administrativo
        try:
            perfil_admin = Perfil.objects.get(usuario=request.user)
            if perfil_admin.rol != 'administrativo' or perfil_admin.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
        # Obtener el usuario a editar
        try:
            usuario = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
            
        # Obtener datos del cuerpo de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Formato de datos inválido')
            
        # Validar que el correo termine con @uab.edu.bo
        email = data.get('email', '')
        if email and not email.endswith('@uab.edu.bo'):
            return JsonResponse({'error': 'El correo debe terminar con @uab.edu.bo'}, status=400)
            
        # Actualizar datos del usuario
        usuario.first_name = data.get('first_name', usuario.first_name)
        usuario.last_name = data.get('last_name', usuario.last_name)
        usuario.email = email if email else usuario.email
        
        # Validar email único
        if User.objects.filter(email=email).exclude(id=usuario.id).exists():
            return JsonResponse({'error': 'El correo ya está en uso'}, status=400)
            
        # Guardar usuario
        usuario.save()
        
        # Actualizar perfil
        rol = data.get('rol')
        try:
            perfil = Perfil.objects.get(usuario=usuario)
            
            # Guardar rol anterior para verificaciones
            rol_anterior = perfil.rol
            
            if rol:
                perfil.rol = rol
                
            # Para estudiantes, se requiere carrera
            if rol == 'estudiante':
                carrera_id = data.get('carrera_id')
                if not carrera_id:
                    return JsonResponse({'error': 'Se requiere especificar una carrera para el estudiante'}, status=400)
                try:
                    carrera = Carrera.objects.get(id=carrera_id)
                    perfil.carrera = carrera
                except Carrera.DoesNotExist:
                    return JsonResponse({'error': 'Carrera no encontrada'}, status=404)
            
            # Si cambia de estudiante a administrativo, ponemos en estado pendiente
            if rol_anterior == 'estudiante' and rol == 'administrativo':
                perfil.estado_verificacion = 'pendiente'
                perfil.carrera = None
            
            perfil.save()
                
        except Perfil.DoesNotExist:
            # Si no tiene perfil, lo creamos
            perfil_data = {
                'usuario': usuario,
                'rol': rol if rol else 'estudiante',
                'estado_verificacion': 'pendiente' if rol == 'administrativo' else 'aprobado'
            }
            
            if rol == 'estudiante':
                carrera_id = data.get('carrera_id')
                if not carrera_id:
                    return JsonResponse({'error': 'Se requiere especificar una carrera para el estudiante'}, status=400)
                try:
                    carrera = Carrera.objects.get(id=carrera_id)
                    perfil_data['carrera'] = carrera
                except Carrera.DoesNotExist:
                    return JsonResponse({'error': 'Carrera no encontrada'}, status=404)
                
            Perfil.objects.create(**perfil_data)
        
        return JsonResponse({'success': True, 'message': 'Usuario actualizado correctamente'})
        
    @method_decorator(login_required)
    def delete(self, request, user_id):
        # Verificar si el usuario es administrativo
        try:
            perfil_admin = Perfil.objects.get(usuario=request.user)
            if perfil_admin.rol != 'administrativo' or perfil_admin.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
        # Obtener datos del cuerpo de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return HttpResponseBadRequest('Formato de datos inválido')
            
        # Verificar la contraseña del administrador
        admin_password = data.get('admin_password', '')
        if not authenticate(username=request.user.username, password=admin_password):
            return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
        
        # Obtener el usuario a eliminar
        try:
            usuario = User.objects.get(id=user_id)
            
            # No permitir eliminar al propio administrador
            if usuario == request.user:
                return JsonResponse({'error': 'No puedes eliminar tu propio usuario'}, status=400)
                
            # No permitir eliminar superusuarios
            if usuario.is_superuser:
                return JsonResponse({'error': 'No se pueden eliminar usuarios superadmin'}, status=403)
                
            # Eliminar el perfil primero (si existe)
            try:
                perfil = Perfil.objects.get(usuario=usuario)
                perfil.delete()
            except Perfil.DoesNotExist:
                pass  # No hay problema si no existe el perfil
                
            # Eliminar el usuario
            usuario.delete()
            
            return JsonResponse({'success': True, 'message': 'Usuario eliminado correctamente'})
            
        except User.DoesNotExist:
            return JsonResponse({'error': 'Usuario no encontrado'}, status=404)