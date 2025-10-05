"""
Ejemplo completo del sistema de controles con SQLite

Este archivo demuestra cómo usar el sistema completo de controles
con todos los repositorios SQLite implementados.
"""
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository

from src.domain.services.control_service import ControlService
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.crear_parametro_use_case import CrearParametroUseCase
from src.application.use_cases.crear_consulta_use_case import CrearConsultaUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase

from src.application.dto.control_dto import CrearControlDTO
from src.application.dto.entidades_dto import CrearParametroDTO, CrearConsultaDTO, CrearConexionDTO, CrearReferenteDTO

from src.domain.entities.conexion import Conexion
from src.domain.entities.referente import Referente


def ejemplo_sistema_completo():
    """Ejemplo de uso del sistema completo con SQLite"""
    
    print("=== Sistema de Controles SQL - Completo con SQLite ===\n")
    
    # 1. Configurar todos los repositorios SQLite (usan la misma BD)
    db_path = "sistema_controles.db"
    
    control_repository = SQLiteControlRepository(db_path)
    parametro_repository = SQLiteParametroRepository(db_path)
    consulta_repository = SQLiteConsultaRepository(db_path)
    conexion_repository = SQLiteConexionRepository(db_path)
    referente_repository = SQLiteReferenteRepository(db_path)
    
    # 2. Configurar servicios
    control_service = ControlService(
        control_repository=control_repository,
        consulta_repository=consulta_repository,
        conexion_repository=conexion_repository,
        parametro_repository=parametro_repository,
        referente_repository=referente_repository
    )
    
    # 3. Configurar casos de uso
    crear_parametro_use_case = CrearParametroUseCase(parametro_repository)
    crear_consulta_use_case = CrearConsultaUseCase(consulta_repository)
    crear_control_use_case = CrearControlUseCase(control_service)
    listar_controles_use_case = ListarControlesUseCase(control_service)
    
    print("✅ Todos los repositorios SQLite configurados correctamente")
    print(f"📁 Base de datos: {db_path}")
    print()
    
    # 4. Crear datos de ejemplo
    print("📝 Creando datos de ejemplo...\n")
    
    # Crear conexión de ejemplo (guardada en SQLite)
    conexion_ejemplo = Conexion(
        nombre="SQL Server Producción",
        base_datos="EmpresaDB",
        servidor="sqlserver.empresa.com",
        puerto=1433,
        usuario="control_user",
        contraseña="password123",
        tipo_motor="sqlserver",  # Esta es la BD donde se ejecutarán los controles
        activa=True
    )
    conexion_guardada = conexion_repository.guardar(conexion_ejemplo)
    print(f"✅ Conexión creada: {conexion_guardada}")
    
    # Crear referente de ejemplo
    referente_ejemplo = Referente(
        nombre="Juan Pérez",
        email="juan.perez@empresa.com",
        carpeta_red="\\\\servidor\\reportes\\controles",
        notificar_por_email=True,
        notificar_por_archivo=True
    )
    referente_guardado = referente_repository.guardar(referente_ejemplo)
    print(f"✅ Referente creado: {referente_guardado}")
    
    # Crear parámetros
    try:
        parametro_fecha = crear_parametro_use_case.ejecutar(CrearParametroDTO(
            nombre="fecha_proceso",
            tipo="date",
            descripcion="Fecha del proceso a controlar",
            obligatorio=True
        ))
        print(f"✅ Parámetro creado: {parametro_fecha.nombre}")
        
        parametro_estado = crear_parametro_use_case.ejecutar(CrearParametroDTO(
            nombre="estado",
            tipo="string",
            descripcion="Estado a filtrar",
            valor_por_defecto="ACTIVO",
            obligatorio=False
        ))
        print(f"✅ Parámetro creado: {parametro_estado.nombre}")
    except ValueError as e:
        print(f"⚠️  Error creando parámetros: {e}")
    
    # Crear consultas
    try:
        consulta_disparo = crear_consulta_use_case.ejecutar(CrearConsultaDTO(
            nombre="Verificar Procesos Pendientes",
            sql="SELECT COUNT(*) as total FROM procesos WHERE fecha = :fecha_proceso AND estado = :estado",
            descripcion="Consulta que verifica si hay procesos pendientes"
        ))
        print(f"✅ Consulta de disparo creada: {consulta_disparo.nombre}")
        
        consulta_detalle = crear_consulta_use_case.ejecutar(CrearConsultaDTO(
            nombre="Detalle Procesos Problema",
            sql="SELECT id, nombre, fecha, estado FROM procesos WHERE fecha = :fecha_proceso AND estado != 'COMPLETADO'",
            descripcion="Consulta que obtiene el detalle de procesos con problemas"
        ))
        print(f"✅ Consulta de detalle creada: {consulta_detalle.nombre}")
    except ValueError as e:
        print(f"⚠️  Error creando consultas: {e}")
    
    print()
    
    # 5. Mostrar el estado actual
    print("📊 Estado actual del sistema:")
    
    conexiones = conexion_repository.obtener_todos()
    print(f"   - Conexiones: {len(conexiones)}")
    
    parametros = parametro_repository.obtener_todos()
    print(f"   - Parámetros: {len(parametros)}")
    
    consultas = consulta_repository.obtener_todos()
    print(f"   - Consultas: {len(consultas)}")
    
    referentes = referente_repository.obtener_todos()
    print(f"   - Referentes: {len(referentes)}")
    
    controles = listar_controles_use_case.ejecutar()
    print(f"   - Controles: {len(controles.data) if hasattr(controles, 'data') else len(controles)}")
    
    print("\n🎯 Resumen:")
    print("✅ Toda la información del sistema se guarda en SQLite")
    print("✅ Los controles se configuran y almacenan en SQLite")
    print("🎲 Los controles se EJECUTARÁN sobre las bases de datos configuradas")
    print("   (SQL Server, PostgreSQL, MySQL, iSeries, etc.)")
    print("\n📋 Arquitectura:")
    print("   SQLite (control.db) -> Configuración del sistema")
    print("   SQL Server/Oracle/etc -> Bases de datos objetivo de los controles")


def mostrar_estructura_sqlite():
    """Muestra la estructura de tablas creadas en SQLite"""
    import sqlite3
    
    db_path = "sistema_controles.db"
    print("\n🗄️  Estructura de la base de datos SQLite:")
    
    with sqlite3.connect(db_path) as conn:
        cursor = conn.execute("""
            SELECT name FROM sqlite_master 
            WHERE type='table' AND name NOT LIKE 'sqlite_%'
            ORDER BY name
        """)
        tablas = cursor.fetchall()
        
        for (tabla,) in tablas:
            print(f"\n📋 Tabla: {tabla}")
            cursor = conn.execute(f"PRAGMA table_info({tabla})")
            columnas = cursor.fetchall()
            
            for columna in columnas:
                nombre = columna[1]
                tipo = columna[2]
                not_null = "NOT NULL" if columna[3] else ""
                pk = "PRIMARY KEY" if columna[5] else ""
                print(f"   - {nombre}: {tipo} {not_null} {pk}".strip())


if __name__ == "__main__":
    ejemplo_sistema_completo()
    mostrar_estructura_sqlite()