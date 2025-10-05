"""
Caso de uso: Listar Controles

Este caso de uso maneja la obtención de la lista de controles
"""
from typing import List
from src.domain.services.control_service import ControlService
from src.application.dto.control_dto import ControlResponseDTO


class ListarControlesUseCase:
    """Caso de uso para listar controles"""
    
    def __init__(self, control_service: ControlService):
        self._control_service = control_service
    
    def ejecutar(self, solo_activos: bool = False) -> List[ControlResponseDTO]:
        """Ejecuta el caso de uso de listado de controles"""
        
        if solo_activos:
            controles = self._control_service._control_repository.obtener_activos()
        else:
            controles = self._control_service._control_repository.obtener_todos()
        
        # Convertir a DTOs
        controles_dto = []
        for control in controles:
            control_dto = ControlResponseDTO(
                id=control.id,
                nombre=control.nombre,
                descripcion=control.descripcion,
                activo=control.activo,
                fecha_creacion=control.fecha_creacion,
                disparar_si_hay_datos=control.disparar_si_hay_datos,
                conexion_id=control.conexion_id,
                consulta_disparo_id=control.consulta_disparo_id,
                consultas_a_disparar_ids=control.consultas_a_disparar_ids,
                parametros_ids=control.parametros_ids,
                referentes_ids=control.referentes_ids
            )
            controles_dto.append(control_dto)
        
        return controles_dto