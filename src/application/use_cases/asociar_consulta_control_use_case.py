"""
Caso de uso: Asociar Consulta a Control

Este caso de uso maneja la asociación de consultas con controles
"""
from src.domain.entities.consulta_control import ConsultaControl
from src.domain.repositories.consulta_control_repository import ConsultaControlRepository
from src.application.dto.consulta_control_dto import CrearConsultaControlDTO, ConsultaControlResponseDTO


class AsociarConsultaControlUseCase:
    """Caso de uso para asociar una consulta a un control"""
    
    def __init__(self, consulta_control_repository: ConsultaControlRepository):
        self._consulta_control_repository = consulta_control_repository
    
    def ejecutar(self, datos: CrearConsultaControlDTO) -> ConsultaControlResponseDTO:
        """
        Ejecuta el caso de uso de asociación de consulta a control
        
        Args:
            datos: Datos de la asociación
            
        Returns:
            ConsultaControlResponseDTO: Datos de la asociación creada
            
        Raises:
            ValueError: Si hay errores de validación
        """
        
        # Verificar que no exista ya la asociación
        asociaciones_existentes = self._consulta_control_repository.obtener_por_control(datos.control_id)
        for asociacion in asociaciones_existentes:
            if asociacion.consulta_id == datos.consulta_id:
                raise ValueError(f"La consulta {datos.consulta_id} ya está asociada al control {datos.control_id}")
        
        # Si se marca como disparo, quitar el flag de otras consultas del control
        if datos.es_disparo:
            for asociacion in asociaciones_existentes:
                if asociacion.es_disparo:
                    raise ValueError("Ya existe una consulta de disparo para este control. Primero desmarca la actual.")
        
        # Crear entidad consulta-control
        consulta_control = ConsultaControl(
            control_id=datos.control_id,
            consulta_id=datos.consulta_id,
            es_disparo=datos.es_disparo,
            orden=datos.orden,
            activa=datos.activa
        )
        
        # Validaciones de negocio
        if not consulta_control.es_valida():
            raise ValueError("Los datos de la asociación no son válidos")
        
        # Guardar asociación
        asociacion_guardada = self._consulta_control_repository.guardar(consulta_control)
        
        # Retornar DTO de respuesta
        return ConsultaControlResponseDTO(
            id=asociacion_guardada.id,
            control_id=asociacion_guardada.control_id,
            consulta_id=asociacion_guardada.consulta_id,
            es_disparo=asociacion_guardada.es_disparo,
            orden=asociacion_guardada.orden,
            activa=asociacion_guardada.activa,
            fecha_asociacion=asociacion_guardada.fecha_asociacion.isoformat() if asociacion_guardada.fecha_asociacion else ""
        )