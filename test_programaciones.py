"""
Script de prueba para el sistema de programaciones

Prueba la creación, listado y gestión de programaciones
"""
from datetime import datetime, time
from src.infrastructure.repositories.sqlite_programacion_repository import SQLiteProgramacionRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.domain.entities.programacion import Programacion, TipoProgramacion, DiaSemana
from src.application.use_cases.crear_programacion_use_case import CrearProgramacionUseCase
from src.application.use_cases.listar_programaciones_use_case import ListarProgramacionesUseCase
from src.application.dto.programacion_dto import CrearProgramacionDTO

def probar_sistema_programaciones():
    print("🧪 Probando sistema de programaciones...")
    
    # Crear repositorios
    programacion_repo = SQLiteProgramacionRepository('sistema_controles.db')
    control_repo = SQLiteControlRepository('sistema_controles.db')
    
    # Crear casos de uso
    crear_programacion_uc = CrearProgramacionUseCase(programacion_repo, control_repo)
    listar_programaciones_uc = ListarProgramacionesUseCase(programacion_repo, control_repo)
    
    # Listar controles disponibles
    controles = control_repo.obtener_todos()
    print(f"\n📋 Controles disponibles: {len(controles)}")
    for control in controles[:3]:  # Solo mostrar los primeros 3
        print(f"  - ID: {control.id}, Nombre: {control.nombre}")
    
    if not controles:
        print("❌ No hay controles disponibles para probar")
        return
    
    # Usar el primer control para la prueba
    control_test = controles[0]
    print(f"\n🎯 Usando control: {control_test.nombre} (ID: {control_test.id})")
    
    try:
        # Crear programación diaria
        dto_diaria = CrearProgramacionDTO(
            control_id=control_test.id,
            nombre="Ejecución Diaria Test",
            descripcion="Programación de prueba que ejecuta todos los días",
            tipo_programacion=TipoProgramacion.DIARIA,
            activo=True,
            hora_ejecucion=time(9, 30),  # 09:30
            creado_por="Sistema Test"
        )
        
        programacion_diaria = crear_programacion_uc.ejecutar(dto_diaria)
        print(f"✅ Programación diaria creada: ID {programacion_diaria.id}")
        print(f"   Descripción: {programacion_diaria.obtener_descripcion_programacion()}")
        
        # Crear programación semanal
        dto_semanal = CrearProgramacionDTO(
            control_id=control_test.id,
            nombre="Ejecución Semanal Test",
            descripcion="Programación de prueba que ejecuta lunes, miércoles y viernes",
            tipo_programacion=TipoProgramacion.SEMANAL,
            activo=True,
            hora_ejecucion=time(14, 0),  # 14:00
            dias_semana=[DiaSemana.LUNES, DiaSemana.MIERCOLES, DiaSemana.VIERNES],
            creado_por="Sistema Test"
        )
        
        programacion_semanal = crear_programacion_uc.ejecutar(dto_semanal)
        print(f"✅ Programación semanal creada: ID {programacion_semanal.id}")
        print(f"   Descripción: {programacion_semanal.obtener_descripcion_programacion()}")
        
        # Crear programación por intervalo
        dto_intervalo = CrearProgramacionDTO(
            control_id=control_test.id,
            nombre="Ejecución por Intervalo Test",
            descripcion="Programación de prueba que ejecuta cada 30 minutos",
            tipo_programacion=TipoProgramacion.INTERVALO,
            activo=True,
            intervalo_minutos=30,
            creado_por="Sistema Test"
        )
        
        programacion_intervalo = crear_programacion_uc.ejecutar(dto_intervalo)
        print(f"✅ Programación por intervalo creada: ID {programacion_intervalo.id}")
        print(f"   Descripción: {programacion_intervalo.obtener_descripcion_programacion()}")
        
        # Listar programaciones del control
        print(f"\n📋 Listando programaciones del control {control_test.nombre}:")
        response = listar_programaciones_uc.ejecutar(control_id=control_test.id)
        
        if response.success:
            print(f"   Total: {response.total}, Activas: {response.activas}")
            for prog in response.data:
                estado = "🟢" if prog.activo else "🔴"
                print(f"   {estado} {prog.nombre} - {prog.descripcion_programacion}")
        else:
            print(f"   ❌ Error: {response.message}")
        
        # Probar lógica de ejecución
        print("\n⏰ Probando lógica de ejecución:")
        fecha_actual = datetime.now()
        for programacion in [programacion_diaria, programacion_semanal, programacion_intervalo]:
            debe_ejecutarse = programacion.debe_ejecutarse_ahora(fecha_actual)
            print(f"   - {programacion.nombre}: {'✅ Debe ejecutarse' if debe_ejecutarse else '⏳ No debe ejecutarse'}")
        
        # Obtener estadísticas
        stats = programacion_repo.obtener_estadisticas(control_test.id)
        print(f"\n📊 Estadísticas del control:")
        print(f"   - Total programaciones: {stats['total_programaciones']}")
        print(f"   - Activas: {stats['activas']}")
        print(f"   - Ejecuciones totales: {stats['total_ejecuciones']}")
        
        print(f"\n🎉 Pruebas completadas exitosamente!")
        
    except Exception as e:
        print(f"❌ Error durante las pruebas: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    probar_sistema_programaciones()