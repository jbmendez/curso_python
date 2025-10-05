"""
Entidad Parámetro

Representa un parámetro que puede ser utilizado en las consultas SQL
"""
from dataclasses import dataclass
from typing import Optional
from enum import Enum


class TipoParametro(Enum):
    """Tipos de parámetros disponibles"""
    STRING = "string"
    INTEGER = "integer"
    FLOAT = "float"
    BOOLEAN = "boolean"
    DATE = "date"
    DATETIME = "datetime"


@dataclass
class Parametro:
    """Entidad Parámetro - Representa un parámetro de control"""
    
    id: Optional[int] = None
    nombre: str = ""
    tipo: TipoParametro = TipoParametro.STRING
    descripcion: str = ""
    valor_por_defecto: Optional[str] = None
    obligatorio: bool = True
    
    def es_nombre_valido(self) -> bool:
        """Valida que el nombre del parámetro sea válido"""
        return bool(self.nombre and self.nombre.strip() and self.nombre.isidentifier())
    
    def validar_valor(self, valor: str) -> bool:
        """Valida si un valor es compatible con el tipo del parámetro"""
        if not valor and self.obligatorio:
            return False
            
        if not valor and not self.obligatorio:
            return True
            
        try:
            if self.tipo == TipoParametro.INTEGER:
                int(valor)
            elif self.tipo == TipoParametro.FLOAT:
                float(valor)
            elif self.tipo == TipoParametro.BOOLEAN:
                if valor.lower() not in ['true', 'false', '1', '0']:
                    return False
            # Para DATE y DATETIME podríamos agregar validaciones adicionales
            return True
        except (ValueError, AttributeError):
            return False
    
    def __str__(self) -> str:
        return f"Parametro(nombre={self.nombre}, tipo={self.tipo.value})"