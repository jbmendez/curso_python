"""
Controlador para operaciones de conexión
"""
from typing import Dict, Any
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.use_cases.actualizar_conexion_use_case import ActualizarConexionUseCase
from src.application.use_cases.listar_conexiones_use_case import ListarConexionesUseCase
from src.application.dto.conexion_dto import CrearConexionDTO
from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestFactory


class ConexionController:
    """Controlador para endpoints de conexión"""
    
    def __init__(
        self, 
        crear_conexion_use_case: CrearConexionUseCase,
        listar_conexiones_use_case: ListarConexionesUseCase = None,
        actualizar_conexion_use_case: ActualizarConexionUseCase = None
    ):
        self._crear_conexion_use_case = crear_conexion_use_case
        self._listar_conexiones_use_case = listar_conexiones_use_case
        self._actualizar_conexion_use_case = actualizar_conexion_use_case
    
    def obtener_todas(self) -> Dict[str, Any]:
        """Obtiene todas las conexiones para la interfaz GUI"""
        try:
            if self._listar_conexiones_use_case is None:
                # Fallback si no hay caso de uso disponible
                return {
                    'success': True,
                    'data': [],
                    'status': 200,
                    'message': 'Caso de uso de listar conexiones no disponible'
                }
            
            conexiones = self._listar_conexiones_use_case.ejecutar(solo_activas=False)
            
            # Convertir a formato de respuesta para la GUI
            conexiones_data = []
            for conexion in conexiones:
                conexion_data = {
                    'id': conexion.id,
                    'nombre': conexion.nombre,
                    'motor': conexion.tipo_motor,
                    'servidor': conexion.servidor,
                    'puerto': conexion.puerto,
                    'base_datos': conexion.base_datos,
                    'usuario': conexion.usuario,
                    'activa': conexion.activa,
                }
                conexiones_data.append(conexion_data)
            
            return {
                'success': True,
                'data': conexiones_data,
                'status': 200,
                'message': f'Se encontraron {len(conexiones_data)} conexiones'
            }
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'status': 500
            }
    
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
    
    def actualizar_conexion(
        self,
        conexion_id: int,
        nombre: str,
        motor: str,
        servidor: str,
        puerto: int,
        base_datos: str,
        usuario: str,
        password: str,
        activa: bool = True
    ) -> Dict[str, Any]:
        """
        Actualiza una conexión existente
        
        Args:
            conexion_id: ID de la conexión a actualizar
            nombre: Nombre de la conexión
            motor: Tipo de motor de base de datos
            servidor: Servidor de la base de datos
            puerto: Puerto de conexión
            base_datos: Nombre de la base de datos
            usuario: Usuario para la conexión
            password: Contraseña para la conexión
            
        Returns:
            dict: Respuesta con los datos de la conexión actualizada
        """
        try:
            if self._actualizar_conexion_use_case is None:
                return {
                    "success": False,
                    "error": "Funcionalidad de actualización no disponible"
                }
            
            dto = CrearConexionDTO(
                nombre=nombre,
                motor=motor,
                servidor=servidor,
                puerto=puerto,
                base_datos=base_datos,
                usuario=usuario,
                password=password,
                activa=activa
            )
            
            resultado = self._actualizar_conexion_use_case.ejecutar(conexion_id, dto)
            
            return {
                "success": True,
                "data": {
                    "id": resultado.id,
                    "nombre": resultado.nombre,
                    "motor": resultado.tipo_motor,
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
    
    def probar_conexion(
        self,
        motor: str,
        servidor: str,
        puerto: int,
        base_datos: str,
        usuario: str,
        password: str
    ) -> Dict[str, Any]:
        """
        Prueba una conexión sin guardarla
        
        Args:
            motor: Tipo de motor de base de datos
            servidor: Servidor de la base de datos
            puerto: Puerto de conexión
            base_datos: Nombre de la base de datos
            usuario: Usuario para la conexión
            password: Contraseña para la conexión
            
        Returns:
            dict: Respuesta con el resultado de la prueba
        """
        try:
            # Crear una entidad Conexion temporal para la prueba
            conexion_temporal = Conexion(
                id=None,
                nombre="prueba_temporal",
                base_datos=base_datos,
                servidor=servidor,
                puerto=puerto,
                usuario=usuario,
                contraseña=password,
                tipo_motor=motor,
                activa=True
            )
            
            # Obtener el servicio de prueba apropiado
            servicio_test = ConexionTestFactory.obtener_servicio(motor)
            
            if not servicio_test:
                return {
                    "success": False,
                    "error": f"Motor de base de datos '{motor}' no soportado para pruebas de conexión"
                }
            
            # Realizar la prueba
            resultado = servicio_test.probar_conexion(conexion_temporal)
            
            if resultado.exitosa:
                return {
                    "success": True,
                    "data": {
                        "mensaje": resultado.mensaje,
                        "tiempo_respuesta": resultado.tiempo_respuesta,
                        "version_servidor": resultado.version_servidor
                    }
                }
            else:
                return {
                    "success": False,
                    "error": resultado.mensaje,
                    "detalles": resultado.detalles_error
                }
                
        except Exception as e:
            return {
                "success": False,
                "error": f"Error inesperado al probar conexión: {str(e)}"
            }