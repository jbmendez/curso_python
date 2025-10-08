"""
Script de prueba para la ventana de programaciones
"""
import tkinter as tk
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '.')))

from src.presentation.gui.programaciones_window import ProgramacionesWindow
from src.presentation.controllers.programacion_controller import ProgramacionController
from src.presentation.controllers.control_controller import ControlController

# Imports para controladores
from src.infrastructure.repositories.sqlite_programacion_repository import SQLiteProgramacionRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.application.use_cases.crear_programacion_use_case import CrearProgramacionUseCase
from src.application.use_cases.listar_programaciones_use_case import ListarProgramacionesUseCase
from src.application.use_cases.actualizar_programacion_use_case import ActualizarProgramacionUseCase
from src.application.use_cases.eliminar_programacion_use_case import EliminarProgramacionUseCase
from src.application.use_cases.activar_desactivar_programacion_use_case import ActivarDesactivarProgramacionUseCase
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.application.use_cases.actualizar_control_use_case import ActualizarControlUseCase
from src.application.use_cases.eliminar_control_use_case import EliminarControlUseCase
from src.domain.services.control_service import ControlService

def test_programaciones_window():
    """Prueba la ventana de programaciones"""
    root = tk.Tk()
    root.withdraw()  # Ocultar ventana principal
    
    # Configurar repositorios
    db_path = "sistema_controles.db"
    programacion_repo = SQLiteProgramacionRepository(db_path)
    control_repo = SQLiteControlRepository(db_path)
    
    # Configurar use cases
    crear_programacion_uc = CrearProgramacionUseCase(programacion_repo, control_repo)
    listar_programaciones_uc = ListarProgramacionesUseCase(programacion_repo, control_repo)
    actualizar_programacion_uc = ActualizarProgramacionUseCase(programacion_repo)
    eliminar_programacion_uc = EliminarProgramacionUseCase(programacion_repo)
    activar_desactivar_programacion_uc = ActivarDesactivarProgramacionUseCase(programacion_repo)
    
    # Para el control controller necesitamos más dependencias
    from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
    from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
    from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
    from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
    
    consulta_repo = SQLiteConsultaRepository(db_path)
    conexion_repo = SQLiteConexionRepository(db_path)
    parametro_repo = SQLiteParametroRepository(db_path)
    referente_repo = SQLiteReferenteRepository(db_path)
    
    control_service = ControlService(control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo)
    crear_control_uc = CrearControlUseCase(control_service)
    listar_controles_uc = ListarControlesUseCase(control_service)
    actualizar_control_uc = ActualizarControlUseCase(control_service, control_repo)
    eliminar_control_uc = EliminarControlUseCase(control_service, control_repo)
    
    # Configurar controladores
    programacion_ctrl = ProgramacionController(
        crear_programacion_uc, listar_programaciones_uc, actualizar_programacion_uc,
        eliminar_programacion_uc, activar_desactivar_programacion_uc
    )
    
    control_ctrl = ControlController(
        crear_control_uc, listar_controles_uc, actualizar_control_uc, eliminar_control_uc
    )
    
    # Crear y mostrar ventana
    try:
        programaciones_window = ProgramacionesWindow(root, programacion_ctrl, control_ctrl)
        programaciones_window.show()
        print("✅ Ventana de programaciones creada exitosamente")
        
        root.mainloop()
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_programaciones_window()