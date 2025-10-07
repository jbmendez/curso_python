"""
Entidad ControlReferente

Representa la asociación entre Control y Referente
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime


@dataclass
class ControlReferente:
    """Entidad ControlReferente - Representa la asociación N:M entre Control y Referente"""
    
    id: Optional[int] = None
    control_id: int = 0
    referente_id: int = 0
    activa: bool = True
    fecha_asociacion: Optional[datetime] = None
    notificar_por_email: bool = True
    notificar_por_archivo: bool = False
    observaciones: str = ""
    
    def es_valida(self) -> bool:
        """Validación de la asociación"""
        return (self.control_id > 0 and 
                self.referente_id > 0 and
                (self.notificar_por_email or self.notificar_por_archivo))
    
    def __str__(self) -> str:
        return f"ControlReferente(control_id={self.control_id}, referente_id={self.referente_id})"