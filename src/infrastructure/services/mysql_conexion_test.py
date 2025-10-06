"""
Implementación específica para probar conexiones MySQL
"""
import time
from typing import Optional
try:
    import pymysql
    from pymysql import OperationalError, DatabaseError, InternalError
    PYMYSQL_DISPONIBLE = True
except ImportError:
    PYMYSQL_DISPONIBLE = False

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class MySQLConexionTest(ConexionTestService):
    """Servicio para probar conexiones MySQL"""
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba una conexión MySQL
        
        Args:
            conexion: Datos de la conexión a probar
            
        Returns:
            ResultadoPruebaConexion: Resultado de la prueba
        """
        if not PYMYSQL_DISPONIBLE:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error: La librería pymysql no está instalada",
                detalles_error="Instalar con: pip install pymysql"
            )
        
        inicio = time.time()
        
        try:
            # Intentar conexión
            with pymysql.connect(
                host=conexion.servidor,
                port=conexion.puerto,
                user=conexion.usuario,
                password=conexion.contraseña,
                database=conexion.base_datos,
                connect_timeout=10,
                charset='utf8mb4'
            ) as conn:
                with conn.cursor() as cursor:
                    # Probar con una consulta simple
                    cursor.execute("SELECT VERSION();")
                    version = cursor.fetchone()[0]
                    
                    tiempo_respuesta = time.time() - inicio
                    
                    return ResultadoPruebaConexion(
                        exitosa=True,
                        mensaje="Conexión exitosa",
                        tiempo_respuesta=tiempo_respuesta,
                        version_servidor=version
                    )
                    
        except OperationalError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            # Categorizar errores comunes de MySQL
            if "access denied" in error_msg.lower():
                mensaje = "Error de autenticación: Usuario o contraseña incorrectos"
            elif "can't connect" in error_msg.lower() or "connection refused" in error_msg.lower():
                mensaje = "Error de conexión: No se puede conectar al servidor MySQL"
            elif "unknown database" in error_msg.lower():
                mensaje = "Error: La base de datos especificada no existe"
            elif "timeout" in error_msg.lower():
                mensaje = "Error: Tiempo de conexión agotado"
            elif "host" in error_msg.lower() and "not allowed" in error_msg.lower():
                mensaje = "Error: El host no tiene permisos para conectarse"
            else:
                mensaje = f"Error de conexión MySQL: {error_msg}"
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=mensaje,
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
            
        except DatabaseError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error de base de datos MySQL: {error_msg}",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
            
        except InternalError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error interno de MySQL: {error_msg}",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
            
        except Exception as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error inesperado: {error_msg}",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
    
    def tipos_soportados(self) -> list[str]:
        """Retorna los tipos de motor soportados"""
        return ["mysql", "mariadb"]