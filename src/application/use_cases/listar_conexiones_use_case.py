"""
Caso de uso para listar conexiones
"""
from typing import List
from src.domain.entities.conexion import Conexion
from src.domain.repositories.conexion_repository import ConexionRepository


class ListarConexionesUseCase:
    """Caso de uso para obtener lista de conexiones"""
    
    def __init__(self, conexion_repository: ConexionRepository):
        self._conexion_repository = conexion_repository
    
    def ejecutar(self, solo_activas: bool = False) -> List[Conexion]:
        """
        Ejecuta el caso de uso para listar conexiones
        
        Args:
            solo_activas: Si True, solo devuelve conexiones activas
            
        Returns:
            List[Conexion]: Lista de conexiones
        """
        if solo_activas:
            return self._conexion_repository.obtener_activas()
        else:
            return self._conexion_repository.obtener_todos()