"""
Ejemplo de entidad de dominio - Usuario

En Clean Architecture, las entidades representan los objetos de negocio
más importantes y contienen las reglas de negocio fundamentales.
"""
from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Usuario:
    """Entidad Usuario - Representa un usuario del sistema"""
    
    id: Optional[int] = None
    nombre: str = ""
    email: str = ""
    fecha_creacion: Optional[datetime] = None
    activo: bool = True
    
    def activar(self) -> None:
        """Regla de negocio: activar usuario"""
        self.activo = True
    
    def desactivar(self) -> None:
        """Regla de negocio: desactivar usuario"""
        self.activo = False
    
    def es_email_valido(self) -> bool:
        """Regla de negocio: validar formato de email"""
        return "@" in self.email and "." in self.email
    
    def __str__(self) -> str:
        return f"Usuario(id={self.id}, nombre={self.nombre}, email={self.email})"