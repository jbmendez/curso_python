"""
Caso de uso para eliminar programación

Maneja la eliminación de programaciones con validaciones
de seguridad y reglas de negocio.
"""
from ...domain.repositories.programacion_repository import ProgramacionRepository


class EliminarProgramacionUseCase:
    """Caso de uso para eliminar una programación"""
    
    def __init__(self, programacion_repository: ProgramacionRepository):
        self.programacion_repository = programacion_repository
    
    def ejecutar(self, programacion_id: int) -> bool:
        """
        Elimina una programación
        
        Args:
            programacion_id: ID de la programación a eliminar
            
        Returns:
            bool: True si se eliminó correctamente
            
        Raises:
            ValueError: Si la programación no existe
        """
        # Verificar que la programación existe
        programacion = self.programacion_repository.obtener_por_id(programacion_id)
        if not programacion:
            raise ValueError(f"La programación con ID {programacion_id} no existe")
        
        # Eliminar
        return self.programacion_repository.eliminar(programacion_id)