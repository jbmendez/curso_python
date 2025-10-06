#!/usr/bin/env python3
"""
Prueba JDBC específica con tus datos reales de IBM i Series.
Usando la misma configuración que funciona en DBeaver.
"""

import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

from src.domain.entities.conexion import Conexion
from src.infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector

def probar_jdbc_real():
    """Prueba JDBC con los datos reales de IBM i Series."""
    
    print("=" * 60)
    print("🚀 PRUEBA JDBC - CONFIGURACIÓN REAL IBM i SERIES")
    print("=" * 60)
    
    # Usar tus datos reales
    conexion = Conexion(
        nombre="IBM i Production",
        tipo_motor="ibmiseries",
        servidor="172.20.0.10",      # Tu servidor real
        puerto=0,                  # Puerto SSL (igual que DBeaver)
        base_datos="*LIBL",          # Bibliotecas por defecto
        usuario="jmendez",           # Tu usuario real
        contraseña="barbiet9",       # Tu contraseña real
        driver_type="jdbc"           # Forzar JDBC como DBeaver
    )
    
    print(f"Servidor: {conexion.servidor}:{conexion.puerto}")
    print(f"Usuario: {conexion.usuario}")
    print(f"Driver: {conexion.driver_type} (igual que DBeaver)")
    print(f"Base datos: {conexion.base_datos}")
    print("-" * 60)
    
    # Crear selector
    selector = IBMiSeriesConexionSelector()
    
    print("\n🔄 Conectando con JDBC (mismo protocolo que DBeaver)...")
    
    # Probar conexión
    resultado = selector.probar_conexion(conexion)
    
    print("\n📋 RESULTADO:")
    if resultado.exitosa:
        print("✅ ¡CONEXIÓN JDBC EXITOSA!")
        print(f"   Mensaje: {resultado.mensaje}")
        print(f"   Tiempo: {resultado.tiempo_respuesta:.2f}s")
        if resultado.version_servidor:
            print(f"   Versión servidor: {resultado.version_servidor}")
        if resultado.detalles_error:
            print(f"   Información adicional: {resultado.detalles_error}")
    else:
        print("❌ CONEXIÓN JDBC FALLÓ")
        print(f"   Mensaje: {resultado.mensaje}")
        if resultado.detalles_error:
            print(f"   Detalles: {resultado.detalles_error}")
        print(f"   Tiempo: {resultado.tiempo_respuesta:.2f}s" if resultado.tiempo_respuesta else "   Tiempo: N/A")
    
    print("\n" + "=" * 60)
    
    return resultado.exitosa

def probar_auto_deteccion():
    """Prueba auto-detección (debería elegir JDBC automáticamente)."""
    
    print("\n🤖 PRUEBA AUTO-DETECCIÓN")
    print("-" * 40)
    
    conexion = Conexion(
        nombre="IBM i Auto",
        tipo_motor="ibmiseries", 
        servidor="172.20.0.10",
        puerto=446,
        base_datos="*LIBL",
        usuario="jmendez",
        contraseña="barbiet9",
        driver_type="auto"  # Auto-detección
    )
    
    selector = IBMiSeriesConexionSelector()
    resultado = selector.probar_conexion(conexion)
    
    print(f"Resultado auto-detección: {resultado.exitosa}")
    print(f"Mensaje: {resultado.mensaje}")
    
    return resultado.exitosa

def main():
    """Función principal."""
    print("🎯 Probando JDBC con configuración real...")
    
    # Probar JDBC específicamente
    jdbc_ok = probar_jdbc_real()
    
    # Probar auto-detección
    auto_ok = probar_auto_deteccion()
    
    print("\n" + "=" * 60)
    print("📊 RESUMEN FINAL")
    print("=" * 60)
    
    if jdbc_ok:
        print("🎉 ¡JDBC FUNCIONA PERFECTAMENTE!")
        print("   - Mismo protocolo que DBeaver")
        print("   - Conexión exitosa a IBM i Series")
        print("   - Sistema completamente operativo")
        print("\n✅ PRÓXIMOS PASOS:")
        print("   1. Usa la GUI: py main_gui.py")
        print("   2. Configura driver_type='jdbc' o 'auto'")
        print("   3. El sistema funcionará igual que DBeaver")
    else:
        print("⚠️  JDBC no conectó - posibles causas:")
        print("   1. Servidor IBM i no accesible")
        print("   2. Credenciales incorrectas")
        print("   3. Firewall bloqueando puerto 446")
        print("   4. Servicio SQL no activo en IBM i")
        
    print("=" * 60)

if __name__ == "__main__":
    main()