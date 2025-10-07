"""
Caso de uso: Listar Referentes

Este caso de uso maneja la obtención de referentes
"""
from typing import List
from src.domain.repositories.referente_repository import ReferenteRepository
from src.application.dto.referente_dto import ReferenteResponseDTO


class ListarReferentesUseCase:
    """Caso de uso para listar referentes"""
    
    def __init__(self, referente_repository: ReferenteRepository):
        self._referente_repository = referente_repository
    
    def ejecutar(self, solo_activos: bool = False) -> List[ReferenteResponseDTO]:
        """Ejecuta el caso de uso de listado de referentes"""
        
        if solo_activos:
            referentes = self._referente_repository.obtener_activos()
        else:
            referentes = self._referente_repository.obtener_todos()
        
        # Convertir a DTOs de respuesta
        return [
            ReferenteResponseDTO(
                id=referente.id,
                nombre=referente.nombre,
                email=referente.email,
                path_archivos=referente.path_archivos,
                activo=referente.activo
            )
            for referente in referentes
        ]