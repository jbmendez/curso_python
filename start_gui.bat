@echo off
REM Script para ejecutar la GUI con Java 11 configurado
echo 🔧 Configurando Java 11 para JPype...

REM Configurar JAVA_HOME y PATH para Java 11
set JAVA_HOME=C:\Program Files\Java\jdk-11
set PATH=C:\Program Files\Java\jdk-11\bin;%PATH%

echo ☕ Java 11 configurado
echo 🚀 Iniciando GUI del Sistema de Controles...
echo.

REM Ejecutar la GUI usando py del sistema (no virtual env)
py main_gui.py

pause