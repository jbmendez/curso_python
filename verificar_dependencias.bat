@echo off
REM Script para verificar dependencias del Sistema de Controles
echo 🔍 VERIFICACION DE DEPENDENCIAS
echo ===============================
echo.

REM Verificar Python
echo 📋 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no está instalado o no está en el PATH
    goto :fin
) else (
    echo ✅ Python detectado:
    python --version
)

REM Verificar Java
echo.
echo ☕ Verificando Java...
set JAVA_HOME=C:\Program Files\Java\jdk-11
if not exist "%JAVA_HOME%" (
    echo ❌ Java 11 no encontrado en %JAVA_HOME%
) else (
    echo ✅ Java 11 detectado en %JAVA_HOME%
)

echo.
echo 📦 Verificando paquetes Python...
echo ----------------------------------------

REM Verificar cada dependencia crítica
echo Verificando openpyxl...
python -c "try: import openpyxl; print('✅ openpyxl instalado - Version:', openpyxl.__version__); except ImportError: print('❌ openpyxl NO instalado')" 2>nul

echo Verificando jpype1...
python -c "try: import jpype; print('✅ jpype1 instalado'); except ImportError: print('❌ jpype1 NO instalado')" 2>nul

echo Verificando jaydebeapi...
python -c "try: import jaydebeapi; print('✅ jaydebeapi instalado'); except ImportError: print('❌ jaydebeapi NO instalado')" 2>nul

echo Verificando pyodbc...
python -c "try: import pyodbc; print('✅ pyodbc instalado - Version:', pyodbc.version); except ImportError: print('❌ pyodbc NO instalado')" 2>nul

echo Verificando psutil...
python -c "try: import psutil; print('✅ psutil instalado - Version:', psutil.version_info); except ImportError: print('❌ psutil NO instalado')" 2>nul

echo Verificando email-validator...
python -c "try: import email_validator; print('✅ email-validator instalado'); except ImportError: print('⚠️ email-validator no instalado (opcional)')" 2>nul

echo.
echo 🔧 Verificando archivos críticos...
echo ----------------------------------------

if exist "sistema_controles.db" (
    echo ✅ Base de datos encontrada: sistema_controles.db
) else (
    echo ⚠️ Base de datos no existe: sistema_controles.db
)

if exist "drivers\jt400.jar" (
    echo ✅ Driver iSeries encontrado: drivers\jt400.jar
) else (
    echo ❌ Driver iSeries NO encontrado: drivers\jt400.jar
)

if exist "logs" (
    echo ✅ Carpeta de logs existe: logs\
) else (
    echo ⚠️ Carpeta de logs no existe: logs\
)

echo.
echo 🎯 RESUMEN DE VERIFICACION
echo ========================
echo.
echo Si hay elementos con ❌, ejecuta:
echo   📦 Para dependencias Python: pip install -r requirements.txt
echo   📄 Para driver iSeries: descargar jt400.jar a drivers\
echo   📊 Para base de datos: py -c "from src.infrastructure.database.database_setup import DatabaseSetup; DatabaseSetup().initialize_database()"
echo.

:fin
pause