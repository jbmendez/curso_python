#!/usr/bin/env python3
"""
Script para verificar el contenido de la base de datos y mostrar controles existentes
"""
import sqlite3
import os

def verificar_base_datos():
    db_path = "sistema_controles.db"
    
    if not os.path.exists(db_path):
        print("❌ La base de datos no existe. Crea algunos controles primero.")
        return
    
    with sqlite3.connect(db_path) as conn:
        # Verificar controles
        cursor = conn.execute("SELECT COUNT(*) FROM controles")
        count_controles = cursor.fetchone()[0]
        
        print(f"📊 Total de controles: {count_controles}")
        
        if count_controles > 0:
            cursor = conn.execute("SELECT id, nombre, descripcion FROM controles LIMIT 5")
            controles = cursor.fetchall()
            
            print("\n🎮 Controles existentes:")
            for control in controles:
                print(f"  - ID: {control[0]}, Nombre: {control[1]}, Descripción: {control[2]}")
        
        # Verificar consultas
        cursor = conn.execute("SELECT COUNT(*) FROM consultas")
        count_consultas = cursor.fetchone()[0]
        
        print(f"\n📝 Total de consultas: {count_consultas}")
        
        if count_consultas > 0:
            cursor = conn.execute("SELECT id, nombre, sql FROM consultas LIMIT 3")
            consultas = cursor.fetchall()
            
            print("\n💾 Consultas existentes:")
            for consulta in consultas:
                print(f"  - ID: {consulta[0]}, Nombre: {consulta[1]}, SQL: {consulta[2][:50]}...")
        
        # Verificar asociaciones
        try:
            cursor = conn.execute("SELECT COUNT(*) FROM consultas_controles")
            count_asociaciones = cursor.fetchone()[0]
            print(f"\n🔗 Total de asociaciones: {count_asociaciones}")
        except sqlite3.OperationalError:
            print("\n🔗 Tabla de asociaciones no existe (se creará automáticamente)")

if __name__ == "__main__":
    verificar_base_datos()