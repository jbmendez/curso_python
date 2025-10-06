@echo off
REM Script para instalar Java 11 y configurar JAVA_HOME automáticamente
echo ===============================================
echo  INSTALADOR JAVA 11 PARA IBM i SERIES
echo ===============================================
echo.

REM Crear directorio temporal
set TEMP_DIR=%TEMP%\java_install
if not exist "%TEMP_DIR%" mkdir "%TEMP_DIR%"

echo [1/5] Descargando OpenJDK 11...
echo Esto puede tomar varios minutos...

REM URL de OpenJDK 11 para Windows x64
set JAVA_URL=https://github.com/adoptium/temurin11-binaries/releases/download/jdk-11.0.21+9/OpenJDK11U-jdk_x64_windows_hotspot_11.0.21_9.zip
set JAVA_ZIP=%TEMP_DIR%\openjdk11.zip

REM Descargar Java usando PowerShell
powershell -Command "& {[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12; Invoke-WebRequest -Uri '%JAVA_URL%' -OutFile '%JAVA_ZIP%'}"

if not exist "%JAVA_ZIP%" (
    echo ERROR: No se pudo descargar Java 11
    echo Descarga manual desde: https://adoptium.net/
    pause
    exit /b 1
)

echo [2/5] Extrayendo Java 11...
REM Extraer usando PowerShell
powershell -Command "Expand-Archive -Path '%JAVA_ZIP%' -DestinationPath '%TEMP_DIR%' -Force"

REM Buscar el directorio extraído
for /d %%i in ("%TEMP_DIR%\jdk*") do set EXTRACTED_DIR=%%i

if not exist "%EXTRACTED_DIR%" (
    echo ERROR: No se pudo extraer Java 11
    pause
    exit /b 1
)

echo [3/5] Instalando Java 11...
REM Mover a Program Files
set JAVA_INSTALL_DIR=C:\Program Files\Java\jdk-11
if exist "%JAVA_INSTALL_DIR%" rmdir /s /q "%JAVA_INSTALL_DIR%"
mkdir "%JAVA_INSTALL_DIR%" 2>nul
xcopy "%EXTRACTED_DIR%\*" "%JAVA_INSTALL_DIR%\" /e /i /h /y

echo [4/5] Configurando variables de entorno...
REM Configurar JAVA_HOME permanentemente
setx JAVA_HOME "%JAVA_INSTALL_DIR%" /M >nul 2>&1
if errorlevel 1 (
    echo ADVERTENCIA: No se pudo configurar JAVA_HOME globalmente
    echo Configurando para usuario actual...
    setx JAVA_HOME "%JAVA_INSTALL_DIR%" >nul
)

REM Obtener PATH actual y agregar Java
for /f "tokens=2*" %%A in ('reg query "HKEY_LOCAL_MACHINE\SYSTEM\CurrentControlSet\Control\Session Manager\Environment" /v Path 2^>nul') do set "SYSTEM_PATH=%%B"
echo %SYSTEM_PATH% | find "%JAVA_INSTALL_DIR%\bin" >nul
if errorlevel 1 (
    setx PATH "%SYSTEM_PATH%;%JAVA_INSTALL_DIR%\bin" /M >nul 2>&1
    if errorlevel 1 (
        echo ADVERTENCIA: No se pudo actualizar PATH globalmente
        echo Configurando PATH para usuario actual...
        setx PATH "%PATH%;%JAVA_INSTALL_DIR%\bin" >nul
    )
)

echo [5/5] Verificando instalación...
REM Configurar variables para esta sesión
set JAVA_HOME=%JAVA_INSTALL_DIR%
set PATH=%JAVA_HOME%\bin;%PATH%

echo.
echo Variables configuradas:
echo JAVA_HOME=%JAVA_HOME%
echo.

REM Probar Java
"%JAVA_HOME%\bin\java.exe" -version
if errorlevel 1 (
    echo ERROR: Java no funciona correctamente
    pause
    exit /b 1
)

echo.
echo [LIMPIEZA] Eliminando archivos temporales...
rmdir /s /q "%TEMP_DIR%" >nul 2>&1

echo.
echo ===============================================
echo  INSTALACION COMPLETADA EXITOSAMENTE
echo ===============================================
echo.
echo Java 11 instalado en: %JAVA_INSTALL_DIR%
echo.
echo IMPORTANTE:
echo 1. Reinicia tu terminal/IDE para usar la nueva versión
echo 2. Verifica con: java -version
echo 3. Ahora puedes usar JDBC con IBM i Series
echo.
echo Presiona cualquier tecla para continuar...
pause >nul