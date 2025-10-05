"""
Controlador para operaciones de conexión
"""
from typing import Dict, Any
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.dto.conexion_dto import CrearConexionDTO


class ConexionController:
    """Controlador para endpoints de conexión"""
    
    def __init__(self, crear_conexion_use_case: CrearConexionUseCase):
        self._crear_conexion_use_case = crear_conexion_use_case
    
    def crear_conexion(
        self,
        nombre: str,
        motor: str,
        servidor: str,
        puerto: int,
        base_datos: str,
        usuario: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Crea una nueva conexión
        
        Args:
            nombre: Nombre de la conexión
            motor: Tipo de motor de base de datos
            servidor: Servidor de la base de datos
            puerto: Puerto de conexión
            base_datos: Nombre de la base de datos
            usuario: Usuario para la conexión
            password: Contraseña para la conexión
            
        Returns:
            dict: Respuesta con los datos de la conexión creada
        """
        try:
            dto = CrearConexionDTO(
                nombre=nombre,
                motor=motor,
                servidor=servidor,
                puerto=puerto,
                base_datos=base_datos,
                usuario=usuario,
                password=password
            )
            
            resultado = self._crear_conexion_use_case.ejecutar(dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "motor": resultado.motor,
                    "servidor": resultado.servidor,
                    "puerto": resultado.puerto,
                    "base_datos": resultado.base_datos,
                    "usuario": resultado.usuario,
                    "activa": resultado.activa
                }
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }