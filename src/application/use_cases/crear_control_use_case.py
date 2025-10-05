"""
Caso de uso: Crear Control

Este caso de uso maneja la creación de un nuevo control
"""
from datetime import datetime
from typing import List
from src.domain.entities.control import Control
from src.domain.services.control_service import ControlService
from src.application.dto.control_dto import CrearControlDTO, ControlResponseDTO


class CrearControlUseCase:
    """Caso de uso para crear un nuevo control"""
    
    def __init__(self, control_service: ControlService):
        self._control_service = control_service
    
    def ejecutar(self, datos: CrearControlDTO) -> ControlResponseDTO:
        """Ejecuta el caso de uso de creación de control"""
        
        # Verificar que el nombre esté disponible
        if not self._control_service.nombre_control_disponible(datos.nombre):
            raise ValueError(f"Ya existe un control con el nombre '{datos.nombre}'")
        
        # Crear entidad control
        control = Control(
            nombre=datos.nombre,
            descripcion=datos.descripcion,
            disparar_si_hay_datos=datos.disparar_si_hay_datos,
            conexion_id=datos.conexion_id,
            consulta_disparo_id=datos.consulta_disparo_id,
            consultas_a_disparar_ids=datos.consultas_a_disparar_ids.copy(),
            parametros_ids=datos.parametros_ids.copy(),
            referentes_ids=datos.referentes_ids.copy(),
            fecha_creacion=datetime.now(),
            activo=True
        )
        
        # Validar que el control sea válido para creación
        errores = self._control_service.validar_control_para_creacion(control)
        if errores:
            raise ValueError(f"Errores de validación: {'; '.join(errores)}")
        
        # Guardar control
        control_guardado = self._control_service._control_repository.guardar(control)
        
        # Retornar DTO de respuesta
        return ControlResponseDTO(
            id=control_guardado.id,
            nombre=control_guardado.nombre,
            descripcion=control_guardado.descripcion,
            activo=control_guardado.activo,
            fecha_creacion=control_guardado.fecha_creacion,
            disparar_si_hay_datos=control_guardado.disparar_si_hay_datos,
            conexion_id=control_guardado.conexion_id,
            consulta_disparo_id=control_guardado.consulta_disparo_id,
            consultas_a_disparar_ids=control_guardado.consultas_a_disparar_ids,
            parametros_ids=control_guardado.parametros_ids,
            referentes_ids=control_guardado.referentes_ids
        )