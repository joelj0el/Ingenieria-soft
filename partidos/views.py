# partidos/views.py
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.db.models import Q
from django.core.exceptions import ValidationError
import json
import traceback
from datetime import datetime, timedelta, date
from itertools import combinations
import random
from django.shortcuts import render

from .models import Partido, FixtureGenerado
from usuarios.models import Perfil, Disciplina, Equipo
from django.contrib.auth.models import User


class PartidosAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener lista de partidos con filtros opcionales"""
        try:
            # Filtros opcionales
            estado = request.GET.get('estado', '')
            disciplina_id = request.GET.get('disciplina_id', '')
            
            # Obtener todos los partidos
            partidos = Partido.objects.all()
            
            # Aplicar filtros
            if estado:
                partidos = partidos.filter(estado=estado)
            
            if disciplina_id:
                partidos = partidos.filter(disciplina_id=disciplina_id)
            
            # Convertir a lista de diccionarios
            resultado = []
            for partido in partidos:
                resultado.append({
                    'id': partido.id,
                    'equipo_a': {
                        'id': partido.equipo_a.id,
                        'nombre': partido.equipo_a.nombre,
                        'logo': partido.equipo_a.logo.url if partido.equipo_a.logo else None,
                    },
                    'equipo_b': {
                        'id': partido.equipo_b.id,
                        'nombre': partido.equipo_b.nombre,
                        'logo': partido.equipo_b.logo.url if partido.equipo_b.logo else None,
                    },
                    'disciplina': {
                        'id': partido.disciplina.id,
                        'nombre': partido.disciplina.nombre,
                    },
                    'categoria': partido.categoria,
                    'fecha': partido.fecha.strftime('%Y-%m-%d'),
                    'hora': partido.hora.strftime('%H:%M'),
                    'lugar': partido.lugar,
                    'estado': partido.estado,
                    'goles_equipo_a': partido.goles_equipo_a,
                    'goles_equipo_b': partido.goles_equipo_b,
                    'resultado': partido.resultado,
                    'jornada': partido.jornada,
                    'es_fixture': partido.es_fixture,
                    'fecha_creacion': partido.fecha_creacion.strftime('%d/%m/%Y %H:%M')
                })
            
            return JsonResponse(resultado, safe=False)
        
        except Exception as e:
            print(f"Error al obtener partidos: {str(e)}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """Crear un nuevo partido (solo administrativos)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Solo los administradores pueden crear partidos'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            # Obtener datos del request
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
            
            # Campos requeridos
            equipo_a_id = data.get('equipo_a_id')
            equipo_b_id = data.get('equipo_b_id')
            fecha = data.get('fecha')
            hora = data.get('hora')
            lugar = data.get('lugar', '')
            
            # Validaciones básicas
            if not all([equipo_a_id, equipo_b_id, fecha, hora]):
                return JsonResponse({'error': 'Faltan campos requeridos'}, status=400)
            
            if equipo_a_id == equipo_b_id:
                return JsonResponse({'error': 'Un equipo no puede jugar contra sí mismo'}, status=400)
            
            # Obtener equipos
            try:
                equipo_a = Equipo.objects.get(id=equipo_a_id)
                equipo_b = Equipo.objects.get(id=equipo_b_id)
            except Equipo.DoesNotExist:
                return JsonResponse({'error': 'Uno de los equipos no existe'}, status=404)
            
            # Verificar que los equipos sean de la misma disciplina y categoría
            if equipo_a.disciplina != equipo_b.disciplina:
                return JsonResponse({'error': 'Los equipos deben ser de la misma disciplina'}, status=400)
            
            if equipo_a.categoria != equipo_b.categoria:
                return JsonResponse({'error': 'Los equipos deben ser de la misma categoría'}, status=400)
            
            # Convertir fecha y hora
            try:
                fecha_obj = datetime.strptime(fecha, '%Y-%m-%d').date()
                hora_obj = datetime.strptime(hora, '%H:%M').time()
            except ValueError:
                return JsonResponse({'error': 'Formato de fecha u hora inválido'}, status=400)
            
            # Crear el partido
            partido = Partido.objects.create(
                equipo_a=equipo_a,
                equipo_b=equipo_b,
                disciplina=equipo_a.disciplina,
                categoria=equipo_a.categoria,
                fecha=fecha_obj,
                hora=hora_obj,
                lugar=lugar,
                creado_por=request.user
            )
            
            return JsonResponse({
                'id': partido.id,
                'equipo_a': {
                    'id': partido.equipo_a.id,
                    'nombre': partido.equipo_a.nombre,
                },
                'equipo_b': {
                    'id': partido.equipo_b.id,
                    'nombre': partido.equipo_b.nombre,
                },
                'disciplina': {
                    'id': partido.disciplina.id,
                    'nombre': partido.disciplina.nombre,
                },
                'categoria': partido.categoria,
                'fecha': partido.fecha.strftime('%Y-%m-%d'),
                'hora': partido.hora.strftime('%H:%M'),
                'lugar': partido.lugar,
                'estado': partido.estado,
                'message': 'Partido creado correctamente'
            }, status=201)
        
        except Exception as e:
            print(f"Error al crear partido: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


class PartidoDetailAPIView(View):
    @method_decorator(login_required)
    def get(self, request, partido_id):
        """Obtener detalles de un partido"""
        try:
            partido = Partido.objects.get(id=partido_id)
            
            return JsonResponse({
                'id': partido.id,
                'equipo_a': {
                    'id': partido.equipo_a.id,
                    'nombre': partido.equipo_a.nombre,
                    'logo': partido.equipo_a.logo.url if partido.equipo_a.logo else None,
                },
                'equipo_b': {
                    'id': partido.equipo_b.id,
                    'nombre': partido.equipo_b.nombre,
                    'logo': partido.equipo_b.logo.url if partido.equipo_b.logo else None,
                },
                'disciplina': {
                    'id': partido.disciplina.id,
                    'nombre': partido.disciplina.nombre,
                },
                'categoria': partido.categoria,
                'fecha': partido.fecha.strftime('%Y-%m-%d'),
                'hora': partido.hora.strftime('%H:%M'),
                'lugar': partido.lugar,
                'estado': partido.estado,
                'goles_equipo_a': partido.goles_equipo_a,
                'goles_equipo_b': partido.goles_equipo_b,
                'resultado': partido.resultado,
                'jornada': partido.jornada,
                'es_fixture': partido.es_fixture,
                'fecha_creacion': partido.fecha_creacion.strftime('%d/%m/%Y %H:%M')
            })
        
        except Partido.DoesNotExist:
            return JsonResponse({'error': 'Partido no encontrado'}, status=404)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def put(self, request, partido_id):
        """Actualizar un partido (solo administrativos)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Solo los administradores pueden editar partidos'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            try:
                partido = Partido.objects.get(id=partido_id)
            except Partido.DoesNotExist:
                return JsonResponse({'error': 'Partido no encontrado'}, status=404)
            
            # Obtener datos del request
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
            
            # Actualizar campos si se proporcionan
            if 'fecha' in data:
                try:
                    partido.fecha = datetime.strptime(data['fecha'], '%Y-%m-%d').date()
                except ValueError:
                    return JsonResponse({'error': 'Formato de fecha inválido'}, status=400)
            
            if 'hora' in data:
                try:
                    partido.hora = datetime.strptime(data['hora'], '%H:%M').time()
                except ValueError:
                    return JsonResponse({'error': 'Formato de hora inválido'}, status=400)
            
            if 'lugar' in data:
                partido.lugar = data['lugar']
            
            if 'estado' in data:
                if data['estado'] in ['programado', 'en_vivo', 'finalizado']:
                    partido.estado = data['estado']
                else:
                    return JsonResponse({'error': 'Estado inválido'}, status=400)
            
            if 'goles_equipo_a' in data:
                partido.goles_equipo_a = data['goles_equipo_a']
            
            if 'goles_equipo_b' in data:
                partido.goles_equipo_b = data['goles_equipo_b']
            
            partido.save()
            
            return JsonResponse({
                'id': partido.id,
                'estado': partido.estado,
                'goles_equipo_a': partido.goles_equipo_a,
                'goles_equipo_b': partido.goles_equipo_b,
                'resultado': partido.resultado,
                'message': 'Partido actualizado correctamente'
            })
        
        except Exception as e:
            print(f"Error al actualizar partido: {str(e)}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)

    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def delete(self, request, partido_id):
        """Eliminar un partido (solo administrativos)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Solo los administradores pueden eliminar partidos'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            try:
                partido = Partido.objects.get(id=partido_id)
            except Partido.DoesNotExist:
                return JsonResponse({'error': 'Partido no encontrado'}, status=404)
            
            partido.delete()
            return JsonResponse({'message': 'Partido eliminado correctamente'})
        
        except Exception as e:
            print(f"Error al eliminar partido: {str(e)}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


class GenerarFixtureAPIView(View):
    @method_decorator(login_required)
    @method_decorator(csrf_exempt)
    def post(self, request):
        """Generar la siguiente jornada del fixture (una jornada por vez)"""
        try:
            # Verificar si el usuario es administrativo
            try:
                perfil = Perfil.objects.get(usuario=request.user)
                if perfil.rol != 'administrativo' or perfil.estado_verificacion != 'aprobado':
                    return JsonResponse({'error': 'Solo los administradores pueden generar fixtures'}, status=403)
            except Perfil.DoesNotExist:
                return JsonResponse({'error': 'Acceso denegado'}, status=403)
            
            # Obtener datos del request
            try:
                data = json.loads(request.body)
            except json.JSONDecodeError:
                return JsonResponse({'error': 'Formato de datos inválido'}, status=400)
            
            # Campos requeridos
            disciplina_id = data.get('disciplina_id')
            categoria = data.get('categoria')
            fecha_partido = data.get('fecha_partido')  # Fecha para los partidos de esta jornada
            hora_inicio = data.get('hora_inicio', '09:00')
            hora_fin = data.get('hora_fin', '18:00')
            duracion_partido = data.get('duracion_partido', 90)  # minutos
            descanso_partidos = data.get('descanso_partidos', 30)  # minutos
            sedes = data.get('sedes', [])
            
            # Validaciones
            if not all([disciplina_id, categoria, fecha_partido]):
                return JsonResponse({'error': 'Faltan campos requeridos (disciplina_id, categoria, fecha_partido)'}, status=400)
            
            try:
                disciplina = Disciplina.objects.get(id=disciplina_id)
            except Disciplina.DoesNotExist:
                return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
            
            # Obtener equipos de la disciplina y categoría especificada
            equipos = Equipo.objects.filter(disciplina=disciplina, categoria=categoria)
            
            if equipos.count() < 2:
                return JsonResponse({'error': 'Se necesitan al menos 2 equipos para generar un fixture'}, status=400)
            
            # Convertir fecha y horas
            try:
                fecha_partido_obj = datetime.strptime(fecha_partido, '%Y-%m-%d').date()
                hora_inicio_obj = datetime.strptime(hora_inicio, '%H:%M').time()
                hora_fin_obj = datetime.strptime(hora_fin, '%H:%M').time()
            except ValueError:
                return JsonResponse({'error': 'Formato de fecha u hora inválido'}, status=400)
              # Obtener o crear el registro de fixture para esta disciplina y categoría
            fixture_registro, created = FixtureGenerado.objects.get_or_create(
                disciplina=disciplina,
                categoria=categoria,
                defaults={
                    'fecha_inicio': fecha_partido_obj,
                    'fecha_fin': fecha_partido_obj,
                    'total_jornadas': 0,
                    'total_partidos': 0,
                    'jornadas_generadas': 0,
                    'creado_por': request.user
                }
            )
            
            # Obtener equipos para el algoritmo round-robin
            equipos_list = list(equipos)
            num_equipos = len(equipos_list)
            
            # Si hay un número impar de equipos, agregar un "equipo fantasma" (BYE)
            if num_equipos % 2 == 1:
                equipos_list.append(None)  # None representa el "descanso"
                num_equipos += 1
            
            # Número total de jornadas necesarias para el round-robin completo
            total_jornadas_teoricas = num_equipos - 1
            
            # Calcular la siguiente jornada a generar
            siguiente_jornada = fixture_registro.jornadas_generadas + 1
            
            # Verificar si ya se completó el fixture
            if siguiente_jornada > total_jornadas_teoricas:
                return JsonResponse({
                    'error': f'El fixture ya está completo. Total de jornadas: {total_jornadas_teoricas}',
                    'fixture_completo': True,
                    'total_jornadas': total_jornadas_teoricas,
                    'jornadas_generadas': fixture_registro.jornadas_generadas
                }, status=400)
            
            # Generar los enfrentamientos de la siguiente jornada usando round-robin
            partidos_jornada = []
            
            # Crear una lista de índices de equipos para el algoritmo round-robin
            equipos_indices = list(range(num_equipos))
            
            # Rotar los equipos según la jornada actual para obtener los enfrentamientos correctos
            # Para la jornada N, rotamos N-1 veces
            for _ in range(siguiente_jornada - 1):
                if len(equipos_indices) > 1:
                    # Tomar el último elemento y moverlo a la segunda posición
                    ultimo = equipos_indices.pop()
                    equipos_indices.insert(1, ultimo)
            
            # En cada jornada, emparejar equipos
            for i in range(num_equipos // 2):
                equipo_a_idx = equipos_indices[i]
                equipo_b_idx = equipos_indices[num_equipos - 1 - i]
                
                equipo_a = equipos_list[equipo_a_idx] if equipo_a_idx < len(equipos_list) else None
                equipo_b = equipos_list[equipo_b_idx] if equipo_b_idx < len(equipos_list) else None
                
                # Saltar si alguno de los equipos es None (BYE)
                if equipo_a is None or equipo_b is None:
                    continue
                
                partidos_jornada.append((equipo_a, equipo_b))
            
            # Verificar que no haya enfrentamientos duplicados
            enfrentamientos_nuevos = set()
            for equipo_a, equipo_b in partidos_jornada:
                # Crear un identificador único para el enfrentamiento (sin importar el orden)
                enfrentamiento = tuple(sorted([equipo_a.id, equipo_b.id]))
                if enfrentamiento in enfrentamientos_nuevos:
                    return JsonResponse({
                        'error': f'Error en el algoritmo: enfrentamiento duplicado en la jornada {siguiente_jornada}'
                    }, status=500)
                enfrentamientos_nuevos.add(enfrentamiento)
            
            # Verificar que no se repitan enfrentamientos de jornadas anteriores
            enfrentamientos_previos = set()
            partidos_previos = Partido.objects.filter(
                disciplina=disciplina,
                categoria=categoria,
                es_fixture=True
            )
            
            for partido in partidos_previos:
                enfrentamiento = tuple(sorted([partido.equipo_a.id, partido.equipo_b.id]))
                enfrentamientos_previos.add(enfrentamiento)
            
            # Verificar que los nuevos enfrentamientos no se repitan
            for enfrentamiento in enfrentamientos_nuevos:
                if enfrentamiento in enfrentamientos_previos:
                    equipos_enfrentamiento = [equipos.get(id=eq_id).nombre for eq_id in enfrentamiento]
                    return JsonResponse({
                        'error': f'El enfrentamiento {equipos_enfrentamiento[0]} vs {equipos_enfrentamiento[1]} ya existe en una jornada anterior'
                    }, status=400)
            
            # Crear los partidos de esta jornada
            partidos_creados = []
            hora_actual = hora_inicio_obj
            
            for equipo_a, equipo_b in partidos_jornada:
                # Verificar que la hora no exceda el límite diario
                hora_siguiente = datetime.combine(date.today(), hora_actual)
                hora_siguiente += timedelta(minutes=duracion_partido + descanso_partidos)
                
                if hora_siguiente.time() > hora_fin_obj:
                    return JsonResponse({
                        'error': f'No es posible programar todos los partidos en el horario especificado ({hora_inicio} - {hora_fin}). Intente con un rango horario más amplio o menos partidos por día.'
                    }, status=400)
                
                # Seleccionar sede aleatoriamente si hay varias
                lugar = random.choice(sedes) if sedes else 'Por definir'
                
                # Crear el partido
                partido = Partido.objects.create(
                    equipo_a=equipo_a,
                    equipo_b=equipo_b,
                    disciplina=disciplina,
                    categoria=categoria,
                    fecha=fecha_partido_obj,
                    hora=hora_actual,
                    lugar=lugar,
                    jornada=siguiente_jornada,
                    es_fixture=True,
                    creado_por=request.user
                )
                
                partidos_creados.append(partido)
                
                # Avanzar hora para el siguiente partido del mismo día
                hora_actual = hora_siguiente.time()
              # Actualizar el registro del fixture
            fixture_registro.jornadas_generadas = siguiente_jornada
            fixture_registro.total_jornadas = max(fixture_registro.total_jornadas, siguiente_jornada)
            fixture_registro.total_partidos = fixture_registro.total_partidos + len(partidos_creados)
            fixture_registro.fecha_fin = fecha_partido_obj
            fixture_registro.completado = siguiente_jornada >= total_jornadas_teoricas
            fixture_registro.save()
            
            return JsonResponse({
                'message': f'Jornada {siguiente_jornada} generada correctamente',
                'jornada_generada': siguiente_jornada,
                'partidos_creados': len(partidos_creados),
                'total_jornadas_teoricas': total_jornadas_teoricas,
                'jornadas_restantes': total_jornadas_teoricas - siguiente_jornada,
                'fixture_completo': siguiente_jornada >= total_jornadas_teoricas,
                'disciplina': disciplina.nombre,
                'categoria': categoria,
                'fecha_partidos': fecha_partido,
                'fixture_id': fixture_registro.id,
                'partidos': [
                    {
                        'id': p.id,
                        'equipo_a': p.equipo_a.nombre,
                        'equipo_b': p.equipo_b.nombre,
                        'hora': p.hora.strftime('%H:%M'),
                        'lugar': p.lugar
                    } for p in partidos_creados
                ]
            })
        
        except Exception as e:
            print(f"Error al generar fixture: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


class EquiposPorDisciplinaAPIView(View):
    @method_decorator(login_required)
    def get(self, request, disciplina_id):
        """Obtener equipos filtrados por disciplina y opcionalmente por categoría"""
        try:
            categoria = request.GET.get('categoria', '')
            
            try:
                disciplina = Disciplina.objects.get(id=disciplina_id)
            except Disciplina.DoesNotExist:
                return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
            
            equipos = Equipo.objects.filter(disciplina=disciplina)
            
            if categoria:
                equipos = equipos.filter(categoria=categoria)
            
            resultado = []
            for equipo in equipos:
                resultado.append({
                    'id': equipo.id,
                    'nombre': equipo.nombre,
                    'categoria': equipo.categoria,
                    'logo': equipo.logo.url if equipo.logo else None,
                })
            
            return JsonResponse(resultado, safe=False)
        
        except Exception as e:
            print(f"Error al obtener equipos: {str(e)}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)


@login_required
def partidos_view(request):
    """Vista principal para la gestión de partidos"""
    try:
        perfil = Perfil.objects.get(usuario=request.user)
        is_admin = perfil.rol == 'administrativo' and perfil.estado_verificacion == 'aprobado'
    except Perfil.DoesNotExist:
        is_admin = False
    
    # Obtener disciplinas para los filtros
    disciplinas = Disciplina.objects.all()
    
    context = {
        'is_admin': is_admin,
        'disciplinas': disciplinas,
        'user': request.user,
    }
    
    return render(request, 'partidos/partidos.html', context)


class EstadoFixtureAPIView(View):
    @method_decorator(login_required)
    def get(self, request):
        """Obtener el estado del fixture para una disciplina y categoría específica"""
        try:
            disciplina_id = request.GET.get('disciplina_id')
            categoria = request.GET.get('categoria')
            
            if not all([disciplina_id, categoria]):
                return JsonResponse({'error': 'Faltan parámetros requeridos (disciplina_id, categoria)'}, status=400)
            
            try:
                disciplina = Disciplina.objects.get(id=disciplina_id)
            except Disciplina.DoesNotExist:
                return JsonResponse({'error': 'Disciplina no encontrada'}, status=404)
            
            # Obtener equipos de la disciplina y categoría
            equipos = Equipo.objects.filter(disciplina=disciplina, categoria=categoria)
            num_equipos = equipos.count()
            
            if num_equipos < 2:
                return JsonResponse({
                    'error': 'Se necesitan al menos 2 equipos para generar un fixture',
                    'num_equipos': num_equipos,
                    'equipos_necesarios': 2
                }, status=400)
            
            # Calcular total de jornadas teóricas
            total_jornadas_teoricas = num_equipos - 1 if num_equipos % 2 == 0 else num_equipos
              # Verificar si existe un fixture para esta disciplina y categoría
            try:
                fixture_registro = FixtureGenerado.objects.get(
                    disciplina=disciplina,
                    categoria=categoria
                )
                
                jornadas_generadas = fixture_registro.jornadas_generadas
                
                return JsonResponse({
                    'fixture_existe': True,
                    'fixture_id': fixture_registro.id,
                    'disciplina': disciplina.nombre,
                    'categoria': categoria,
                    'num_equipos': num_equipos,
                    'total_jornadas_teoricas': total_jornadas_teoricas,
                    'jornadas_generadas': jornadas_generadas,
                    'jornadas_restantes': total_jornadas_teoricas - jornadas_generadas,
                    'fixture_completo': fixture_registro.completado,
                    'siguiente_jornada': jornadas_generadas + 1 if not fixture_registro.completado else None,
                    'total_partidos': fixture_registro.total_partidos,
                    'fecha_inicio': fixture_registro.fecha_inicio.strftime('%Y-%m-%d') if fixture_registro.fecha_inicio else None,
                    'fecha_fin': fixture_registro.fecha_fin.strftime('%Y-%m-%d') if fixture_registro.fecha_fin else None,
                    'lista_jornadas_generadas': list(range(1, jornadas_generadas + 1))                })
            
            except FixtureGenerado.DoesNotExist:
                return JsonResponse({
                    'fixture_existe': False,
                    'disciplina': disciplina.nombre,
                    'categoria': categoria,
                    'num_equipos': num_equipos,
                    'total_jornadas_teoricas': total_jornadas_teoricas,
                    'jornadas_generadas': 0,
                    'jornadas_restantes': total_jornadas_teoricas,
                    'fixture_completo': False,
                    'siguiente_jornada': 1,
                    'total_partidos': 0,
                    'fecha_inicio': None,
                    'fecha_fin': None,
                    'lista_jornadas_generadas': []
                })
        
        except Exception as e:
            print(f"Error al obtener estado del fixture: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            return JsonResponse({'error': f'Error interno: {str(e)}'}, status=500)
