"""
Configuración e inicialización de servicios de prueba de conexión
"""
from src.domain.services.conexion_test_service import ConexionTestFactory
from src.infrastructure.services.postgresql_conexion_test import PostgreSQLConexionTest


def inicializar_servicios_conexion():
    """Inicializa y registra todos los servicios de prueba de conexión disponibles"""
    
    # Registrar PostgreSQL
    postgresql_service = PostgreSQLConexionTest()
    ConexionTestFactory.registrar_servicio(
        postgresql_service.tipos_soportados(), 
        postgresql_service
    )
    
    # Aquí se agregarán otros servicios cuando los implementemos
    # mysql_service = MySQLConexionTest()
    # ConexionTestFactory.registrar_servicio(mysql_service.tipos_soportados(), mysql_service)
    
    print(f"✅ Servicios de conexión registrados: {ConexionTestFactory.tipos_soportados()}")


def obtener_tipos_motor_soportados():
    """Retorna la lista de tipos de motor soportados para pruebas de conexión"""
    return ConexionTestFactory.tipos_soportados()