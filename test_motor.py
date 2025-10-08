#!/usr/bin/env python3
"""
Script para probar el motor de ejecución
Crea una programación de prueba y la ejecuta
"""
import sys
import time
from pathlib import Path
from datetime import datetime, time as dt_time

# Agregar src al path
sys.path.append(str(Path(__file__).parent / "src"))

from src.infrastructure.database.database_setup import DatabaseSetup
from src.infrastructure.repositories.sqlite_programacion_repository import SQLiteProgramacionRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.domain.entities.programacion import Programacion, TipoProgramacion

def crear_programacion_prueba():
    """Crea una programación de prueba cada 2 minutos"""
    print("🧪 Creando programación de prueba...")
    
    # Configurar BD
    db_path = "sistema_controles.db"
    db_setup = DatabaseSetup(db_path)
    db_setup.initialize_database()
    
    # Repositorios
    programacion_repo = SQLiteProgramacionRepository(db_path)
    control_repo = SQLiteControlRepository(db_path)
    
    # Obtener primer control disponible
    controles = control_repo.listar_todos()
    if not controles:
        print("❌ No hay controles disponibles. Cree un control primero.")
        return
    
    control = controles[0]
    print(f"📋 Usando control: {control.nombre} (ID: {control.id})")
    
    # Eliminar programaciones anteriores para este control (cleanup)
    programaciones_existentes = programacion_repo.obtener_por_control_id(control.id)
    for prog in programaciones_existentes:
        if "PRUEBA MOTOR" in prog.nombre:
            programacion_repo.eliminar(prog.id)
            print(f"🗑️ Eliminada programación anterior: {prog.nombre}")
    
    # Crear nueva programación por intervalo (cada 2 minutos)
    programacion = Programacion(
        id=None,
        control_id=control.id,
        nombre="PRUEBA MOTOR - Cada 2 minutos",
        descripcion="Programación de prueba para el motor de ejecución automática",
        tipo_programacion=TipoProgramacion.INTERVALO,
        activo=True,
        
        # Configuración básica
        hora_ejecucion=None,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        
        # Configuración de intervalo
        dias_semana=None,
        dias_mes=None,
        intervalo_minutos=2,  # Cada 2 minutos
        
        # Estado
        ultima_ejecucion=None,
        proxima_ejecucion=None,
        total_ejecuciones=0,
        fecha_creacion=datetime.now(),
        fecha_modificacion=None,
        creado_por="Script de prueba"
    )
    
    # Calcular próxima ejecución
    programacion._calcular_proxima_ejecucion()
    
    # Guardar
    programacion_creada = programacion_repo.crear(programacion)
    
    print(f"✅ Programación creada exitosamente:")
    print(f"   ID: {programacion_creada.id}")
    print(f"   Nombre: {programacion_creada.nombre}")
    print(f"   Tipo: {programacion_creada.tipo_programacion.value}")
    print(f"   Intervalo: {programacion_creada.intervalo_minutos} minutos")
    print(f"   Próxima ejecución: {programacion_creada.proxima_ejecucion}")
    print(f"   Descripción: {programacion_creada.obtener_descripcion_programacion()}")

def crear_programacion_diaria():
    """Crea una programación diaria para probar"""
    print("🧪 Creando programación diaria de prueba...")
    
    # Configurar BD
    db_path = "sistema_controles.db"
    db_setup = DatabaseSetup(db_path)
    db_setup.initialize_database()
    
    # Repositorios
    programacion_repo = SQLiteProgramacionRepository(db_path)
    control_repo = SQLiteControlRepository(db_path)
    
    # Obtener primer control disponible
    controles = control_repo.listar_todos()
    if not controles:
        print("❌ No hay controles disponibles. Cree un control primero.")
        return
    
    control = controles[0]
    print(f"📋 Usando control: {control.nombre} (ID: {control.id})")
    
    # Eliminar programaciones anteriores para este control (cleanup)
    programaciones_existentes = programacion_repo.obtener_por_control_id(control.id)
    for prog in programaciones_existentes:
        if "PRUEBA DIARIA" in prog.nombre:
            programacion_repo.eliminar(prog.id)
            print(f"🗑️ Eliminada programación anterior: {prog.nombre}")
    
    # Crear nueva programación diaria (en 1 minuto desde ahora)
    ahora = datetime.now()
    hora_ejecucion = dt_time((ahora.hour * 60 + ahora.minute + 1) // 60 % 24, (ahora.minute + 1) % 60)
    
    programacion = Programacion(
        id=None,
        control_id=control.id,
        nombre="PRUEBA DIARIA - Test Motor",
        descripcion="Programación diaria de prueba para el motor",
        tipo_programacion=TipoProgramacion.DIARIA,
        activo=True,
        
        # Configuración diaria
        hora_ejecucion=hora_ejecucion,
        fecha_inicio=datetime.now(),
        fecha_fin=None,
        
        # No aplica para diaria
        dias_semana=None,
        dias_mes=None,
        intervalo_minutos=None,
        
        # Estado
        ultima_ejecucion=None,
        proxima_ejecucion=None,
        total_ejecuciones=0,
        fecha_creacion=datetime.now(),
        fecha_modificacion=None,
        creado_por="Script de prueba"
    )
    
    # Calcular próxima ejecución
    programacion._calcular_proxima_ejecucion()
    
    # Guardar
    programacion_creada = programacion_repo.crear(programacion)
    
    print(f"✅ Programación diaria creada exitosamente:")
    print(f"   ID: {programacion_creada.id}")
    print(f"   Nombre: {programacion_creada.nombre}")
    print(f"   Hora: {programacion_creada.hora_ejecucion}")
    print(f"   Próxima ejecución: {programacion_creada.proxima_ejecucion}")
    print(f"   Descripción: {programacion_creada.obtener_descripcion_programacion()}")

def listar_programaciones():
    """Lista todas las programaciones activas"""
    print("📋 Listando programaciones activas...")
    
    # Configurar BD
    db_path = "sistema_controles.db"
    db_setup = DatabaseSetup(db_path)
    db_setup.initialize_database()
    
    programacion_repo = SQLiteProgramacionRepository(db_path)
    programaciones = programacion_repo.obtener_todas()
    
    if not programaciones:
        print("📝 No hay programaciones configuradas")
        return
    
    print(f"\n📊 Total de programaciones: {len(programaciones)}")
    print("=" * 80)
    
    for prog in programaciones:
        estado = "🟢 ACTIVA" if prog.activo else "🔴 INACTIVA"
        print(f"ID: {prog.id} | {estado} | {prog.nombre}")
        print(f"   Tipo: {prog.tipo_programacion.value}")
        print(f"   Control ID: {prog.control_id}")
        print(f"   Descripción: {prog.obtener_descripcion_programacion()}")
        print(f"   Última ejecución: {prog.ultima_ejecucion or 'Nunca'}")
        print(f"   Próxima ejecución: {prog.proxima_ejecucion or 'No calculada'}")
        print(f"   Total ejecuciones: {prog.total_ejecuciones}")
        print("-" * 80)

def main():
    if len(sys.argv) < 2:
        print("🎯 Uso: py test_motor.py [intervalo|diaria|listar]")
        return
    
    accion = sys.argv[1].lower()
    
    if accion == "intervalo":
        crear_programacion_prueba()
    elif accion == "diaria":
        crear_programacion_diaria()
    elif accion == "listar":
        listar_programaciones()
    else:
        print("❌ Acción no válida. Use: intervalo, diaria, o listar")

if __name__ == "__main__":
    main()