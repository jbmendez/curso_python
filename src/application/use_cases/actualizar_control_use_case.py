"""
Caso de uso para actualizar controles existentes
"""
from src.domain.entities.control import Control
from src.domain.services.control_service import ControlService
from src.domain.repositories.control_repository import ControlRepository
from src.application.dto.control_dto import CrearControlDTO


class ActualizarControlUseCase:
    """Caso de uso para actualizar un control existente"""
    
    def __init__(self, control_service: ControlService, control_repository: ControlRepository):
        self._control_service = control_service
        self._control_repository = control_repository
    
    def ejecutar(self, control_id: int, dto: CrearControlDTO) -> Control:
        """
        Actualiza un control existente
        
        Args:
            control_id: ID del control a actualizar
            dto: Datos actualizados del control
            
        Returns:
            Control: El control actualizado
            
        Raises:
            ValueError: Si el control no existe o los datos son inválidos
        """
        # Verificar que el control existe usando el método correcto
        try:
            control_existente = self._control_service.cargar_control_completo(control_id)
        except ValueError:
            raise ValueError(f"No se encontró el control con ID {control_id}")
        
        # Crear el control actualizado manteniendo algunos datos existentes
        control_actualizado = Control(
            id=control_id,
            nombre=dto.nombre,
            descripcion=dto.descripcion,
            disparar_si_hay_datos=dto.disparar_si_hay_datos,
            conexion_id=dto.conexion_id,
            consulta_disparo_id=control_existente.consulta_disparo_id,  # Preservar valor existente
            consultas_a_disparar_ids=control_existente.consultas_a_disparar_ids,  # Preservar valor existente
            parametros_ids=control_existente.parametros_ids,  # Preservar valor existente
            referentes_ids=control_existente.referentes_ids,  # Preservar valor existente
            activo=dto.activo,  # Usar el valor del DTO
            fecha_creacion=control_existente.fecha_creacion,  # Mantener fecha original
        )
        
        # Validar el control actualizado
        errores = self._control_service.validar_control_para_creacion(control_actualizado)
        if errores:
            raise ValueError(f"Errores de validación: {', '.join(errores)}")
        
        # Guardar el control actualizado usando el repositorio
        return self._control_repository.guardar(control_actualizado)