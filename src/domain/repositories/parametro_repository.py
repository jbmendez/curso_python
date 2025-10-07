"""
Repositorio abstracto para Parámetro
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.parametro import Parametro


class ParametroRepository(ABC):
    """Interface abstracta para el repositorio de parámetros"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Parametro]:
        """Obtiene un parámetro por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Parametro]:
        """Obtiene todos los parámetros"""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Parametro]:
        """Obtiene un parámetro por su nombre"""
        pass
    
    @abstractmethod
    def obtener_por_ids(self, ids: List[int]) -> List[Parametro]:
        """Obtiene múltiples parámetros por sus IDs"""
        pass
    
    @abstractmethod
    def obtener_por_control(self, control_id: int) -> List[Parametro]:
        """Obtiene todos los parámetros asociados a un control"""
        pass
    
    @abstractmethod
    def guardar(self, parametro: Parametro) -> Parametro:
        """Guarda un parámetro (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un parámetro por su ID"""
        pass