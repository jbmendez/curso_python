"""
Implementación específica para probar conexiones SQL Server
"""
import time
from typing import Optional
try:
    import pyodbc
    PYODBC_DISPONIBLE = True
except ImportError:
    PYODBC_DISPONIBLE = False

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class SQLServerConexionTest(ConexionTestService):
    """Servicio para probar conexiones SQL Server"""
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba una conexión SQL Server
        
        Args:
            conexion: Datos de la conexión a probar
            
        Returns:
            ResultadoPruebaConexion: Resultado de la prueba
        """
        if not PYODBC_DISPONIBLE:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error: La librería pyodbc no está instalada",
                detalles_error="Instalar con: pip install pyodbc"
            )
        
        inicio = time.time()
        
        try:
            # Construir string de conexión para SQL Server
            connection_string = self._construir_connection_string(conexion)
            
            # Intentar conexión
            with pyodbc.connect(connection_string, timeout=10) as conn:
                with conn.cursor() as cursor:
                    # Probar con una consulta simple
                    cursor.execute("SELECT @@VERSION;")
                    version = cursor.fetchone()[0]
                    
                    tiempo_respuesta = time.time() - inicio
                    
                    return ResultadoPruebaConexion(
                        exitosa=True,
                        mensaje="Conexión exitosa",
                        tiempo_respuesta=tiempo_respuesta,
                        version_servidor=version.split('\n')[0] if version else "SQL Server"
                    )
                    
        except pyodbc.OperationalError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            # Categorizar errores comunes de SQL Server
            if "login failed" in error_msg.lower():
                mensaje = "Error de autenticación: Usuario o contraseña incorrectos"
            elif "server not found" in error_msg.lower() or "network-related" in error_msg.lower():
                mensaje = "Error de conexión: No se puede conectar al servidor SQL Server"
            elif "cannot open database" in error_msg.lower():
                mensaje = "Error: No se puede abrir la base de datos especificada"
            elif "timeout" in error_msg.lower():
                mensaje = "Error: Tiempo de conexión agotado"
            elif "driver" in error_msg.lower():
                mensaje = "Error: Driver ODBC no encontrado o no compatible"
            else:
                mensaje = f"Error de conexión SQL Server: {error_msg}"
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=mensaje,
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
            
        except pyodbc.DatabaseError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error de base de datos SQL Server: {error_msg}",
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
        return ["sqlserver", "mssql"]
    
    def _construir_connection_string(self, conexion: Conexion) -> str:
        """
        Construye el string de conexión para SQL Server
        
        Args:
            conexion: Datos de la conexión
            
        Returns:
            str: String de conexión ODBC
        """
        # Usar SQL Server Native Client si está disponible, sino ODBC Driver
        drivers = [
            "ODBC Driver 17 for SQL Server",
            "ODBC Driver 13 for SQL Server", 
            "SQL Server Native Client 11.0",
            "SQL Server"
        ]
        
        # Intentar encontrar un driver disponible
        available_drivers = pyodbc.drivers()
        driver = None
        
        for d in drivers:
            if d in available_drivers:
                driver = d
                break
        
        if not driver:
            # Fallback al driver genérico
            driver = "SQL Server"
        
        connection_string = (
            f"DRIVER={{{driver}}};"
            f"SERVER={conexion.servidor},{conexion.puerto};"
            f"DATABASE={conexion.base_datos};"
            f"UID={conexion.usuario};"
            f"PWD={conexion.contraseña};"
            f"Trusted_Connection=no;"
            f"Connection Timeout=10;"
        )
        
        return connection_string