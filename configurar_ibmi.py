#!/usr/bin/env python3
"""
Script de configuración automática para drivers IBM i Series.
Detecta problemas comunes y proporciona soluciones automáticas.
"""

import os
import sys
import subprocess
import urllib.request
import zipfile
from pathlib import Path

def print_banner():
    """Muestra el banner del script."""
    print("=" * 60)
    print("🔧 CONFIGURADOR AUTOMÁTICO IBM i SERIES")
    print("   Diagnóstico y corrección de drivers JDBC/ODBC")
    print("=" * 60)

def check_python_requirements():
    """Verifica e instala dependencias de Python."""
    print("\n📦 Verificando dependencias de Python...")
    
    required_packages = [
        "jaydebeapi>=1.2.3",
        "pyodbc>=4.0.0",
        "JPype1>=1.4.0"
    ]
    
    for package in required_packages:
        try:
            module_name = package.split(">=")[0].split("==")[0]
            if module_name == "JPype1":
                module_name = "jpype"
            __import__(module_name)
            print(f"✅ {package} - OK")
        except ImportError:
            print(f"❌ {package} - FALTA")
            print(f"   Instalando {package}...")
            try:
                subprocess.check_call([sys.executable, "-m", "pip", "install", package])
                print(f"✅ {package} - INSTALADO")
            except subprocess.CalledProcessError:
                print(f"❌ Error instalando {package}")
                return False
    
    return True

def setup_jdbc_driver():
    """Configura el driver JDBC descargando jt400.jar si es necesario."""
    print("\n🔌 Configurando driver JDBC...")
    
    drivers_dir = Path("drivers")
    drivers_dir.mkdir(exist_ok=True)
    
    jt400_path = drivers_dir / "jt400.jar"
    
    if jt400_path.exists():
        print("✅ jt400.jar ya existe")
        return True
    
    print("📥 Descargando jt400.jar desde Maven Central...")
    
    # URL oficial de Maven Central para JT400
    jt400_url = "https://repo1.maven.org/maven2/net/sf/jt400/jt400/20.0.7/jt400-20.0.7.jar"
    
    try:
        print(f"   Descargando desde: {jt400_url}")
        urllib.request.urlretrieve(jt400_url, jt400_path)
        
        # Verificar que el archivo se descargó correctamente
        if jt400_path.exists() and jt400_path.stat().st_size > 1000000:  # Al menos 1MB
            print(f"✅ jt400.jar descargado exitosamente ({jt400_path.stat().st_size // 1024} KB)")
            return True
        else:
            print("❌ Error: archivo descargado parece incompleto")
            if jt400_path.exists():
                jt400_path.unlink()
            return False
            
    except Exception as e:
        print(f"❌ Error descargando jt400.jar: {e}")
        print("\n🔧 SOLUCIÓN MANUAL:")
        print("1. Visita: https://mvnrepository.com/artifact/net.sf.jt400/jt400")
        print("2. Descarga la última versión de jt400.jar")
        print(f"3. Coloca el archivo en: {jt400_path.absolute()}")
        return False

def check_odbc_driver():
    """Verifica la disponibilidad del driver ODBC."""
    print("\n🔌 Verificando driver ODBC...")
    
    try:
        import pyodbc
        drivers = pyodbc.drivers()
        
        # Buscar drivers IBM i
        ibmi_drivers = [d for d in drivers if any(term in d.upper() 
                       for term in ['IBM', 'DB2', 'ISERIES', 'AS400'])]
        
        if ibmi_drivers:
            print("✅ Drivers ODBC IBM i encontrados:")
            for driver in ibmi_drivers:
                print(f"   - {driver}")
            return True
        else:
            print("❌ No se encontraron drivers ODBC para IBM i")
            print("\n🔧 SOLUCIÓN:")
            print("1. Instala IBM i Access for Windows")
            print("2. O instala IBM Data Server Driver Package")
            print("3. Reinicia el sistema después de la instalación")
            return False
            
    except ImportError:
        print("❌ pyodbc no está disponible")
        return False
    except Exception as e:
        print(f"❌ Error verificando drivers ODBC: {e}")
        return False

