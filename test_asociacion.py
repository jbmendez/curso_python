#!/usr/bin/env python3
"""
Script de prueba para verificar la funcionalidad de asociación consulta-control
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.infrastructure.repositories.sqlite_consulta_control_repository import SQLiteConsultaControlRepository
from src.application.use_cases.asociar_consulta_control_use_case import AsociarConsultaControlUseCase
from src.application.use_cases.listar_consulta_control_use_case import ListarConsultaControlUseCase
from src.presentation.controllers.consulta_control_controller import ConsultaControlController

def test_consulta_control():
    print("🧪 Probando funcionalidad ConsultaControl...")
    
    # Configurar repositorio y use cases
    repo = SQLiteConsultaControlRepository("sistema_controles.db")
    asociar_uc = AsociarConsultaControlUseCase(repo)
    listar_uc = ListarConsultaControlUseCase(repo)
    
    # Crear controlador
    controller = ConsultaControlController(
        asociar_uc, listar_uc, None, None
    )
    
    # Test: Listar asociaciones existentes para control ID 2
    print("\n📋 Listando asociaciones para control ID 2:")
    response = controller.obtener_consultas_por_control(2)
    print(f"   Respuesta: {response}")
    
    # Test: Asociar consulta ID 1 al control ID 2
    print("\n🔗 Asociando consulta ID 1 al control ID 2:")
    response = controller.asociar_consulta(
        control_id=2,
        consulta_id=1,
        es_disparo=True,
        orden=1
    )
    print(f"   Respuesta: {response}")
    
    # Test: Listar asociaciones después de la asociación
    print("\n📋 Listando asociaciones después de asociar:")
    response = controller.obtener_consultas_por_control(2)
    print(f"   Respuesta: {response}")

if __name__ == "__main__":
    test_consulta_control()