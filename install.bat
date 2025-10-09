@echo off
REM Script de instalación completa para Sistema de Controles
echo 🚀 INSTALACION DEL SISTEMA DE CONTROLES
echo =========================================
echo.

REM Verificar que Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    echo    Instala Python desde https://python.org
    pause
    exit /b 1
)

echo ✅ Python detectado:
python --version

REM Verificar que Java 11 está instalado
set JAVA_HOME=C:\Program Files\Java\jdk-11
if not exist "%JAVA_HOME%" (
    echo ❌ Java 11 no encontrado en %JAVA_HOME%
    echo    Instala Java 11 JDK para JPype/iSeries
    pause
    exit /b 1
)

echo ✅ Java 11 detectado en %JAVA_HOME%

REM Verificar dependencias críticas existentes
echo.
echo 🔍 Verificando dependencias existentes...

REM Verificar openpyxl
python -c "try: import openpyxl; print('✅ openpyxl ya instalado:', openpyxl.__version__); except ImportError: print('⚠️ openpyxl no instalado')" 2>nul

REM Verificar jpype1
python -c "try: import jpype; print('✅ jpype1 ya instalado'); except ImportError: print('⚠️ jpype1 no instalado')" 2>nul

REM Verificar pyodbc
python -c "try: import pyodbc; print('✅ pyodbc ya instalado:', pyodbc.version); except ImportError: print('⚠️ pyodbc no instalado')" 2>nul

REM Verificar jaydebeapi
python -c "try: import jaydebeapi; print('✅ jaydebeapi ya instalado'); except ImportError: print('⚠️ jaydebeapi no instalado')" 2>nul

REM Verificar psutil
python -c "try: import psutil; print('✅ psutil ya instalado:', psutil.version_info); except ImportError: print('⚠️ psutil no instalado')" 2>nul

REM Instalar dependencias de Python
echo.
echo 📦 Instalando dependencias de Python...
pip install -r requirements.txt

if %errorlevel% neq 0 (
    echo ❌ Error instalando dependencias de Python
    pause
    exit /b 1
)

echo ✅ Dependencias de Python instaladas

REM Verificar que jt400.jar existe
if not exist "drivers\jt400.jar" (
    echo ⚠️  IMPORTANTE: drivers\jt400.jar no encontrado
    echo    Descarga jt400.jar desde IBM y colócalo en la carpeta drivers\
    echo    URL: https://www.ibm.com/support/pages/java-toolbox-i-jtopen
)

REM Crear base de datos si no existe
if not exist "sistema_controles.db" (
    echo 📊 Creando base de datos inicial...
    python -c "from src.infrastructure.database.database_setup import DatabaseSetup; db = DatabaseSetup(); db.initialize_database(); print('✅ Base de datos creada')"
)

REM Crear carpeta de logs
if not exist "logs" mkdir logs

echo.
echo 🎉 INSTALACION COMPLETADA
echo ========================
echo.
echo 📋 Para usar el sistema:
echo   🖥️  Abrir GUI:           start_gui.bat
echo   ⚙️  Gestionar motor:     py gestionar_motor.py [iniciar^|detener^|estado]
echo   🔧 Ejecutar motor:       py motor_ejecucion.py
echo   📊 Verificar datos:      py verificar_db.py
echo.
echo 📁 Archivos importantes:
echo   📄 Base de datos:        sistema_controles.db
echo   📂 Logs:                 logs\
echo   🔧 Configuración:        src\infrastructure\config\
echo.
pause