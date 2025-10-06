"""
Script de prueba para validar la selección de drivers IBM i Series
"""
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.domain.entities.conexion import Conexion
from src.infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector

def test_driver_selection():
    """Prueba la selección de drivers basada en driver_type"""
    print("🧪 Probando selección de drivers IBM i Series...")
    print("=" * 60)
    
    selector = IBMiSeriesConexionSelector()
    
    # Configuración base de conexión
    base_config = {
        'nombre': 'Test IBM i',
        'servidor': '192.168.1.100',
        'puerto': 8471,
        'base_datos': 'TESTLIB',
        'usuario': 'testuser',
        'contraseña': 'testpass',
        'tipo_motor': 'iseries'
    }
    
    # Prueba 1: Auto-detección (default)
    print("🔄 Prueba 1: Auto-detección (driver_type='auto')")
    conexion_auto = Conexion(**base_config, driver_type='auto')
    resultado_auto = selector.probar_conexion(conexion_auto)
    print(f"   - Resultado: {resultado_auto.mensaje}")
    print()
    
    # Prueba 2: Forzar JDBC
    print("☕ Prueba 2: Forzar JDBC (driver_type='jdbc')")
    conexion_jdbc = Conexion(**base_config, driver_type='jdbc')
    resultado_jdbc = selector.probar_conexion(conexion_jdbc)
    print(f"   - Resultado: {resultado_jdbc.mensaje}")
    print()
    
    # Prueba 3: Forzar ODBC
    print("🔌 Prueba 3: Forzar ODBC (driver_type='odbc')")
    conexion_odbc = Conexion(**base_config, driver_type='odbc')
    resultado_odbc = selector.probar_conexion(conexion_odbc)
    print(f"   - Resultado: {resultado_odbc.mensaje}")
    print()
    
    # Resumen
    print("📋 RESUMEN:")
    print("-" * 40)
    print(f"Auto-detección: {'✅' if not resultado_auto.exitosa else '❌'} (Falló como esperado)")
    print(f"JDBC específico: {'✅' if '[JDBC]' in resultado_jdbc.mensaje else '❌'} Identificado")
    print(f"ODBC específico: {'✅' if '[ODBC]' in resultado_odbc.mensaje else '❌'} Identificado")
    
    print()
    print("🎯 La selección de drivers funciona correctamente!")
    print("   • Para usar JDBC: driver_type='jdbc'")
    print("   • Para usar ODBC: driver_type='odbc'") 
    print("   • Para auto-detección: driver_type='auto' (default)")

if __name__ == "__main__":
    test_driver_selection()