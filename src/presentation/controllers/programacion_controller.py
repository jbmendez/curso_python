"""
Controlador para gestión de programaciones

Maneja las operaciones CRUD de programaciones desde la GUI
siguiendo el patrón de controladores de la aplicación.
"""
from datetime import datetime, time
from typing import Dict, Any, List

from ...application.use_cases.crear_programacion_use_case import CrearProgramacionUseCase
from ...application.use_cases.listar_programaciones_use_case import ListarProgramacionesUseCase
from ...application.use_cases.actualizar_programacion_use_case import ActualizarProgramacionUseCase
from ...application.use_cases.eliminar_programacion_use_case import EliminarProgramacionUseCase
from ...application.use_cases.activar_desactivar_programacion_use_case import ActivarDesactivarProgramacionUseCase
from ...application.dto.programacion_dto import CrearProgramacionDTO, ActualizarProgramacionDTO
from ...domain.entities.programacion import TipoProgramacion, DiaSemana


class ProgramacionController:
    """Controlador para gestión de programaciones"""
    
    def __init__(
        self,
        crear_programacion_uc: CrearProgramacionUseCase,
        listar_programaciones_uc: ListarProgramacionesUseCase,
        actualizar_programacion_uc: ActualizarProgramacionUseCase,
        eliminar_programacion_uc: EliminarProgramacionUseCase,
        activar_desactivar_programacion_uc: ActivarDesactivarProgramacionUseCase
    ):
        self.crear_programacion_uc = crear_programacion_uc
        self.listar_programaciones_uc = listar_programaciones_uc
        self.actualizar_programacion_uc = actualizar_programacion_uc
        self.eliminar_programacion_uc = eliminar_programacion_uc
        self.activar_desactivar_programacion_uc = activar_desactivar_programacion_uc
    
    def crear_programacion(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Crea una nueva programación
        
        Args:
            datos: Diccionario con los datos de la programación
            
        Returns:
            Dict con respuesta del controlador
        """
        try:
            # Validar datos requeridos
            campos_requeridos = ['control_id', 'nombre', 'descripcion', 'tipo_programacion']
            for campo in campos_requeridos:
                if campo not in datos or not datos[campo]:
                    return {
                        'success': False,
                        'message': f'El campo {campo} es requerido',
                        'status': 400
                    }
            
            # Parsear tipo de programación
            try:
                tipo_programacion = TipoProgramacion(datos['tipo_programacion'])
            except ValueError:
                return {
                    'success': False,
                    'message': f'Tipo de programación inválido: {datos["tipo_programacion"]}',
                    'status': 400
                }
            
            # Parsear configuraciones específicas según el tipo
            hora_ejecucion = None
            if 'hora_ejecucion' in datos and datos['hora_ejecucion']:
                try:
                    hora_ejecucion = self._parse_time(datos['hora_ejecucion'])
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Formato de hora inválido. Use HH:MM',
                        'status': 400
                    }
            
            fecha_inicio = None
            if 'fecha_inicio' in datos and datos['fecha_inicio']:
                try:
                    fecha_inicio = self._parse_datetime(datos['fecha_inicio'])
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Formato de fecha de inicio inválido',
                        'status': 400
                    }
            
            fecha_fin = None
            if 'fecha_fin' in datos and datos['fecha_fin']:
                try:
                    fecha_fin = self._parse_datetime(datos['fecha_fin'])
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Formato de fecha de fin inválido',
                        'status': 400
                    }
            
            # Parsear días de semana
            dias_semana = None
            if 'dias_semana' in datos and datos['dias_semana']:
                try:
                    dias_semana = [DiaSemana(dia) for dia in datos['dias_semana']]
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Días de semana inválidos',
                        'status': 400
                    }
            
            # Crear DTO
            dto = CrearProgramacionDTO(
                control_id=int(datos['control_id']),
                nombre=datos['nombre'].strip(),
                descripcion=datos['descripcion'].strip(),
                tipo_programacion=tipo_programacion,
                activo=datos.get('activo', True),
                hora_ejecucion=hora_ejecucion,
                fecha_inicio=fecha_inicio,
                fecha_fin=fecha_fin,
                dias_semana=dias_semana,
                dias_mes=datos.get('dias_mes'),
                intervalo_minutos=datos.get('intervalo_minutos'),
                creado_por=datos.get('creado_por', 'GUI')
            )
            
            # Ejecutar caso de uso
            programacion = self.crear_programacion_uc.ejecutar(dto)
            
            return {
                'success': True,
                'data': {
                    'id': programacion.id,
                    'nombre': programacion.nombre,
                    'descripcion_programacion': programacion.obtener_descripcion_programacion()
                },
                'message': f'Programación "{programacion.nombre}" creada exitosamente',
                'status': 201
            }
            
        except ValueError as e:
            return {
                'success': False,
                'message': str(e),
                'status': 400
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}',
                'status': 500
            }
    
    def actualizar_programacion(self, datos: Dict[str, Any]) -> Dict[str, Any]:
        """
        Actualiza una programación existente
        
        Args:
            datos: Diccionario con los datos actualizados de la programación
            
        Returns:
            Dict con respuesta del controlador
        """
        try:
            # Validar datos requeridos
            campos_requeridos = ['id', 'control_id', 'nombre', 'descripcion', 'tipo_programacion']
            for campo in campos_requeridos:
                if campo not in datos or (campo != 'id' and not datos[campo]):
                    return {
                        'success': False,
                        'message': f'El campo {campo} es requerido',
                        'status': 400
                    }
            
            # Parsear tipo de programación
            try:
                tipo_programacion = TipoProgramacion(datos['tipo_programacion'])
            except ValueError:
                return {
                    'success': False,
                    'message': f'Tipo de programación inválido: {datos["tipo_programacion"]}',
                    'status': 400
                }
            
            # Parsear configuraciones específicas según el tipo
            hora_ejecucion = None
            if 'hora_ejecucion' in datos and datos['hora_ejecucion']:
                try:
                    hora_ejecucion = self._parse_time(datos['hora_ejecucion'])
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Formato de hora inválido. Use HH:MM',
                        'status': 400
                    }
            
            # Parsear días de semana
            dias_semana = None
            if 'dias_semana' in datos and datos['dias_semana']:
                try:
                    dias_semana = [DiaSemana(dia) for dia in datos['dias_semana']]
                except ValueError:
                    return {
                        'success': False,
                        'message': 'Días de semana inválidos',
                        'status': 400
                    }
            
            # Crear DTO de actualización
            from ...application.dto.programacion_dto import ActualizarProgramacionDTO
            dto = ActualizarProgramacionDTO(
                id=int(datos['id']),
                control_id=int(datos['control_id']),  # ← AGREGADO: control_id faltante
                nombre=datos['nombre'].strip(),
                descripcion=datos['descripcion'].strip(),
                tipo_programacion=tipo_programacion,
                activo=datos.get('activo', True),
                hora_ejecucion=hora_ejecucion,
                fecha_inicio=None,
                fecha_fin=None,
                dias_semana=dias_semana,
                dias_mes=datos.get('dias_mes'),
                intervalo_minutos=datos.get('intervalo_minutos')
            )
            
            # Ejecutar caso de uso
            programacion = self.actualizar_programacion_uc.ejecutar(dto)
            
            return {
                'success': True,
                'data': {
                    'id': programacion.id,
                    'nombre': programacion.nombre,
                    'descripcion_programacion': programacion.obtener_descripcion_programacion()
                },
                'message': f'Programación "{programacion.nombre}" actualizada exitosamente',
                'status': 200
            }
            
        except ValueError as e:
            return {
                'success': False,
                'message': str(e),
                'status': 400
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}',
                'status': 500
            }
    
    def listar_programaciones(self, control_id: int = None, solo_activas: bool = False) -> Dict[str, Any]:
        """
        Lista programaciones con filtros opcionales
        
        Args:
            control_id: ID del control (opcional)
            solo_activas: Si True, solo retorna activas
            
        Returns:
            Dict con respuesta del controlador
        """
        try:
            print(f"DEBUG Controlador - Listando programaciones. control_id: {control_id}, solo_activas: {solo_activas}")
            response = self.listar_programaciones_uc.ejecutar(control_id, solo_activas)
            print(f"DEBUG Controlador - Respuesta del use case: success={response.success}, total={response.total}")
            
            return {
                'success': response.success,
                'data': [self._programacion_dto_to_dict(p) for p in response.data],
                'total': response.total,
                'activas': response.activas,
                'inactivas': response.inactivas,
                'message': response.message,
                'status': 200 if response.success else 500
            }
            
        except Exception as e:
            print(f"DEBUG Controlador - Excepción: {e}")
            import traceback
            traceback.print_exc()
            return {
                'success': False,
                'data': [],
                'message': f'Error al listar programaciones: {str(e)}',
                'status': 500
            }
    
    def eliminar_programacion(self, programacion_id: int) -> Dict[str, Any]:
        """
        Elimina una programación
        
        Args:
            programacion_id: ID de la programación a eliminar
            
        Returns:
            Dict con respuesta del controlador
        """
        try:
            resultado = self.eliminar_programacion_uc.ejecutar(programacion_id)
            
            if resultado:
                return {
                    'success': True,
                    'message': 'Programación eliminada exitosamente',
                    'status': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo eliminar la programación',
                    'status': 400
                }
                
        except ValueError as e:
            return {
                'success': False,
                'message': str(e),
                'status': 404
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}',
                'status': 500
            }
    
    def activar_desactivar_programacion(self, programacion_id: int, activo: bool) -> Dict[str, Any]:
        """
        Activa o desactiva una programación
        
        Args:
            programacion_id: ID de la programación
            activo: True para activar, False para desactivar
            
        Returns:
            Dict con respuesta del controlador
        """
        try:
            resultado = self.activar_desactivar_programacion_uc.ejecutar(programacion_id, activo)
            
            if resultado:
                accion = "activada" if activo else "desactivada"
                return {
                    'success': True,
                    'message': f'Programación {accion} exitosamente',
                    'status': 200
                }
            else:
                return {
                    'success': False,
                    'message': 'No se pudo actualizar el estado de la programación',
                    'status': 400
                }
                
        except ValueError as e:
            return {
                'success': False,
                'message': str(e),
                'status': 404
            }
        except Exception as e:
            return {
                'success': False,
                'message': f'Error interno: {str(e)}',
                'status': 500
            }
    
    def obtener_tipos_programacion(self) -> Dict[str, Any]:
        """
        Obtiene los tipos de programación disponibles
        
        Returns:
            Dict con los tipos de programación
        """
        tipos = []
        for tipo in TipoProgramacion:
            tipos.append({
                'value': tipo.value,
                'name': tipo.name,
                'description': self._get_tipo_description(tipo)
            })
        
        return {
            'success': True,
            'data': tipos,
            'status': 200
        }
    
    def obtener_dias_semana(self) -> Dict[str, Any]:
        """
        Obtiene los días de la semana disponibles
        
        Returns:
            Dict con los días de la semana
        """
        dias = []
        for dia in DiaSemana:
            dias.append({
                'value': dia.value,
                'name': dia.name,
                'display_name': dia.name.capitalize()
            })
        
        return {
            'success': True,
            'data': dias,
            'status': 200
        }
    
    def _programacion_dto_to_dict(self, dto) -> Dict[str, Any]:
        """Convierte un DTO de programación a diccionario"""
        return {
            'id': dto.id,
            'control_id': dto.control_id,
            'nombre': dto.nombre,
            'descripcion': dto.descripcion,
            'tipo_programacion': dto.tipo_programacion,
            'activo': dto.activo,
            'hora_ejecucion': dto.hora_ejecucion,
            'fecha_inicio': dto.fecha_inicio,
            'fecha_fin': dto.fecha_fin,
            'dias_semana': dto.dias_semana,
            'dias_mes': dto.dias_mes,
            'intervalo_minutos': dto.intervalo_minutos,
            'ultima_ejecucion': dto.ultima_ejecucion,
            'proxima_ejecucion': dto.proxima_ejecucion,
            'total_ejecuciones': dto.total_ejecuciones,
            'descripcion_programacion': dto.descripcion_programacion,
            'fecha_creacion': dto.fecha_creacion,
            'creado_por': dto.creado_por
        }
    
    def _parse_time(self, time_str: str) -> time:
        """Parsea string de hora en formato HH:MM"""
        return datetime.strptime(time_str, '%H:%M').time()
    
    def _parse_datetime(self, datetime_str: str) -> datetime:
        """Parsea string de datetime en formato ISO"""
        return datetime.fromisoformat(datetime_str)
    
    def _get_tipo_description(self, tipo: TipoProgramacion) -> str:
        """Obtiene descripción legible del tipo de programación"""
        descriptions = {
            TipoProgramacion.UNICA_VEZ: "Ejecutar solo una vez en fecha/hora específica",
            TipoProgramacion.DIARIA: "Ejecutar todos los días a hora específica",
            TipoProgramacion.SEMANAL: "Ejecutar días específicos de la semana",
            TipoProgramacion.MENSUAL: "Ejecutar días específicos del mes",
            TipoProgramacion.INTERVALO: "Ejecutar cada X minutos/horas"
        }
        return descriptions.get(tipo, "Tipo no definido")