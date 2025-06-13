# usuarios/equipos_views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
import json
from .models import Perfil, Disciplina, Equipo, JugadorEquipo
from django.contrib.auth.models import User
import traceback

class DisciplinasAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener lista de disciplinas"""        # Obtener todas las disciplinas
        disciplinas = Disciplina.objects.all()
        resultado = []
        for disciplina in disciplinas:
            resultado.append({
                'id': disciplina.id,
                'nombre': disciplina.nombre,
                'descripcion': disciplina.descripcion,
                'imagen': disciplina.imagen.url if disciplina.imagen else None,
            })
        
        return JsonResponse(resultado, safe=False)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)  # Agregamos csrf_exempt para descartar problemas de CSRF
    def post(self, request):
        """Crear una nueva disciplina (solo administrativos)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Acceso denegado'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            # Depuración - imprimir encabezados y contenido del formulario
            print("POST recibido para crear disciplina")
            print(f"Content-Type: {request.content_type}")
            print(f"POST data: {request.POST}")
            print(f"FILES data: {request.FILES}")
            print(f"Método: {request.method}")
            print(f"Headers: {request.headers}")
            
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            imagen = request.FILES.get('imagen')
            
            if not nombre:
                return JsonResponse({'error': 'El nombre de la disciplina es obligatorio'}, status=400)
            
            # Comprobar si ya existe una disciplina con ese nombre
            if Disciplina.objects.filter(nombre=nombre).exists():
                return JsonResponse({'error': 'Ya existe una disciplina con ese nombre'}, status=400)
            
            # Crear la carpeta de medios para disciplinas si no existe
            import os
            from django.conf import settings
            
            media_dir = os.path.join(settings.MEDIA_ROOT, 'disciplinas')
            if not os.path.exists(media_dir):
                os.makedirs(media_dir, exist_ok=True)
                
            # Usar try/except para manejar errores específicos al guardar
            try:
                # Crear la disciplina
                disciplina = Disciplina.objects.create(
                    nombre=nombre,
                    descripcion=descripcion,
                    imagen=imagen
                )
                
                return JsonResponse({
                    'id': disciplina.id,
                    'nombre': disciplina.nombre,
                    'descripcion': disciplina.descripcion,
                    'imagen': disciplina.imagen.url if disciplina.imagen else None,
                    'message': 'Disciplina creada correctamente'
                }, status=201)
            except Exception as e:
                print(f"Error específico al crear la disciplina: {str(e)}")
                return JsonResponse({'error': f'Error al guardar la disciplina: {str(e)}'}, status=400)
        except Exception as e:
            print(f"Error al crear disciplina: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

class DisciplinaDetailAPIView(View):
    @method_decorator(login_required)
    def get(self, request, disciplina_id):
        """Obtener detalles de una disciplina"""
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
            
            return JsonResponse({
                'id': disciplina.id,
                'nombre': disciplina.nombre,
                'descripcion': disciplina.descripcion,
                'imagen': disciplina.imagen.url if disciplina.imagen else None,
            })
        except Disciplina.DoesNotExist:
            return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
    
    @method_decorator(login_required)
    def put(self, request, disciplina_id):
        """Actualizar una disciplina (solo administrativos)"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
        except Disciplina.DoesNotExist:
            return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
        
        # Verificar si es FormData o JSON
        if request.content_type and 'multipart/form-data' in request.content_type:
            # FormData
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
        else:
            # JSON
            try:
                data = json.loads(request.body)
                nombre = data.get('nombre')
                descripcion = data.get('descripcion')
            except (json.JSONDecodeError, UnicodeDecodeError):
                return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
                
        if nombre and nombre != disciplina.nombre:
            if Disciplina.objects.filter(nombre=nombre).exists():
                return JsonResponse({'error': 'Ya existe una disciplina con ese nombre'}, status=400)
            disciplina.nombre = nombre
        
        if descripcion is not None:
            disciplina.descripcion = descripcion
            
        # Manejar la imagen si se proporciona
        imagen = request.FILES.get('imagen')
        if imagen:
            disciplina.imagen = imagen
        
        disciplina.save()
        
        return JsonResponse({
            'id': disciplina.id,
            'nombre': disciplina.nombre,
            'descripcion': disciplina.descripcion,
            'imagen': disciplina.imagen.url if disciplina.imagen else None,
            'message': 'Disciplina actualizada correctamente'
        })
    
    @method_decorator(login_required)
    def delete(self, request, disciplina_id):
        """Eliminar una disciplina (solo administrativos)"""
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
        except Disciplina.DoesNotExist:
            return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
        
        # Verificar si tiene equipos asociados
        if Equipo.objects.filter(disciplina=disciplina).exists():
            return JsonResponse({'error': 'No se puede eliminar la disciplina porque tiene equipos asociados'}, status=400)
        
        disciplina.delete()
        return JsonResponse({'message': 'Disciplina eliminada correctamente'})

class EquiposAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener lista de equipos"""
        equipos = Equipo.objects.all()
        resultado = []
        
        for equipo in equipos:
            resultado.append({
                'id': equipo.id,
                'nombre': equipo.nombre,
                'disciplina': {
                    'id': equipo.disciplina.id,
                    'nombre': equipo.disciplina.nombre,
                },
                'carrera': {
                    'id': equipo.carrera.id,
                    'nombre': equipo.carrera.nombre,
                } if equipo.carrera else None,
                'categoria': equipo.categoria,
                'capitan': {
                    'id': equipo.capitan.id,
                    'nombre': f"{equipo.capitan.first_name} {equipo.capitan.last_name}"
                } if equipo.capitan else None,
                'descripcion': equipo.descripcion,
                'logo': equipo.logo.url if equipo.logo else None,
                'fecha_registro': equipo.fecha_registro.strftime('%d/%m/%Y %H:%M')
            })
        
        return JsonResponse(resultado, safe=False)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)  # Agregamos csrf_exempt para descartar problemas de CSRF
    def post(self, request):
        """Crear un nuevo equipo (solo administrativos)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Acceso denegado'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            # Depuración - imprimir encabezados y contenido
            print("POST recibido para crear equipo")
            print(f"Content-Type: {request.content_type}")
            print(f"POST data: {request.POST}")
            print(f"FILES data: {request.FILES}")
            
            # Obtener datos del formulario
            nombre = request.POST.get('nombre')
            descripcion = request.POST.get('descripcion')
            disciplina_id = request.POST.get('disciplina_id')
            carrera_id = request.POST.get('carrera_id')
            categoria = request.POST.get('categoria')
            capitan_id = request.POST.get('capitan_id')
            logo = request.FILES.get('logo')
            jugadores = request.POST.getlist('jugadores[]')
            
            if not nombre:
                return JsonResponse({'error': 'El nombre del equipo es obligatorio'}, status=400)
                
            if not disciplina_id:
                return JsonResponse({'error': 'Debe seleccionar una disciplina'}, status=400)
                
            if not carrera_id:
                return JsonResponse({'error': 'Debe seleccionar una carrera'}, status=400)
                
            if not categoria:
                return JsonResponse({'error': 'Debe seleccionar una categoría'}, status=400)
            
            # Comprobar si ya existe un equipo con ese nombre
            if Equipo.objects.filter(nombre=nombre).exists():
                return JsonResponse({'error': 'Ya existe un equipo con ese nombre'}, status=400)
            
            try:
                disciplina = Disciplina.objects.get(id=disciplina_id)
            except Disciplina.DoesNotExist:
                return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
                
            try:
                from .models import Carrera
                carrera = Carrera.objects.get(id=carrera_id)
            except Carrera.DoesNotExist:
                return JsonResponse({'error': 'Carrera no encontrada'}, status=404)
                
            capitan = None
            if capitan_id:
                try:
                    capitan = User.objects.get(id=capitan_id)
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Capitán no encontrado'}, status=404)
            
            # Crear la carpeta de medios para equipos si no existe
            import os
            from django.conf import settings
            
            media_dir = os.path.join(settings.MEDIA_ROOT, 'equipos')
            if not os.path.exists(media_dir):
                os.makedirs(media_dir, exist_ok=True)
                
            # Crear el equipo
            equipo = Equipo.objects.create(
                nombre=nombre,
                descripcion=descripcion,
                disciplina=disciplina,
                carrera=carrera,
                categoria=categoria,
                capitan=capitan,
                logo=logo
            )
            
            # Agregar jugadores al equipo
            for jugador_id in jugadores:
                try:
                    usuario = User.objects.get(id=jugador_id)
                    # Verificar que no esté ya en un equipo de esa disciplina
                    if JugadorEquipo.objects.filter(jugador=usuario, equipo__disciplina=disciplina).exists():
                        equipo.delete()  # Eliminar equipo creado
                        return JsonResponse({
                            'error': f'El jugador {usuario.first_name} {usuario.last_name} ya pertenece a otro equipo en esta disciplina'
                        }, status=400)
                    
                    JugadorEquipo.objects.create(
                        jugador=usuario,
                        equipo=equipo
                    )
                except User.DoesNotExist:
                    # Si no existe el usuario, continuamos con los demás
                    continue
            
            return JsonResponse({
                'id': equipo.id,
                'nombre': equipo.nombre,
                'disciplina': {
                    'id': equipo.disciplina.id,
                    'nombre': equipo.disciplina.nombre,
                },
                'carrera': {
                    'id': equipo.carrera.id,
                    'nombre': equipo.carrera.nombre,
                },
                'categoria': equipo.categoria,
                'capitan': {
                    'id': equipo.capitan.id,
                    'nombre': f"{equipo.capitan.first_name} {equipo.capitan.last_name}"
                } if equipo.capitan else None,
                'descripcion': equipo.descripcion,
                'logo': equipo.logo.url if equipo.logo else None,
                'message': 'Equipo creado correctamente'
            }, status=201)
        except Exception as e:
            print(f"Error al crear equipo: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

class EquipoDetailAPIView(View):
    @method_decorator(login_required)
    def get(self, request, equipo_id):
        """Obtener detalles de un equipo"""
        try:
            equipo = Equipo.objects.get(id=equipo_id)
            
            # Obtener todos los jugadores del equipo
            jugadores_equipo = JugadorEquipo.objects.filter(equipo=equipo)
            jugadores_data = []
            
            for jugador_equipo in jugadores_equipo:
                jugador = jugador_equipo.jugador
                try:
                    perfil = Perfil.objects.get(usuario=jugador)
                    carrera = perfil.carrera.nombre if perfil.carrera else None
                except Perfil.DoesNotExist:
                    carrera = None
                
                # Asegurarse de que siempre haya un nombre para mostrar
                nombre_completo = f"{jugador.first_name} {jugador.last_name}".strip()
                if not nombre_completo:
                    nombre_completo = jugador.username
                
                jugadores_data.append({
                    'id': jugador.id,
                    'nombre': nombre_completo,
                    'email': jugador.email,
                    'carrera': carrera                })
            
            return JsonResponse({
                'id': equipo.id,
                'nombre': equipo.nombre,
                'disciplina': {
                    'id': equipo.disciplina.id,
                    'nombre': equipo.disciplina.nombre,
                },
                'carrera': {
                    'id': equipo.carrera.id,
                    'nombre': equipo.carrera.nombre,
                } if equipo.carrera else None,
                'categoria': equipo.categoria,
                'capitan': {
                    'id': equipo.capitan.id,
                    'nombre': f"{equipo.capitan.first_name} {equipo.capitan.last_name}"
                } if equipo.capitan else None,
                'descripcion': equipo.descripcion,
                'logo': equipo.logo.url if equipo.logo else None,
                'jugadores': jugadores_data,
                'fecha_registro': equipo.fecha_registro.strftime('%d/%m/%Y %H:%M')            })
        except Equipo.DoesNotExist:
            return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
    
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def put(self, request, equipo_id):
        """Actualizar un equipo (solo administrativos)"""
        try:
            print(f"PUT request recibido para equipo {equipo_id}")
            print(f"Content-Type: {request.content_type}")
            print(f"POST data: {request.POST}")
            print(f"FILES data: {request.FILES}")
              # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Acceso denegado'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            try:
                equipo = Equipo.objects.get(id=equipo_id)
                print(f"Equipo encontrado: {equipo.nombre}")
            except Equipo.DoesNotExist:
                return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
            
            # Verificar si es JSON o FormData (JSON primero para PUT)
            if request.content_type and 'application/json' in request.content_type:
                # JSON
                try:
                    data = json.loads(request.body)
                    nombre = data.get('nombre')
                    descripcion = data.get('descripcion')
                    disciplina_id = data.get('disciplina_id')
                    carrera_id = data.get('carrera_id')
                    categoria = data.get('categoria')
                    capitan_id = data.get('capitan_id')
                    jugadores = data.get('jugadores', [])
                    logo = None
                    print(f"JSON - nombre: {nombre}, carrera_id: {carrera_id}, categoria: {categoria}, capitan_id: {capitan_id}, jugadores: {jugadores}")
                except (json.JSONDecodeError, UnicodeDecodeError) as e:
                    print(f"Error al decodificar JSON: {e}")
                    return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
            elif request.content_type and 'multipart/form-data' in request.content_type:
                # FormData
                nombre = request.POST.get('nombre')
                descripcion = request.POST.get('descripcion')
                disciplina_id = request.POST.get('disciplina_id')
                carrera_id = request.POST.get('carrera_id')
                categoria = request.POST.get('categoria')
                capitan_id = request.POST.get('capitan_id')
                jugadores = request.POST.getlist('jugadores[]')
                logo = request.FILES.get('logo')
                print(f"FormData - nombre: {nombre}, carrera_id: {carrera_id}, categoria: {categoria}, capitan_id: {capitan_id}, jugadores: {jugadores}")
            else:
                # Si no hay content-type específico, intentar JSON
                try:
                    data = json.loads(request.body)
                    nombre = data.get('nombre')
                    descripcion = data.get('descripcion')
                    disciplina_id = data.get('disciplina_id')
                    carrera_id = data.get('carrera_id')
                    categoria = data.get('categoria')
                    capitan_id = data.get('capitan_id')
                    jugadores = data.get('jugadores', [])
                    logo = None
                    print(f"JSON (sin content-type) - nombre: {nombre}, carrera_id: {carrera_id}, categoria: {categoria}, capitan_id: {capitan_id}, jugadores: {jugadores}")
                except (json.JSONDecodeError, UnicodeDecodeError, ValueError) as e:
                    print(f"Error al procesar datos: {e}")
                    return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
            
            # Actualizar nombre si se proporciona y es diferente
            if nombre and nombre != equipo.nombre:
                if Equipo.objects.filter(nombre=nombre).exclude(id=equipo_id).exists():
                    return JsonResponse({'error': 'Ya existe un equipo con ese nombre'}, status=400)
                equipo.nombre = nombre
            
            # Actualizar descripción
            if descripcion is not None:
                equipo.descripcion = descripcion
            
            # Actualizar categoría
            if categoria is not None:
                equipo.categoria = categoria
                
            # Actualizar disciplina
            if disciplina_id:
                try:
                    disciplina = Disciplina.objects.get(id=disciplina_id)
                    equipo.disciplina = disciplina
                except Disciplina.DoesNotExist:
                    return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
            
            # Actualizar carrera
            if carrera_id:
                try:
                    from .models import Carrera
                    carrera = Carrera.objects.get(id=carrera_id)
                    equipo.carrera = carrera
                except Carrera.DoesNotExist:
                    return JsonResponse({'error': 'Carrera no encontrada'}, status=404)
            
            # Actualizar capitán
            if capitan_id:
                try:
                    capitan = User.objects.get(id=capitan_id)
                    equipo.capitan = capitan
                except User.DoesNotExist:
                    return JsonResponse({'error': 'Capitán no encontrado'}, status=404)
            elif capitan_id == '':
                # Si se envía string vacío, limpiar capitán
                equipo.capitan = None
            
            # Manejar logo si se proporciona
            if logo:
                equipo.logo = logo
            
            equipo.save()
            
            # Actualizar jugadores si se proporcionan
            if jugadores is not None:  # Permitir lista vacía
                # Eliminar todas las asociaciones actuales
                JugadorEquipo.objects.filter(equipo=equipo).delete()
                
                # Crear nuevas asociaciones
                for jugador_id in jugadores:
                    try:
                        usuario = User.objects.get(id=jugador_id)
                        # Verificar que no esté ya en un equipo de esa disciplina (excluyendo el equipo actual)
                        if JugadorEquipo.objects.filter(
                            jugador=usuario, 
                            equipo__disciplina=equipo.disciplina
                        ).exclude(equipo=equipo).exists():
                            return JsonResponse({
                                'error': f'El jugador {usuario.first_name} {usuario.last_name} ya pertenece a otro equipo en esta disciplina'
                            }, status=400)
                        
                        JugadorEquipo.objects.create(
                            jugador=usuario,
                            equipo=equipo
                        )
                    except User.DoesNotExist:
                        continue
            
            return JsonResponse({
                'id': equipo.id,
                'nombre': equipo.nombre,
                'disciplina': {
                    'id': equipo.disciplina.id,
                    'nombre': equipo.disciplina.nombre,
                },
                'carrera': {
                    'id': equipo.carrera.id,
                    'nombre': equipo.carrera.nombre,
                } if equipo.carrera else None,
                'categoria': equipo.categoria,
                'capitan': {
                    'id': equipo.capitan.id,
                    'nombre': f"{equipo.capitan.first_name} {equipo.capitan.last_name}"
                } if equipo.capitan else None,
                'descripcion': equipo.descripcion,
                'logo': equipo.logo.url if equipo.logo else None,
                'message': 'Equipo actualizado correctamente'
            })
        except Exception as e:
            print(f"Error al actualizar equipo: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)    
    @method_decorator(login_required)
    def delete(self, request, equipo_id):
        """Eliminar un equipo (solo administrativos)"""
        print(f"DELETE request recibido para equipo {equipo_id}")
        
        # Verificar si el usuario es administrativo
        try:
            perfil = Perfil.objects.get(usuario=request.user)
            if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                print(f"Acceso denegado - Usuario: {request.user.username}, Rol: {perfil.rol}, Estado: {perfil.estado_verificacion}")
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
        except Perfil.DoesNotExist:
            print(f"Perfil no encontrado para usuario: {request.user.username}")
            return JsonResponse({'error': 'Acceso denegado'}, status=403)
        
        try:
            equipo = Equipo.objects.get(id=equipo_id)
            print(f"Equipo encontrado: {equipo.nombre}")
        except Equipo.DoesNotExist:
            print(f"Equipo no encontrado con ID: {equipo_id}")
            return JsonResponse({'error': 'Equipo no encontrado'}, status=404)
        
        # Verificar la contraseña del administrador si se proporciona
        try:
            data = json.loads(request.body)
            admin_password = data.get('admin_password')
            print(f"Contraseña recibida: {'Sí' if admin_password else 'No'}")
            
            if admin_password:
                from django.contrib.auth import authenticate
                if not authenticate(username=request.user.username, password=admin_password):
                    print("Contraseña incorrecta")
                    return JsonResponse({'error': 'Contraseña incorrecta'}, status=401)
                else:
                    print("Contraseña correcta")
        except (json.JSONDecodeError, UnicodeDecodeError) as e:
            print(f"Error al decodificar datos: {e}")
            # Si no se puede decodificar el cuerpo, continuamos sin verificar contraseña
            pass
        
        print("Eliminando asociaciones de jugadores...")
        # Eliminar todas las asociaciones de jugadores
        JugadorEquipo.objects.filter(equipo=equipo).delete()
        
        print("Eliminando equipo...")
        equipo.delete()
        print("Equipo eliminado correctamente")
        
        return JsonResponse({'message': 'Equipo eliminado correctamente'})

class JugadoresDisponiblesAPIView(View):
    @method_decorator(login_required)
    def get(self, request, disciplina_id):
        """Obtener lista de jugadores disponibles para una disciplina"""
        try:
            disciplina = Disciplina.objects.get(id=disciplina_id)
        except Disciplina.DoesNotExist:
            return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
            
        # Verificar si se está editando un equipo existente
        equipo_id = request.GET.get('equipo_id')        # Obtener todos los usuarios registrados en el sistema
        usuarios = User.objects.all()
        
        # Jugadores seleccionados del equipo en edición (si aplica)
        jugadores_seleccionados = []
        if equipo_id:
            try:
                equipo = Equipo.objects.get(id=equipo_id)
                jugadores_seleccionados = JugadorEquipo.objects.filter(equipo=equipo).values_list('jugador_id', flat=True)
            except Equipo.DoesNotExist:
                pass
        
        # Filtrar usuarios que ya están en algún equipo de esta disciplina (excluyendo a los del equipo en edición)
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
        
        return JsonResponse(jugadores_disponibles, safe=False)

# Vista API para obtener carreras
class CarrerasAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener lista de carreras activas"""
        from .models import Carrera
        carreras = Carrera.objects.filter(activo=True)
        resultado = []
        
        for carrera in carreras:
            resultado.append({
                'id': carrera.id,
                'nombre': carrera.nombre,
                'abreviatura': carrera.abreviatura,
            })
        
        return JsonResponse(resultado, safe=False)

