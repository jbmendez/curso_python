"""
Entidad Referente

Representa un usuario referente para notificaciones
"""
from dataclasses import dataclass
from typing import Optional
import re


@dataclass
class Referente:
    """Entidad Referente - Representa un referente para reportes"""
    
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    path_archivos: str = ""  # Ruta donde dejar archivos de reportes
    activo: bool = True
    
    def es_email_valido(self) -> bool:
        """Valida el formato del email"""
        if not self.email:
            return False
        patron = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return bool(re.match(patron, self.email))
    
    def es_path_valido(self) -> bool:
        """Valida que el path de archivos sea válido"""
        if not self.path_archivos.strip():
            return False
        # Validación básica de path (podría ser más específica según el OS)
        return len(self.path_archivos.strip()) > 0
    
    def es_valido(self) -> bool:
        """Validación general del referente"""
        return (self.nombre and self.nombre.strip() and 
                self.es_email_valido() and 
                self.es_path_valido())
    
    def __str__(self) -> str:
        return f"Referente(nombre={self.nombre}, email={self.email})"