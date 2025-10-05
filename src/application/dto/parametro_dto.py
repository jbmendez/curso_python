"""
DTOs para operaciones de parámetros
"""
from dataclasses import dataclass
from typing import Any, Optional


@dataclass
class CrearParametroDTO:
    """DTO para crear un nuevo parámetro"""
    control_id: int
    nombre: str
    tipo: str
    descripcion: str
    valor_por_defecto: Any
    obligatorio: bool = True


@dataclass
class ParametroResponseDTO:
    """DTO de respuesta para parámetro"""
    id: int
    control_id: int
    nombre: str
    tipo: str
    descripcion: str
    valor_por_defecto: Any
    obligatorio: bool


@dataclass
class ActualizarParametroDTO:
    """DTO para actualizar un parámetro existente"""
    nombre: Optional[str] = None
    tipo: Optional[str] = None
    descripcion: Optional[str] = None
    valor_por_defecto: Optional[Any] = None
    obligatorio: Optional[bool] = None