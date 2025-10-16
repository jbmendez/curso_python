@echo off
echo ========================================
echo Monitor de Notificaciones de Archivos
echo ========================================
echo.

REM Activar entorno virtual si existe
if exist ".venv\Scripts\activate.bat" (
    echo Activando entorno virtual...
    call .venv\Scripts\activate.bat
) else (
    echo ⚠️  Entorno virtual no encontrado - usando Python del sistema
)

echo.
echo Iniciando monitor de notificaciones...
echo Presiona Ctrl+C para detener
echo.

REM Ejecutar monitor con configuración
python monitor_notificaciones.py --config config_monitor_notificaciones.json

echo.
echo Monitor detenido.
echo Presiona cualquier tecla para salir...
pause >nul