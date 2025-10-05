"""
Repositorio abstracto para Control
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.control import Control


class ControlRepository(ABC):
    """Interface abstracta para el repositorio de controles"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Control]:
        """Obtiene un control por su ID con todas sus relaciones cargadas"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Control]:
        """Obtiene todos los controles"""
        pass
    
    @abstractmethod
    def obtener_activos(self) -> List[Control]:
        """Obtiene solo los controles activos"""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Control]:
        """Obtiene un control por su nombre"""
        pass
    
    @abstractmethod
    def guardar(self, control: Control) -> Control:
        """Guarda un control (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un control por su ID"""
        pass
    
    @abstractmethod
    def cargar_relaciones(self, control: Control) -> Control:
        """Carga todas las relaciones de un control (conexión, consultas, etc.)"""
        pass