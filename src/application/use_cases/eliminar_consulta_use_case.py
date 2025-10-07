"""
Caso de uso: Eliminar Consulta

Este caso de uso maneja la eliminación de consultas
"""
from src.domain.repositories.consulta_repository import ConsultaRepository


class EliminarConsultaUseCase:
    """Caso de uso para eliminar una consulta"""
    
    def __init__(self, consulta_repository: ConsultaRepository):
        self._consulta_repository = consulta_repository
    
    def ejecutar(self, consulta_id: int) -> bool:
        """
        Ejecuta el caso de uso de eliminación de consulta
        
        Args:
            consulta_id: ID de la consulta a eliminar
            
        Returns:
            bool: True si se eliminó exitosamente
            
        Raises:
            ValueError: Si la consulta no existe
        """
        
        # Verificar que la consulta existe
        consulta_existente = self._consulta_repository.obtener_por_id(consulta_id)
        if not consulta_existente:
            raise ValueError(f"No se encontró la consulta con ID {consulta_id}")
        
        # Eliminar consulta
        resultado = self._consulta_repository.eliminar(consulta_id)
        
        if not resultado:
            raise ValueError(f"No se pudo eliminar la consulta con ID {consulta_id}")
        
        return resultado
    
    def desactivar(self, consulta_id: int) -> bool:
        """
        Desactiva una consulta en lugar de eliminarla permanentemente
        
        Args:
            consulta_id: ID de la consulta a desactivar
            
        Returns:
            bool: True si se desactivó exitosamente
        """
        
        # Obtener consulta existente
        consulta_existente = self._consulta_repository.obtener_por_id(consulta_id)
        if not consulta_existente:
            raise ValueError(f"No se encontró la consulta con ID {consulta_id}")
        
        # Crear consulta desactivada
        consulta_existente.activa = False
        
        # Guardar cambios
        consulta_actualizada = self._consulta_repository.actualizar(consulta_existente)
        
        return consulta_actualizada.activa == False