#!/usr/bin/env python3
"""
Diagnóstico y solución de problemas de versión de Java.
Detecta versiones incompatibles y proporciona soluciones.
"""

import subprocess
import sys
import os
from pathlib import Path

def verificar_java():
    """Verifica las versiones de Java disponibles."""
    print("[JAVA] Verificando instalaciones de Java...")
    
    # Verificar Java en PATH
    try:
        result = subprocess.run(['java', '-version'], 
                              capture_output=True, text=True, timeout=10)
        java_version = result.stderr.split('\n')[0] if result.stderr else "No disponible"
        print(f"[INFO] Java en PATH: {java_version}")
        
        # Extraer número de versión
        if "1.8" in java_version or '"8' in java_version:
            print("[WARN] Java 8 detectado - INCOMPATIBLE con JPype moderno")
            return False, "8"
        elif "11" in java_version:
            print("[OK] Java 11 detectado - COMPATIBLE")
            return True, "11"
        elif "17" in java_version:
            print("[OK] Java 17 detectado - COMPATIBLE")
            return True, "17"
        elif "21" in java_version:
            print("[OK] Java 21 detectado - COMPATIBLE")
            return True, "21"
        else:
            print(f"[WARN] Versión de Java no reconocida: {java_version}")
            return False, "unknown"
            
    except (subprocess.TimeoutExpired, FileNotFoundError):
        print("[ERROR] Java no encontrado en PATH")
        return False, "none"

def buscar_javas_sistema():
    """Busca instalaciones de Java en el sistema."""
    print("\n[SEARCH] Buscando instalaciones de Java en el sistema...")
    
    java_paths = []
    
    # Rutas comunes de Java en Windows
    common_paths = [
        Path("C:/Program Files/Java"),
        Path("C:/Program Files (x86)/Java"),
        Path("C:/Program Files/OpenJDK"),
        Path("C:/Program Files/Eclipse Adoptium"),
        Path("C:/Program Files/Amazon Corretto"),
        Path(os.environ.get("JAVA_HOME", "")) if os.environ.get("JAVA_HOME") else None
    ]
    
    for base_path in common_paths:
        if base_path and base_path.exists():
            print(f"[FOUND] Directorio Java: {base_path}")
            
            # Buscar subdirectorios con versiones
            for item in base_path.iterdir():
                if item.is_dir():
                    java_exe = item / "bin" / "java.exe"
                    if java_exe.exists():
                        try:
                            result = subprocess.run([str(java_exe), '-version'], 
                                                  capture_output=True, text=True, timeout=5)
                            version_line = result.stderr.split('\n')[0] if result.stderr else ""
                            java_paths.append({
                                'path': str(java_exe),
                                'version': version_line,
                                'compatible': not ("1.8" in version_line or '"8' in version_line)
                            })
                            print(f"  - {item.name}: {version_line}")
                        except:
                            continue
    
    return java_paths

def verificar_jpype_version():
    """Verifica la versión de JPype instalada."""
    print("\n[JPYPE] Verificando versión de JPype...")
    
    try:
        import jpype
        version = jpype.__version__
        print(f"[INFO] JPype versión: {version}")
        
        # Versiones JPype compatibles con Java 8
        if version.startswith("1.2") or version.startswith("1.3"):
            print("[INFO] Versión JPype compatible con Java 8")
            return True, version
        else:
            print("[WARN] Versión JPype moderna - requiere Java 11+")
            return False, version
            
    except ImportError:
        print("[ERROR] JPype no está instalado")
        return False, None

