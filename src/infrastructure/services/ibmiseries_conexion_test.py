"""
Servicio de prueba de conexión para IBM i Series (AS/400) con timeouts robustos.
"""
from typing import Dict, Any
import pyodbc
import threading
import time
from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class IBMiSeriesConexionTest(ConexionTestService):
    """Servicio para probar conexiones a IBM i Series (AS/400) con protección contra cuelgues."""
    
    def tipos_soportados(self) -> list:
        """Retorna los tipos de base de datos soportados por este servicio."""
        return ["IBM i Series", "AS/400", "iSeries", "IBM i"]
    
    def _probar_conexion_con_timeout(self, connection_string: str, timeout_seconds: int = 45) -> tuple:
        """
        Prueba la conexión con timeout usando threading para evitar cuelgues.
        
        Returns:
            tuple: (exitoso: bool, resultado: dict/str, tiempo_elapsed: float)
        """
        resultado = {'exitoso': False, 'datos': None, 'error': None}
        
        def _conectar():
            try:
                start_time = time.time()
                # Configurar pyodbc para evitar cuelgues
                pyodbc.pooling = False
                
                with pyodbc.connect(connection_string, timeout=30) as conn:
                    conn.timeout = 30
                    conn.autocommit = True
                    
                    with conn.cursor() as cursor:
                        cursor.timeout = 20
                        
                        # Consulta simple y rápida
                        cursor.execute("SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_USER FROM SYSIBM.SYSDUMMY1")
                        row = cursor.fetchone()
                        
                        if row:
                            resultado['exitoso'] = True
                            resultado['datos'] = {
                                'fecha_sistema': str(row[0]) if row[0] else "N/A",
                                'hora_sistema': str(row[1]) if row[1] else "N/A", 
                                'usuario_conectado': str(row[2]) if row[2] else "N/A",
                                'tiempo_conexion': time.time() - start_time
                            }
                        else:
                            resultado['error'] = "No se obtuvieron datos del sistema"
                            
            except Exception as e:
                resultado['error'] = str(e)
        
        # Ejecutar en thread con timeout
        start_time = time.time()
        thread = threading.Thread(target=_conectar)
        thread.daemon = True
        thread.start()
        thread.join(timeout=timeout_seconds)
        
        elapsed_time = time.time() - start_time
        
        if thread.is_alive():
            # Thread todavía corriendo = timeout
            return False, f"Timeout después de {timeout_seconds}s - conexión se colgó", elapsed_time
        elif resultado['exitoso']:
            return True, resultado['datos'], elapsed_time
        else:
            error_msg = resultado['error'] or "Error desconocido"
            return False, error_msg, elapsed_time
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Prueba la conexión a IBM i Series.
        
        Args:
            conexion: Entidad de conexión con los datos necesarios
                
        Returns:
            ResultadoPruebaConexion con el resultado de la prueba
        """
        try:
            # Extraer parámetros de la entidad conexion
            servidor = conexion.servidor or ''
            puerto = conexion.puerto or 446  # Puerto por defecto para SSL
            usuario = conexion.usuario or ''
            password = conexion.contraseña or ''
            base_datos = conexion.base_datos or ''
            # Para IBM i Series podríamos usar conexion.motor para configuraciones específicas
            ssl = True  # Por defecto SSL habilitado
            
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
            
            # Detectar driver disponible
            driver = self._detectar_driver_ibmi()
            if not driver:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje="No se encontró driver ODBC para IBM i Series",
                    detalles_error=self._listar_drivers_disponibles()
                )
            
            # Construir cadena de conexión
            connection_string = self._construir_cadena_conexion(
                driver, servidor, puerto, usuario, password, base_datos, ssl
            )
            
            # Usar conexión con timeout robusto para evitar cuelgues
            print(f"[DEBUG] Probando conexión ODBC con timeout de 45s...")
            exitoso, datos, tiempo_elapsed = self._probar_conexion_con_timeout(connection_string, 45)
            
            if exitoso:
                info_adicional = {
                    "driver_usado": driver,
                    "servidor": servidor,
                    "puerto": puerto,
                    "ssl_habilitado": ssl,
                    "tiempo_respuesta_real": tiempo_elapsed,
                    **datos
                }
                
                if base_datos:
                    info_adicional["biblioteca_defecto"] = base_datos
                
                return ResultadoPruebaConexion(
                    exitosa=True,
                    mensaje=f"Conexión exitosa a IBM i Series {servidor} en {tiempo_elapsed:.2f}s",
                    version_servidor=f"Conectado usando {driver}",
                    tiempo_respuesta=tiempo_elapsed,
                    info_adicional=info_adicional
                )
            else:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje=f"[ODBC] No se puede conectar al servidor IBM i Series {servidor}",
                    tiempo_respuesta=tiempo_elapsed,
                    detalles_error=f"Error después de {tiempo_elapsed:.2f}s: {datos}"
                )
                    
        except pyodbc.Error as e:
            return self._manejar_error_pyodbc(e, servidor)
        except Exception as e:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error inesperado: {str(e)}",
                detalles_error=f"Tipo de error: {type(e).__name__}"
            )
    
    def _detectar_driver_ibmi(self, driver_personalizado: str = "") -> str:
        """Detecta el driver ODBC disponible para IBM i Series."""
        # Drivers comunes para IBM i Series
        drivers_ibmi = [
            "IBM i Access ODBC Driver",
            "IBM i Access ODBC Driver 64-bit",
            "iSeries Access ODBC Driver",
            "IBM DB2 for i",
            "DB2 for i5/OS",
            "Client Access ODBC Driver (32-bit)",
            "IBM i Access for Windows",
        ]
        
        # Si se especificó un driver personalizado, probarlo primero
        if driver_personalizado:
            drivers_ibmi.insert(0, driver_personalizado)
        
        drivers_disponibles = [d for d in pyodbc.drivers() if d]
        
        for driver in drivers_ibmi:
            if driver in drivers_disponibles:
                return driver
        
        # Buscar drivers que contengan palabras clave
        palabras_clave = ['IBM', 'i Series', 'iSeries', 'AS/400', 'DB2']
        for driver_disponible in drivers_disponibles:
            for palabra in palabras_clave:
                if palabra.lower() in driver_disponible.lower():
                    return driver_disponible
        
        return ""
    
    def _listar_drivers_disponibles(self) -> str:
        """Lista todos los drivers ODBC disponibles."""
        try:
            drivers = pyodbc.drivers()
            if drivers:
                return f"Drivers disponibles: {', '.join(drivers)}"
            else:
                return "No se encontraron drivers ODBC instalados"
        except Exception:
            return "No se pudo listar los drivers disponibles"
    
    def _construir_cadena_conexion(self, driver: str, servidor: str, puerto: int, 
                                 usuario: str, password: str, base_datos: str = "", 
                                 ssl: bool = True) -> str:
        """Construye la cadena de conexión para IBM i Series con timeouts configurados."""
        # Cadena base - para IBM DB2 ODBC DRIVER usamos DATABASE en lugar de DBQ
        if "IBM DB2" in driver:
            # Para drivers DB2 nativos
            connection_string = f"DRIVER={{{driver}}};HOSTNAME={servidor};PORT={puerto};DATABASE={base_datos or 'QSYS'};UID={usuario};PWD={password};"
            if ssl:
                connection_string += "SECURITY=SSL;"
        else:
            # Para drivers IBM i Access tradicionales
            connection_string = f"DRIVER={{{driver}}};SYSTEM={servidor};PORT={puerto};UID={usuario};PWD={password};"
            if ssl:
                connection_string += "SSL=1;"
            # Biblioteca por defecto
            if base_datos:
                connection_string += f"DBQ={base_datos};"
        
        # Configuraciones adicionales para IBM i con timeouts
        connection_string += (
            "LANGUAGEID=ENU;"
            "QRYSTGLMT=-1;"
            "CONNECTTIMEOUT=30;"     # Timeout de conexión en segundos
            "QUERYTIMEOUT=60;"       # Timeout de consulta en segundos
            "LOGINTIMEOUT=30;"       # Timeout de login
            "AUTOCOMMIT=1;"          # Habilitar autocommit
            "PROTOCOL=TCPIP;"        # Forzar protocolo TCP/IP
        )
        
        return connection_string
    
    def _obtener_info_sistema(self, cursor) -> Dict[str, Any]:
        """Obtiene información adicional del sistema IBM i."""
        info = {}
        
        try:
            # Información de la versión
            cursor.execute("""
                SELECT OS_VERSION, OS_RELEASE 
                FROM QSYS2.SYSTEM_STATUS 
                FETCH FIRST 1 ROWS ONLY
            """)
            version_result = cursor.fetchone()
            if version_result:
                info["os_version"] = str(version_result[0])
                info["os_release"] = str(version_result[1])
        except:
            try:
                # Método alternativo para obtener versión
                cursor.execute("VALUES QSYS2.OS_VERSION()")
                version_alt = cursor.fetchone()
                if version_alt:
                    info["os_version"] = str(version_alt[0])
            except:
                info["os_version"] = "No disponible"
        
        try:
            # Información de bibliotecas del usuario
            cursor.execute("""
                SELECT COUNT(*) as LIBRARY_COUNT 
                FROM QSYS2.LIBRARY_LIST_INFO 
                WHERE TYPE = 'USER'
            """)
            lib_result = cursor.fetchone()
            if lib_result:
                info["bibliotecas_usuario"] = int(lib_result[0])
        except:
            info["bibliotecas_usuario"] = "No disponible"
        
        try:
            # Obtener el nombre del trabajo actual
            cursor.execute("VALUES JOB_NAME")
            job_result = cursor.fetchone()
            if job_result:
                info["trabajo_actual"] = str(job_result[0])
        except:
            info["trabajo_actual"] = "No disponible"
        
        return info
    
    def _manejar_error_pyodbc(self, error: pyodbc.Error, servidor: str) -> ResultadoPruebaConexion:
        """Maneja errores específicos de pyodbc para IBM i Series."""
        error_msg = str(error).lower()
        
        # Errores de conexión de red
        if any(term in error_msg for term in ['connection', 'network', 'timeout', 'host']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"No se puede conectar al servidor IBM i Series {servidor}",
                detalles_error=f"Error de conectividad: {str(error)}"
            )
        
        # Errores de autenticación
        if any(term in error_msg for term in ['authentication', 'login', 'password', 'user', 'invalid']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Credenciales inválidas para IBM i Series",
                detalles_error=f"Error de autenticación: {str(error)}"
            )
        
        # Errores de SSL/TLS
        if any(term in error_msg for term in ['ssl', 'tls', 'certificate', 'encryption']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error de SSL/TLS en la conexión",
                detalles_error=f"Error de seguridad: {str(error)}"
            )
        
        # Errores de driver
        if any(term in error_msg for term in ['driver', 'odbc', 'data source']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Error con el driver ODBC de IBM i Series",
                detalles_error=f"Error de driver: {str(error)}"
            )
        
        # Errores de biblioteca/esquema
        if any(term in error_msg for term in ['library', 'schema', 'object', 'not found']):
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Biblioteca o objeto no encontrado en IBM i Series",
                detalles_error=f"Error de biblioteca: {str(error)}"
            )
        
        # Error genérico
        return ResultadoPruebaConexion(
            exitosa=False,
            mensaje=f"Error de IBM i Series: {str(error)}",
            detalles_error=f"Error ODBC: {str(error)}"
        )