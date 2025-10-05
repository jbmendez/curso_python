"""
Repositorio abstracto para Conexión
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.conexion import Conexion


class ConexionRepository(ABC):
    """Interface abstracta para el repositorio de conexiones"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Conexion]:
        """Obtiene una conexión por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Conexion]:
        """Obtiene todas las conexiones"""
        pass
    
    @abstractmethod
    def obtener_activas(self) -> List[Conexion]:
        """Obtiene solo las conexiones activas"""
        pass
    
    @abstractmethod
    def obtener_por_nombre(self, nombre: str) -> Optional[Conexion]:
        """Obtiene una conexión por su nombre"""
        pass
    
    @abstractmethod
    def guardar(self, conexion: Conexion) -> Conexion:
        """Guarda una conexión (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina una conexión por su ID"""
        pass
    
    @abstractmethod
    def probar_conexion(self, conexion: Conexion) -> bool:
        """Prueba si la conexión funciona correctamente"""
        pass