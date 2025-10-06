"""
Caso de uso para eliminar controles
"""
from src.domain.services.control_service import ControlService
from src.domain.repositories.control_repository import ControlRepository


class EliminarControlUseCase:
    """Caso de uso para eliminar un control existente"""
    
    def __init__(self, control_service: ControlService, control_repository: ControlRepository):
        self._control_service = control_service
        self._control_repository = control_repository
    
    def ejecutar(self, control_id: int) -> bool:
        """
        Elimina un control existente
        
        Args:
            control_id: ID del control a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False en caso contrario
            
        Raises:
            ValueError: Si el control no existe o no se puede eliminar
        """
        # Verificar que el control existe
        try:
            control_existente = self._control_service.cargar_control_completo(control_id)
        except ValueError:
            raise ValueError(f"No se encontró el control con ID {control_id}")
        
        # Verificaciones adicionales antes de eliminar
        # Por ejemplo, verificar si el control tiene ejecuciones recientes
        # o si está siendo usado por otros procesos
        
        # Realizar la eliminación
        eliminado = self._control_repository.eliminar(control_id)
        
        if not eliminado:
            raise ValueError(f"No se pudo eliminar el control con ID {control_id}")
        
        return True