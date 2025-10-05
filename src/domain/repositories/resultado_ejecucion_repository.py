"""
Repositorio abstracto para ResultadoEjecucion
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from datetime import datetime
from src.domain.entities.resultado_ejecucion import ResultadoEjecucion


class ResultadoEjecucionRepository(ABC):
    """Interface abstracta para el repositorio de resultados de ejecución"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[ResultadoEjecucion]:
        """Obtiene un resultado por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[ResultadoEjecucion]:
        """Obtiene todos los resultados"""
        pass
    
    @abstractmethod
    def obtener_por_control(self, control_id: int) -> List[ResultadoEjecucion]:
        """Obtiene todos los resultados de un control específico"""
        pass
    
    @abstractmethod
    def obtener_por_fecha_rango(
        self, 
        fecha_desde: datetime, 
        fecha_hasta: datetime
    ) -> List[ResultadoEjecucion]:
        """Obtiene resultados en un rango de fechas"""
        pass
    
    @abstractmethod
    def obtener_por_estado(self, estado: str) -> List[ResultadoEjecucion]:
        """Obtiene resultados por estado (exitoso, error, control_disparado)"""
        pass
    
    @abstractmethod
    def guardar(self, resultado: ResultadoEjecucion) -> ResultadoEjecucion:
        """Guarda un resultado de ejecución"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un resultado por su ID"""
        pass
    
    @abstractmethod
    def obtener_ultimos_por_control(self, control_id: int, limite: int = 10) -> List[ResultadoEjecucion]:
        """Obtiene los últimos N resultados de un control"""
        pass