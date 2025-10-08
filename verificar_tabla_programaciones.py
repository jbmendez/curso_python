"""
Script para verificar la tabla programaciones
"""
import sqlite3

def verificar_tabla():
    conn = sqlite3.connect('sistema_controles.db')
    
    # Verificar si existe la tabla
    cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='programaciones'")
    tabla = cursor.fetchone()
    
    if tabla:
        print('✅ Tabla programaciones existe')
        
        # Ver estructura de la tabla
        cursor = conn.execute('PRAGMA table_info(programaciones)')
        columnas = cursor.fetchall()
        print('\nColumnas de la tabla:')
        for col in columnas:
            print(f'  - {col[1]} ({col[2]})')
        
        # Ver índices
        cursor = conn.execute("SELECT name FROM sqlite_master WHERE type='index' AND tbl_name='programaciones'")
        indices = cursor.fetchall()
        if indices:
            print('\nÍndices:')
            for idx in indices:
                print(f'  - {idx[0]}')
    else:
        print('❌ Tabla programaciones no encontrada')
    
    conn.close()

if __name__ == "__main__":
    verificar_tabla()