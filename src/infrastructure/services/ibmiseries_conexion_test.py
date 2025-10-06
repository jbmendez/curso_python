"""
Servicio de prueba de conexión para IBM i Series (AS/400).
"""
from typing import Dict, Any
import pyodbc
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion


class IBMiSeriesConexionTest(ConexionTestService):
    """Servicio para probar conexiones a IBM i Series (AS/400)."""
    
    def tipos_soportados(self) -> list:
        """Retorna los tipos de base de datos soportados por este servicio."""
        return ["IBM i Series", "AS/400", "iSeries", "IBM i"]
    
    def probar_conexion(self, parametros_conexion: Dict[str, Any]) -> ResultadoPruebaConexion:
        """
        Prueba la conexión a IBM i Series.
        
        Args:
            parametros_conexion: Diccionario con parámetros de conexión:
                - servidor: Nombre o IP del servidor IBM i
                - puerto: Puerto (por defecto 446 para encrypted, 8471 para unencrypted)
                - base_datos: Nombre de la biblioteca por defecto (opcional)
                - usuario: Usuario de IBM i
                - password: Contraseña
                - driver: Driver ODBC específico (opcional)
                - ssl: Si usar SSL (por defecto True)
                
        Returns:
            ResultadoPruebaConexion con el resultado de la prueba
        """
        try:
            # Extraer parámetros
            servidor = parametros_conexion.get('servidor', '').strip()
            puerto = parametros_conexion.get('puerto', 446)  # Puerto por defecto para SSL
            usuario = parametros_conexion.get('usuario', '').strip()
            password = parametros_conexion.get('password', '')
            base_datos = parametros_conexion.get('base_datos', '').strip()
            driver_personalizado = parametros_conexion.get('driver', '').strip()
            ssl = parametros_conexion.get('ssl', True)
            
            # Validaciones básicas
            if not servidor:
                return ResultadoPruebaConexion(
                    exitoso=False,
                    mensaje="El servidor es requerido",
                    categoria_error="CONFIGURACION",
                    detalles_tecnicos="Parámetro 'servidor' vacío o no proporcionado"
                )
            
            if not usuario:
                return ResultadoPruebaConexion(
                    exitoso=False,
                    mensaje="El usuario es requerido",
                    categoria_error="CONFIGURACION",
                    detalles_tecnicos="Parámetro 'usuario' vacío o no proporcionado"
                )
            
            # Detectar driver disponible
            driver = self._detectar_driver_ibmi(driver_personalizado)
            if not driver:
                return ResultadoPruebaConexion(
                    exitoso=False,
                    mensaje="No se encontró driver ODBC para IBM i Series",
                    categoria_error="DRIVER",
                    detalles_tecnicos=self._listar_drivers_disponibles()
                )
            
            # Construir cadena de conexión
            connection_string = self._construir_cadena_conexion(
                driver, servidor, puerto, usuario, password, base_datos, ssl
            )
            
            # Intentar conexión
            with pyodbc.connect(connection_string, timeout=10) as conn:
                # Ejecutar consulta de prueba
                with conn.cursor() as cursor:
                    # Consulta para obtener información del sistema
                    cursor.execute("SELECT CURRENT_DATE, CURRENT_TIME, CURRENT_USER FROM SYSIBM.SYSDUMMY1")
                    resultado = cursor.fetchone()
                    
                    fecha_actual = resultado[0] if resultado else "N/A"
                    hora_actual = resultado[1] if resultado else "N/A"
                    usuario_actual = resultado[2] if resultado else "N/A"
                    
                    # Obtener información adicional del sistema
                    info_sistema = self._obtener_info_sistema(cursor)
                    
                    info_adicional = {
                        "driver_usado": driver,
                        "fecha_sistema": str(fecha_actual),
                        "hora_sistema": str(hora_actual),
                        "usuario_conectado": str(usuario_actual),
                        "servidor": servidor,
                        "puerto": puerto,
                        "ssl_habilitado": ssl,
                        **info_sistema
                    }
                    
                    if base_datos:
                        info_adicional["biblioteca_defecto"] = base_datos
                    
                    return ResultadoPruebaConexion(
                        exitoso=True,
                        mensaje=f"Conexión exitosa a IBM i Series {servidor}",
                        detalles_tecnicos=f"Conectado usando {driver}",
                        info_adicional=info_adicional
                    )
                    
        except pyodbc.Error as e:
            return self._manejar_error_pyodbc(e, servidor)
        except Exception as e:
            return ResultadoPruebaConexion(
                exitoso=False,
                mensaje=f"Error inesperado: {str(e)}",
                categoria_error="DESCONOCIDO",
                detalles_tecnicos=f"Tipo de error: {type(e).__name__}"
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
        """Construye la cadena de conexión para IBM i Series."""
        # Cadena base
        connection_string = f"DRIVER={{{driver}}};SYSTEM={servidor};PORT={puerto};UID={usuario};PWD={password};"
        
        # Configuraciones de seguridad
        if ssl:
            connection_string += "SSL=1;"
        
        # Biblioteca por defecto
        if base_datos:
            connection_string += f"DBQ={base_datos};"
        
        # Configuraciones adicionales comunes para IBM i
        connection_string += "LANGUAGEID=ENU;QRYSTGLMT=-1;BLOCKFETCH=1;BLOCKSIZE=128;PREFETCH=1;"
        
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
                exitoso=False,
                mensaje=f"No se puede conectar al servidor IBM i Series {servidor}",
                categoria_error="RED",
                detalles_tecnicos=f"Error de conectividad: {str(error)}"
            )
        
        # Errores de autenticación
        if any(term in error_msg for term in ['authentication', 'login', 'password', 'user', 'invalid']):
            return ResultadoPruebaConexion(
                exitoso=False,
                mensaje="Credenciales inválidas para IBM i Series",
                categoria_error="AUTENTICACION",
                detalles_tecnicos=f"Error de autenticación: {str(error)}"
            )
        
        # Errores de SSL/TLS
        if any(term in error_msg for term in ['ssl', 'tls', 'certificate', 'encryption']):
            return ResultadoPruebaConexion(
                exitoso=False,
                mensaje="Error de SSL/TLS en la conexión",
                categoria_error="SSL",
                detalles_tecnicos=f"Error de seguridad: {str(error)}"
            )
        
        # Errores de driver
        if any(term in error_msg for term in ['driver', 'odbc', 'data source']):
            return ResultadoPruebaConexion(
                exitoso=False,
                mensaje="Error con el driver ODBC de IBM i Series",
                categoria_error="DRIVER",
                detalles_tecnicos=f"Error de driver: {str(error)}"
            )
        
        # Errores de biblioteca/esquema
        if any(term in error_msg for term in ['library', 'schema', 'object', 'not found']):
            return ResultadoPruebaConexion(
                exitoso=False,
                mensaje="Biblioteca o objeto no encontrado en IBM i Series",
                categoria_error="CONFIGURACION",
                detalles_tecnicos=f"Error de biblioteca: {str(error)}"
            )
        
        # Error genérico
        return ResultadoPruebaConexion(
            exitoso=False,
            mensaje=f"Error de IBM i Series: {str(error)}",
            categoria_error="DATABASE",
            detalles_tecnicos=f"Error ODBC: {str(error)}"
        )