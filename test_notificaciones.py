#!/usr/bin/env python3
"""
Test simple para verificar que las notificaciones de Windows funcionan
"""
import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.services.notification_service import WindowsNotificationService
import time

def test_notificaciones():
    """Test básico de notificaciones"""
    print("=== Test de Notificaciones de Windows ===")
    
    # Crear servicio
    notification_service = WindowsNotificationService()
    
    # Verificar disponibilidad
    if not notification_service.is_available():
        print("❌ Notificaciones no disponibles en este sistema")
        print("Verifica que:")
        print("- plyer esté instalado: pip install plyer")
        print("- Las notificaciones estén habilitadas en Windows")
        return
    
    print("✅ Servicio de notificaciones disponible")
    
    # Test 1: Notificación de motor iniciado
    print("\n1. Probando notificación de motor iniciado...")
    notification_service.mostrar_motor_iniciado()
    time.sleep(3)
    
    # Test 2: Notificación de control disparado
    print("2. Probando notificación de control disparado...")
    notification_service.mostrar_control_disparado(
        control_nombre="Control Test",
        filas_procesadas=25,
        tiempo_ejecucion_ms=1500,
        mensaje_adicional="Test desde Python"
    )
    time.sleep(3)
    
    # Test 3: Notificación de error
    print("3. Probando notificación de error...")
    notification_service.mostrar_control_error(
        control_nombre="Control Error Test",
        error_mensaje="Error de prueba para verificar notificaciones",
        tiempo_ejecucion_ms=800
    )
    time.sleep(3)
    
    # Test 4: Notificación de resumen
    print("4. Probando notificación de resumen...")
    notification_service.mostrar_resumen_ejecucion(
        total_controles=5,
        controles_disparados=2,
        controles_error=1,
        tiempo_total_ms=3200
    )
    time.sleep(3)
    
    # Test 5: Notificación de motor detenido
    print("5. Probando notificación de motor detenido...")
    notification_service.mostrar_motor_detenido()
    
    print("\n✅ Test completado. Deberías haber visto 5 notificaciones en Windows.")
    print("💡 Las notificaciones usando plyer son más estables y sin errores de consola.")

if __name__ == "__main__":
    test_notificaciones()