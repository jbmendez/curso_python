"""
Controlador para operaciones de ConsultaControl
"""
from typing import Dict, Any, List
from src.application.use_cases.asociar_consulta_control_use_case import AsociarConsultaControlUseCase
from src.application.use_cases.listar_consulta_control_use_case import ListarConsultaControlUseCase
from src.application.use_cases.desasociar_consulta_control_use_case import DesasociarConsultaControlUseCase
from src.application.use_cases.establecer_consulta_disparo_use_case import EstablecerConsultaDisparoUseCase
from src.application.dto.consulta_control_dto import CrearConsultaControlDTO


class ConsultaControlController:
    """Controlador para endpoints de asociaciones consulta-control"""
    
    def __init__(
        self, 
        asociar_use_case: AsociarConsultaControlUseCase,
        listar_use_case: ListarConsultaControlUseCase,
        desasociar_use_case: DesasociarConsultaControlUseCase,
        establecer_disparo_use_case: EstablecerConsultaDisparoUseCase
    ):
        self._asociar_use_case = asociar_use_case
        self._listar_use_case = listar_use_case
        self._desasociar_use_case = desasociar_use_case
        self._establecer_disparo_use_case = establecer_disparo_use_case
    
    def asociar_consulta(
        self,
        control_id: int,
        consulta_id: int,
        es_disparo: bool = False,
        orden: int = 1
    ) -> Dict[str, Any]:
        """
        Asocia una consulta a un control
        
        Args:
            control_id: ID del control
            consulta_id: ID de la consulta
            es_disparo: Si es consulta de disparo
            orden: Orden de ejecución
            
        Returns:
            dict: Respuesta con los datos de la asociación creada
        """
        try:
            dto = CrearConsultaControlDTO(
                control_id=control_id,
                consulta_id=consulta_id,
                es_disparo=es_disparo,
                orden=orden
            )
            
            resultado = self._asociar_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "control_id": resultado.control_id,
                    "consulta_id": resultado.consulta_id,
                    "es_disparo": resultado.es_disparo,
                    "orden": resultado.orden,
                    "activa": resultado.activa,
                    "fecha_asociacion": resultado.fecha_asociacion
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def obtener_consultas_por_control(self, control_id: int) -> Dict[str, Any]:
        """
        Obtiene todas las consultas asociadas a un control
        
        Args:
            control_id: ID del control
            
        Returns:
            dict: Respuesta con la lista de asociaciones
        """
        try:
            asociaciones = self._listar_use_case.ejecutar_por_control(control_id)
            
            asociaciones_data = []
            for asociacion in asociaciones:
                asociacion_data = {
                    'id': asociacion.id,
                    'control_id': asociacion.control_id,
                    'consulta_id': asociacion.consulta_id,
                    'es_disparo': asociacion.es_disparo,
                    'orden': asociacion.orden,
                    'activa': asociacion.activa,
                    'fecha_asociacion': asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else ""
                }
                asociaciones_data.append(asociacion_data)
            
            return {
                'success': True,
                'data': asociaciones_data,
                'status': 200,
                'message': f'Se encontraron {len(asociaciones_data)} asociaciones'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e)
            }
    
    def obtener_consulta_disparo(self, control_id: int) -> Dict[str, Any]:
        """
        Obtiene la consulta de disparo de un control
        
        Args:
            control_id: ID del control
            
        Returns:
            dict: Respuesta con la asociación de disparo
        """
        try:
            asociacion = self._listar_use_case.obtener_consulta_disparo(control_id)
            
            if asociacion:
                return {
                    "success": True,
                    "data": {
                        "id": asociacion.id,
                        "control_id": asociacion.control_id,
                        "consulta_id": asociacion.consulta_id,
                        "es_disparo": asociacion.es_disparo,
                        "orden": asociacion.orden,
                        "activa": asociacion.activa,
                        "fecha_asociacion": asociacion.fecha_asociacion.isoformat() if asociacion.fecha_asociacion else ""
                    }
                }
            else:
                return {
                    "success": True,
                    "data": None,
                    "message": "No hay consulta de disparo definida"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def desasociar_consulta(self, control_id: int, consulta_id: int) -> Dict[str, Any]:
        """
        Desasocia una consulta de un control
        
        Args:
            control_id: ID del control
            consulta_id: ID de la consulta
            
        Returns:
            dict: Respuesta de la operación
        """
        try:
            resultado = self._desasociar_use_case.ejecutar(control_id, consulta_id)
            
            if resultado:
                return {
                    "success": True,
                    "message": "Consulta desasociada exitosamente"
                }
            else:
                return {
                    "success": False,
                    "error": "No se pudo desasociar la consulta"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    def establecer_consulta_disparo(self, control_id: int, consulta_id: int) -> Dict[str, Any]:
        """
        Establece una consulta como de disparo para un control
        
        Args:
            control_id: ID del control
            consulta_id: ID de la consulta
            
        Returns:
            dict: Respuesta de la operación
        """
        try:
            resultado = self._establecer_disparo_use_case.ejecutar(control_id, consulta_id)
            
            if resultado:
                return {
                    "success": True,
                    "message": "Consulta de disparo establecida exitosamente"
                }
            else:
                return {
                    "success": False,
                    "error": "No se pudo establecer la consulta de disparo"
                }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }