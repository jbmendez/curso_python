"""
Script de prueba completo para validar todas las bases de datos soportadas
"""
import sys
import os

# Agregar src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.domain.entities.conexion import Conexion
from src.domain.services.conexion_test_service import ConexionTestFactory
from src.infrastructure.services.postgresql_conexion_test import PostgreSQLConexionTest
from src.infrastructure.services.mysql_conexion_test import MySQLConexionTest
from src.infrastructure.services.sqlserver_conexion_test import SQLServerConexionTest
from src.infrastructure.services.sqlite_conexion_test import SQLiteConexionTest

def inicializar_servicios():
    """Inicializa todos los servicios de conexión"""
    # PostgreSQL
    postgresql_service = PostgreSQLConexionTest()
    ConexionTestFactory.registrar_servicio(
        postgresql_service.tipos_soportados(), 
        postgresql_service
    )
    
    # MySQL
    mysql_service = MySQLConexionTest()
    ConexionTestFactory.registrar_servicio(
        mysql_service.tipos_soportados(), 
        mysql_service
    )
    
    # SQL Server
    sqlserver_service = SQLServerConexionTest()
    ConexionTestFactory.registrar_servicio(
        sqlserver_service.tipos_soportados(), 
        sqlserver_service
    )
    
    # SQLite
    sqlite_service = SQLiteConexionTest()
    ConexionTestFactory.registrar_servicio(
        sqlite_service.tipos_soportados(), 
        sqlite_service
    )

def probar_conexion(nombre, conexion):
    """Prueba una conexión específica"""
    print(f"\n🔌 Probando {nombre}:")
    print(f"   Motor: {conexion.tipo_motor}")
    print(f"   Servidor: {conexion.servidor}")
    if conexion.puerto:
        print(f"   Puerto: {conexion.puerto}")
    print(f"   Base de datos: {conexion.base_datos}")
    print(f"   Usuario: {conexion.usuario}")
    
    # Obtener servicio del factory
    servicio = ConexionTestFactory.obtener_servicio(conexion.tipo_motor)
    
    if servicio:
        resultado = servicio.probar_conexion(conexion)
        
        if resultado.exitosa:
            print(f"   ✅ ÉXITO: {resultado.mensaje}")
            if resultado.tiempo_respuesta:
                print(f"   ⏱️  Tiempo: {resultado.tiempo_respuesta:.2f}s")
            if resultado.version_servidor:
                print(f"   📋 Versión: {resultado.version_servidor}")
        else:
            print(f"   ❌ FALLO: {resultado.mensaje}")
            if resultado.detalles_error:
                print(f"   🔍 Detalle: {resultado.detalles_error}")
    else:
        print(f"   ❌ No se encontró servicio para {conexion.tipo_motor}")

def main():
    print("🧪 PRUEBA COMPLETA DE SERVICIOS DE CONEXIÓN")
    print("=" * 60)
    
    # Inicializar servicios
    inicializar_servicios()
    
    print(f"📋 Tipos registrados: {ConexionTestFactory.tipos_soportados()}")
    
    # Conexiones de prueba
    conexiones_prueba = [
        # PostgreSQL
        ("PostgreSQL Local", Conexion(
            nombre="test_postgresql",
            tipo_motor="postgresql",
            servidor="localhost",
            puerto=5432,
            base_datos="postgres",
            usuario="postgres",
            contraseña="password"
        )),
        
        # MySQL
        ("MySQL Local", Conexion(
            nombre="test_mysql",
            tipo_motor="mysql",
            servidor="localhost",
            puerto=3306,
            base_datos="mysql",
            usuario="root",
            contraseña="password"
        )),
        
        # SQL Server
        ("SQL Server Local", Conexion(
            nombre="test_sqlserver",
            tipo_motor="sqlserver",
            servidor="localhost",
            puerto=1433,
            base_datos="master",
            usuario="sa",
            contraseña="YourPassword123"
        )),
        
        # SQLite
        ("SQLite Archivo", Conexion(
            nombre="test_sqlite",
            tipo_motor="sqlite",
            servidor="test_database.db",
            puerto=None,
            base_datos="",
            usuario="",
            contraseña=""
        )),
    ]
    
    # Probar cada conexión
    for nombre, conexion in conexiones_prueba:
        try:
            probar_conexion(nombre, conexion)
        except Exception as e:
            print(f"\n❌ Error inesperado probando {nombre}: {e}")
    
    print(f"\n🏁 Pruebas completadas")
    print("\n💡 Notas:")
    print("   - Las conexiones fallarán si no tienes los servidores configurados")
    print("   - SQLite debería funcionar siempre (no requiere servidor)")
    print("   - Para usar otros motores, instala: pip install pymysql pyodbc")

if __name__ == "__main__":
    main()