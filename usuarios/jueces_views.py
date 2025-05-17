# usuarios/jueces_views.py

from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
import json
from .models import Perfil, Juez

class JuecesAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener lista de jueces"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        # Obtener todos los jueces
        jueces = Juez.objects.all()
        resultado = []
        
        for juez in jueces:
            resultado.append({
                'id': juez.id,
                'nombre_completo': juez.nombre_completo,
                'correo_electronico': juez.correo_electronico,
                'telefono': juez.telefono,
                'especialidad': juez.especialidad,
                'fecha_registro': juez.fecha_registro.strftime('%d/%m/%Y %H:%M')
            })
        
        return JsonResponse(resultado, safe=False)
    
    @method_decorator(login_required)
    def post(self, request):
        """Crear un nuevo juez"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        # Obtener datos del cuerpo de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
        
        # Validar datos obligatorios
        nombre = data.get('nombre_completo')
        email = data.get('correo_electronico')
        telefono = data.get('telefono')
        especialidad = data.get('especialidad')
        
        if not all([nombre, email, telefono, especialidad]):
            return JsonResponse({'error': 'Todos los campos son obligatorios'}, status=400)
        
        # Comprobar si ya existe un juez con ese correo
        if Juez.objects.filter(correo_electronico=email).exists():
            return JsonResponse({'error': 'Ya existe un juez con ese correo electrónico'}, status=400)
        
        # Crear el juez
        juez = Juez.objects.create(
            nombre_completo=nombre,
            correo_electronico=email,
            telefono=telefono,
            especialidad=especialidad
        )
        
        return JsonResponse({
            'id': juez.id,
            'nombre_completo': juez.nombre_completo,
            'correo_electronico': juez.correo_electronico,
            'telefono': juez.telefono,
            'especialidad': juez.especialidad,
            'fecha_registro': juez.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            'message': 'Juez creado correctamente'
        }, status=201)

class JuezDetailAPIView(View):
    @method_decorator(login_required)
    def get(self, request, juez_id):
        """Obtener detalles de un juez"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        # Buscar el juez
        try:
            juez = Juez.objects.get(id=juez_id)
        except Juez.DoesNotExist:
            return JsonResponse({'error': 'Juez no encontrado'}, status=404)
        
        return JsonResponse({
            'id': juez.id,
            'nombre_completo': juez.nombre_completo,
            'correo_electronico': juez.correo_electronico,
            'telefono': juez.telefono,
            'especialidad': juez.especialidad,
            'fecha_registro': juez.fecha_registro.strftime('%d/%m/%Y %H:%M')
        })
    
    @method_decorator(login_required)
    def put(self, request, juez_id):
        """Actualizar un juez"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        # Buscar el juez
        try:
            juez = Juez.objects.get(id=juez_id)
        except Juez.DoesNotExist:
            return JsonResponse({'error': 'Juez no encontrado'}, status=404)
        
        # Obtener datos del cuerpo de la solicitud
        try:
            data = json.loads(request.body)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
        
        # Actualizar datos
        nombre = data.get('nombre_completo', juez.nombre_completo)
        email = data.get('correo_electronico', juez.correo_electronico)
        telefono = data.get('telefono', juez.telefono)
        especialidad = data.get('especialidad', juez.especialidad)
        
        # Validar correo electrónico único
        if email != juez.correo_electronico and Juez.objects.filter(correo_electronico=email).exists():
            return JsonResponse({'error': 'Ya existe un juez con ese correo electrónico'}, status=400)
        
        # Actualizar los datos
        juez.nombre_completo = nombre
        juez.correo_electronico = email
        juez.telefono = telefono
        juez.especialidad = especialidad
        juez.save()
        
        return JsonResponse({
            'id': juez.id,
            'nombre_completo': juez.nombre_completo,
            'correo_electronico': juez.correo_electronico,
            'telefono': juez.telefono,
            'especialidad': juez.especialidad,
            'fecha_registro': juez.fecha_registro.strftime('%d/%m/%Y %H:%M'),
            'message': 'Juez actualizado correctamente'
        })
    
    @method_decorator(login_required)
    def delete(self, request, juez_id):
        """Eliminar un juez"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        # Buscar el juez
        try:
            juez = Juez.objects.get(id=juez_id)
        except Juez.DoesNotExist:
            return JsonResponse({'error': 'Juez no encontrado'}, status=404)
        
        # Eliminar el juez
        juez.delete()
        
        return JsonResponse({
            'message': 'Juez eliminado correctamente'
        })
