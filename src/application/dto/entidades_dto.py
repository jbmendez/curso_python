"""
DTOs para otras entidades del sistema
"""
from dataclasses import dataclass
from typing import Optional
from src.domain.entities.parametro import TipoParametro


# DTOs para Parámetro
@dataclass
class CrearParametroDTO:
    """DTO para crear un nuevo parámetro"""
    nombre: str
    tipo: str  # Se convertirá a TipoParametro
    descripcion: str
    valor_por_defecto: Optional[str] = None
    obligatorio: bool = True


@dataclass
class ParametroResponseDTO:
    """DTO de respuesta para parámetro"""
    id: int
    nombre: str
    tipo: str
    descripcion: str
    valor_por_defecto: Optional[str]
    obligatorio: bool


# DTOs para Consulta
@dataclass
class CrearConsultaDTO:
    """DTO para crear una nueva consulta"""
    nombre: str
    sql: str
    descripcion: str


@dataclass
class ConsultaResponseDTO:
    """DTO de respuesta para consulta"""
    id: int
    nombre: str
    sql: str
    descripcion: str
    activa: bool


# DTOs para Conexión
@dataclass
class CrearConexionDTO:
    """DTO para crear una nueva conexión"""
    nombre: str
    base_datos: str
    servidor: str
    puerto: Optional[int]
    usuario: str
    contraseña: str
    tipo_motor: str


@dataclass
class ConexionResponseDTO:
    """DTO de respuesta para conexión (sin contraseña)"""
    id: int
    nombre: str
    base_datos: str
    servidor: str
    puerto: Optional[int]
    usuario: str
    tipo_motor: str
    activa: bool


# DTOs para Referente
@dataclass
class CrearReferenteDTO:
    """DTO para crear un nuevo referente"""
    nombre: str
    email: str
    carpeta_red: str = ""
    notificar_por_email: bool = True
    notificar_por_archivo: bool = False


@dataclass
class ReferenteResponseDTO:
    """DTO de respuesta para referente"""
    id: int
    nombre: str
    email: str
    carpeta_red: str
    activo: bool
    notificar_por_email: bool
    notificar_por_archivo: bool