"""
DTOs para operaciones de referentes
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearReferenteDTO:
    """DTO para crear un nuevo referente"""
    nombre: str
    email: str
    path_archivos: str = ""
    activo: bool = True


@dataclass
class ReferenteResponseDTO:
    """DTO de respuesta para referente"""
    id: int
    nombre: str
    email: str
    path_archivos: str
    activo: bool


@dataclass
class ActualizarReferenteDTO:
    """DTO para actualizar un referente existente"""
    nombre: Optional[str] = None
    email: Optional[str] = None
    path_archivos: Optional[str] = None
    activo: Optional[bool] = None