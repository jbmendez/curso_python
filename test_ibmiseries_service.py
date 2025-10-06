"""
Script de prueba mejorado para validar ODBC IBM i Series.
Incluye timeouts, múltiples configuraciones y diagnóstico detallado.
"""
import sys
import os
import time

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.domain.entities.conexion import Conexion
from src.infrastructure.services.ibmiseries_conexion_test import IBMiSeriesConexionTest

def probar_drivers_disponibles():
    """Lista los drivers ODBC disponibles."""
    print("\n🔍 DRIVERS ODBC DISPONIBLES:")
    try:
        import pyodbc
        drivers = pyodbc.drivers()
        
        print(f"Total de drivers: {len(drivers)}")
        for i, driver in enumerate(drivers, 1):
            es_ibm = any(term in driver.upper() 
                        for term in ['IBM', 'DB2', 'ISERIES', 'AS400'])
            marca = " 🎯 IBM i" if es_ibm else ""
            print(f"  {i:2d}. {driver}{marca}")
            
    except Exception as e:
        print(f"❌ Error listando drivers: {e}")

def probar_configuraciones():
    """Prueba diferentes configuraciones de conexión."""
    print("=" * 60)
    print("🔍 PRUEBA ODBC IBM i SERIES - CONFIGURACIONES MÚLTIPLES")
    print("=" * 60)
    
    # Crear servicio ODBC
    servicio_odbc = IBMiSeriesConexionTest()
    
    # Configuraciones de prueba
    configuraciones_prueba = [
        {
            "nombre": "Prueba SSL",
            "servidor": "172.20.0.10",  # ⚠️ CAMBIA POR TU IP REAL
            "puerto": 446,
            "usuario": "jmendez",        # ⚠️ CAMBIA POR USUARIO REAL
            "contraseña": "barbiet9",     # ⚠️ CAMBIA POR CONTRASEÑA REAL
            "base_datos": "*LIBL",
            "descripcion": "Conexión con SSL (puerto 446)"
        },
        {
            "nombre": "Prueba Sin SSL",
            "servidor": "172.20.0.10",  # ⚠️ CAMBIA POR TU IP REAL
            "puerto": 8471,               # Puerto sin SSL
            "usuario": "jmendez",        # ⚠️ CAMBIA POR USUARIO REAL
            "contraseña": "barbiet9",     # ⚠️ CAMBIA POR CONTRASEÑA REAL
            "base_datos": "*LIBL",
            "descripcion": "Conexión sin SSL (puerto 8471)"
        }
    ]
    
    print("\n⚠️  IMPORTANTE: Edita este archivo con tus datos reales:")
    print("   - servidor: IP de tu IBM i Series")
    print("   - usuario: Usuario válido de IBM i")
    print("   - contraseña: Contraseña correspondiente")
    print("\n" + "=" * 60)
    
    for i, config in enumerate(configuraciones_prueba, 1):
        print(f"\n[PRUEBA {i}] {config['descripcion']}")
        print(f"Servidor: {config['servidor']}:{config['puerto']}")
        print(f"Usuario: {config['usuario']}")
        print(f"Base datos: {config['base_datos']}")
        
        # Crear entidad de conexión
        conexion = Conexion(
            nombre=config["nombre"],
            tipo_motor="ibmiseries",
            servidor=config["servidor"],
            puerto=config["puerto"],
            base_datos=config["base_datos"],
            usuario=config["usuario"],
            contraseña=config["contraseña"],
            driver_type="odbc"
        )
        
        print("\n🔄 Probando conexión con timeouts...")
        start_time = time.time()
        
        try:
            # Probar con timeout
            resultado = servicio_odbc.probar_conexion(conexion)
            elapsed_time = time.time() - start_time
            
            if resultado.exitosa:
                print(f"✅ ÉXITO ({elapsed_time:.2f}s)")
                print(f"   Mensaje: {resultado.mensaje}")
                if resultado.info_adicional:
                    print("   Información del sistema:")
                    for key, value in resultado.info_adicional.items():
                        if len(str(value)) < 100:  # Evitar salida muy larga
                            print(f"     {key}: {value}")
            else:
                print(f"❌ FALLÓ ({elapsed_time:.2f}s)")
                print(f"   Mensaje: {resultado.mensaje}")
                if resultado.detalles_error:
                    print(f"   Detalles: {resultado.detalles_error}")
                
        except Exception as e:
            elapsed_time = time.time() - start_time
            print(f"💥 ERROR CRÍTICO ({elapsed_time:.2f}s)")
            print(f"   Excepción: {str(e)}")
            
        print("-" * 40)

def main():
    """Función principal mejorada."""
    print("🚀 Iniciando pruebas ODBC mejoradas para IBM i Series...")
    
    # Listar drivers disponibles
    probar_drivers_disponibles()
    
    # Ejecutar pruebas de conectividad
    probar_configuraciones()
    
    print("\n" + "=" * 60)
    print("📋 RESUMEN DE PRUEBAS COMPLETADO")
    print("\nSi todas las pruebas fallan:")
    print("1. Verifica que el servidor IBM i esté accesible")
    print("2. Confirma usuario/contraseña correctos")
    print("3. Revisa firewall y conectividad de red")
    print("4. Verifica que el servicio SQL esté activo en IBM i")
    print("5. Prueba con diferentes puertos (446, 8471, 8476)")
    print("=" * 60)

if __name__ == "__main__":
    main()

def test_ibmiseries_service():
    """Prueba el servicio IBM i Series con una conexión ficticia"""
    print("🧪 Probando servicio IBM i Series...")
    
    # Crear una conexión de prueba
    conexion_test = Conexion(
        nombre="Prueba IBM i",
        servidor="192.168.1.100",  # IP ficticia
        puerto=446,
        base_datos="MILIB",
        usuario="usuario_test",
        contraseña="password_test",
        tipo_motor="iseries"
    )
    
    # Crear el servicio
    servicio = IBMiSeriesConexionTest()
    
    # Verificar tipos soportados
    tipos = servicio.tipos_soportados()
    print(f"✅ Tipos soportados: {tipos}")
    
    # Intentar probar conexión (esto fallará por no tener servidor real, pero validará la estructura)
    print("🔗 Intentando probar conexión...")
    resultado = servicio.probar_conexion(conexion_test)
    
    print(f"📋 Resultado:")
    print(f"   - Exitosa: {resultado.exitosa}")
    print(f"   - Mensaje: {resultado.mensaje}")
    print(f"   - Detalles: {resultado.detalles_error}")
    
    if not resultado.exitosa:
        print("✅ Fallo esperado - no hay servidor real para conectar")
        print("✅ El servicio maneja correctamente los errores")
    
    print("🎉 Prueba completada exitosamente!")

if __name__ == "__main__":
    test_ibmiseries_service()