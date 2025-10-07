"""
Repositorio abstracto para ControlReferente
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.control_referente import ControlReferente


class ControlReferenteRepository(ABC):
    """Interface abstracta para el repositorio de asociaciones Control-Referente"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[ControlReferente]:
        """Obtiene una asociación por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[ControlReferente]:
        """Obtiene todas las asociaciones"""
        pass
    
    @abstractmethod
    def obtener_por_control(self, control_id: int) -> List[ControlReferente]:
        """Obtiene todas las asociaciones de un control específico"""
        pass
    
    @abstractmethod
    def obtener_por_referente(self, referente_id: int) -> List[ControlReferente]:
        """Obtiene todas las asociaciones de un referente específico"""
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[ControlReferente]:
        """Obtiene solo las asociaciones activas"""
        pass
    
    @abstractmethod
    def existe_asociacion(self, control_id: int, referente_id: int) -> bool:
        """Verifica si existe una asociación entre un control y referente"""
        pass
    
    @abstractmethod
    def guardar(self, control_referente: ControlReferente) -> ControlReferente:
        """Guarda una asociación (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una asociación por su ID"""
        pass
    
    @abstractmethod
    def eliminar_por_control_referente(self, control_id: int, referente_id: int) -> bool:
        """Elimina una asociación específica entre control y referente"""
        pass