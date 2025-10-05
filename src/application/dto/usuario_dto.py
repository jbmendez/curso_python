"""
DTOs (Data Transfer Objects) para Usuario

Los DTOs son objetos simples que transportan datos entre capas
sin contener lógica de negocio.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class CrearUsuarioDTO:
    """DTO para crear un nuevo usuario"""
    nombre: str
    email: str


@dataclass 
class ActualizarUsuarioDTO:
    """DTO para actualizar un usuario existente"""
    nombre: Optional[str] = None
    email: Optional[str] = None
    activo: Optional[bool] = None


@dataclass
class UsuarioResponseDTO:
    """DTO de respuesta con datos del usuario"""
    id: int
    nombre: str
    email: str
    fecha_creacion: datetime
    activo: bool