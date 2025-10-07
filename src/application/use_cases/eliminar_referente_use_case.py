"""
Caso de uso: Eliminar Referente

Este caso de uso maneja la eliminación de referentes
"""
from src.domain.repositories.referente_repository import ReferenteRepository


class EliminarReferenteUseCase:
    """Caso de uso para eliminar un referente"""
    
    def __init__(self, referente_repository: ReferenteRepository):
        self._referente_repository = referente_repository
    
    def ejecutar(self, referente_id: int) -> bool:
        """
        Ejecuta el caso de uso de eliminación de referente
        
        Args:
            referente_id: ID del referente a eliminar
            
        Returns:
            bool: True si se eliminó correctamente, False si no se encontró
            
        Raises:
            ValueError: Si el referente no existe
        """
        
        # Verificar que el referente existe
        referente_existente = self._referente_repository.obtener_por_id(referente_id)
        if not referente_existente:
            raise ValueError(f"No se encontró el referente con ID {referente_id}")
        
        # TODO: Verificar si tiene asociaciones con controles antes de eliminar
        # Por ahora, eliminar directamente
        
        # Eliminar referente
        return self._referente_repository.eliminar(referente_id)