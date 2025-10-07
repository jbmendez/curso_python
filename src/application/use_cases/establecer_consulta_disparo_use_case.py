"""
Caso de uso: Establecer Consulta de Disparo

Este caso de uso maneja el establecimiento de la consulta de disparo para un control
"""
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository


class EstablecerConsultaDisparoUseCase:
    """Caso de uso para establecer la consulta de disparo de un control"""
    
    def __init__(self, consulta_control_repository: ConsultaControlRepository):
        self._consulta_control_repository = consulta_control_repository
    
    def ejecutar(self, control_id: int, consulta_id: int) -> bool:
        """
        Ejecuta el caso de uso de establecimiento de consulta de disparo
        
        Args:
            control_id: ID del control
            consulta_id: ID de la consulta que será de disparo
            
        Returns:
            bool: True si se estableció exitosamente
            
        Raises:
            ValueError: Si no existe la asociación
        """
        
        # Verificar que existe la asociación
        asociaciones = self._consulta_control_repository.obtener_por_control(control_id)
        asociacion_existe = any(a.consulta_id == consulta_id for a in asociaciones)
        
        if not asociacion_existe:
            raise ValueError(f"No existe asociación entre el control {control_id} y la consulta {consulta_id}")
        
        # Establecer la consulta como disparo (esto automáticamente quita el flag de las demás)
        return self._consulta_control_repository.establecer_consulta_disparo(control_id, consulta_id)