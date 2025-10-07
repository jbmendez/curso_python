"""
Script para configurar un referente de prueba con generación de archivos Excel
"""
import sqlite3
import os
from datetime import datetime

# Configuración
DB_PATH = "sistema_controles.db"
TEST_PATH = r"C:\temp\reportes_test"

def configurar_referente_test():
    """Configura un referente de prueba para generación de archivos"""
    
    # Crear carpeta de prueba si no existe
    os.makedirs(TEST_PATH, exist_ok=True)
    
    with sqlite3.connect(DB_PATH) as conn:
        # Insertar o actualizar referente
        cursor = conn.execute("""
            INSERT OR REPLACE INTO referentes 
            (id, nombre, email, path_archivos, activo) 
            VALUES (1, 'Referente Test Excel', 'test@excel.com', ?, 1)
        """, (TEST_PATH,))
        
        referente_id = cursor.lastrowid if cursor.lastrowid else 1
        
        # Verificar si existe asociación control-referente
        cursor = conn.execute("""
            SELECT id FROM control_referente 
            WHERE control_id = 1 AND referente_id = ?
        """, (referente_id,))
        
        asociacion = cursor.fetchone()
        
        if asociacion:
            # Actualizar asociación existente para habilitar archivo
            conn.execute("""
                UPDATE control_referente 
                SET notificar_por_archivo = 1, activa = 1
                WHERE control_id = 1 AND referente_id = ?
            """, (referente_id,))
            print(f"✅ Actualizada asociación existente para habilitar archivo")
        else:
            # Crear nueva asociación
            conn.execute("""
                INSERT INTO control_referente 
                (control_id, referente_id, activa, fecha_asociacion, notificar_por_email, notificar_por_archivo, observaciones)
                VALUES (1, ?, 1, ?, 1, 1, 'Configurado para test de Excel')
            """, (referente_id, datetime.now()))
            print(f"✅ Creada nueva asociación control-referente con archivo habilitado")
        
        conn.commit()
        
        print(f"✅ Referente configurado:")
        print(f"   - ID: {referente_id}")
        print(f"   - Nombre: Referente Test Excel") 
        print(f"   - Path: {TEST_PATH}")
        print(f"   - Notificar por archivo: SÍ")
        print(f"   - Asociado al control ID: 1")

if __name__ == "__main__":
    configurar_referente_test()
    print("\n🎯 Configuración completada. Ahora ejecuta un control para generar Excel.")