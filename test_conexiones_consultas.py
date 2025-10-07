"""
Script de prueba para verificar la lógica de conexiones en consultas
"""
import os
import sys

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository

def verificar_consultas_y_conexiones():
    """Verifica qué consultas tienen conexiones específicas"""
    
    # Inicializar repositorios
    consulta_repo = SQLiteConsultaRepository("sistema_controles.db")
    conexion_repo = SQLiteConexionRepository("sistema_controles.db")
    
    # Obtener todas las consultas
    consultas = consulta_repo.obtener_todos()
    conexiones = conexion_repo.obtener_todos()
    
    print("=== VERIFICACIÓN DE CONEXIONES EN CONSULTAS ===\n")
    
    print("Conexiones disponibles:")
    for conn in conexiones:
        print(f"  ID: {conn.id} - {conn.nombre} ({conn.tipo_motor})")
    
    print(f"\nConsultas encontradas: {len(consultas)}")
    print("-" * 50)
    
    for consulta in consultas:
        print(f"Consulta: {consulta.nombre} (ID: {consulta.id})")
        print(f"  SQL: {consulta.sql[:60]}...")
        print(f"  Conexión específica: {consulta.conexion_id}")
        
        if consulta.conexion_id:
            # Buscar la conexión específica
            conexion_especifica = next((c for c in conexiones if c.id == consulta.conexion_id), None)
            if conexion_especifica:
                print(f"  → Usará conexión: {conexion_especifica.nombre} ({conexion_especifica.tipo_motor})")
            else:
                print(f"  → ERROR: Conexión ID {consulta.conexion_id} no encontrada")
        else:
            print(f"  → Usará conexión del control (fallback)")
        
        print()

if __name__ == "__main__":
    verificar_consultas_y_conexiones()