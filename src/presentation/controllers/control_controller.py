"""
Controlador para operaciones de Control

Los controladores manejan las peticiones HTTP y coordinan
con los casos de uso de la aplicación.
"""
from typing import Dict, Any, List
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.application.dto.control_dto import CrearControlDTO


class ControlController:
    """Controlador para endpoints de control"""
    
    def __init__(
        self, 
        crear_control_use_case: CrearControlUseCase,
        listar_controles_use_case: ListarControlesUseCase
    ):
        self._crear_control_use_case = crear_control_use_case
        self._listar_controles_use_case = listar_controles_use_case
    
    def crear_control_simple(
        self, 
        nombre: str, 
        descripcion: str, 
        conexion_id: int, 
        usuario_creador_id: int
    ) -> Dict[str, Any]:
        """Método simplificado para crear control básico"""
        return self.crear_control({
            'nombre': nombre,
            'descripcion': descripcion,
            'conexion_id': conexion_id,
            'consulta_disparo_id': 1,  # Por ahora valores mock
            'consultas_a_disparar_ids': [1],
            'parametros_ids': [1],
            'referentes_ids': [1],
            'disparar_si_hay_datos': True,
            'activo': True,
            'usuario_creador_id': usuario_creador_id
        })
    
    def crear_control(self, datos_request: Dict[str, Any]) -> Dict[str, Any]:
        """Endpoint para crear un nuevo control"""
        try:
            # Validar datos de entrada obligatorios
            campos_obligatorios = [
                'nombre', 'descripcion', 'conexion_id', 
                'consulta_disparo_id', 'consultas_a_disparar_ids'
            ]
            
            for campo in campos_obligatorios:
                if campo not in datos_request or not datos_request[campo]:
                    return {
                        'error': f'El campo {campo} es obligatorio',
                        'status': 400
                    }
            
            # Crear DTO
            dto = CrearControlDTO(
                nombre=datos_request['nombre'],
                descripcion=datos_request['descripcion'],
                disparar_si_hay_datos=datos_request.get('disparar_si_hay_datos', True),
                conexion_id=datos_request['conexion_id'],
                consulta_disparo_id=datos_request['consulta_disparo_id'],
                consultas_a_disparar_ids=datos_request['consultas_a_disparar_ids'],
                parametros_ids=datos_request.get('parametros_ids', []),
                referentes_ids=datos_request.get('referentes_ids', [])
            )
            
            # Ejecutar caso de uso
            control_response = self._crear_control_use_case.ejecutar(dto)
            
            # Retornar respuesta exitosa
            return {
                'success': True,
                'data': {
                    'id': control_response.id,
                    'nombre': control_response.nombre,
                    'descripcion': control_response.descripcion,
                    'activo': control_response.activo,
                    'fecha_creacion': control_response.fecha_creacion.isoformat(),
                    'disparar_si_hay_datos': control_response.disparar_si_hay_datos,
                    'conexion_id': control_response.conexion_id,
                    'consulta_disparo_id': control_response.consulta_disparo_id,
                    'consultas_a_disparar_ids': control_response.consultas_a_disparar_ids,
                    'parametros_ids': control_response.parametros_ids,
                    'referentes_ids': control_response.referentes_ids
                },
                'status': 201,
                'message': 'Control creado exitosamente'
            }
            
        except ValueError as e:
            return {
                'success': False,
                'error': str(e),
                'status': 400
            }
        except Exception as e:
            return {
                'success': False,
                'error': 'Error interno del servidor',
                'status': 500
            }
    
    def listar_controles(self, solo_activos: bool = False) -> Dict[str, Any]:
        """Endpoint para listar controles"""
        try:
            controles = self._listar_controles_use_case.ejecutar(solo_activos)
            
            # Convertir a formato de respuesta
            controles_data = []
            for control in controles:
                control_data = {
                    'id': control.id,
                    'nombre': control.nombre,
                    'descripcion': control.descripcion,
                    'activo': control.activo,
                    'fecha_creacion': control.fecha_creacion.isoformat(),
                    'disparar_si_hay_datos': control.disparar_si_hay_datos,
                    'conexion_id': control.conexion_id,
                    'consulta_disparo_id': control.consulta_disparo_id,
                    'consultas_a_disparar_ids': control.consultas_a_disparar_ids,
                    'parametros_ids': control.parametros_ids,
                    'referentes_ids': control.referentes_ids
                }
                controles_data.append(control_data)
            
            return {
                'data': controles_data,
                'status': 200,
                'message': f'Se encontraron {len(controles_data)} controles'
            }
            
        except Exception as e:
            return {
                'error': 'Error interno del servidor',
                'status': 500
            }