# Vista API para buscar usuarios/jugadores
class BuscarUsuariosAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Buscar usuarios para agregar a equipos - mostrando disponibilidad por disciplina"""
        query = request.GET.get('q', '')
        carrera_id = request.GET.get('carrera_id', '')
        disciplina_id = request.GET.get('disciplina_id', '')  # Nuevo parámetro para verificar disponibilidad
        
        # Empezar con todos los usuarios activos
        usuarios = User.objects.filter(is_active=True)
        
        # Aplicar filtro de carrera solo si se especifica (opcional)
        if carrera_id:
            usuarios = usuarios.filter(perfil__carrera_id=carrera_id)
        
        # Filtrar por búsqueda de texto si se proporciona
        if query:
            usuarios = usuarios.filter(
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(username__icontains=query) |
                Q(email__icontains=query)
            )
        
        # Si no hay filtros, mostrar los primeros 20 usuarios
        if not query and not carrera_id:
            usuarios = usuarios[:20]
        else:
            # Limitar resultados cuando hay filtros
            usuarios = usuarios[:50]
        
        # Obtener jugadores ya ocupados en la disciplina seleccionada
        jugadores_ocupados = set()
        if disciplina_id:
            try:
                from .models import Disciplina
                disciplina = Disciplina.objects.get(id=disciplina_id)
                jugadores_ocupados = set(
                    JugadorEquipo.objects.filter(equipo__disciplina=disciplina)
                    .values_list('jugador_id', flat=True)
                )
            except:
                pass
        
        resultado = []
        for usuario in usuarios:
            try:
                perfil = usuario.perfil
                carrera_nombre = perfil.carrera.nombre if perfil.carrera else 'Sin carrera'
                rol = perfil.rol
            except:
                carrera_nombre = 'Sin carrera'
                rol = 'Sin rol'
                
            # Crear nombre completo
            nombre_completo = f"{usuario.first_name} {usuario.last_name}".strip()
            if not nombre_completo:
                nombre_completo = usuario.username
            
            # Verificar si está ocupado en esta disciplina
            esta_ocupado = usuario.id in jugadores_ocupados
            
            resultado.append({
                'id': usuario.id,
                'nombre': nombre_completo,
                'email': usuario.email,
                'carrera': carrera_nombre,
                'username': usuario.username,
                'rol': rol,
                'disponible': not esta_ocupado,
                'mensaje_estado': 'Ya está en otro equipo de esta disciplina' if esta_ocupado else 'Disponible'
            })
        
        return JsonResponse(resultado, safe=False)
