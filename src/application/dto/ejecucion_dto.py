"""
DTOs para la ejecución de controles
"""
from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from datetime import datetime
from src.domain.entities.resultado_ejecucion import EstadoEjecucion


@dataclass
class EjecutarControlDTO:
    """DTO para ejecutar un control"""
    control_id: int
    parametros_adicionales: Optional[Dict[str, Any]] = None
    ejecutar_solo_disparo: bool = False  # Si True, solo ejecuta la consulta de disparo
    mock_execution: bool = False  # Para testing o simulación


@dataclass
class ResultadoEjecucionResponseDTO:
    """DTO de respuesta para resultados de ejecución"""
    id: int
    control_id: int
    control_nombre: str
    fecha_ejecucion: datetime
    estado: str
    mensaje: str
    parametros_utilizados: Dict[str, Any]
    tiempo_total_ejecucion_ms: float
    total_filas_disparo: int
    total_filas_disparadas: int
    conexion_nombre: str
    
    # Detalles opcionales de consultas
    resultado_consulta_disparo: Optional[Dict[str, Any]] = None
    resultados_consultas_disparadas: Optional[List[Dict[str, Any]]] = None


@dataclass
class HistorialEjecucionDTO:
    """DTO para obtener historial de ejecuciones"""
    control_id: Optional[int] = None
    fecha_desde: Optional[datetime] = None
    fecha_hasta: Optional[datetime] = None
    estado: Optional[str] = None
    limite: int = 50
    incluir_detalles: bool = False


@dataclass
class EstadisticasEjecucionDTO:
    """DTO con estadísticas de ejecución"""
    total_ejecuciones: int
    ejecuciones_exitosas: int
    ejecuciones_con_error: int
    controles_disparados: int
    sin_datos: int
    tiempo_promedio_ejecucion_ms: float
    ultima_ejecucion: Optional[datetime] = None
    
    @property
    def tasa_exito(self) -> float:
        """Calcula la tasa de éxito en porcentaje"""
        if self.total_ejecuciones == 0:
            return 0.0
        return (self.ejecuciones_exitosas / self.total_ejecuciones) * 100


@dataclass
class ResumenControlDTO:
    """DTO con resumen de ejecución de un control específico"""
    control_id: int
    control_nombre: str
    total_ejecuciones: int
    ultima_ejecucion: Optional[datetime]
    ultimo_estado: Optional[str]
    tasa_exito: float
    tiempo_promedio_ms: float