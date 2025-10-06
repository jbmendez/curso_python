"""
DTOs para operaciones de conexión
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearConexionDTO:
    """DTO para crear una nueva conexión"""
    nombre: str
    motor: str
    servidor: str
    puerto: int
    base_datos: str
    usuario: str
    password: str
    activa: bool = True
    

@dataclass  
class ConexionResponseDTO:
    """DTO de respuesta para conexión"""
    id: int
    nombre: str
    motor: str
    servidor: str
    puerto: int
    base_datos: str
    usuario: str
    activa: bool


@dataclass
class ActualizarConexionDTO:
    """DTO para actualizar una conexión existente"""
    nombre: Optional[str] = None
    motor: Optional[str] = None
    servidor: Optional[str] = None
    puerto: Optional[int] = None
    base_datos: Optional[str] = None
    usuario: Optional[str] = None
    password: Optional[str] = None
    activa: Optional[bool] = None