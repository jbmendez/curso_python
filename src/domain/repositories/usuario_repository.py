"""
Repositorio abstracto para Usuario

En Clean Architecture, los repositorios definen interfaces (contratos)
para el acceso a datos, pero no implementan la lógica de persistencia.
La implementación real va en la capa de infrastructure.
"""
from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.usuario import Usuario


class UsuarioRepository(ABC):
    """Interface abstracta para el repositorio de usuarios"""
    
    @abstractmethod
    def obtener_por_id(self, id: int) -> Optional[Usuario]:
        """Obtiene un usuario por su ID"""
        pass
    
    @abstractmethod
    def obtener_todos(self) -> List[Usuario]:
        """Obtiene todos los usuarios"""
        pass
    
    @abstractmethod
    def guardar(self, usuario: Usuario) -> Usuario:
        """Guarda un usuario (crear o actualizar)"""
        pass
    
    @abstractmethod
    def eliminar(self, id: int) -> bool:
        """Elimina un usuario por su ID"""
        pass
    
    @abstractmethod
    def obtener_por_email(self, email: str) -> Optional[Usuario]:
        """Obtiene un usuario por su email"""
        pass