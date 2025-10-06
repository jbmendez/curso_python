@echo off
REM Script para ejecutar Python con Java 11 configurado
echo 🔧 Configurando Java 11 para JPype...

REM Configurar JAVA_HOME y PATH para Java 11
set JAVA_HOME=C:\Program Files\Java\jdk-11
set PATH=C:\Program Files\Java\jdk-11\bin;%PATH%

REM Verificar Java version
echo ☕ Verificando Java version:
java -version

echo.
echo 🚀 Ejecutando Python con Java 11...
echo.

REM Ejecutar el comando Python pasado como parámetro
"%~dp0.venv\Scripts\python.exe" %*