"""
DTOs para gestión de programaciones

Define los objetos de transferencia de datos para
las operaciones de programaciones de controles.
"""
from dataclasses import dataclass
from datetime import datetime, time
from typing import Optional, List

from ...domain.entities.programacion import TipoProgramacion, DiaSemana


@dataclass
class CrearProgramacionDTO:
    """DTO para crear una nueva programación"""
    control_id: int
    nombre: str
    descripcion: str
    tipo_programacion: TipoProgramacion
    activo: bool = True
    
    # Configuración de horario
    hora_ejecucion: Optional[time] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    # Para programación semanal
    dias_semana: Optional[List[DiaSemana]] = None
    
    # Para programación mensual
    dias_mes: Optional[List[int]] = None
    
    # Para programación por intervalo
    intervalo_minutos: Optional[int] = None
    
    # Metadatos
    creado_por: Optional[str] = None


@dataclass
class ActualizarProgramacionDTO:
    """DTO para actualizar una programación existente"""
    id: int
    nombre: str
    descripcion: str
    tipo_programacion: TipoProgramacion
    activo: bool
    
    # Configuración de horario
    hora_ejecucion: Optional[time] = None
    fecha_inicio: Optional[datetime] = None
    fecha_fin: Optional[datetime] = None
    
    # Para programación semanal
    dias_semana: Optional[List[DiaSemana]] = None
    
    # Para programación mensual
    dias_mes: Optional[List[int]] = None
    
    # Para programación por intervalo
    intervalo_minutos: Optional[int] = None


@dataclass
class ProgramacionResponseDTO:
    """DTO de respuesta para programaciones"""
    id: int
    control_id: int
    nombre: str
    descripcion: str
    tipo_programacion: str
    activo: bool
    
    # Configuración de horario
    hora_ejecucion: Optional[str] = None  # String format HH:MM
    fecha_inicio: Optional[str] = None    # String format ISO
    fecha_fin: Optional[str] = None       # String format ISO
    
    # Para programación semanal
    dias_semana: Optional[List[str]] = None  # Nombres de días
    
    # Para programación mensual
    dias_mes: Optional[List[int]] = None
    
    # Para programación por intervalo
    intervalo_minutos: Optional[int] = None
    
    # Control de ejecución
    ultima_ejecucion: Optional[str] = None  # String format ISO
    proxima_ejecucion: Optional[str] = None # String format ISO
    total_ejecuciones: int = 0
    
    # Descripción legible
    descripcion_programacion: str = ""
    
    # Metadatos
    fecha_creacion: Optional[str] = None
    fecha_modificacion: Optional[str] = None
    creado_por: Optional[str] = None
    
    @classmethod
    def from_entity(cls, programacion) -> 'ProgramacionResponseDTO':
        """Crea un DTO de respuesta desde una entidad Programacion"""
        return cls(
            id=programacion.id,
            control_id=programacion.control_id,
            nombre=programacion.nombre,
            descripcion=programacion.descripcion,
            tipo_programacion=programacion.tipo_programacion.value,
            activo=programacion.activo,
            hora_ejecucion=programacion.hora_ejecucion.strftime('%H:%M') if programacion.hora_ejecucion else None,
            fecha_inicio=programacion.fecha_inicio.isoformat() if programacion.fecha_inicio else None,
            fecha_fin=programacion.fecha_fin.isoformat() if programacion.fecha_fin else None,
            dias_semana=[dia.name.capitalize() for dia in programacion.dias_semana] if programacion.dias_semana else None,
            dias_mes=programacion.dias_mes,
            intervalo_minutos=programacion.intervalo_minutos,
            ultima_ejecucion=programacion.ultima_ejecucion.isoformat() if programacion.ultima_ejecucion else None,
            proxima_ejecucion=programacion.proxima_ejecucion.isoformat() if programacion.proxima_ejecucion else None,
            total_ejecuciones=programacion.total_ejecuciones,
            descripcion_programacion=programacion.obtener_descripcion_programacion(),
            fecha_creacion=programacion.fecha_creacion.isoformat() if programacion.fecha_creacion else None,
            fecha_modificacion=programacion.fecha_modificacion.isoformat() if programacion.fecha_modificacion else None,
            creado_por=programacion.creado_por
        )


@dataclass
class ListarProgramacionesResponseDTO:
    """DTO de respuesta para listado de programaciones"""
    success: bool
    data: List[ProgramacionResponseDTO]
    total: int
    activas: int
    inactivas: int
    message: str = ""


@dataclass
class EstadisticasProgramacionDTO:
    """DTO para estadísticas de programaciones"""
    control_id: Optional[int]
    control_nombre: Optional[str]
    total_programaciones: int
    activas: int
    inactivas: int
    total_ejecuciones: int
    ultima_ejecucion_general: Optional[str]
    proxima_ejecucion: Optional[str]


@dataclass
class HistorialEjecucionProgramadaDTO:
    """DTO para historial de ejecuciones programadas"""
    programacion_nombre: str
    fecha_ejecucion: str
    tipo_programacion: str
    resultado: str = "Exitosa"  # Por defecto, luego se puede expandir