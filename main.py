"""
Ejemplo de uso completo del sistema

Este archivo demuestra cómo se integran todas las capas
de Clean Architecture en Python.
"""
from src.domain.services.usuario_service import UsuarioService
from src.infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from src.presentation.controllers.usuario_controller import UsuarioController


def main():
    """Función principal que demuestra el flujo completo"""
    
    # Configurar dependencias (Inyección de dependencias)
    # Infrastructure layer
    usuario_repository = SQLiteUsuarioRepository("ejemplo.db")
    
    # Domain layer
    usuario_service = UsuarioService(usuario_repository)
    
    # Application layer
    registrar_usuario_use_case = RegistrarUsuarioUseCase(
        usuario_repository, 
        usuario_service
    )
    
    # Presentation layer
    usuario_controller = UsuarioController(registrar_usuario_use_case)
    
    # Simular una petición HTTP
    datos_request = {
        'nombre': 'Juan Pérez',
        'email': 'juan@ejemplo.com'
    }
    
    # Procesar la petición
    resultado = usuario_controller.registrar_usuario(datos_request)
    
    print("Resultado del registro:")
    print(f"Status: {resultado['status']}")
    if 'data' in resultado:
        print(f"Usuario creado: {resultado['data']}")
        print(f"Mensaje: {resultado['message']}")
    else:
        print(f"Error: {resultado['error']}")


if __name__ == "__main__":
    main()