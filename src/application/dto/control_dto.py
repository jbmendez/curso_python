"""
DTOs (Data Transfer Objects) para Control
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List


@dataclass
class CrearControlDTO:
    """DTO para crear un nuevo control"""
    nombre: str
    descripcion: str
    disparar_si_hay_datos: bool
    conexion_id: int
    consulta_disparo_id: int
    consultas_a_disparar_ids: List[int]
    parametros_ids: List[int]
    referentes_ids: List[int]
    activo: bool = True


@dataclass
class ActualizarControlDTO:
    """DTO para actualizar un control existente"""
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    disparar_si_hay_datos: Optional[bool] = None
    conexion_id: Optional[int] = None
    consulta_disparo_id: Optional[int] = None
    consultas_a_disparar_ids: Optional[List[int]] = None
    parametros_ids: Optional[List[int]] = None
    referentes_ids: Optional[List[int]] = None
    activo: Optional[bool] = None


@dataclass
class ControlResponseDTO:
    """DTO de respuesta con datos del control"""
    id: int
    nombre: str
    descripcion: str
    activo: bool
    fecha_creacion: datetime
    disparar_si_hay_datos: bool
    conexion_id: int
    consulta_disparo_id: int
    consultas_a_disparar_ids: List[int]
    parametros_ids: List[int]
    referentes_ids: List[int]


@dataclass
class EjecutarControlDTO:
    """DTO para ejecutar un control"""
    control_id: int
    valores_parametros: dict  # Dict[str, str]