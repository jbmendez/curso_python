"""
Entidad Referente

Representa un usuario referente para notificaciones
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Referente:
    """Entidad Referente - Representa un referente para notificaciones"""
    
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    carpeta_red: str = ""
    activo: bool = True
    notificar_por_email: bool = True
    notificar_por_archivo: bool = False
    
    def es_email_valido(self) -> bool:
        """Valida el formato del email"""
        if not self.email:
            return False
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, self.email))
    
    def es_carpeta_valida(self) -> bool:
        """Valida que la carpeta de red sea válida si está configurada"""
        if self.notificar_por_archivo and not self.carpeta_red.strip():
            return False
        return True
    
    def debe_notificar_email(self) -> bool:
        """Verifica si debe notificar por email"""
        return self.activo and self.notificar_por_email and self.es_email_valido()
    
    def debe_notificar_archivo(self) -> bool:
        """Verifica si debe notificar por archivo"""
        return self.activo and self.notificar_por_archivo and self.es_carpeta_valida()
    
    def __str__(self) -> str:
        return f"Referente(nombre={self.nombre}, email={self.email})"