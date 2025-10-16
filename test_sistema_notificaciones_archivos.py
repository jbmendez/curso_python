"""
Test completo del nuevo sistema de notificaciones por archivos
Simula el flujo completo: control dispara → archivo creado → monitor procesa → notificación mostrada
"""

import sys
import os
import time
import tempfile
import shutil
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.infrastructure.services.notification_file_service import NotificationFileService
from monitor_notificaciones import NotificationFileMonitor


def test_flujo_completo():
    """Test del flujo completo del sistema de notificaciones por archivos"""
    print("=== TEST SISTEMA NOTIFICACIONES POR ARCHIVOS ===\n")
    
    # Crear carpeta temporal para pruebas
    carpeta_test = os.path.join(tempfile.gettempdir(), "test_notificaciones")
    os.makedirs(carpeta_test, exist_ok=True)
    
    print(f"📁 Carpeta de pruebas: {carpeta_test}")
    
    try:
        # Paso 1: Crear servicio de archivos de notificación
        print("\n1. Creando servicio de archivos de notificación...")
        file_service = NotificationFileService()
        print("   ✅ Servicio creado")
        
        # Paso 2: Simular control disparado - crear archivo de notificación
        print("\n2. Simulando control disparado - creando archivo de notificación...")
        archivo_notificacion = file_service.crear_archivo_notificacion_control(
            carpeta_destino=carpeta_test,
            control_nombre="Control de Prueba Completa",
            filas_procesadas=150,
            tiempo_ejecucion_ms=2500.5,
            archivo_excel="Control_de_Prueba_Completa_20241016_143025.xlsx",
            mensaje_adicional="Esta es una prueba del sistema completo"
        )
        
        if archivo_notificacion:
            print(f"   ✅ Archivo de notificación creado: {os.path.basename(archivo_notificacion)}")
        else:
            print("   ❌ Error creando archivo de notificación")
            return False
        
        # Paso 3: Verificar que el archivo existe y tiene el contenido correcto
        print("\n3. Verificando contenido del archivo...")
        datos = file_service.leer_archivo_notificacion(archivo_notificacion)
        if datos:
            print("   ✅ Archivo leído correctamente")
            print(f"   - Tipo: {datos.get('tipo')}")
            print(f"   - Control: {datos.get('control', {}).get('nombre')}")
            print(f"   - Filas: {datos.get('control', {}).get('filas_procesadas')}")
            print(f"   - Equipo origen: {datos.get('sistema', {}).get('equipo_origen')}")
        else:
            print("   ❌ Error leyendo archivo")
            return False
        
        # Paso 4: Crear monitor y procesar archivo
        print("\n4. Creando monitor y procesando archivo...")
        monitor = NotificationFileMonitor([carpeta_test], intervalo_segundos=1)
        
        # Procesar archivo específico
        exito = monitor.procesar_archivo_unico(archivo_notificacion)
        
        if exito:
            print("   ✅ Archivo procesado exitosamente")
            print("   📢 Debería haber aparecido una notificación de Windows")
            
            # Verificar que el archivo fue eliminado
            if not os.path.exists(archivo_notificacion):
                print("   ✅ Archivo eliminado después del procesamiento")
            else:
                print("   ❌ Archivo no fue eliminado")
                return False
        else:
            print("   ❌ Error procesando archivo")
            return False
        
        print("\n✅ TEST COMPLETO EXITOSO")
        print("   El flujo completo funciona correctamente:")
        print("   1. ✅ Archivo de notificación creado")
        print("   2. ✅ Archivo procesado por monitor")
        print("   3. ✅ Notificación mostrada")
        print("   4. ✅ Archivo eliminado")
        
        return True
        
    except Exception as e:
        print(f"\n❌ ERROR EN TEST: {e}")
        import traceback
        traceback.print_exc()
        return False
        
    finally:
        # Limpiar carpeta de pruebas
        try:
            shutil.rmtree(carpeta_test)
            print(f"\n🧹 Carpeta de pruebas eliminada: {carpeta_test}")
        except:
            print(f"\n⚠️ No se pudo eliminar carpeta de pruebas: {carpeta_test}")


def test_multiples_tipos_notificacion():
    """Test de múltiples tipos de notificación"""
    print("\n=== TEST MÚLTIPLES TIPOS DE NOTIFICACIÓN ===\n")
    
    # Crear carpeta temporal
    carpeta_test = os.path.join(tempfile.gettempdir(), "test_tipos_notif")
    os.makedirs(carpeta_test, exist_ok=True)
    
    file_service = NotificationFileService()
    monitor = NotificationFileMonitor([carpeta_test])
    
    try:
        tipos_test = [
            {
                "nombre": "Control Disparado",
                "funcion": lambda: file_service.crear_archivo_notificacion_control(
                    carpeta_test, "Control Test", 75, 1200.0, "test.xlsx"
                )
            },
            {
                "nombre": "Error en Control", 
                "funcion": lambda: file_service.crear_archivo_notificacion_error(
                    carpeta_test, "Control Con Error", "Error de conexión a base de datos", 800.0
                )
            },
            {
                "nombre": "Motor Iniciado",
                "funcion": lambda: file_service.crear_archivo_notificacion_motor(
                    carpeta_test, "iniciado"
                )
            },
            {
                "nombre": "Motor Parado",
                "funcion": lambda: file_service.crear_archivo_notificacion_motor(
                    carpeta_test, "parado", "Error crítico del sistema"
                )
            }
        ]
        
        for i, tipo_test in enumerate(tipos_test, 1):
            print(f"{i}. Probando {tipo_test['nombre']}...")
            
            # Crear archivo
            archivo = tipo_test['funcion']()
            if not archivo:
                print("   ❌ Error creando archivo")
                continue
            
            # Procesar archivo
            exito = monitor.procesar_archivo_unico(archivo)
            if exito:
                print("   ✅ Procesado y notificación mostrada")
            else:
                print("   ❌ Error procesando archivo")
            
            # Pequeña pausa entre notificaciones
            time.sleep(1)
        
        print("\n✅ Test de múltiples tipos completado")
        
    finally:
        # Limpiar
        shutil.rmtree(carpeta_test, ignore_errors=True)


def test_monitor_continuo():
    """Test del monitor continuo (para desarrollo/debug)"""
    print("\n=== TEST MONITOR CONTINUO ===")
    print("Este test ejecutará el monitor de manera continua.")
    print("Genera archivos de notificación en otra terminal para probar.")
    print("Presiona Ctrl+C para detener.\n")
    
    # Usar carpeta configurada
    carpetas = ["C:\\temp\\reportes_test"]
    
    # Crear carpetas si no existen
    for carpeta in carpetas:
        os.makedirs(carpeta, exist_ok=True)
        print(f"📁 Monitoreando: {carpeta}")
    
    # Crear y ejecutar monitor
    monitor = NotificationFileMonitor(carpetas, intervalo_segundos=2)
    
    try:
        monitor.iniciar_monitoreo()
    except KeyboardInterrupt:
        print("\n✅ Monitor detenido por el usuario")


def generar_archivos_test():
    """Genera archivos de prueba para testing manual"""
    print("\n=== GENERADOR DE ARCHIVOS DE PRUEBA ===\n")
    
    carpeta_destino = "C:\\temp\\reportes_test"
    os.makedirs(carpeta_destino, exist_ok=True)
    
    file_service = NotificationFileService()
    
    archivos_generados = []
    
    # Control disparado
    archivo1 = file_service.crear_archivo_notificacion_control(
        carpeta_destino, "Control Mensual de Facturación", 234, 3500.0, "facturacion_20241016.xlsx"
    )
    if archivo1:
        archivos_generados.append(archivo1)
    
    # Error en control
    archivo2 = file_service.crear_archivo_notificacion_error(
        carpeta_destino, "Control de Validación", "Error de timeout en consulta SQL", 5000.0
    )
    if archivo2:
        archivos_generados.append(archivo2)
    
    # Motor parado
    archivo3 = file_service.crear_archivo_notificacion_motor(
        carpeta_destino, "parado", "Fallo en conexión a base de datos principal"
    )
    if archivo3:
        archivos_generados.append(archivo3)
    
    print(f"✅ {len(archivos_generados)} archivos de prueba generados en:")
    print(f"   {carpeta_destino}")
    print("\nArchivos generados:")
    for archivo in archivos_generados:
        print(f"   - {os.path.basename(archivo)}")
    
    print(f"\n💡 Ejecuta el monitor para procesarlos:")
    print(f"   python monitor_notificaciones.py --config config_monitor_notificaciones.json")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Test del sistema de notificaciones por archivos')
    parser.add_argument('--test', choices=['completo', 'tipos', 'monitor', 'generar'], 
                       default='completo', help='Tipo de test a ejecutar')
    
    args = parser.parse_args()
    
    if args.test == 'completo':
        exito = test_flujo_completo()
        exit(0 if exito else 1)
    elif args.test == 'tipos':
        test_multiples_tipos_notificacion()
    elif args.test == 'monitor':
        test_monitor_continuo()
    elif args.test == 'generar':
        generar_archivos_test()