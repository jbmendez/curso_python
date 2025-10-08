"""
Caso de uso para listar programaciones

Maneja la consulta de programaciones con filtros
y transformación a DTOs de respuesta.
"""
from typing import List, Optional

from ...domain.repositories.programacion_repository import ProgramacionRepository
from ...domain.repositories.control_repository import ControlRepository
from ..dto.programacion_dto import ListarProgramacionesResponseDTO, ProgramacionResponseDTO


class ListarProgramacionesUseCase:
    """Caso de uso para listar programaciones"""
    
    def __init__(
        self, 
        programacion_repository: ProgramacionRepository,
        control_repository: ControlRepository
    ):
        self.programacion_repository = programacion_repository
        self.control_repository = control_repository
    
    def ejecutar(self, control_id: Optional[int] = None, solo_activas: bool = False) -> ListarProgramacionesResponseDTO:
        """
        Lista programaciones con filtros opcionales
        
        Args:
            control_id: ID del control (opcional, si no se especifica lista todas)
            solo_activas: Si True, solo retorna programaciones activas
            
        Returns:
            ListarProgramacionesResponseDTO: Lista de programaciones
        """
        try:
            # Obtener programaciones según filtros
            if control_id:
                programaciones = self.programacion_repository.obtener_por_control_id(control_id)
                if solo_activas:
                    programaciones = [p for p in programaciones if p.activo]
            elif solo_activas:
                programaciones = self.programacion_repository.obtener_activas()
            else:
                programaciones = self.programacion_repository.obtener_todas()
            
            # Transformar a DTOs
            programaciones_dto = [
                ProgramacionResponseDTO.from_entity(programacion)
                for programacion in programaciones
            ]
            
            # Calcular estadísticas
            total = len(programaciones_dto)
            activas = sum(1 for p in programaciones_dto if p.activo)
            inactivas = total - activas
            
            # Mensaje descriptivo
            if control_id:
                control = self.control_repository.obtener_por_id(control_id)
                control_nombre = control.nombre if control else f"Control {control_id}"
                message = f"Se encontraron {total} programaciones para el control '{control_nombre}'"
            else:
                message = f"Se encontraron {total} programaciones en total"
            
            return ListarProgramacionesResponseDTO(
                success=True,
                data=programaciones_dto,
                total=total,
                activas=activas,
                inactivas=inactivas,
                message=message
            )
            
        except Exception as e:
            return ListarProgramacionesResponseDTO(
                success=False,
                data=[],
                total=0,
                activas=0,
                inactivas=0,
                message=f"Error al listar programaciones: {str(e)}"
            )