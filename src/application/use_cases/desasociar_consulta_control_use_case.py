"""
Caso de uso: Desasociar Consulta de Control

Este caso de uso maneja la eliminación de asociaciones entre consultas y controles
"""
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository


class DesasociarConsultaControlUseCase:
    """Caso de uso para desasociar una consulta de un control"""
    
    def __init__(self, consulta_control_repository: ConsultaControlRepository):
        self._consulta_control_repository = consulta_control_repository
    
    def ejecutar(self, control_id: int, consulta_id: int) -> bool:
        """
        Ejecuta el caso de uso de desasociación de consulta de control
        
        Args:
            control_id: ID del control
            consulta_id: ID de la consulta
            
        Returns:
            bool: True si se eliminó exitosamente
            
        Raises:
            ValueError: Si no existe la asociación
        """
        
        # Buscar la asociación específica
        asociaciones = self._consulta_control_repository.obtener_por_control(control_id)
        asociacion_a_eliminar = None
        
        for asociacion in asociaciones:
            if asociacion.consulta_id == consulta_id:
                asociacion_a_eliminar = asociacion
                break
        
        if not asociacion_a_eliminar:
            raise ValueError(f"No existe asociación entre el control {control_id} y la consulta {consulta_id}")
        
        # Eliminar la asociación
        return self._consulta_control_repository.eliminar(asociacion_a_eliminar.id)