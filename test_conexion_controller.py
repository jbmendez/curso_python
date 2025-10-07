#!/usr/bin/env python3
"""
Script para probar directamente el método obtener_por_id del controlador de conexiones
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.use_cases.listar_conexiones_use_case import ListarConexionesUseCase
from src.presentation.controllers.conexion_controller import ConexionController

def test_conexion_controller():
    print("🧪 Probando ConexionController.obtener_por_id()...")
    
    # Configurar repositorio y use cases
    conexion_repo = SQLiteConexionRepository("sistema_controles.db")
    crear_uc = CrearConexionUseCase(conexion_repo)
    listar_uc = ListarConexionesUseCase(conexion_repo)
    
    # Crear controlador
    controller = ConexionController(crear_uc, listar_uc)
    
    # Probar obtener todas las conexiones
    print("\n📋 Probando obtener_todas():")
    response = controller.obtener_todas()
    print(f"   Respuesta: {response}")
    
    # Probar obtener conexión ID 4
    print("\n🔍 Probando obtener_por_id(4):")
    response = controller.obtener_por_id(4)
    print(f"   Respuesta: {response}")
    
    # Probar obtener conexión que no existe
    print("\n❌ Probando obtener_por_id(999) (no existe):")
    response = controller.obtener_por_id(999)
    print(f"   Respuesta: {response}")

if __name__ == "__main__":
    test_conexion_controller()