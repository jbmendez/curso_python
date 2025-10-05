"""
DTOs para operaciones de consultas
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearConsultaDTO:
    """DTO para crear una nueva consulta"""
    control_id: int
    nombre: str
    sql: str
    tipo: str
    activa: bool = True


@dataclass
class ConsultaResponseDTO:
    """DTO de respuesta para consulta"""
    id: int
    control_id: int
    nombre: str
    sql: str
    tipo: str
    activa: bool


@dataclass
class ActualizarConsultaDTO:
    """DTO para actualizar una consulta existente"""
    nombre: Optional[str] = None
    sql: Optional[str] = None
    tipo: Optional[str] = None
    activa: Optional[bool] = None