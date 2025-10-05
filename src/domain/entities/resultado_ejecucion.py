"""
Entidad ResultadoEjecucion

Representa el resultado de ejecutar un control SQL
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional, List, Dict, Any
from enum import Enum


class EstadoEjecucion(Enum):
    """Estados posibles de una ejecución"""
    EXITOSO = "exitoso"
    ERROR = "error"
    CONTROL_DISPARADO = "control_disparado"
    SIN_DATOS = "sin_datos"


@dataclass
class ResultadoConsulta:
    """Resultado de una consulta individual"""
    consulta_id: int
    consulta_nombre: str
    sql_ejecutado: str
    filas_afectadas: int
    datos: List[Dict[str, Any]] = field(default_factory=list)
    tiempo_ejecucion_ms: float = 0.0
    error: Optional[str] = None


@dataclass
class ResultadoEjecucion:
    """Entidad ResultadoEjecucion - Representa el resultado de ejecutar un control"""
    
    id: Optional[int] = None
    control_id: int = 0
    control_nombre: str = ""
    fecha_ejecucion: Optional[datetime] = None
    estado: EstadoEjecucion = EstadoEjecucion.EXITOSO
    mensaje: str = ""
    
    # Parámetros utilizados en la ejecución
    parametros_utilizados: Dict[str, str] = field(default_factory=dict)
    
    # Resultados de consultas
    resultado_consulta_disparo: Optional[ResultadoConsulta] = None
    resultados_consultas_disparadas: List[ResultadoConsulta] = field(default_factory=list)
    
    # Métricas
    tiempo_total_ejecucion_ms: float = 0.0
    total_filas_disparo: int = 0
    total_filas_disparadas: int = 0
    
    # Información de la conexión utilizada
    conexion_id: int = 0
    conexion_nombre: str = ""
    
    def fue_exitoso(self) -> bool:
        """Indica si la ejecución fue exitosa"""
        return self.estado == EstadoEjecucion.EXITOSO
    
    def hubo_error(self) -> bool:
        """Indica si hubo algún error en la ejecución"""
        return self.estado == EstadoEjecucion.ERROR
    
    def control_fue_disparado(self) -> bool:
        """Indica si el control fue disparado (encontró problemas)"""
        return self.estado == EstadoEjecucion.CONTROL_DISPARADO
    
    def obtener_resumen(self) -> str:
        """Obtiene un resumen textual del resultado"""
        if self.hubo_error():
            return f"ERROR: {self.mensaje}"
        elif self.control_fue_disparado():
            return f"CONTROL DISPARADO: {self.total_filas_disparo} filas en disparo, {self.total_filas_disparadas} filas en consultas"
        else:
            return f"CONTROL OK: Sin problemas detectados"
    
    def agregar_resultado_consulta_disparada(self, resultado: ResultadoConsulta) -> None:
        """Agrega el resultado de una consulta disparada"""
        self.resultados_consultas_disparadas.append(resultado)
        self.total_filas_disparadas += resultado.filas_afectadas
    
    def __str__(self) -> str:
        return f"ResultadoEjecucion(control={self.control_nombre}, estado={self.estado.value})"