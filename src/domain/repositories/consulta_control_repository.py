"""
Repositorio para la entidad ConsultaControl

Define las operaciones de persistencia para las asociaciones Control-Consulta
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.consulta_control import ConsultaControl


class ConsultaControlRepository(ABC):
    """Interfaz del repositorio para ConsultaControl"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[ConsultaControl]:
        """Obtiene una asociación por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_control(self, control_id: int) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones de un control específico"""
        pass
    
    @abstractmethod
    def obtener_por_consulta(self, consulta_id: int) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones de una consulta específica"""
        pass
    
    @abstractmethod
    def obtener_disparo_por_control(self, control_id: int) -> Optional[ConsultaControl]:
        """Obtiene la consulta de disparo de un control específico"""
        pass
    
    @abstractmethod
    def guardar(self, asociacion: ConsultaControl) -> ConsultaControl:
        """Guarda una asociación (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una asociación por su ID"""
        pass
    
    @abstractmethod
    def eliminar_por_control(self, control_id: int) -> bool:
        """Elimina todas las asociaciones de un control"""
        pass
    
    @abstractmethod
    def eliminar_por_consulta(self, consulta_id: int) -> bool:
        """Elimina todas las asociaciones de una consulta"""
        pass
    
    @abstractmethod
    def establecer_consulta_disparo(self, control_id: int, consulta_id: int) -> bool:
        """Establece una consulta como la de disparo para un control"""
        pass
    
    @abstractmethod
    def obtener_todas(self) -> List[ConsultaControl]:
        """Obtiene todas las asociaciones"""
        pass