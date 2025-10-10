#!/usr/bin/env python3
"""
Test para verificar que los controles sin consulta de disparo funcionen correctamente
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from src.infrastructure.database.sqlite_database import SQLiteDatabase
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_consulta_control_repository import SQLiteConsultaControlRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_resultado_ejecucion_repository import SQLiteResultadoEjecucionRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.infrastructure.services.excel_generator_service import ExcelGeneratorService
from src.domain.services.ejecucion_control_service import EjecucionControlService
from src.domain.entities.control import Control
from src.domain.entities.conexion import Conexion, TipoConexion
from src.domain.entities.consulta import Consulta
from src.domain.entities.consulta_control import ConsultaControl
from src.domain.entities.estado_ejecucion import EstadoEjecucion

def crear_test_database():
    """Crea una base de datos de prueba con datos de ejemplo"""
    db = SQLiteDatabase("test_control_sin_disparo.db")
    
    # Repositorios
    conexion_repo = SQLiteConexionRepository(db)
    control_repo = SQLiteControlRepository(db)
    consulta_repo = SQLiteConsultaRepository(db)
    consulta_control_repo = SQLiteConsultaControlRepository(db)
    parametro_repo = SQLiteParametroRepository(db)
    resultado_repo = SQLiteResultadoEjecucionRepository(db)
    referente_repo = SQLiteReferenteRepository(db)
    
    # Crear tablas
    db.crear_tablas()
    
    # Crear conexión de test
    conexion = Conexion(
        id=1,
        nombre="TestDB",
        tipo=TipoConexion.SQLITE,
        servidor="",
        puerto=None,
        base_datos="test_control_sin_disparo.db",
        usuario="",
        contrasena="",
        activa=True
    )
    conexion_repo.crear(conexion)
    
    # Crear control sin consulta de disparo
    control = Control(
        id=1,
        nombre="Control Sin Disparo",
        descripcion="Control de prueba sin consulta de disparo específica",
        disparar_si_hay_datos=True,  # Se dispara si hay datos
        activo=True
    )
    control_repo.crear(control)
    
    # Crear consulta que retornará datos
    consulta = Consulta(
        id=1,
        nombre="Consulta Test",
        descripcion="Consulta que devuelve datos de prueba",
        sql="SELECT 1 as id, 'Dato de prueba' as descripcion UNION SELECT 2, 'Otro dato'",
        conexion_id=1,
        activa=True
    )
    consulta_repo.crear(consulta)
    
    # Asociar consulta al control (sin marcar como disparo)
    asociacion = ConsultaControl(
        control_id=1,
        consulta_id=1,
        es_disparo=False,  # NO es consulta de disparo
        orden=1,
        activa=True
    )
    consulta_control_repo.crear(asociacion)
    
    return db, {
        'conexion_repo': conexion_repo,
        'control_repo': control_repo,
        'consulta_repo': consulta_repo,
        'consulta_control_repo': consulta_control_repo,
        'parametro_repo': parametro_repo,
        'resultado_repo': resultado_repo,
        'referente_repo': referente_repo
    }, conexion, control

def test_control_sin_disparo():
    """Test principal"""
    print("=== Test Control Sin Consulta de Disparo ===")
    
    # Crear base de datos de prueba
    db, repos, conexion, control = crear_test_database()
    
    try:
        # Crear servicio de ejecución
        excel_service = ExcelGeneratorService()
        ejecucion_service = EjecucionControlService(
            control_repository=repos['control_repo'],
            consulta_repository=repos['consulta_repo'],
            consulta_control_repository=repos['consulta_control_repo'],
            parametro_repository=repos['parametro_repo'],
            resultado_ejecucion_repository=repos['resultado_repo'],
            referente_repository=repos['referente_repo'],
            excel_generator_service=excel_service
        )
        
        print(f"Ejecutando control: {control.nombre}")
        print(f"- Control configurado para disparar si hay datos: {control.disparar_si_hay_datos}")
        print(f"- Control sin consulta de disparo específica")
        
        # Ejecutar control
        resultado = ejecucion_service.ejecutar_control(control, conexion)
        
        print(f"\nResultado de la ejecución:")
        print(f"- Estado: {resultado.estado}")
        print(f"- Mensaje: {resultado.mensaje}")
        print(f"- Filas disparo: {resultado.total_filas_disparo}")
        print(f"- Filas disparadas: {resultado.total_filas_disparadas}")
        print(f"- Consultas ejecutadas: {len(resultado.resultados_consultas_disparadas)}")
        
        # Verificar que el control se disparó correctamente
        if resultado.estado == EstadoEjecucion.CONTROL_DISPARADO:
            print("\n✅ SUCCESS: El control se disparó correctamente sin consulta de disparo específica")
            
            # Verificar que se generaron resultados
            if resultado.total_filas_disparadas > 0:
                print(f"✅ SUCCESS: Se procesaron {resultado.total_filas_disparadas} filas")
            else:
                print("❌ WARNING: No se procesaron filas")
                
            # Mostrar resultados de consultas
            for i, res_consulta in enumerate(resultado.resultados_consultas_disparadas):
                print(f"- Consulta {i+1}: {res_consulta.filas_afectadas} filas")
                
        else:
            print(f"❌ FAILED: Estado inesperado: {resultado.estado}")
            
        # Test de solo disparo (debería fallar)
        print(f"\n=== Test Ejecutar Solo Disparo (debería fallar) ===")
        resultado_solo_disparo = ejecucion_service.ejecutar_control(control, conexion, ejecutar_solo_disparo=True)
        
        if resultado_solo_disparo.estado == EstadoEjecucion.ERROR:
            print("✅ SUCCESS: Ejecutar solo disparo falló correctamente (no hay consulta de disparo)")
            print(f"- Mensaje: {resultado_solo_disparo.mensaje}")
        else:
            print(f"❌ FAILED: Ejecutar solo disparo debería haber fallado, estado: {resultado_solo_disparo.estado}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpiar
        db.cerrar()
        try:
            os.remove("test_control_sin_disparo.db")
            print("\nBase de datos de prueba eliminada")
        except:
            pass

def test_control_sin_disparo_sin_datos():
    """Test con control que no debería dispararse"""
    print("\n=== Test Control Sin Disparo - Sin Datos ===")
    
    # Crear base de datos de prueba
    db = SQLiteDatabase("test_control_sin_disparo_empty.db")
    
    # Repositorios
    conexion_repo = SQLiteConexionRepository(db)
    control_repo = SQLiteControlRepository(db)
    consulta_repo = SQLiteConsultaRepository(db)
    consulta_control_repo = SQLiteConsultaControlRepository(db)
    parametro_repo = SQLiteParametroRepository(db)
    resultado_repo = SQLiteResultadoEjecucionRepository(db)
    referente_repo = SQLiteReferenteRepository(db)
    
    try:
        # Crear tablas
        db.crear_tablas()
        
        # Crear conexión de test
        conexion = Conexion(
            id=1,
            nombre="TestDB",
            tipo=TipoConexion.SQLITE,
            servidor="",
            puerto=None,
            base_datos="test_control_sin_disparo_empty.db",
            usuario="",
            contrasena="",
            activa=True
        )
        conexion_repo.crear(conexion)
        
        # Crear control sin consulta de disparo
        control = Control(
            id=1,
            nombre="Control Sin Disparo Empty",
            descripcion="Control que no debería dispararse",
            disparar_si_hay_datos=True,  # Se dispara si hay datos
            activo=True
        )
        control_repo.crear(control)
        
        # Crear consulta que NO retornará datos
        consulta = Consulta(
            id=1,
            nombre="Consulta Empty",
            descripcion="Consulta que no devuelve datos",
            sql="SELECT 1 as id WHERE 1=0",  # No devuelve filas
            conexion_id=1,
            activa=True
        )
        consulta_repo.crear(consulta)
        
        # Asociar consulta al control (sin marcar como disparo)
        asociacion = ConsultaControl(
            control_id=1,
            consulta_id=1,
            es_disparo=False,
            orden=1,
            activa=True
        )
        consulta_control_repo.crear(asociacion)
        
        # Crear servicio de ejecución
        excel_service = ExcelGeneratorService()
        ejecucion_service = EjecucionControlService(
            control_repository=control_repo,
            consulta_repository=consulta_repo,
            consulta_control_repository=consulta_control_repo,
            parametro_repository=parametro_repo,
            resultado_ejecucion_repository=resultado_repo,
            referente_repository=referente_repo,
            excel_generator_service=excel_service
        )
        
        print(f"Ejecutando control: {control.nombre}")
        
        # Ejecutar control
        resultado = ejecucion_service.ejecutar_control(control, conexion)
        
        print(f"\nResultado de la ejecución:")
        print(f"- Estado: {resultado.estado}")
        print(f"- Mensaje: {resultado.mensaje}")
        print(f"- Filas disparo: {resultado.total_filas_disparo}")
        print(f"- Filas disparadas: {resultado.total_filas_disparadas}")
        
        # Verificar que el control NO se disparó
        if resultado.estado == EstadoEjecucion.SIN_DATOS:
            print("\n✅ SUCCESS: El control NO se disparó correctamente (no hay datos)")
        else:
            print(f"❌ FAILED: Estado inesperado: {resultado.estado}")
            
    except Exception as e:
        print(f"❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
        
    finally:
        # Limpiar
        db.cerrar()
        try:
            os.remove("test_control_sin_disparo_empty.db")
        except:
            pass

if __name__ == "__main__":
    test_control_sin_disparo()
    test_control_sin_disparo_sin_datos()
    print("\n=== Tests completados ===")