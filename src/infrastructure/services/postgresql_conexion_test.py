"""
Implementación específica para probar conexiones PostgreSQL
"""
import time
from typing import Optional
try:
    import psycopg2
    from psycopg2 import sql, OperationalError, DatabaseError
    PSYCOPG2_DISPONIBLE = True
except ImportError:
    PSYCOPG2_DISPONIBLE = False

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class PostgreSQLConexionTest(ConexionTestService):
    """Servicio para probar conexiones PostgreSQL"""
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba una conexión PostgreSQL
        
        Args:
            conexion: Datos de la conexión a probar
            
        Returns:
            ResultadoPruebaConexion: Resultado de la prueba
        """
        if not PSYCOPG2_DISPONIBLE:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error: La librería psycopg2 no está instalada",
                detalles_error="Instalar con: pip install psycopg2-binary"
            )
        
        inicio = time.time()
        
        try:
            # Construir string de conexión
            connection_string = self._construir_connection_string(conexion)
            
            # Intentar conexión
            with psycopg2.connect(connection_string) as conn:
                with conn.cursor() as cursor:
                    # Probar con una consulta simple
                    cursor.execute("SELECT version();")
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
            
            # Categorizar errores comunes
            if "authentication failed" in error_msg.lower():
                mensaje = "Error de autenticación: Usuario o contraseña incorrectos"
            elif "could not connect to server" in error_msg.lower():
                mensaje = "Error de conexión: No se puede conectar al servidor"
            elif "database" in error_msg.lower() and "does not exist" in error_msg.lower():
                mensaje = "Error: La base de datos especificada no existe"
            elif "timeout" in error_msg.lower():
                mensaje = "Error: Tiempo de conexión agotado"
            else:
                mensaje = f"Error de conexión: {error_msg}"
            
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
                mensaje=f"Error de base de datos: {error_msg}",
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
        return ["postgresql", "postgres"]
    
    def _construir_connection_string(self, conexion: Conexion) -> str:
        """
        Construye el string de conexión para PostgreSQL
        
        Args:
            conexion: Datos de la conexión
            
        Returns:
            str: String de conexión
        """
        return (
            f"host={conexion.servidor} "
            f"port={conexion.puerto} "
            f"dbname={conexion.base_datos} "
            f"user={conexion.usuario} "
            f"password={conexion.contraseña} "
            f"connect_timeout=10"  # Timeout de 10 segundos
        )