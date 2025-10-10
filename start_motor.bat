@echo off
REM Script para ejecutar el Motor de Ejecución con ambiente virtual
echo 🔧 Configurando Java 11 para JPype...

REM Configurar JAVA_HOME y PATH para Java 11
set JAVA_HOME=C:\Program Files\Java\jdk-11
set PATH=C:\Program Files\Java\jdk-11\bin;%PATH%

echo ☕ Java 11 configurado
echo 🚀 Iniciando Motor de Ejecución de Controles...
echo 📦 Usando ambiente virtual (.venv)...
echo.

REM Ejecutar el motor usando el Python del ambiente virtual
.venv\Scripts\python.exe motor_ejecucion.py

pause