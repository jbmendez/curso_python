"""
Implementación específica para probar conexiones SQLite
"""
import time
import sqlite3
import os
from typing import Optional

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class SQLiteConexionTest(ConexionTestService):
    """Servicio para probar conexiones SQLite"""
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba una conexión SQLite
        
        Args:
            conexion: Datos de la conexión a probar
            
        Returns:
            ResultadoPruebaConexion: Resultado de la prueba
        """
        inicio = time.time()
        
        try:
            # Para SQLite, el "servidor" es realmente la ruta del archivo
            # y base_datos puede ser ignorado o usado como parte de la ruta
            ruta_archivo = self._construir_ruta_archivo(conexion)
            
            # Verificar si el directorio padre existe (para archivos nuevos)
            directorio = os.path.dirname(ruta_archivo)
            if directorio and not os.path.exists(directorio):
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje=f"Error: El directorio {directorio} no existe",
                    tiempo_respuesta=time.time() - inicio,
                    detalles_error=f"Directorio no encontrado: {directorio}"
                )
            
            # Intentar conexión
            with sqlite3.connect(ruta_archivo, timeout=10) as conn:
                cursor = conn.cursor()
                
                # Probar con una consulta simple
                cursor.execute("SELECT sqlite_version();")
                version = cursor.fetchone()[0]
                
                # Verificar si la base de datos tiene tablas
                cursor.execute("SELECT count(*) FROM sqlite_master WHERE type='table';")
                num_tablas = cursor.fetchone()[0]
                
                tiempo_respuesta = time.time() - inicio
                
                # Determinar si el archivo existía antes
                existe_archivo = os.path.exists(ruta_archivo)
                tamaño_archivo = os.path.getsize(ruta_archivo) if existe_archivo else 0
                
                mensaje_adicional = f" ({num_tablas} tablas, {tamaño_archivo} bytes)"
                
                return ResultadoPruebaConexion(
                    exitosa=True,
                    mensaje=f"Conexión SQLite exitosa{mensaje_adicional}",
                    tiempo_respuesta=tiempo_respuesta,
                    version_servidor=f"SQLite {version}"
                )
                
        except sqlite3.OperationalError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            # Categorizar errores comunes de SQLite
            if "database is locked" in error_msg.lower():
                mensaje = "Error: La base de datos SQLite está bloqueada por otro proceso"
            elif "no such file" in error_msg.lower():
                mensaje = "Error: Archivo de base de datos SQLite no encontrado"
            elif "permission denied" in error_msg.lower():
                mensaje = "Error: Sin permisos para acceder al archivo SQLite"
            elif "disk full" in error_msg.lower():
                mensaje = "Error: Disco lleno, no se puede escribir en SQLite"
            elif "corrupted" in error_msg.lower() or "malformed" in error_msg.lower():
                mensaje = "Error: Archivo SQLite corrupto o malformado"
            else:
                mensaje = f"Error SQLite: {error_msg}"
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=mensaje,
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=error_msg
            )
            
        except sqlite3.DatabaseError as e:
            tiempo_respuesta = time.time() - inicio
            error_msg = str(e).strip()
            
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error de base de datos SQLite: {error_msg}",
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
        return ["sqlite", "sqlite3"]
    
    def _construir_ruta_archivo(self, conexion: Conexion) -> str:
        """
        Construye la ruta del archivo SQLite
        
        Para SQLite interpretamos los campos así:
        - servidor: ruta del archivo o directorio
        - base_datos: nombre del archivo (si servidor es directorio)
        - Si servidor ya incluye .db, se usa tal como está
        
        Args:
            conexion: Datos de la conexión
            
        Returns:
            str: Ruta completa al archivo SQLite
        """
        servidor = conexion.servidor.strip()
        base_datos = conexion.base_datos.strip()
        
        # Si servidor ya tiene extensión de base de datos, usarlo tal como está
        if servidor.lower().endswith(('.db', '.sqlite', '.sqlite3')):
            return servidor
        
        # Si base_datos está vacío, asumir que servidor es el archivo completo
        if not base_datos:
            # Si no tiene extensión, agregar .db
            if not servidor.lower().endswith(('.db', '.sqlite', '.sqlite3')):
                return f"{servidor}.db"
            return servidor
        
        # Combinar servidor (directorio) con base_datos (archivo)
        if not base_datos.lower().endswith(('.db', '.sqlite', '.sqlite3')):
            base_datos = f"{base_datos}.db"
        
        return os.path.join(servidor, base_datos)