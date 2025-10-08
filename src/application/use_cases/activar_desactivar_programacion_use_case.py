"""
Caso de uso para activar/desactivar programación

Maneja la activación y desactivación de programaciones
con recálculo de próximas ejecuciones.
"""
from ...domain.repositories.programacion_repository import ProgramacionRepository


class ActivarDesactivarProgramacionUseCase:
    """Caso de uso para activar o desactivar una programación"""
    
    def __init__(self, programacion_repository: ProgramacionRepository):
        self.programacion_repository = programacion_repository
    
    def ejecutar(self, programacion_id: int, activo: bool) -> bool:
        """
        Activa o desactiva una programación
        
        Args:
            programacion_id: ID de la programación
            activo: True para activar, False para desactivar
            
        Returns:
            bool: True si se actualizó correctamente
            
        Raises:
            ValueError: Si la programación no existe
        """
        # Verificar que la programación existe
        programacion = self.programacion_repository.obtener_por_id(programacion_id)
        if not programacion:
            raise ValueError(f"La programación con ID {programacion_id} no existe")
        
        # Si no hay cambio, no hacer nada
        if programacion.activo == activo:
            return True
        
        # Actualizar usando el repositorio
        resultado = self.programacion_repository.activar_desactivar(programacion_id, activo)
        
        if resultado and activo:
            # Si se activó, recalcular próxima ejecución
            programacion.activo = activo
            programacion._calcular_proxima_ejecucion()
            self.programacion_repository.actualizar(programacion)
        
        return resultado