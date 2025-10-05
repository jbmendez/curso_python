"""
Caso de uso para crear referentes
"""
from src.domain.entities.referente import Referente
from src.domain.repositories.referente_repository import ReferenteRepository
from src.application.dto.referente_dto import CrearReferenteDTO, ReferenteResponseDTO


class CrearReferenteUseCase:
    """Caso de uso para crear un nuevo referente"""
    
    def __init__(self, referente_repository: ReferenteRepository):
        self._referente_repository = referente_repository
    
    def ejecutar(self, datos: CrearReferenteDTO) -> ReferenteResponseDTO:
        """Ejecuta el caso de uso de creación de referente"""
        
        # Crear entidad referente
        referente = Referente(
            id=None,
            control_id=datos.control_id,
            nombre=datos.nombre,
            email=datos.email,
            cargo=datos.cargo
        )
        
        # Guardar referente
        referente_guardado = self._referente_repository.guardar(referente)
        
        # Retornar DTO de respuesta
        return ReferenteResponseDTO(
            id=referente_guardado.id,
            control_id=referente_guardado.control_id,
            nombre=referente_guardado.nombre,
            email=referente_guardado.email,
            cargo=referente_guardado.cargo
        )