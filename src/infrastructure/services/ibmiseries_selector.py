"""
Selector de servicios de conexión para IBM i Series.
Permite elegir entre ODBC y JDBC basado en la configuración.
"""
from typing import Optional
from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestService, ResultadoPruebaConexion, ConexionTestFactory
from src.infrastructure.services.ibmiseries_conexion_test import IBMiSeriesConexionTest
from src.infrastructure.services.ibmiseries_jdbc_conexion_test import IBMiSeriesJDBCConexionTest


class IBMiSeriesConexionSelector(ConexionTestService):
    """Selector inteligente para servicios de conexión IBM i Series."""
    
    def tipos_soportados(self) -> list:
        """Retorna los tipos de base de datos soportados por este selector."""
        return ["IBM i Series", "AS/400", "iSeries", "IBM i"]
    
    def probar_conexion(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Selecciona y ejecuta el servicio apropiado según driver_type.
        
        Args:
            conexion: Entidad de conexión con driver_type especificado
                
        Returns:
            ResultadoPruebaConexion del servicio seleccionado
        """
        # Determinar qué servicio usar
        driver_type = getattr(conexion, 'driver_type', 'auto').lower()
        
        if driver_type == 'jdbc':
            # Usar específicamente JDBC
            return self._usar_jdbc(conexion)
        elif driver_type == 'odbc':
            # Usar específicamente ODBC
            return self._usar_odbc(conexion)
        else:
            # Auto-detección: intentar JDBC primero, luego ODBC
            return self._auto_detectar(conexion)
    
    def _usar_jdbc(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """Usa específicamente el servicio JDBC."""
        try:
            # Verificar si JPype está disponible
            import jpype
            from src.infrastructure.services.ibmiseries_jdbc_conexion_test import IBMiSeriesJDBCConexionTest
            
            servicio_jdbc = IBMiSeriesJDBCConexionTest()
            resultado = servicio_jdbc.probar_conexion(conexion)
            
            # Agregar información del driver usado
            if resultado.exitosa:
                resultado.version_servidor = f"JDBC - {resultado.version_servidor or 'Driver conectado'}"
            else:
                resultado.mensaje = f"[JDBC] {resultado.mensaje}"
            
            return resultado
            
        except ImportError as e:
            if "jpype" in str(e).lower():
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje="JPype no está instalado - ejecuta install_jpype_java8.bat",
                    detalles_error="JDBC requiere JPype. Ejecuta install_jpype_java8.bat para instalarlo."
                )
            else:
                return ResultadoPruebaConexion(
                    exitosa=False,
                    mensaje=f"Error importando servicio JDBC: {str(e)}",
                    detalles_error="Verifica la instalación de jaydebeapi y JPype"
                )
        except Exception as e:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje=f"Error inesperado en JDBC: {str(e)}",
                detalles_error="Contacta soporte técnico"
            )
    
    def _usar_odbc(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """Usa específicamente el servicio ODBC."""
        servicio_odbc = IBMiSeriesConexionTest()
        resultado = servicio_odbc.probar_conexion(conexion)
        
        # Agregar información del driver usado
        if resultado.exitosa:
            resultado.version_servidor = f"ODBC - {resultado.version_servidor or 'Driver conectado'}"
        else:
            resultado.mensaje = f"[ODBC] {resultado.mensaje}"
        
        return resultado
    
    def _auto_detectar(self, conexion: Conexion) -> ResultadoPruebaConexion:
        """
        Auto-detección: Intenta JDBC primero (recomendado para IBM i), luego ODBC.
        """
        print("[INFO] Auto-detección: probando JDBC primero...")
        
        # Intentar JDBC primero (recomendado para IBM i después de cambios del sistema)
        resultado_jdbc = self._usar_jdbc(conexion)
        if resultado_jdbc.exitosa:
            return resultado_jdbc
        
        print("[INFO] JDBC falló, probando ODBC como respaldo...")
        
        # Si JDBC falla, intentar ODBC como respaldo
        resultado_odbc = self._usar_odbc(conexion)
        if resultado_odbc.exitosa:
            return resultado_odbc
        
        # Si ambos fallan, combinar errores
        return self._crear_resultado_combinado(resultado_jdbc, resultado_odbc)
    
    def _crear_resultado_combinado(self, resultado_jdbc: ResultadoPruebaConexion, 
                                 resultado_odbc: ResultadoPruebaConexion) -> ResultadoPruebaConexion:
        """Crea un resultado que combina información de ambos intentos."""
        
        # Verificar si son errores de configuración de drivers
        jdbc_no_disponible = "No se encontró el driver JDBC" in resultado_jdbc.mensaje
        odbc_no_disponible = "No se encontró driver ODBC" in resultado_odbc.mensaje
        
        if jdbc_no_disponible and odbc_no_disponible:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="No hay drivers IBM i Series disponibles",
                detalles_error="Instala IBM i Access for Windows (ODBC) o descarga jt400.jar (JDBC). Ver diagnóstico para más detalles."
            )
        elif jdbc_no_disponible:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Solo ODBC disponible - " + resultado_odbc.mensaje,
                detalles_error=f"JDBC no disponible: {resultado_jdbc.detalles_error}. Error ODBC: {resultado_odbc.detalles_error}"
            )
        elif odbc_no_disponible:
            return ResultadoPruebaConexion(
                exitosa=False,
                mensaje="Solo JDBC disponible - " + resultado_jdbc.mensaje,
                detalles_error=f"ODBC no disponible: {resultado_odbc.detalles_error}. Error JDBC: {resultado_jdbc.detalles_error}"
            )
        
        # Determinar qué error es más útil
        error_jdbc_es_config = any(term in resultado_jdbc.mensaje.lower() 
                                 for term in ['driver', 'jar', 'no se encontró'])
        error_odbc_es_config = any(term in resultado_odbc.mensaje.lower() 
                                 for term in ['driver', 'no se encontró'])
        
        if error_jdbc_es_config and not error_odbc_es_config:
            # Error JDBC es de configuración, mostrar error ODBC
            mensaje_principal = resultado_odbc.mensaje
            detalles_extra = f"También se intentó JDBC: {resultado_jdbc.mensaje}"
        elif error_odbc_es_config and not error_jdbc_es_config:
            # Error ODBC es de configuración, mostrar error JDBC
            mensaje_principal = resultado_jdbc.mensaje
            detalles_extra = f"También se intentó ODBC: {resultado_odbc.mensaje}"
        else:
            # Ambos son errores de configuración o ambos son errores de conexión
            mensaje_principal = "No se pudo conectar con ningún driver (JDBC/ODBC)"
            detalles_extra = f"JDBC: {resultado_jdbc.mensaje} | ODBC: {resultado_odbc.mensaje}"
        
        return ResultadoPruebaConexion(
            exitosa=False,
            mensaje=mensaje_principal,
            tiempo_respuesta=max(resultado_jdbc.tiempo_respuesta or 0, 
                               resultado_odbc.tiempo_respuesta or 0),
            detalles_error=detalles_extra
        )


def obtener_servicio_ibmiseries(conexion: Conexion) -> ConexionTestService:
    """
    Función helper para obtener el servicio correcto para IBM i Series.
    
    Args:
        conexion: Entidad de conexión con driver_type especificado
        
    Returns:
        ConexionTestService apropiado
    """
    driver_type = getattr(conexion, 'driver_type', 'auto').lower()
    
    if driver_type == 'jdbc':
        return IBMiSeriesJDBCConexionTest()
    elif driver_type == 'odbc':
        return IBMiSeriesConexionTest()
    else:
        return IBMiSeriesConexionSelector()