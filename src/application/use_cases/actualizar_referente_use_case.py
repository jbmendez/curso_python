"""
Caso de uso: Actualizar Referente

Este caso de uso maneja la actualización de referentes existentes
"""
from src.domain.entities.referente import Referente
from src.domain.repositories.referente_repository import ReferenteRepository
from src.application.dto.referente_dto import ActualizarReferenteDTO, ReferenteResponseDTO


class ActualizarReferenteUseCase:
    """Caso de uso para actualizar un referente existente"""
    
    def __init__(self, referente_repository: ReferenteRepository):
        self._referente_repository = referente_repository
    
    def ejecutar(self, referente_id: int, datos: ActualizarReferenteDTO) -> ReferenteResponseDTO:
        """
        Ejecuta el caso de uso de actualización de referente
        
        Args:
            referente_id: ID del referente a actualizar
            datos: Datos para actualizar
            
        Returns:
            ReferenteResponseDTO: Datos del referente actualizado
            
        Raises:
            ValueError: Si el referente no existe o hay errores de validación
        """
        
        # Obtener referente existente
        referente_existente = self._referente_repository.obtener_por_id(referente_id)
        if not referente_existente:
            raise ValueError(f"No se encontró el referente con ID {referente_id}")
        
        # Verificar email único si se está cambiando
        if datos.email and datos.email != referente_existente.email:
            referente_con_email = self._referente_repository.obtener_por_email(datos.email)
            if referente_con_email and referente_con_email.id != referente_id:
                raise ValueError(f"Ya existe otro referente con el email '{datos.email}'")
        
        # Crear referente actualizado
        referente_actualizado = Referente(
            id=referente_existente.id,
            nombre=datos.nombre if datos.nombre is not None else referente_existente.nombre,
            email=datos.email if datos.email is not None else referente_existente.email,
            path_archivos=datos.path_archivos if datos.path_archivos is not None else referente_existente.path_archivos,
            activo=datos.activo if datos.activo is not None else referente_existente.activo
        )
        
        # Validaciones de negocio
        if not referente_actualizado.es_valido():
            raise ValueError("Los datos del referente no son válidos")
        
        # Guardar referente actualizado
        referente_guardado = self._referente_repository.guardar(referente_actualizado)
        
        # Retornar DTO de respuesta
        return ReferenteResponseDTO(
            id=referente_guardado.id,
            nombre=referente_guardado.nombre,
            email=referente_guardado.email,
            path_archivos=referente_guardado.path_archivos,
            activo=referente_guardado.activo
        )