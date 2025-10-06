@echo off
REM Instalación rápida de Java 11 usando Chocolatey
echo ===============================================
echo  INSTALACION RAPIDA JAVA 11 (Chocolatey)
echo ===============================================
echo.

REM Verificar si Chocolatey está instalado
choco --version >nul 2>&1
if errorlevel 1 (
    echo Chocolatey no está instalado.
    echo.
    echo OPCION 1: Instalar Chocolatey primero
    echo 1. Abre PowerShell como Administrador
    echo 2. Ejecuta: Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://community.chocolatey.org/install.ps1'))
    echo 3. Luego ejecuta este script de nuevo
    echo.
    echo OPCION 2: Usar instalador manual
    echo Ejecuta: install_java11.bat
    echo.
    pause
    exit /b 1
)

echo Chocolatey detectado. Instalando Java 11...
echo.

REM Instalar OpenJDK 11
choco install openjdk11 -y

if errorlevel 1 (
    echo Error instalando Java 11 con Chocolatey
    echo Intenta el instalador manual: install_java11.bat
    pause
    exit /b 1
)

echo.
echo ===============================================
echo  INSTALACION COMPLETADA
echo ===============================================
echo.
echo Java 11 instalado exitosamente.
echo.
echo PASOS SIGUIENTES:
echo 1. Reinicia tu terminal
echo 2. Verifica: java -version
echo 3. Ejecuta: py configurar_ibmi.py
echo.
pause