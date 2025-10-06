"""
Servicio de prueba de conexión para IBM i Series usando JayDeBeDB (JDBC).
"""
from typing import Dict, Any
import time
try:
    import jaydebeapi
    JAYDEBEAPI_DISPONIBLE = True
except ImportError:
    JAYDEBEAPI_DISPONIBLE = False

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class IBMiSeriesJDBCConexionTest(ConexionTestService):
    """Servicio para probar conexiones a IBM i Series usando JDBC (JayDeBeDB)."""
    
    def tipos_soportados(self) -> list:
        """Retorna los tipos de base de datos soportados por este servicio."""
        return ["IBM i Series JDBC", "AS/400 JDBC", "iSeries JDBC", "IBM i JDBC"]
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba la conexión a IBM i Series usando JDBC.
        
        Args:
            conexion: Entidad de conexión con los datos necesarios
                
        Returns:
            ResultadoPruebaConexion con el resultado de la prueba
        """
        if not JAYDEBEAPI_DISPONIBLE:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error: La librería jaydebeapi no está instalada",
                detalles_error="Instalar con: pip install jaydebeapi"
            )
        
        inicio = time.time()
        
        try:
            # Extraer parámetros de la entidad conexion
            servidor = conexion.servidor or ''
            puerto = conexion.puerto or 8471  # Puerto por defecto para IBM i
            usuario = conexion.usuario or ''
            password = conexion.contraseña or ''
            base_datos = conexion.base_datos or ''
            
            # Validaciones básicas
            if not servidor:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje="El servidor es requerido",
                    detalles_error="Parámetro 'servidor' vacío o no proporcionado"
                )
            
            if not usuario:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje="El usuario es requerido",
                    detalles_error="Parámetro 'usuario' vacío o no proporcionado"
                )
            
            # Verificar si existe el driver JAR
            jar_path = self._encontrar_driver_jar()
            if not jar_path:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje="No se encontró el driver JDBC para IBM i Series",
                    detalles_error=self._obtener_instrucciones_driver()
                )
            
            # Construir URL de conexión JDBC
            jdbc_url = self._construir_jdbc_url(servidor, puerto, base_datos)
            print(f"🔧 JDBC URL construida: {jdbc_url}")
            print(f"📁 JAR path: {jar_path}")
            print(f"👤 Usuario: {usuario}")
            print(f"🖥️ Servidor: {servidor}:{puerto}")
            
            # Intentar conexión
            print("🔄 Estableciendo conexión JDBC...")
            connection = jaydebeapi.connect(
                "com.ibm.as400.access.AS400JDBCDriver",
                jdbc_url,
                [usuario, password],
                jar_path
            )
            print("✅ Conexión JDBC establecida!")
            
            # Ejecutar consulta de prueba
            print("🔄 Ejecutando consulta de prueba...")
            cursor = connection.cursor()
            cursor.execute("SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_USER FROM SYSIBM.SYSDUMMY1")
            resultado = cursor.fetchone()
            print(f"✅ Resultado consulta: {resultado}")
            
            fecha_actual = resultado[0] if resultado else "N/A"
            hora_actual = resultado[1] if resultado else "N/A"
            usuario_actual = resultado[2] if resultado else "N/A"
            
            # Obtener información adicional del sistema
            info_sistema = self._obtener_info_sistema_jdbc(cursor)
            
            cursor.close()
            connection.close()
            print("✅ Conexión cerrada correctamente")
            
            tiempo_respuesta = time.time() - inicio
            
            return ResultadoPruebaConexion(
                exitosa=True,
                mensaje=f"Conexión JDBC exitosa a IBM i Series {servidor}",
                tiempo_respuesta=tiempo_respuesta,
                version_servidor=f"JDBC Driver - Usuario: {usuario_actual}",
                detalles_error=f"Info: Fecha: {fecha_actual}, Hora: {hora_actual}, {info_sistema}"
            )
                    
        except Exception as e:
            tiempo_respuesta = time.time() - inicio
            return self._manejar_error_jdbc(e, servidor, tiempo_respuesta)
    
    def _encontrar_driver_jar(self) -> str:
        """Busca el archivo JAR del driver JDBC de IBM i Series."""
        import os
        
        # Rutas comunes donde puede estar el driver
        posibles_rutas = [
            # Ruta relativa en el proyecto
            "drivers/jt400.jar",
            "lib/jt400.jar",
            "jdbc/jt400.jar",
            
            # Rutas comunes en Windows
            "C:/IBM/JTOpen/lib/jt400.jar",
            "C:/Program Files/IBM/Java/jt400/lib/jt400.jar",
            "C:/jt400/lib/jt400.jar",
            
            # Rutas comunes en sistemas Unix
            "/opt/ibm/jt400/lib/jt400.jar",
            "/usr/local/lib/jt400.jar",
            "/home/*/jt400/lib/jt400.jar",
            
            # Variable de entorno
            os.environ.get("JT400_JAR", "")
        ]
        
        for ruta in posibles_rutas:
            if ruta and os.path.exists(ruta):
                return ruta
        
        return ""
    
    def _obtener_instrucciones_driver(self) -> str:
        """Retorna instrucciones para obtener el driver JDBC."""
        return (
            "Para conectar a IBM i Series via JDBC necesitas:\n"
            "1. Descargar JT400.jar de IBM (gratis)\n"
            "2. Colocarlo en una de estas rutas:\n"
            "   - drivers/jt400.jar (recomendado)\n"
            "   - C:/IBM/JTOpen/lib/jt400.jar\n"
            "3. O definir variable JT400_JAR con la ruta completa\n"
            "Descarga: https://sourceforge.net/projects/jt400/"
        )
    
    def _construir_jdbc_url(self, servidor: str, puerto: int, base_datos: str = "") -> str:
        """Construye la URL de conexión JDBC para IBM i Series - Versión simplificada."""
        
        # URL base SIN puerto y SIN bibliotecas problemáticas
        jdbc_url = f"jdbc:as400://{servidor}"
        
        # Parámetros mínimos necesarios (sin libraries que causa PWS0082)
        parametros = [
            "naming=system",             # Naming convention del sistema
            "errors=full",               # Errores completos
            "extended dynamic=true",     # Dynamic SQL extendido
            "package cache=true",        # Cache de paquetes
            "translate binary=true"      # Traducir binarios
        ]
        
        # Construir URL final
        jdbc_url += ";" + ";".join(parametros)
        
        return jdbc_url
    
    def _obtener_info_sistema_jdbc(self, cursor) -> str:
        """Obtiene información adicional del sistema IBM i via JDBC."""
        info_partes = []
        
        try:
            # Información de la versión del sistema
            cursor.execute("SELECT OS_VERSION, OS_RELEASE FROM QSYS2.SYSTEM_STATUS FETCH FIRST 1 ROWS ONLY")
            version_result = cursor.fetchone()
            if version_result:
                info_partes.append(f"OS: {version_result[0]}.{version_result[1]}")
        except:
            try:
                # Método alternativo
                cursor.execute("VALUES QSYS2.OS_VERSION()")
                version_alt = cursor.fetchone()
                if version_alt:
                    info_partes.append(f"OS Version: {version_alt[0]}")
            except:
                info_partes.append("OS: No disponible")
        
        try:
            # Información del trabajo actual
            cursor.execute("VALUES JOB_NAME")
            job_result = cursor.fetchone()
            if job_result:
                info_partes.append(f"Job: {job_result[0]}")
        except:
            info_partes.append("Job: No disponible")
        
        return ", ".join(info_partes) if info_partes else "Info del sistema: No disponible"
    
    def _manejar_error_jdbc(self, error: Exception, servidor: str, tiempo_respuesta: float) -> ResultadoPruebaConexion:
        """Maneja errores específicos de conexión JDBC."""
        error_msg = str(error).lower()
        
        # Errores de conexión de red
        if any(term in error_msg for term in ['connection', 'network', 'timeout', 'host', 'refused']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"No se puede conectar al servidor IBM i Series {servidor}",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=f"Error de conectividad: {str(error)}"
            )
        
        # Errores de autenticación
        if any(term in error_msg for term in ['authentication', 'login', 'password', 'user', 'invalid', 'authority']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Credenciales inválidas para IBM i Series",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=f"Error de autenticación: {str(error)}"
            )
        
        # Errores de driver JDBC
        if any(term in error_msg for term in ['driver', 'class', 'jar', 'classpath']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error con el driver JDBC de IBM i Series",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=f"Error de driver: {str(error)}"
            )
        
        # Errores de biblioteca/esquema
        if any(term in error_msg for term in ['library', 'schema', 'object', 'not found', 'sql0204']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Biblioteca o objeto no encontrado en IBM i Series",
                tiempo_respuesta=tiempo_respuesta,
                detalles_error=f"Error de biblioteca: {str(error)}"
            )
        
        # Error genérico
        return ResultadoPruebaConexion(
            exitosa=False,
            mensaje=f"Error de IBM i Series JDBC: {str(error)}",
            tiempo_respuesta=tiempo_respuesta,
            detalles_error=f"Error JDBC: {str(error)}"
        )