def proponer_soluciones(java_compatible, java_version, jpype_compatible, jpype_version, java_paths):
    """Propone soluciones basadas en el diagnóstico."""
    print("\n" + "=" * 60)
    print("[SOLUCIONES] Opciones para resolver el problema:")
    
    compatible_javas = [j for j in java_paths if j['compatible']]
    
    if compatible_javas:
        print("\n[OPCION 1] Cambiar a Java compatible (RECOMENDADO)")
        print("  Tienes Java 11+ instalado pero no está en PATH")
        for java in compatible_javas:
            print(f"  - {java['version']}")
            print(f"    Ruta: {java['path']}")
        
        print("\n  PASOS:")
        print("  1. Configura JAVA_HOME:")
        best_java = compatible_javas[0]['path'].replace('\\bin\\java.exe', '')
        print(f"     set JAVA_HOME={best_java}")
        print("  2. Actualiza PATH:")
        print(f"     set PATH=%JAVA_HOME%\\bin;%PATH%")
        print("  3. Reinicia el terminal y prueba de nuevo")
        
    else:
        print("\n[OPCION 1] Instalar Java 11+ (RECOMENDADO)")
        print("  Descarga e instala una versión moderna de Java:")
        print("  - OpenJDK 11: https://jdk.java.net/11/")
        print("  - OpenJDK 17: https://jdk.java.net/17/")
        print("  - Eclipse Temurin: https://adoptium.net/")
    
    if jpype_version and jpype_version.startswith("1."):
        print("\n[OPCION 2] Downgrade JPype (alternativa)")
        print("  Instalar versión JPype compatible con Java 8:")
        print("  pip uninstall JPype1")
        print("  pip install JPype1==1.3.0")
        print("  NOTA: Esto puede causar otros problemas de compatibilidad")
    
    print("\n[OPCION 3] Usar solo ODBC (sin JDBC)")
    print("  Si no necesitas JDBC, puedes:")
    print("  1. Configurar driver_type='odbc' en conexiones")
    print("  2. Solo usar el driver ODBC de IBM i")
    print("  3. Evitar completamente el problema de Java")

def crear_script_configuracion():
    """Crea un script para configurar Java automáticamente."""
    print("\n[SCRIPT] Creando script de configuración...")
    
    java_paths = buscar_javas_sistema()
    compatible_javas = [j for j in java_paths if j['compatible']]
    
    if compatible_javas:
        best_java = compatible_javas[0]['path'].replace('\\bin\\java.exe', '').replace('/', '\\')
        
        script_content = f'''@echo off
REM Script para configurar Java compatible con JPype
echo Configurando Java para IBM i Series...

REM Configurar JAVA_HOME
set JAVA_HOME={best_java}
echo JAVA_HOME configurado: %JAVA_HOME%

REM Actualizar PATH
set PATH=%JAVA_HOME%\\bin;%PATH%
echo PATH actualizado

REM Verificar configuración
echo.
echo Verificando configuración:
java -version
echo.

REM Configurar variables permanentemente (opcional)
echo Para hacer permanente esta configuración:
echo 1. Ve a "Sistema" en Configuración de Windows
echo 2. Clic en "Configuración avanzada del sistema"
echo 3. Clic en "Variables de entorno"
echo 4. Agrega/edita JAVA_HOME: {best_java}
echo 5. Agrega %%JAVA_HOME%%\\bin al PATH

pause
'''
        
        script_path = Path("configurar_java.bat")
        with open(script_path, 'w', encoding='utf-8') as f:
            f.write(script_content)
        
        print(f"[OK] Script creado: {script_path.absolute()}")
        print("     Ejecuta 'configurar_java.bat' para configurar Java")
        return True
    
    return False

def main():
    """Función principal de diagnóstico."""
    print("[DIAG] DIAGNOSTICO DE PROBLEMA JAVA + JPYPE")
    print("=" * 60)
    
    # 1. Verificar Java actual
    java_compatible, java_version = verificar_java()
    
    # 2. Buscar otras instalaciones
    java_paths = buscar_javas_sistema()
    
    # 3. Verificar JPype
    jpype_compatible, jpype_version = verificar_jpype_version()
    
    # 4. Proponer soluciones
    proponer_soluciones(java_compatible, java_version, jpype_compatible, jpype_version, java_paths)
    
    # 5. Crear script si es posible
    if crear_script_configuracion():
        print("\n[NEXT] Ejecuta: configurar_java.bat")
    
    print("\n" + "=" * 60)
    print("[RESUMEN] El problema es incompatibilidad Java 8 + JPype moderno")
    print("          Solución: Usar Java 11+ o JPype 1.3.0")

if __name__ == "__main__":
    main()