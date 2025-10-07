"""
DTOs para operaciones de ConsultaControl
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearConsultaControlDTO:
    """DTO para crear una nueva asociación consulta-control"""
    control_id: int
    consulta_id: int
    es_disparo: bool = False
    orden: int = 1
    activa: bool = True


@dataclass
class ActualizarConsultaControlDTO:
    """DTO para actualizar una asociación consulta-control existente"""
    es_disparo: Optional[bool] = None
    orden: Optional[int] = None
    activa: Optional[bool] = None


@dataclass
class ConsultaControlResponseDTO:
    """DTO de respuesta para asociación consulta-control"""
    id: int
    control_id: int
    consulta_id: int
    es_disparo: bool
    orden: int
    activa: bool
    fecha_asociacion: str