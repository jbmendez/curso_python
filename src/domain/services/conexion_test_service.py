"""
Servicios para probar conexiones de base de datos

Este módulo contiene la interfaz abstracta y las implementaciones
específicas para probar conexiones a diferentes tipos de bases de datos.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Dict, Any, Optional
from src.domain.entities.conexion import Conexion


@dataclass
class ResultadoPruebaConexion:
    """Resultado de una prueba de conexión"""
    exitosa: bool
    mensaje: str
    tiempo_respuesta: Optional[float] = None  # en segundos
    version_servidor: Optional[str] = None
    detalles_error: Optional[str] = None


class ConexionTestService(ABC):
    """Interfaz abstracta para servicios de prueba de conexión"""
    
    @abstractmethod
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba una conexión a la base de datos
        
        Args:
            conexion: Datos de la conexión a probar
            
        Returns:
            ResultadoPruebaConexion: Resultado de la prueba
        """
        pass
    
    @abstractmethod
    def tipos_soportados(self) -> list[str]:
        """
        Retorna la lista de tipos de motor que soporta este servicio
        
        Returns:
            list: Lista de tipos de motor soportados
        """
        pass


class ConexionTestFactory:
    """Factory para crear servicios de prueba de conexión según el tipo de motor"""
    
    _servicios: Dict[str, ConexionTestService] = {}
    
    @classmethod
    def registrar_servicio(cls, tipos_motor: list[str], servicio: ConexionTestService):
        """Registra un servicio para uno o más tipos de motor"""
        for tipo in tipos_motor:
            cls._servicios[tipo.lower()] = servicio
    
    @classmethod
    def obtener_servicio(cls, tipo_motor: str) -> Optional[ConexionTestService]:
        """Obtiene el servicio apropiado para un tipo de motor"""
        return cls._servicios.get(tipo_motor.lower())
    
    @classmethod
    def tipos_soportados(cls) -> list[str]:
        """Retorna todos los tipos de motor soportados"""
        return list(cls._servicios.keys())