def test_connectivity():
    """Prueba la conectividad básica usando el sistema de diagnóstico."""
    print("\n🔍 Probando conectividad...")
    
    try:
        # Ejecutar el diagnóstico existente
        result = subprocess.run([sys.executable, "diagnostico_ibmi.py"], 
                              capture_output=True, text=True, timeout=30)
        
        if result.returncode == 0:
            print("✅ Diagnóstico ejecutado exitosamente")
            # Mostrar solo las líneas más importantes
            lines = result.stdout.split('\n')
            for line in lines:
                if any(term in line for term in ['✅', '❌', 'ERROR', 'DISPONIBLE', 'FALTA']):
                    print(f"   {line}")
        else:
            print("❌ Error en diagnóstico")
            print(f"   {result.stderr}")
            
    except subprocess.TimeoutExpired:
        print("⏱️ Diagnóstico tomó demasiado tiempo")
    except FileNotFoundError:
        print("❌ No se encontró diagnostico_ibmi.py")
    except Exception as e:
        print(f"❌ Error ejecutando diagnóstico: {e}")

def create_example_connection():
    """Crea un archivo de ejemplo con configuración de conexión."""
    print("\n📝 Creando ejemplo de configuración...")
    
    example_content = '''"""
Ejemplo de configuración para conexión IBM i Series.
Copia este archivo y personaliza con tus datos.
"""

# Datos de conexión de ejemplo
CONEXION_EJEMPLO = {
    "nombre": "MiIBMi",
    "motor": "ibmiseries",
    "servidor": "192.168.1.100",  # IP de tu sistema IBM i
    "puerto": 446,                # Puerto estándar para JDBC
    "base_datos": "MYLIB",        # Biblioteca inicial
    "usuario": "MIUSUARIO",       # Usuario IBM i
    "contrasena": "MIPASSWORD",   # Contraseña
    "driver_type": "auto"         # auto, jdbc, odbc
}

# Para probar desde código:
if __name__ == "__main__":
    from src.domain.entities.conexion import Conexion
    from src.infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector
    
    # Crear entidad de conexión
    conexion = Conexion(
        nombre=CONEXION_EJEMPLO["nombre"],
        motor=CONEXION_EJEMPLO["motor"],
        servidor=CONEXION_EJEMPLO["servidor"],
        puerto=CONEXION_EJEMPLO["puerto"],
        base_datos=CONEXION_EJEMPLO["base_datos"],
        usuario=CONEXION_EJEMPLO["usuario"],
        contrasena=CONEXION_EJEMPLO["contrasena"],
        driver_type=CONEXION_EJEMPLO["driver_type"]
    )
    
    # Probar conexión
    selector = IBMiSeriesConexionSelector()
    resultado = selector.probar_conexion(conexion)
    
    print(f"Resultado: {resultado.mensaje}")
    if not resultado.exitosa:
        print(f"Error: {resultado.detalles_error}")
'''
    
    example_path = Path("ejemplo_conexion_ibmi.py")
    with open(example_path, 'w', encoding='utf-8') as f:
        f.write(example_content)
    
    print(f"✅ Creado: {example_path.absolute()}")

def main():
    """Función principal del configurador."""
    print_banner()
    
    success_count = 0
    total_checks = 4
    
    # 1. Verificar dependencias Python
    if check_python_requirements():
        success_count += 1
    
    # 2. Configurar JDBC
    if setup_jdbc_driver():
        success_count += 1
    
    # 3. Verificar ODBC
    if check_odbc_driver():
        success_count += 1
    
    # 4. Crear ejemplo
    try:
        create_example_connection()
        success_count += 1
    except Exception as e:
        print(f"❌ Error creando ejemplo: {e}")
    
    # Resumen final
    print("\n" + "=" * 60)
    print(f"📊 RESUMEN: {success_count}/{total_checks} verificaciones exitosas")
    
    if success_count == total_checks:
        print("🎉 ¡Configuración completa! El sistema está listo.")
        print("\n📋 PRÓXIMOS PASOS:")
        print("1. Edita 'ejemplo_conexion_ibmi.py' con tus datos")
        print("2. Ejecuta: python ejemplo_conexion_ibmi.py")
        print("3. O usa la GUI: python main_gui.py")
    else:
        print("⚠️  Configuración incompleta. Revisa los errores arriba.")
        print("\n🔧 Para soporte adicional:")
        print("- Ejecuta: python diagnostico_ibmi.py")
        print("- Revisa los archivos de documentación")
    
    # Opcional: probar conectividad si todo está configurado
    if success_count >= 3:  # Python deps + al menos un driver
        test_connectivity()
    
    print("=" * 60)

if __name__ == "__main__":
    main()