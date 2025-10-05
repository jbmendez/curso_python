"""
Repositorio abstracto para Referente
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.referente import Referente


class ReferenteRepository(ABC):
    """Interface abstracta para el repositorio de referentes"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Referente]:
        """Obtiene un referente por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Referente]:
        """Obtiene todos los referentes"""
        pass
    
    @abstractmethod
    def obtener_activos(self) -> List[Referente]:
        """Obtiene solo los referentes activos"""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Referente]:
        """Obtiene un referente por su email"""
        pass
    
    @abstractmethod
    def obtener_por_ids(self, ids: List[int]) -> List[Referente]:
        """Obtiene múltiples referentes por sus IDs"""
        pass
    
    @abstractmethod
    def guardar(self, referente: Referente) -> Referente:
        """Guarda un referente (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un referente por su ID"""
        pass