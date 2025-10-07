#!/usr/bin/env python3
"""
Script para verificar el esquema de la base de datos
"""
import sqlite3

def verificar_esquema():
    with sqlite3.connect("sistema_controles.db") as conn:
        # Obtener todas las tablas
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tablas = cursor.fetchall()
        
        print("📋 Tablas en la base de datos:")
        for tabla in tablas:
            print(f"  - {tabla[0]}")
            
        # Ver esquema de parámetros
        print("\n🔧 Esquema de la tabla parametros:")
        try:
            cursor = conn.execute("PRAGMA table_info(parametros)")
            columnas = cursor.fetchall()
            for columna in columnas:
                print(f"  - {columna[1]} ({columna[2]})")
        except sqlite3.OperationalError:
            print("  ❌ Tabla parametros no existe")
            
        # Ver esquema de controles
        print("\n🎮 Esquema de la tabla controles:")
        try:
            cursor = conn.execute("PRAGMA table_info(controles)")
            columnas = cursor.fetchall()
            for columna in columnas:
                print(f"  - {columna[1]} ({columna[2]})")
        except sqlite3.OperationalError:
            print("  ❌ Tabla controles no existe")

if __name__ == "__main__":
    verificar_esquema()