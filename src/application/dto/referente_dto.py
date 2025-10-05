"""
DTOs para operaciones de referentes
"""
from dataclasses import dataclass
from typing import Optional


@dataclass
class CrearReferenteDTO:
    """DTO para crear un nuevo referente"""
    control_id: int
    nombre: str
    email: str
    cargo: str


@dataclass
class ReferenteResponseDTO:
    """DTO de respuesta para referente"""
    id: int
    control_id: int
    nombre: str
    email: str
    cargo: str


@dataclass
class ActualizarReferenteDTO:
    """DTO para actualizar un referente existente"""
    nombre: Optional[str] = None
    email: Optional[str] = None
    cargo: Optional[str] = None