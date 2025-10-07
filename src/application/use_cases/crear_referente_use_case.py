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
        
        # Verificar que el email no exista
        referente_existente = self._referente_repository.obtener_por_email(datos.email)
        if referente_existente:
            raise ValueError(f"Ya existe un referente con el email '{datos.email}'")
        
        # Crear entidad referente
        referente = Referente(
            nombre=datos.nombre,
            email=datos.email,
            path_archivos=datos.path_archivos,
            activo=datos.activo
        )
        
        # Validaciones de negocio
        if not referente.es_valido():
            raise ValueError("Los datos del referente no son válidos")
        
        # Guardar referente
        referente_guardado = self._referente_repository.guardar(referente)
        
        # Retornar DTO de respuesta
        return ReferenteResponseDTO(
            id=referente_guardado.id,
            nombre=referente_guardado.nombre,
            email=referente_guardado.email,
            path_archivos=referente_guardado.path_archivos,
            activo=referente_guardado.activo
        )