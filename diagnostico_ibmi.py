#!/usr/bin/env python3
"""
Script de diagnóstico para drivers IBM i Series
"""
import sys
import os

# Agregar el directorio src al path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def diagnosticar_jdbc():
    """Diagnostica problemas con JDBC"""
    print("🔍 Diagnóstico JDBC para IBM i Series:")
    
    # 1. Verificar si jaydebeapi está instalado
    try:
        import jaydebeapi
        print("✅ jaydebeapi está instalado")
    except ImportError:
        print("❌ jaydebeapi NO está instalado")
        print("   Solución: py -m pip install jaydebeapi")
        return False
    
    # 2. Verificar si hay Java disponible
    try:
        import jpype
        print("✅ JPype (dependencia de jaydebeapi) está disponible")
    except ImportError:
        print("❌ JPype NO está disponible")
        print("   Nota: Se instaló automáticamente con jaydebeapi")
        return False
    
    # 3. Buscar el archivo jt400.jar
    posibles_rutas = [
        "drivers/jt400.jar",
        "lib/jt400.jar", 
        "jdbc/jt400.jar",
        "C:/IBM/JTOpen/lib/jt400.jar",
        "C:/Program Files/IBM/Java/jt400/lib/jt400.jar",
        "C:/jt400/lib/jt400.jar",
        os.environ.get("JT400_JAR", "")
    ]
    
    jar_encontrado = None
    for ruta in posibles_rutas:
        if ruta and os.path.exists(ruta):
            jar_encontrado = ruta
            break
    
    if jar_encontrado:
        print(f"✅ jt400.jar encontrado en: {jar_encontrado}")
        return True
    else:
        print("❌ jt400.jar NO encontrado")
        print("   Solución:")
        print("   1. Descargar jt400.jar de https://sourceforge.net/projects/jt400/")
        print("   2. Colocar en carpeta 'drivers/' del proyecto")
        print("   3. O definir variable JT400_JAR con la ruta completa")
        return False

def diagnosticar_odbc():
    """Diagnostica problemas con ODBC"""
    print("\n🔍 Diagnóstico ODBC para IBM i Series:")
    
    # 1. Verificar si pyodbc está instalado
    try:
        import pyodbc
        print("✅ pyodbc está instalado")
    except ImportError:
        print("❌ pyodbc NO está instalado")
        print("   Solución: py -m pip install pyodbc")
        return False
    
    # 2. Listar drivers disponibles
    try:
        drivers = pyodbc.drivers()
        print(f"📋 Drivers ODBC disponibles: {len(drivers)}")
        
        # Buscar drivers específicos de IBM i
        drivers_ibmi = []
        for driver in drivers:
            if any(palabra in driver.lower() for palabra in ['ibm', 'iseries', 'as/400', 'db2']):
                drivers_ibmi.append(driver)
        
        if drivers_ibmi:
            print("✅ Drivers IBM i Series encontrados:")
            for driver in drivers_ibmi:
                print(f"   - {driver}")
            return True
        else:
            print("❌ NO se encontraron drivers IBM i Series")
            print("   Drivers disponibles:")
            for driver in drivers[:5]:  # Mostrar solo los primeros 5
                print(f"   - {driver}")
            if len(drivers) > 5:
                print(f"   ... y {len(drivers) - 5} más")
            
            print("\n   Solución:")
            print("   1. Instalar IBM i Access for Windows")
            print("   2. O instalar IBM i Access Client Solutions")
            print("   3. Reiniciar después de la instalación")
            return False
            
    except Exception as e:
        print(f"❌ Error al listar drivers: {e}")
        return False

def diagnosticar_conexion_test():
    """Prueba los servicios de conexión directamente"""
    print("\n🧪 Probando servicios de conexión:")
    
    try:
        from infrastructure.services.ibmiseries_jdbc_conexion_test import IBMiSeriesJDBCConexionTest
        from infrastructure.services.ibmiseries_conexion_test import IBMiSeriesConexionTest
        from domain.entities.conexion import Conexion
        
        # Crear conexión de prueba
        conexion_test = Conexion(
            nombre="Test Diagnóstico",
            servidor="localhost",  # Servidor ficticio para prueba
            puerto=8471,
            usuario="testuser",
            contraseña="testpass",
            base_datos="TESTLIB",
            tipo_motor="iseries",
            driver_type="auto"
        )
        
        # Probar JDBC
        print("\n🔧 Probando servicio JDBC:")
        servicio_jdbc = IBMiSeriesJDBCConexionTest()
        resultado_jdbc = servicio_jdbc.probar_conexion(conexion_test)
        print(f"   Resultado: {'✅' if resultado_jdbc.exitosa else '❌'} {resultado_jdbc.mensaje}")
        if not resultado_jdbc.exitosa:
            print(f"   Detalle: {resultado_jdbc.detalles_error}")
        
        # Probar ODBC
        print("\n🔧 Probando servicio ODBC:")
        servicio_odbc = IBMiSeriesConexionTest()
        resultado_odbc = servicio_odbc.probar_conexion(conexion_test)
        print(f"   Resultado: {'✅' if resultado_odbc.exitosa else '❌'} {resultado_odbc.mensaje}")
        if not resultado_odbc.exitosa:
            print(f"   Detalle: {resultado_odbc.detalles_error}")
        
        return resultado_jdbc.exitosa or resultado_odbc.exitosa
        
    except Exception as e:
        print(f"❌ Error al probar servicios: {e}")
        return False

def main():
    """Ejecuta diagnóstico completo"""
    print("[DIAG] DIAGNOSTICO DE DRIVERS IBM i SERIES")
    print("=" * 50)
    
    jdbc_ok = diagnosticar_jdbc()
    odbc_ok = diagnosticar_odbc()
    
    print("\n" + "=" * 50)
    print("[RESUMEN] RESULTADO DEL DIAGNOSTICO:")
    
    if jdbc_ok and odbc_ok:
        print("[OK] Excelente! Ambos drivers estan disponibles")
        print("   Puedes usar 'auto', 'jdbc' o 'odbc' en driver_type")
    elif jdbc_ok:
        print("[WARN] Solo JDBC esta disponible")
        print("   Usa driver_type='jdbc' o instala IBM i Access for Windows")
    elif odbc_ok:
        print("[WARN] Solo ODBC esta disponible") 
        print("   Usa driver_type='odbc' o descarga jt400.jar")
    else:
        print("[ERROR] Ningun driver esta disponible")
        print("   Instala al menos uno de los drivers")
    
    # Probar servicios si hay algún driver disponible
    if jdbc_ok or odbc_ok:
        servicios_ok = diagnosticar_conexion_test()
        if not servicios_ok:
            print("\n[WARN] Los servicios no funcionan correctamente")
            print("   Esto es normal si no hay un servidor IBM i real disponible")
    
    print("\n[INFO] Enlaces utiles:")
    print("   - jt400.jar: https://sourceforge.net/projects/jt400/")
    print("   - IBM i Access: https://www.ibm.com/support/pages/ibm-i-access-client-solutions")
    
if __name__ == "__main__":
    main()