"""
Script para comparar las opciones de conexión a IBM i Series: ODBC vs JDBC
"""
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.domain.entities.conexion import Conexion
from src.infrastructure.services.ibmiseries_conexion_test import IBMiSeriesConexionTest
from src.infrastructure.services.ibmiseries_jdbc_conexion_test import IBMiSeriesJDBCConexionTest

def test_ibmiseries_comparison():
    """Compara ambas opciones de conexión para IBM i Series"""
    print("🔄 Comparando opciones de conexión IBM i Series...")
    print("=" * 60)
    
    # Crear una conexión de prueba
    conexion_test = Conexion(
        nombre="Prueba IBM i Series",
        servidor="192.168.1.100",  # IP ficticia
        puerto=8471,  # Puerto estándar para IBM i
        base_datos="TESTLIB",
        usuario="testuser",
        contraseña="testpass",
        tipo_motor="iseries"
    )
    
    print(f"📋 Configuración de prueba:")
    print(f"   - Servidor: {conexion_test.servidor}")
    print(f"   - Puerto: {conexion_test.puerto}")
    print(f"   - Usuario: {conexion_test.usuario}")
    print(f"   - Biblioteca: {conexion_test.base_datos}")
    print()
    
    # Probar opción ODBC
    print("🔌 OPCIÓN 1: IBM i Series con ODBC")
    print("-" * 40)
    
    servicio_odbc = IBMiSeriesConexionTest()
    tipos_odbc = servicio_odbc.tipos_soportados()
    print(f"✅ Tipos soportados: {tipos_odbc}")
    
    resultado_odbc = servicio_odbc.probar_conexion(conexion_test)
    print(f"📊 Resultado ODBC:")
    print(f"   - Exitosa: {resultado_odbc.exitosa}")
    print(f"   - Mensaje: {resultado_odbc.mensaje}")
    if resultado_odbc.detalles_error:
        print(f"   - Detalles: {resultado_odbc.detalles_error[:200]}...")
    print()
    
    # Probar opción JDBC
    print("☕ OPCIÓN 2: IBM i Series con JDBC (JayDeBeDB)")
    print("-" * 40)
    
    servicio_jdbc = IBMiSeriesJDBCConexionTest()
    tipos_jdbc = servicio_jdbc.tipos_soportados()
    print(f"✅ Tipos soportados: {tipos_jdbc}")
    
    resultado_jdbc = servicio_jdbc.probar_conexion(conexion_test)
    print(f"📊 Resultado JDBC:")
    print(f"   - Exitosa: {resultado_jdbc.exitosa}")
    print(f"   - Mensaje: {resultado_jdbc.mensaje}")
    if resultado_jdbc.detalles_error:
        print(f"   - Detalles: {resultado_jdbc.detalles_error[:200]}...")
    print()
    
    # Análisis y recomendaciones
    print("🎯 ANÁLISIS Y RECOMENDACIONES")
    print("=" * 60)
    
    if not resultado_odbc.exitosa and not resultado_jdbc.exitosa:
        print("❌ Ambas opciones requieren configuración adicional")
        print()
        print("📋 Para ODBC necesitas:")
        print("   • IBM i Access Client Solutions instalado")
        print("   • Driver ODBC configurado en el sistema")
        print("   • Configuración DSN (opcional)")
        print()
        print("📋 Para JDBC necesitas:")
        print("   • Archivo jt400.jar descargado")
        print("   • Jaydebeapi instalado: pip install jaydebeapi")
        print("   • Java Runtime Environment (JRE)")
        print()
        print("🏆 RECOMENDACIÓN: Usar JDBC (más portable y estable)")
        print("   1. Descargar jt400.jar de: https://sourceforge.net/projects/jt400/")
        print("   2. Colocar en: drivers/jt400.jar")
        print("   3. Instalar: pip install jaydebeapi")
        
    elif resultado_jdbc.exitosa:
        print("🏆 JDBC funcionando correctamente - USAR ESTA OPCIÓN")
    elif resultado_odbc.exitosa:
        print("🏆 ODBC funcionando correctamente - Opción válida")
    
    print()
    print("🎉 Comparación completada!")

def verificar_dependencias():
    """Verifica si las dependencias están instaladas"""
    print("🔍 Verificando dependencias...")
    
    # Verificar pyodbc
    try:
        import pyodbc
        print("✅ pyodbc instalado")
    except ImportError:
        print("❌ pyodbc NO instalado")
    
    # Verificar jaydebeapi
    try:
        import jaydebeapi
        print("✅ jaydebeapi instalado")
    except ImportError:
        print("❌ jaydebeapi NO instalado - ejecutar: pip install jaydebeapi")
    
    # Verificar jt400.jar
    import os
    jar_paths = [
        "drivers/jt400.jar",
        "lib/jt400.jar", 
        "C:/IBM/JTOpen/lib/jt400.jar"
    ]
    
    jar_encontrado = False
    for path in jar_paths:
        if os.path.exists(path):
            print(f"✅ jt400.jar encontrado en: {path}")
            jar_encontrado = True
            break
    
    if not jar_encontrado:
        print("❌ jt400.jar NO encontrado")
        print("   Descargar de: https://sourceforge.net/projects/jt400/")
        print("   Colocar en: drivers/jt400.jar")
    
    print()

if __name__ == "__main__":
    verificar_dependencias()
    test_ibmiseries_comparison()