"""
Ejemplo de uso del sistema de controles SQL

Este archivo demuestra cómo usar el sistema completo de controles
siguiendo la arquitectura Clean Architecture.
"""
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.domain.services.control_service import ControlService
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.presentation.controllers.control_controller import ControlController
from src.application.dto.control_dto import CrearControlDTO


def ejemplo_sistema_controles():
    """Ejemplo de uso del sistema de controles"""
    
    print("=== Sistema de Controles SQL ===\n")
    
    # 1. Configurar dependencias (Inyección de dependencias)
    # Infrastructure layer - TODOS los repositorios SQLite implementados
    control_repository = SQLiteControlRepository("ejemplo_controles.db")
    
    # Importar y configurar todos los repositorios SQLite
    from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
    from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
    from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
    from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
    
    parametro_repository = SQLiteParametroRepository("ejemplo_controles.db")
    consulta_repository = SQLiteConsultaRepository("ejemplo_controles.db")
    conexion_repository = SQLiteConexionRepository("ejemplo_controles.db")
    referente_repository = SQLiteReferenteRepository("ejemplo_controles.db")
    
    # Domain layer - Ahora con TODOS los repositorios implementados
    control_service = ControlService(
        control_repository=control_repository,
        consulta_repository=consulta_repository,  # ✅ Implementado
        conexion_repository=conexion_repository,  # ✅ Implementado  
        parametro_repository=parametro_repository, # ✅ Implementado
        referente_repository=referente_repository  # ✅ Implementado
    )
    
    # Application layer
    crear_control_use_case = CrearControlUseCase(control_service)
    listar_controles_use_case = ListarControlesUseCase(control_service)
    
    # Presentation layer
    control_controller = ControlController(
        crear_control_use_case,
        listar_controles_use_case
    )
    
    # 2. Ejemplo de listado de controles (inicialmente vacío)
    print("📋 Listando controles existentes:")
    resultado_listado = control_controller.listar_controles()
    print(f"Status: {resultado_listado['status']}")
    print(f"Mensaje: {resultado_listado['message']}")
    print(f"Controles encontrados: {len(resultado_listado['data'])}\n")
    
    # 3. Ejemplo de creación de control (esto fallará porque no tenemos las dependencias)
    print("➕ Intentando crear un control de ejemplo:")
    datos_control = {
        'nombre': 'Control Ejemplo',
        'descripcion': 'Un control de ejemplo para demostrar el sistema',
        'disparar_si_hay_datos': True,
        'conexion_id': 1,  # Estas IDs no existen realmente
        'consulta_disparo_id': 1,
        'consultas_a_disparar_ids': [2, 3],
        'parametros_ids': [1, 2],
        'referentes_ids': [1]
    }
    
    resultado_creacion = control_controller.crear_control(datos_control)
    print(f"Status: {resultado_creacion['status']}")
    if 'error' in resultado_creacion:
        print(f"Error esperado (faltan dependencias): {resultado_creacion['error']}")
    else:
        print(f"Control creado: {resultado_creacion['data']['nombre']}")
    
    print("\n=== Estructura del Sistema ===")
    print("✅ Domain Layer: Entidades y reglas de negocio definidas")
    print("   - Control, Parámetro, Consulta, Conexión, Referente")
    print("✅ Application Layer: Casos de uso implementados") 
    print("   - CrearControlUseCase, ListarControlesUseCase")
    print("✅ Infrastructure Layer: Repositorios SQLite COMPLETOS")
    print("   - SQLite: Control, Parámetro, Consulta, Conexión, Referente")
    print("✅ Presentation Layer: ControlController")
    print("\n🎯 Sistema de Controles:")
    print("   📋 Configuración almacenada en SQLite")
    print("   🎲 Controles ejecutados sobre bases objetivo (SQL Server, etc.)")
    print("\n📝 Próximos pasos:")
    print("   - Implementar servicio de ejecución de controles")
    print("   - Agregar sistema de notificaciones")
    print("   - Completar soporte para SQL Server")
    print("   - Crear API REST completa")


if __name__ == "__main__":
    ejemplo_sistema_controles()