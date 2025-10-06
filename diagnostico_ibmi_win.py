#!/usr/bin/env python3
"""
Diagnóstico de drivers IBM i Series - Versión compatible con Windows.
Verifica disponibilidad de drivers JDBC y ODBC sin usar emojis Unicode.
"""

import os
import sys
from pathlib import Path

def diagnosticar_jdbc():
    """Verifica disponibilidad del driver JDBC."""
    print("\n[JDBC] Verificando driver JDBC...")
    
    try:
        import jaydebeapi
        print("[OK] jaydebeapi esta instalado")
    except ImportError:
        print("[ERROR] jaydebeapi NO esta instalado")
        print("        Instala con: pip install jaydebeapi")
        return False
    
    try:
        import jpype
        print("[OK] JPype (dependencia de jaydebeapi) esta disponible")
    except ImportError:
        print("[ERROR] JPype NO esta disponible")
        print("        Instala con: pip install JPype1")
        return False
    
    # Verificar jt400.jar
    posibles_rutas = [
        Path("drivers/jt400.jar"),
        Path("jt400.jar"),
        Path("lib/jt400.jar")
    ]
    
    jar_encontrado = None
    for ruta in posibles_rutas:
        if ruta.exists():
            jar_encontrado = ruta.absolute()
            break
    
    if jar_encontrado:
        print(f"[OK] jt400.jar encontrado en: {jar_encontrado}")
        return True
    else:
        print("[ERROR] jt400.jar NO encontrado")
        print("        Descarga desde: https://sourceforge.net/projects/jt400/")
        print("        Coloca en: drivers/jt400.jar")
        return False

def diagnosticar_odbc():
    """Verifica disponibilidad del driver ODBC."""
    print("\n[ODBC] Verificando driver ODBC...")
    
    try:
        import pyodbc
        print("[OK] pyodbc esta instalado")
    except ImportError:
        print("[ERROR] pyodbc NO esta instalado")
        print("        Instala con: pip install pyodbc")
        return False
    
    try:
        drivers = pyodbc.drivers()
        
        # Buscar drivers IBM i
        ibmi_drivers = []
        for driver in drivers:
            if any(term.upper() in driver.upper() for term in ['IBM', 'DB2', 'ISERIES', 'AS400']):
                ibmi_drivers.append(driver)
        
        if ibmi_drivers:
            print("[OK] Drivers IBM i Series encontrados:")
            for driver in ibmi_drivers:
                print(f"        - {driver}")
            return True
        else:
            print("[ERROR] NO se encontraron drivers IBM i Series")
            print("        Instala IBM i Access for Windows")
            print("        O IBM Data Server Driver Package")
            return False
            
    except Exception as e:
        print(f"[ERROR] Error al listar drivers: {e}")
        return False

def diagnosticar_conexion_test():
    """Prueba los servicios de conexión."""
    print("\n[TEST] Probando servicios de conexion...")
    
    try:
        # Importar servicios
        sys.path.append(str(Path(__file__).parent / "src"))
        
        from domain.entities.conexion import Conexion
        from infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector
        
        # Crear conexión de prueba
        conexion_prueba = Conexion(
            nombre="test",
            tipo_motor="ibmiseries",
            servidor="test.example.com",
            puerto=446,
            base_datos="TEST",
            usuario="test",
            contraseña="test",
            driver_type="auto"
        )
        
        selector = IBMiSeriesConexionSelector()
        
        # Probar JDBC si está disponible
        print("\n[TEST-JDBC] Probando selector JDBC...")
        conexion_prueba.driver_type = "jdbc"
        resultado_jdbc = selector.probar_conexion(conexion_prueba)
        status_jdbc = "[OK]" if resultado_jdbc.exitosa else "[FAIL]"
        print(f"   Resultado: {status_jdbc} {resultado_jdbc.mensaje}")
        
        # Probar ODBC si está disponible
        print("\n[TEST-ODBC] Probando selector ODBC...")
        conexion_prueba.driver_type = "odbc"
        resultado_odbc = selector.probar_conexion(conexion_prueba)
        status_odbc = "[OK]" if resultado_odbc.exitosa else "[FAIL]"
        print(f"   Resultado: {status_odbc} {resultado_odbc.mensaje}")
        
        return True
        
    except Exception as e:
        print(f"[ERROR] Error al probar servicios: {e}")
        print("        Esto es normal si faltan dependencias")
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
        print("     Puedes usar 'auto', 'jdbc' o 'odbc' en driver_type")
    elif jdbc_ok:
        print("[WARN] Solo JDBC esta disponible")
        print("       Usa driver_type='jdbc' o instala IBM i Access for Windows")
    elif odbc_ok:
        print("[WARN] Solo ODBC esta disponible") 
        print("       Usa driver_type='odbc' o descarga jt400.jar")
    else:
        print("[ERROR] Ningun driver esta disponible")
        print("        Instala al menos uno de los drivers")
    
    # Probar servicios si hay algún driver disponible
    if jdbc_ok or odbc_ok:
        servicios_ok = diagnosticar_conexion_test()
        if not servicios_ok:
            print("\n[WARN] Los servicios no funcionan correctamente")
            print("       Esto es normal si no hay un servidor IBM i real disponible")
    
    print("\n[INFO] Enlaces utiles:")
    print("       - jt400.jar: https://sourceforge.net/projects/jt400/")
    print("       - IBM i Access: https://www.ibm.com/support/pages/ibm-i-access-client-solutions")
    
if __name__ == "__main__":
    main()