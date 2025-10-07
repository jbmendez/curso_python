"""
Entidad ConsultaControl

Representa la asociación entre Control y Consulta
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ConsultaControl:
    """Entidad que representa la asociación entre Control y Consulta"""
    
    id: Optional[int] = None
    control_id: int = 0
    consulta_id: int = 0
    es_disparo: bool = False  # Indica si esta consulta es la que dispara el control
    orden: int = 1  # Orden de ejecución de la consulta dentro del control
    activa: bool = True  # Si esta asociación está activa
    fecha_asociacion: Optional[datetime] = None
    
    def __post_init__(self):
        """Inicialización después del constructor"""
        if self.fecha_asociacion is None:
            self.fecha_asociacion = datetime.now()
    
    def es_valida(self) -> bool:
        """Validación de la asociación"""
        if self.control_id <= 0:
            return False
        if self.consulta_id <= 0:
            return False
        if self.orden < 1:
            return False
        return True
    
    def __str__(self) -> str:
        disparo_text = " (DISPARO)" if self.es_disparo else ""
        return f"ConsultaControl(control_id={self.control_id}, consulta_id={self.consulta_id}, orden={self.orden}{disparo_text})"