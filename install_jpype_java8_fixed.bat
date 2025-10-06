@echo off
REM Script mejorado para instalar JPype compatible con Java 8
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
set "JAVA_HOME=C:\Program Files\Java\jre1.8.0_451"
if not exist "%JAVA_HOME%" (
    set "JAVA_HOME=C:\Program Files\Java\jre1.8.0_341"
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
set "PATH=%JAVA_HOME%\bin;%PATH%"

echo.
echo Verificando Java 8...
java -version
echo.

REM Verificar Visual Studio Build Tools
set VS_FOUND=0
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2022\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2022 encontrados
    set VS_FOUND=1
)
if exist "C:\Program Files (x86)\Microsoft Visual Studio\2019\BuildTools\VC\Tools\MSVC" (
    echo ✅ Visual Studio Build Tools 2019 encontrados  
    set VS_FOUND=1
)

if %VS_FOUND%==0 (
    echo ❌ Visual Studio Build Tools no encontrados
    echo Ejecuta primero: install_vs_buildtools.bat
    pause
    exit /b 1
)

echo.

REM Desinstalar JPype existente
echo Desinstalando JPype existente...
.venv\Scripts\pip.exe uninstall JPype1 -y >nul 2>&1

REM Limpiar caché
echo Limpiando caché de pip...
.venv\Scripts\pip.exe cache purge >nul 2>&1

REM Configurar variables para compilación
set DISTUTILS_USE_SDK=1
set MSSdk=1

echo.
echo Instalando JPype compatible con Java 8...
echo (Esto puede tomar varios minutos)
echo.

REM Intentar diferentes versiones de JPype
echo Probando JPype 1.3.0...
.venv\Scripts\pip.exe install JPype1==1.3.0 --no-binary=JPype1 --no-cache-dir

if %errorlevel% neq 0 (
    echo.
    echo ❌ Error con 1.3.0, probando 1.2.1...
    .venv\Scripts\pip.exe install JPype1==1.2.1 --no-binary=JPype1 --no-cache-dir
    
    if %errorlevel% neq 0 (
        echo.
        echo ❌ Error compilando desde código fuente
        echo Probando wheel precompilado...
        .venv\Scripts\pip.exe install JPype1==1.3.0
        
        if %errorlevel% neq 0 (
            echo ❌ No se pudo instalar JPype
            echo.
            echo SOLUCIONES:
            echo 1. Reinicia el sistema después de instalar Build Tools
            echo 2. Prueba con un entorno virtual nuevo
            echo 3. Verifica permisos de administrador
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
.venv\Scripts\python.exe -c "import jpype; print('JPype version:', jpype.__version__)"

if %errorlevel% eq 0 (
    echo.
    echo Probando inicialización JVM...
    .venv\Scripts\python.exe -c "import jpype; jpype.startJVM(); print('JVM iniciada exitosamente'); jpype.shutdownJVM(); print('Prueba exitosa')"
    
    if %errorlevel% eq 0 (
        echo.
        echo ✅ ¡JPype instalado y funcionando correctamente!
        echo.
        echo PRÓXIMO PASO: Ejecutar test con JDBC
        echo   py diagnostico_ibmi_win.py
    ) else (
        echo.
        echo ⚠️  JPype instalado pero con errores de JVM
        echo Revisa la configuración de Java
    )
) else (
    echo.
    echo ❌ JPype instalado pero con errores de importación
)

echo.
echo ===============================================
echo  INSTALACIÓN COMPLETADA
echo ===============================================
pause