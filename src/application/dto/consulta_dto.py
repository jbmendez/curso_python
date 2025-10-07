"""
DTOs para operaciones de consultas
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearConsultaDTO:
    """DTO para crear una nueva consulta"""
    nombre: str
    sql: str
    descripcion: str = ""
    control_id: Optional[int] = None
    conexion_id: Optional[int] = None  # Conexión específica (opcional)
    activa: bool = True


@dataclass
class ConsultaResponseDTO:
    """DTO de respuesta para consulta"""
    id: int
    nombre: str
    sql: str
    descripcion: str
    control_id: Optional[int]
    conexion_id: Optional[int]
    activa: bool


@dataclass
class ActualizarConsultaDTO:
    """DTO para actualizar una consulta existente"""
    nombre: Optional[str] = None
    sql: Optional[str] = None
    descripcion: Optional[str] = None
    conexion_id: Optional[int] = None
    activa: Optional[bool] = None