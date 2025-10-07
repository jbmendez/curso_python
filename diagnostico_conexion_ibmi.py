#!/usr/bin/env python3
"""
Herramienta de diagnóstico para conexiones IBM i Series
"""
import socket
import subprocess
import os
import sys

def verificar_conectividad_red(servidor, puerto=446):
    """Verifica conectividad de red básica"""
    print(f"🔍 Verificando conectividad de red a {servidor}:{puerto}")
    
    try:
        # Ping al servidor
        print(f"  📡 Haciendo ping a {servidor}...")
        resultado_ping = subprocess.run(
            ["ping", "-n", "1", servidor], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if resultado_ping.returncode == 0:
            print(f"  ✅ Ping exitoso a {servidor}")
        else:
            print(f"  ❌ Ping falló a {servidor}")
            print(f"     Salida: {resultado_ping.stdout}")
            return False
            
    except Exception as e:
        print(f"  ❌ Error en ping: {str(e)}")
        return False
    
    try:
        # Verificar puerto
        print(f"  🔌 Verificando puerto {puerto}...")
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(10)
        resultado = sock.connect_ex((servidor, puerto))
        sock.close()
        
        if resultado == 0:
            print(f"  ✅ Puerto {puerto} accesible")
            return True
        else:
            print(f"  ❌ Puerto {puerto} no accesible (código: {resultado})")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando puerto: {str(e)}")
        return False

def verificar_driver_jt400():
    """Verifica que el driver JT400 esté disponible"""
    print("🔍 Verificando driver JT400...")
    
    driver_path = os.path.join(os.getcwd(), "drivers", "jt400.jar")
    
    if os.path.exists(driver_path):
        size = os.path.getsize(driver_path)
        print(f"  ✅ Driver encontrado: {driver_path} ({size} bytes)")
        return True
    else:
        print(f"  ❌ Driver no encontrado en: {driver_path}")
        return False

def verificar_jaydebeapi():
    """Verifica que jaydebeapi esté instalado"""
    print("🔍 Verificando jaydebeapi...")
    
    try:
        import jaydebeapi
        print(f"  ✅ jaydebeapi instalado: {jaydebeapi.__file__}")
        return True
    except ImportError:
        print("  ❌ jaydebeapi no está instalado")
        print("     Instalar con: pip install jaydebeapi")
        return False

def verificar_java():
    """Verifica que Java esté disponible"""
    print("🔍 Verificando Java...")
    
    try:
        resultado = subprocess.run(
            ["java", "-version"], 
            capture_output=True, 
            text=True, 
            timeout=10
        )
        
        if resultado.returncode == 0:
            version_info = resultado.stderr.split('\n')[0]
            print(f"  ✅ Java disponible: {version_info}")
            return True
        else:
            print("  ❌ Java no está disponible")
            return False
            
    except Exception as e:
        print(f"  ❌ Error verificando Java: {str(e)}")
        return False

def probar_conexion_jdbc(servidor, usuario, contraseña, puerto=446):
    """Prueba conexión JDBC básica"""
    print(f"🔍 Probando conexión JDBC a {servidor}...")
    
    try:
        import jaydebeapi
        
        driver_path = os.path.join(os.getcwd(), "drivers", "jt400.jar")
        jdbc_url = f"jdbc:as400://{servidor}:{puerto}"
        driver_class = "com.ibm.as400.access.AS400JDBCDriver"
        
        print(f"  🔗 URL: {jdbc_url}")
        print(f"  👤 Usuario: {usuario}")
        print(f"  📦 Driver: {driver_path}")
        
        # Configuración mínima
        connection_props = {
            'user': usuario,
            'password': contraseña,
            'prompt': 'false',
            'thread used': 'false'
        }
        
        print("  🔄 Intentando conexión...")
        conn = jaydebeapi.connect(
            driver_class,
            jdbc_url,
            connection_props,
            driver_path
        )
        
        print("  ✅ Conexión JDBC exitosa!")
        
        # Probar consulta simple
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_TIMESTAMP FROM SYSIBM.SYSDUMMY1")
        resultado = cursor.fetchone()
        print(f"  📅 Timestamp del servidor: {resultado[0]}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"  ❌ Error en conexión JDBC: {str(e)}")
        return False

def main():
    print("🚀 Diagnóstico de Conexión IBM i Series")
    print("=" * 50)
    
    # Datos de conexión
    servidor = "172.20.0.10"
    usuario = "jmendez"
    contraseña = "barbiet9"
    puerto = 446
    
    print(f"📋 Datos de conexión:")
    print(f"   Servidor: {servidor}")
    print(f"   Puerto: {puerto}")
    print(f"   Usuario: {usuario}")
    print()
    
    resultados = []
    
    # 1. Verificar conectividad de red
    resultados.append(verificar_conectividad_red(servidor, puerto))
    print()
    
    # 2. Verificar Java
    resultados.append(verificar_java())
    print()
    
    # 3. Verificar jaydebeapi
    resultados.append(verificar_jaydebeapi())
    print()
    
    # 4. Verificar driver JT400
    resultados.append(verificar_driver_jt400())
    print()
    
    # 5. Si todo está bien, probar conexión JDBC
    if all(resultados):
        print("🎯 Todos los prerequisitos están bien. Probando conexión JDBC...")
        resultado_jdbc = probar_conexion_jdbc(servidor, usuario, contraseña, puerto)
        resultados.append(resultado_jdbc)
    else:
        print("⚠️  Algunos prerequisitos fallan. Saltando prueba JDBC.")
    
    print()
    print("📊 Resumen:")
    print("=" * 30)
    pruebas = [
        "Conectividad de red",
        "Java disponible", 
        "jaydebeapi instalado",
        "Driver JT400",
        "Conexión JDBC"
    ]
    
    for i, (prueba, resultado) in enumerate(zip(pruebas, resultados)):
        if i < len(resultados):
            estado = "✅ OK" if resultado else "❌ FALLO"
            print(f"{prueba}: {estado}")
    
    if all(resultados):
        print("\n🎉 ¡Todas las pruebas pasaron! La conexión debería funcionar.")
    else:
        print("\n⚠️  Hay problemas que resolver antes de que la conexión funcione.")

if __name__ == "__main__":
    main()