#!/usr/bin/env python3
"""
Script para diagnosticar el problema de conexiones
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

import sqlite3

def diagnosticar_conexiones():
    print("🔍 Diagnosticando problema de conexiones...")
    
    with sqlite3.connect("sistema_controles.db") as conn:
        conn.row_factory = sqlite3.Row
        
        # Ver consultas
        print("\n📝 Consultas en la base de datos:")
        cursor = conn.execute("SELECT id, nombre, conexion_id FROM consultas")
        consultas = cursor.fetchall()
        
        for consulta in consultas:
            print(f"  - ID: {consulta['id']}, Nombre: {consulta['nombre']}, Conexión ID: {consulta['conexion_id']}")
        
        # Ver conexiones
        print("\n🔗 Conexiones en la base de datos:")
        cursor = conn.execute("SELECT id, nombre, activa FROM conexiones")
        conexiones = cursor.fetchall()
        
        for conexion in conexiones:
            print(f"  - ID: {conexion['id']}, Nombre: {conexion['nombre']}, Activa: {conexion['activa']}")
        
        # Probar la lógica de selección de conexión
        if consultas:
            consulta = consultas[0]
            print(f"\n🧪 Probando lógica para consulta '{consulta['nombre']}':")
            print(f"   - conexion_id en consulta: {consulta['conexion_id']}")
            
            if consulta['conexion_id']:
                print(f"   - Buscaría conexión ID: {consulta['conexion_id']}")
                # Verificar si existe esa conexión
                cursor = conn.execute("SELECT * FROM conexiones WHERE id = ?", (consulta['conexion_id'],))
                conexion_encontrada = cursor.fetchone()
                if conexion_encontrada:
                    print(f"   ✅ Conexión encontrada: {conexion_encontrada['nombre']}")
                else:
                    print(f"   ❌ Conexión ID {consulta['conexion_id']} NO encontrada")
            else:
                print("   - conexion_id es NULL, buscaría primera conexión disponible")
                if conexiones:
                    print(f"   - Primera conexión disponible: ID {conexiones[0]['id']}, {conexiones[0]['nombre']}")
                else:
                    print("   ❌ No hay conexiones disponibles")

if __name__ == "__main__":
    diagnosticar_conexiones()