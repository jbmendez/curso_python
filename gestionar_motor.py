"""
Utilidades para gestionar el Motor de Ejecución
===============================================

Este script proporciona funcionalidades para:
- Iniciar/detener el motor
- Verificar estado
- Configuración
- Debugging
"""
import argparse
import json
import subprocess
import sys
import time
import os
from pathlib import Path

def verificar_motor_ejecutandose():
    """Verifica si el motor está ejecutándose (versión simplificada)"""
    # En Windows, usar tasklist
    if sys.platform == "win32":
        try:
            output = subprocess.check_output(['tasklist'], shell=True, text=True)
            for line in output.split('\n'):
                if 'python' in line.lower() and 'motor_ejecucion' in line:
                    return line.split()[1]  # PID
        except:
            pass
    
    # Verificar archivo de PID si existe
    pid_file = Path("motor.pid")
    if pid_file.exists():
        try:
            with open(pid_file, 'r') as f:
                pid = f.read().strip()
                # Verificar si el proceso existe
                if sys.platform == "win32":
                    try:
                        subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}'], shell=True)
                        return pid
                    except:
                        pid_file.unlink()  # Eliminar PID obsoleto
                else:
                    try:
                        os.kill(int(pid), 0)  # No mata, solo verifica
                        return pid
                    except:
                        pid_file.unlink()  # Eliminar PID obsoleto
        except:
            pass
    
    return None

def iniciar_motor():
    """Inicia el motor de ejecución"""
    pid = verificar_motor_ejecutandose()
    if pid:
        print(f"⚠️ Motor ya está ejecutándose (PID: {pid})")
        return
    
    print("🚀 Iniciando motor de ejecución...")
    
    # Ejecutar en segundo plano
    if sys.platform == "win32":
        # Windows
        subprocess.Popen([
            sys.executable, "motor_ejecucion.py"
        ], creationflags=subprocess.CREATE_NEW_CONSOLE)
    else:
        # Linux/macOS
        subprocess.Popen([
            sys.executable, "motor_ejecucion.py"
        ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    
    # Verificar que inició
    time.sleep(2)
    pid = verificar_motor_ejecutandose()
    if pid:
        print(f"✅ Motor iniciado exitosamente (PID: {pid})")
    else:
        print("❌ Error iniciando motor")

def detener_motor():
    """Detiene el motor de ejecución"""
    pid = verificar_motor_ejecutandose()
    if not pid:
        print("⚠️ Motor no está ejecutándose")
        return
    
    print(f"🛑 Deteniendo motor (PID: {pid})...")
    
    try:
        if sys.platform == "win32":
            # Windows
            subprocess.run(['taskkill', '/F', '/PID', str(pid)], check=True)
        else:
            # Linux/macOS
            os.kill(int(pid), 15)  # SIGTERM
        
        print("✅ Motor detenido exitosamente")
        
        # Eliminar archivo PID
        pid_file = Path("motor.pid")
        if pid_file.exists():
            pid_file.unlink()
            
    except Exception as e:
        print(f"❌ Error deteniendo motor: {e}")

def estado_motor():
    """Muestra el estado del motor"""
    pid = verificar_motor_ejecutandose()
    
    print("📊 Estado del Motor de Ejecución")
    print("=" * 40)
    
    if pid:
        print(f"🟢 Estado: EJECUTÁNDOSE")
        print(f"🆔 PID: {pid}")
        
        # Información básica del proceso
        try:
            if sys.platform == "win32":
                output = subprocess.check_output(['tasklist', '/FI', f'PID eq {pid}', '/FO', 'CSV'], shell=True, text=True)
                lines = output.strip().split('\n')
                if len(lines) > 1:
                    # Parsear información básica
                    data = lines[1].split(',')
                    print(f"📄 Nombre proceso: {data[0].strip('\"')}")
                    print(f"💾 Memoria: {data[4].strip('\"')}")
        except:
            print("ℹ️ Información detallada no disponible")
    else:
        print("🔴 Estado: DETENIDO")
    
    # Verificar logs recientes
    log_dir = Path("logs")
    if log_dir.exists():
        log_files = list(log_dir.glob("motor_ejecucion_*.log"))
        if log_files:
            latest_log = max(log_files, key=lambda f: f.stat().st_mtime)
            print(f"📄 Último log: {latest_log}")
            
            # Mostrar últimas líneas
            try:
                with open(latest_log, 'r', encoding='utf-8') as f:
                    lines = f.readlines()
                    if lines:
                        print("\n📋 Últimas 3 líneas del log:")
                        for line in lines[-3:]:
                            print(f"   {line.strip()}")
            except Exception as e:
                print(f"⚠️ Error leyendo log: {e}")

def configurar_motor():
    """Configuración del motor"""
    print("⚙️ Configuración del Motor")
    print("=" * 30)
    print("Funcionalidad en desarrollo...")
    print("Configuraciones disponibles:")
    print("- Intervalo de ejecución (actualmente: 60s)")
    print("- Nivel de logging")
    print("- Modo de ejecución (mock/real)")

def test_motor():
    """Ejecuta el motor en modo test (una sola iteración)"""
    print("🧪 Ejecutando motor en modo test...")
    
    try:
        # Importar y ejecutar una sola iteración
        sys.path.append(str(Path(__file__).parent))
        from motor_ejecucion import MotorEjecucionService
        
        motor = MotorEjecucionService()
        motor.logger.info("🧪 Ejecutando en modo test (una iteración)")
        
        motor.ejecutar_ciclo()
        
        print("✅ Test completado exitosamente")
        
    except Exception as e:
        print(f"❌ Error en test: {e}")

def main():
    parser = argparse.ArgumentParser(description="Gestión del Motor de Ejecución")
    parser.add_argument("accion", choices=[
        "iniciar", "detener", "estado", "config", "test", "restart"
    ], help="Acción a realizar")
    
    args = parser.parse_args()
    
    if args.accion == "iniciar":
        iniciar_motor()
    elif args.accion == "detener":
        detener_motor()
    elif args.accion == "estado":
        estado_motor()
    elif args.accion == "config":
        configurar_motor()
    elif args.accion == "test":
        test_motor()
    elif args.accion == "restart":
        detener_motor()
        time.sleep(2)
        iniciar_motor()

if __name__ == "__main__":
    main()