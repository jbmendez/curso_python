#!/usr/bin/env python3
"""
Test para verificar que las notificaciones manejan correctamente los límites de caracteres
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.services.notification_service import WindowsNotificationService
import time

def test_notificaciones_con_limites():
    """Test para verificar límites de caracteres en notificaciones"""
    
    notification_service = WindowsNotificationService()
    
    print("🧪 Testing notification character limits...")
    
    # Test 1: Control con nombre muy largo
    control_largo = "Control_de_verificacion_de_datos_completos_con_validacion_extendida_y_procesamiento_avanzado_que_excede_los_limites_normales"
    print(f"\n1. Testing control con nombre largo ({len(control_largo)} chars):")
    print(f"   Nombre: {control_largo}")
    
    result1 = notification_service.mostrar_control_disparado(
        control_nombre=control_largo,
        filas_procesadas=150,
        tiempo_ejecucion_ms=2500,
        mensaje_adicional="Este es un mensaje adicional que también puede ser muy largo y causar problemas de visualización"
    )
    print(f"   Resultado: {'✅ Exitoso' if result1 else '❌ Falló'}")
    
    time.sleep(3)
    
    # Test 2: Mensaje de error muy largo
    error_muy_largo = "Error crítico en la base de datos: La consulta SQL falló debido a un problema de conectividad con el servidor principal, timeout en la conexión secundaria, validación de datos inconsistente, y múltiples intentos de reconexión que han resultado en un estado de deadlock irreversible que requiere intervención manual inmediata del administrador del sistema para restablecer la funcionalidad completa del motor de controles"
    print(f"\n2. Testing error con mensaje largo ({len(error_muy_largo)} chars):")
    print(f"   Error: {error_muy_largo[:100]}...")
    
    result2 = notification_service.mostrar_control_error(
        control_nombre="Control_con_error_critico",
        error_mensaje=error_muy_largo,
        tiempo_ejecucion_ms=5000
    )
    print(f"   Resultado: {'✅ Exitoso' if result2 else '❌ Falló'}")
    
    time.sleep(3)
    
    # Test 3: Resumen con números grandes
    print(f"\n3. Testing resumen con números grandes:")
    result3 = notification_service.mostrar_resumen_ejecucion(
        total_controles=9999,
        controles_disparados=8888,
        controles_error=111,
        tiempo_total_ms=123456.789
    )
    print(f"   Resultado: {'✅ Exitoso' if result3 else '❌ Falló'}")
    
    time.sleep(3)
    
    # Test 4: Control con mensaje adicional extremadamente largo
    mensaje_adicional_largo = "Este es un mensaje adicional que contiene una cantidad excesiva de información detallada sobre el proceso de ejecución del control, incluyendo estadísticas completas, detalles de rendimiento, información de configuración, y múltiples advertencias y observaciones que normalmente no cabrían en una notificación estándar de Windows y que podrían causar problemas de truncamiento o errores de visualización en el sistema operativo"
    print(f"\n4. Testing control con mensaje adicional muy largo ({len(mensaje_adicional_largo)} chars):")
    
    result4 = notification_service.mostrar_control_disparado(
        control_nombre="Control_Normal",
        filas_procesadas=50,
        tiempo_ejecucion_ms=1200,
        mensaje_adicional=mensaje_adicional_largo
    )
    print(f"   Resultado: {'✅ Exitoso' if result4 else '❌ Falló'}")
    
    time.sleep(3)
    
    # Test 5: Test de límites extremos
    print(f"\n5. Testing límites extremos:")
    result5 = notification_service.mostrar_control_disparado(
        control_nombre="A" * 200,  # Nombre de 200 caracteres
        filas_procesadas=999999999,
        tiempo_ejecucion_ms=999999.999,
        mensaje_adicional="B" * 500  # Mensaje de 500 caracteres
    )
    print(f"   Resultado: {'✅ Exitoso' if result5 else '❌ Falló'}")
    
    # Resultados finales
    total_tests = 5
    exitosos = sum([result1, result2, result3, result4, result5])
    print(f"\n📊 Resultados finales:")
    print(f"   Tests exitosos: {exitosos}/{total_tests}")
    print(f"   Tests fallidos: {total_tests - exitosos}/{total_tests}")
    
    if exitosos == total_tests:
        print("✅ Todos los tests de límites pasaron correctamente!")
    else:
        print("⚠️ Algunos tests fallaron. Revisar implementación de límites.")
    
    return exitosos == total_tests

if __name__ == "__main__":
    test_notificaciones_con_limites()