"""
Script de prueba para verificar la carga de controles
"""
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.presentation.controllers.control_controller import ControlController
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.application.use_cases.actualizar_control_use_case import ActualizarControlUseCase
from src.application.use_cases.eliminar_control_use_case import EliminarControlUseCase
from src.domain.services.control_service import ControlService

def test_control_controller():
    """Prueba el controlador de controles"""
    
    # Configurar repositorios
    db_path = "sistema_controles.db"
    control_repo = SQLiteControlRepository(db_path)
    consulta_repo = SQLiteConsultaRepository(db_path)
    conexion_repo = SQLiteConexionRepository(db_path)
    parametro_repo = SQLiteParametroRepository(db_path)
    referente_repo = SQLiteReferenteRepository(db_path)
    
    # Configurar servicio
    control_service = ControlService(control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo)
    
    # Configurar use cases
    crear_control_uc = CrearControlUseCase(control_service)
    listar_controles_uc = ListarControlesUseCase(control_service)
    actualizar_control_uc = ActualizarControlUseCase(control_service, control_repo)
    eliminar_control_uc = EliminarControlUseCase(control_service, control_repo)
    
    # Configurar controlador
    control_ctrl = ControlController(crear_control_uc, listar_controles_uc, actualizar_control_uc, eliminar_control_uc)
    
    # Probar listado
    print("Probando listar_controles()...")
    response = control_ctrl.listar_controles()
    
    print(f"Success: {response['success']}")
    print(f"Data: {response['data']}")
    print(f"Message: {response['message']}")
    
    if response['success']:
        print(f"\n✅ Se encontraron {len(response['data'])} controles:")
        for control in response['data']:
            print(f"  - ID: {control['id']}, Nombre: {control['nombre']}")
        
        # Simular formato del combo
        control_names = [""] + [f"{c['id']} - {c['nombre']}" for c in response['data']]
        print(f"\n📋 Valores para combo: {control_names}")
    else:
        print(f"❌ Error: {response['message']}")

if __name__ == "__main__":
    test_control_controller()