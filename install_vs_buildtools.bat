@echo off
REM Script para instalar Visual Studio Build Tools automáticamente
echo ===============================================
echo  INSTALADOR VISUAL STUDIO BUILD TOOLS
echo  (Necesario para compilar JPype)
echo ===============================================
echo.

REM Verificar si ya están instalados
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2019 ya instalados
    goto :end
)

if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2022 ya instalados
    goto :end
)

echo Descargando Visual Studio Build Tools...
echo.

REM Crear directorio temporal
set TEMP_DIR=%TEMP%\vs_buildtools
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

REM URL de Visual Studio Build Tools
set VS_URL=https://aka.ms/vs/17/release/vs_buildtools.exe
set VS_INSTALLER=%TEMP_DIR%\vs_buildtools.exe

echo Descargando desde: %VS_URL%
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%VS_URL%' -OutFile '%VS_INSTALLER%'}"

if not exist "%VS_INSTALLER%" (
    echo ❌ Error descargando Visual Studio Build Tools
    echo.
    echo DESCARGA MANUAL:
    echo 1. Ve a: https://visualstudio.microsoft.com/visual-cpp-build-tools/
    echo 2. Descarga "Build Tools for Visual Studio"
    echo 3. Instala con "C++ build tools" seleccionado
    pause
    exit /b 1
)

echo.
echo Instalando Visual Studio Build Tools...
echo IMPORTANTE: En la ventana que se abre:
echo 1. Selecciona "C++ build tools"
echo 2. En la pestaña derecha, asegúrate que esté marcado:
echo    - MSVC v143 compiler toolset
echo    - Windows 10/11 SDK
echo 3. Clic en "Install"
echo.
echo Presiona cualquier tecla para abrir el instalador...
pause

REM Ejecutar instalador
start /wait "%VS_INSTALLER%" --quiet --wait --add Microsoft.VisualStudio.Workload.VCTools --add Microsoft.VisualStudio.Component.VC.Tools.x86.x64 --add Microsoft.VisualStudio.Component.Windows10SDK.19041

if %errorlevel% neq 0 (
    echo.
    echo ⚠️  Instalación automática falló. Ejecutando modo manual...
    "%VS_INSTALLER%"
    echo.
    echo Después de instalar, presiona cualquier tecla...
    pause
)

:end
echo.
echo ===============================================
echo  INSTALACIÓN COMPLETADA
echo ===============================================
echo.
echo PRÓXIMO PASO: Ejecutar install_jpype_java8.bat
echo.
pause