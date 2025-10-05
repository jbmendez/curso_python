@echo off
REM ===============================================
REM Sistema de Gestión de Controles SQL
REM Script de Instalación para Windows
REM Clean Architecture + Tkinter GUI
REM ===============================================

echo.
echo ======================================================
echo 🏦 SISTEMA DE GESTION DE CONTROLES SQL - WINDOWS
echo ======================================================
echo 🏗️  Arquitectura: Clean Architecture
echo 📋 Interfaz: Tkinter Desktop
echo 💾 Base de datos: SQLite
echo 🪟 Plataforma: Windows
echo ======================================================
echo.

REM Verificar Python
echo 🔍 Verificando Python...
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python no encontrado en el sistema
    echo.
    echo 💡 SOLUCIÓN:
    echo    1. Descargar Python desde: https://python.org/downloads/
    echo    2. Durante instalación, marcar: "Add Python to PATH"
    echo    3. Reinstalar Python 3.8 o superior
    echo.
    pause
    exit /b 1
)

REM Mostrar versión de Python
for /f "tokens=2" %%i in ('python --version') do set PYTHON_VERSION=%%i
echo ✅ Python %PYTHON_VERSION% detectado

REM Verificar Tkinter
echo 🔍 Verificando Tkinter...
python -c "import tkinter" 2>nul
if %errorlevel% neq 0 (
    echo ❌ Tkinter no disponible
    echo.
    echo 💡 SOLUCIÓN:
    echo    1. Reinstalar Python desde python.org (NO Anaconda)
    echo    2. Tkinter viene incluido en instalaciones oficiales
    echo    3. Verificar que la instalación sea completa
    echo.
    pause
    exit /b 1
)
echo ✅ Tkinter disponible

REM Verificar estructura del proyecto
echo 🔍 Verificando estructura del proyecto...
if not exist "src\" (
    echo ❌ Directorio src/ no encontrado
    echo 💡 Asegúrate de estar en el directorio raíz del proyecto
    pause
    exit /b 1
)

if not exist "main_gui.py" (
    echo ❌ Archivo main_gui.py no encontrado
    echo 💡 Asegúrate de estar en el directorio raíz del proyecto
    pause
    exit /b 1
)
echo ✅ Estructura del proyecto OK

REM Crear directorio de datos si no existe
echo 📁 Preparando directorios...
if not exist "data\" mkdir data
if not exist "logs\" mkdir logs
echo ✅ Directorios preparados

REM Mostrar información del sistema
echo.
echo 📊 INFORMACIÓN DEL SISTEMA:
echo    🖥️  OS: %OS%
echo    💻 Usuario: %USERNAME%
echo    📁 Directorio: %CD%
echo    🐍 Python: %PYTHON_VERSION%
echo.

REM Preguntar si continuar
set /p CONTINUAR="🚀 ¿Iniciar la aplicación? (S/N): "
if /i not "%CONTINUAR%"=="S" (
    echo ⏹️  Instalación cancelada por el usuario
    pause
    exit /b 0
)

echo.
echo 🚀 Iniciando Sistema de Gestión de Controles SQL...
echo ⏱️  Esto puede tomar unos segundos...
echo.

REM Ejecutar la aplicación
python main_gui.py

REM Verificar si la aplicación se cerró correctamente
if %errorlevel% equ 0 (
    echo.
    echo ✅ Aplicación cerrada correctamente
) else (
    echo.
    echo ⚠️  La aplicación se cerró con código: %errorlevel%
    echo 💡 Revisa los logs para más información
)

echo.
echo 📚 RECURSOS ADICIONALES:
echo    📖 Documentación: README_GUI.md
echo    🔧 Configuración Windows: WINDOWS_SETUP.md
echo    🧪 Test de compatibilidad: python test_tkinter.py
echo    🏗️  Arquitectura: docs/clean-architecture.md
echo.

pause