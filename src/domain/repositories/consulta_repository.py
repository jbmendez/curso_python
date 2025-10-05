"""
Repositorio abstracto para Consulta
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.consulta import Consulta


class ConsultaRepository(ABC):
    """Interface abstracta para el repositorio de consultas"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Consulta]:
        """Obtiene una consulta por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Consulta]:
        """Obtiene todas las consultas"""
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Consulta]:
        """Obtiene solo las consultas activas"""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Consulta]:
        """Obtiene una consulta por su nombre"""
        pass
    
    @abstractmethod
    def obtener_por_ids(self, ids: List[int]) -> List[Consulta]:
        """Obtiene múltiples consultas por sus IDs"""
        pass
    
    @abstractmethod
    def guardar(self, consulta: Consulta) -> Consulta:
        """Guarda una consulta (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una consulta por su ID"""
        pass