@echo off
REM Script para instalar JPype compatible con Java 8
echo ===============================================
echo  INSTALADOR JPYPE COMPATIBLE CON JAVA 8
echo ===============================================
echo.

REM Verificar que estamos en el entorno virtual correcto
if not exist ".venv\Scripts\python.exe" (
    echo ❌ No se encontró entorno virtual .venv
    echo Ejecuta desde el directorio del proyecto
    pause
    exit /b 1
)

echo ✅ Entorno virtual encontrado
echo.

REM Configurar variables Java para Java 8
set JAVA_HOME=C:\Program Files\Java\jre1.8.0_451
if not exist "%JAVA_HOME%" (
    set JAVA_HOME=C:\Program Files\Java\jre1.8.0_341
)
if not exist "%JAVA_HOME%" (
    echo ❌ No se encontró Java 8
    echo Instalaciones disponibles:
    dir "C:\Program Files\Java" /AD
    echo.
    echo SOLUCIÓN: Especifica la ruta correcta de Java 8
    pause
    exit /b 1
)

echo ✅ Usando Java 8: %JAVA_HOME%
set PATH=%JAVA_HOME%\bin;%PATH%

echo.
echo Verificando Java 8...
java -version
echo.

REM Verificar Visual Studio Build Tools
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2022 encontrados
    set VS_TOOLS_PATH=C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools
    goto :buildtools_found
)
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\*\VC\Tools\MSVC" (
    echo ✅ Visual Studio 2022 encontrado
    set VS_TOOLS_PATH=C:\Program Files (x86)\Microsoft Visual Studio\2022
    goto :buildtools_found
)
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2019 encontrados
    set VS_TOOLS_PATH=C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools
    goto :buildtools_found
)

echo ❌ Visual Studio Build Tools no encontrados
echo Ubicaciones verificadas:
echo - C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC
echo - C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC
echo.
echo Ejecuta primero: install_vs_buildtools.bat
pause
exit /b 1

:buildtools_found
echo.

REM Desinstalar JPype existente
echo Desinstalando JPype existente...
.venv\Scripts\pip.exe uninstall JPype1 -y >nul 2>&1

REM Limpiar caché
echo Limpiando caché de pip...
.venv\Scripts\pip.exe cache purge >nul 2>&1

REM Instalar JPype compatible con Java 8
echo.
echo Instalando JPype compatible con Java 8...
echo (Esto puede tomar varios minutos)
echo.

REM Configurar variables para compilación
set DISTUTILS_USE_SDK=1
set MSSdk=1

REM Instalar JPype compilándolo desde código fuente
.venv\Scripts\pip.exe install JPype1==1.2.1 --no-binary=JPype1 --no-cache-dir

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error instalando JPype 1.2.1, probando 1.3.0...
    .venv\Scripts\pip.exe install JPype1==1.3.0 --no-binary=JPype1 --no-cache-dir
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Error instalando JPype desde código fuente
        echo.
        echo ALTERNATIVA: Probar wheel precompilado
        .venv\Scripts\pip.exe install JPype1==1.2.1
        
        if %errorlevel% neq 0 (
            echo ❌ No se pudo instalar JPype
            echo.
            echo SOLUCIONES:
            echo 1. Verifica que Visual Studio Build Tools estén instalados
            echo 2. Reinicia el sistema después de instalar Build Tools
            echo 3. Prueba con Python 3.11 en lugar de 3.13
            pause
            exit /b 1
        )
    )
)

echo.
echo ===============================================
echo  VERIFICANDO INSTALACIÓN
echo ===============================================
echo.

REM Probar JPype
echo Probando JPype...
.venv\Scripts\python.exe -c "import jpype; print('JPype version:', jpype.__version__); jpype.startJVM(); print('JVM iniciada exitosamente'); jpype.shutdownJVM(); print('Prueba exitosa')"

if %errorlevel% eq 0 (
    echo.
    echo ✅ ¡JPype instalado y funcionando correctamente!
    echo.
    echo PRÓXIMO PASO: Ejecutar test con JDBC
    echo   py diagnostico_ibmi_win.py
) else (
    echo.
    echo ❌ JPype instalado pero con errores
    echo Revisa la configuración de Java
)

echo.
echo ===============================================
echo  INSTALACIÓN COMPLETADA
echo ===============================================
pause