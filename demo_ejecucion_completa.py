"""
Demo completa del sistema de ejecución de c    # Configurar servicios
    usuario_service = UsuarioService(usuario_repo)
    control_service = ControlService(
        control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo
    )
    ejecucion_service = EjecucionControlService(
        control_repo, parametro_repo, consulta_repo, referente_repo, conexion_repo
    )s
"""
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'src')))

from datetime import datetime, timedelta
from src.infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.infrastructure.repositories.sqlite_resultado_ejecucion_repository import SQLiteResultadoEjecucionRepository

from src.domain.services.control_service import ControlService
from src.domain.services.ejecucion_control_service import EjecucionControlService

from src.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.application.use_cases.crear_parametro_use_case import CrearParametroUseCase
from src.application.use_cases.crear_consulta_use_case import CrearConsultaUseCase
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.use_cases.crear_referente_use_case import CrearReferenteUseCase
from src.application.use_cases.ejecutar_control_use_case import EjecutarControlUseCase
from src.application.use_cases.obtener_historial_ejecucion_use_case import ObtenerHistorialEjecucionUseCase

from src.presentation.controllers.usuario_controller import UsuarioController
from src.presentation.controllers.control_controller import ControlController
from src.presentation.controllers.parametro_controller import ParametroController
from src.presentation.controllers.consulta_controller import ConsultaController
from src.presentation.controllers.conexion_controller import ConexionController
from src.presentation.controllers.referente_controller import ReferenteController
from src.presentation.controllers.ejecucion_controller import EjecucionController

from src.domain.services.usuario_service import UsuarioService


def main():
    """Demo completa del sistema de ejecución de controles"""
    
    print("=== DEMO SISTEMA DE EJECUCIÓN DE CONTROLES ===\n")
    
    # Configurar repositorios (usando mismo DB para consistencia)
    db_path = "demo_ejecucion.db"
    
    usuario_repo = SQLiteUsuarioRepository(db_path)
    conexion_repo = SQLiteConexionRepository(db_path)
    control_repo = SQLiteControlRepository(db_path)
    parametro_repo = SQLiteParametroRepository(db_path)
    consulta_repo = SQLiteConsultaRepository(db_path)
    referente_repo = SQLiteReferenteRepository(db_path)
    resultado_repo = SQLiteResultadoEjecucionRepository(db_path)
    
    # Configurar servicios
    usuario_service = UsuarioService(usuario_repo)
    control_service = ControlService(
        control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo
    )
    ejecucion_service = EjecucionControlService(
        control_repo, parametro_repo, consulta_repo, referente_repo, conexion_repo
    )
    
    # Configurar casos de uso
    registrar_usuario_uc = RegistrarUsuarioUseCase(usuario_repo, usuario_service)
    crear_conexion_uc = CrearConexionUseCase(conexion_repo)
    crear_control_uc = CrearControlUseCase(control_service)
    listar_controles_uc = ListarControlesUseCase(control_service)
    crear_parametro_uc = CrearParametroUseCase(parametro_repo)
    crear_consulta_uc = CrearConsultaUseCase(consulta_repo)
    crear_referente_uc = CrearReferenteUseCase(referente_repo)
    ejecutar_control_uc = EjecutarControlUseCase(control_repo, conexion_repo, resultado_repo, ejecucion_service)
    historial_uc = ObtenerHistorialEjecucionUseCase(resultado_repo, control_repo)
    
    # Configurar controladores
    usuario_ctrl = UsuarioController(registrar_usuario_uc)
    conexion_ctrl = ConexionController(crear_conexion_uc)
    control_ctrl = ControlController(crear_control_uc, listar_controles_uc)
    parametro_ctrl = ParametroController(crear_parametro_uc)
    consulta_ctrl = ConsultaController(crear_consulta_uc)
    referente_ctrl = ReferenteController(crear_referente_uc)
    ejecucion_ctrl = EjecucionController(ejecutar_control_uc, historial_uc)
    
    # 1. Crear datos básicos usando los controladores (Clean Architecture)
    print("1. Creando datos básicos...")
    
    # Usuario
    import time
    timestamp = int(time.time())
    usuario_response = usuario_ctrl.crear_usuario(f"admin{timestamp}@demo.com", "Admin", "Demo")
    if not usuario_response['success']:
        print(f"   Error creando usuario: {usuario_response['error']}")
        return
    print(f"   Usuario creado: {usuario_response['data']['email']}")
    
    # Conexión
    conexion_response = conexion_ctrl.crear_conexion(
        "PostgreSQL Producción",
        "postgresql",
        "localhost",
        5432,
        "prod_db",
        "admin",
        "password123"
    )
    if not conexion_response['success']:
        print(f"   Error creando conexión: {conexion_response['error']}")
        return
    conexion_id = conexion_response['data']['id']
    print(f"   Conexión creada: {conexion_response['data']['nombre']}")
    
    # Control
    control_response = control_ctrl.crear_control_simple(
        "Control de Ventas Diarias",
        "Verifica que las ventas diarias no excedan el umbral",
        conexion_id,
        usuario_response['data']['id']
    )
    if not control_response['success']:
        print(f"   Error creando control: {control_response['error']}")
        return
    control_id = control_response['data']['id']
    print(f"   Control creado: {control_response['data']['nombre']}")
    
    # Parámetro
    parametro_response = parametro_ctrl.crear_parametro(
        control_id,
        "umbral_ventas",
        "number",
        "Umbral máximo de ventas diarias",
        10000.0
    )
    if not parametro_response['success']:
        print(f"   Error creando parámetro: {parametro_response['error']}")
        return
    print(f"   Parámetro creado: {parametro_response['data']['nombre']}")
    
    # Consulta de disparo
    consulta_disparo_response = consulta_ctrl.crear_consulta(
        control_id,
        "Consulta Disparo Ventas",
        "SELECT COUNT(*) as total FROM ventas WHERE fecha = CURRENT_DATE AND monto > :umbral_ventas",
        "disparo"
    )
    if not consulta_disparo_response['success']:
        print(f"   Error creando consulta de disparo: {consulta_disparo_response['error']}")
        return
    print(f"   Consulta de disparo creada: {consulta_disparo_response['data']['nombre']}")
    
    # Consulta disparada
    consulta_disparada_response = consulta_ctrl.crear_consulta(
        control_id,
        "Detalle Ventas Altas",
        "SELECT * FROM ventas WHERE fecha = CURRENT_DATE AND monto > :umbral_ventas ORDER BY monto DESC",
        "disparada"
    )
    if not consulta_disparada_response['success']:
        print(f"   Error creando consulta disparada: {consulta_disparada_response['error']}")
        return
    print(f"   Consulta disparada creada: {consulta_disparada_response['data']['nombre']}")
    
    # Referente
    referente_response = referente_ctrl.crear_referente(
        control_id,
        "Gerente de Ventas",
        "gerente.ventas@empresa.com",
        "Juan Pérez"
    )
    if not referente_response['success']:
        print(f"   Error creando referente: {referente_response['error']}")
        return
    print(f"   Referente creado: {referente_response['data']['nombre']}")
    
    print("\n2. Ejecutando controles...")
    
    # Ejecutar el control con diferentes escenarios
    print("   Escenario 1: Ejecución normal (mock)")
    resultado1 = ejecucion_ctrl.ejecutar_control(
        control_id=control_id,
        parametros_adicionales={"umbral_ventas": 5000.0},
        mock_execution=True
    )
    
    if resultado1['success']:
        data = resultado1['data']
        print(f"   ✓ Control ejecutado: {data['estado']}")
        print(f"     - Tiempo total: {data['tiempo_total_ejecucion_ms']:.2f}ms")
        print(f"     - Filas disparo: {data['total_filas_disparo']}")
        print(f"     - Filas disparadas: {data['total_filas_disparadas']}")
        print(f"     - Mensaje: {data['mensaje']}")
    else:
        print(f"   ✗ Error: {resultado1['error']}")
    
    print("\n   Escenario 2: Solo consulta de disparo")
    resultado2 = ejecucion_ctrl.ejecutar_control(
        control_id=control_id,
        parametros_adicionales={"umbral_ventas": 15000.0},
        ejecutar_solo_disparo=True,
        mock_execution=True
    )
    
    if resultado2['success']:
        data = resultado2['data']
        print(f"   ✓ Solo disparo ejecutado: {data['estado']}")
        print(f"     - Tiempo: {data['tiempo_total_ejecucion_ms']:.2f}ms")
        print(f"     - Filas encontradas: {data['total_filas_disparo']}")
    
    print("\n   Escenario 3: Múltiples ejecuciones para historial")
    # Simular varias ejecuciones
    for i in range(3):
        ejecucion_ctrl.ejecutar_control(
            control_id=control_id,
            parametros_adicionales={"umbral_ventas": 8000.0 + (i * 1000)},
            mock_execution=True
        )
    
    print("   ✓ 3 ejecuciones adicionales completadas")
    
    print("\n3. Consultando historial y estadísticas...")
    
    # Obtener historial
    historial = ejecucion_ctrl.obtener_historial(
        control_id=control_id,
        limite=10,
        incluir_detalles=True
    )
    
    if historial['success']:
        print(f"   Historial obtenido: {historial['total']} ejecuciones")
        for i, ejecucion in enumerate(historial['data'][:3]):  # Mostrar solo las primeras 3
            print(f"     {i+1}. {ejecucion['fecha_ejecucion'][:19]} - {ejecucion['estado']}")
            print(f"        Tiempo: {ejecucion['tiempo_total_ejecucion_ms']:.2f}ms")
    
    # Obtener estadísticas
    estadisticas = ejecucion_ctrl.obtener_estadisticas()
    
    if estadisticas['success']:
        stats = estadisticas['data']
        print(f"\n   Estadísticas generales:")
        print(f"     - Total ejecuciones: {stats['total_ejecuciones']}")
        print(f"     - Ejecuciones exitosas: {stats['ejecuciones_exitosas']}")
        print(f"     - Tasa de éxito: {stats['tasa_exito']:.1f}%")
        print(f"     - Tiempo promedio: {stats['tiempo_promedio_ejecucion_ms']:.2f}ms")
    
    # Obtener resumen por controles
    resumen = ejecucion_ctrl.obtener_resumen_controles()
    
    if resumen['success']:
        print(f"\n   Resumen por controles:")
        for control in resumen['data']:
            print(f"     - {control['control_nombre']}: {control['total_ejecuciones']} ejecuciones")
            print(f"       Último estado: {control['ultimo_estado']}")
            print(f"       Tasa éxito: {control['tasa_exito']:.1f}%")
    
    # Obtener últimos resultados del control
    ultimos = ejecucion_ctrl.obtener_ultimos_resultados_control(control_id, 3)
    
    if ultimos['success']:
        print(f"\n   Últimos 3 resultados del control:")
        for resultado in ultimos['data']:
            print(f"     - {resultado['fecha_ejecucion'][:19]}: {resultado['estado']}")
            print(f"       Parámetros: {resultado['parametros_utilizados']}")
    
    print("\n4. Probando diferentes filtros...")
    
    # Filtrar por estado
    exitosos = ejecucion_ctrl.obtener_historial(estado="EXITOSO", limite=5)
    if exitosos['success']:
        print(f"   Ejecuciones exitosas: {exitosos['total']}")
    
    # Filtrar por fechas (últimas 24 horas)
    fecha_ayer = (datetime.now() - timedelta(days=1)).isoformat()
    fecha_hoy = datetime.now().isoformat()
    
    recientes = ejecucion_ctrl.obtener_historial(
        fecha_desde=fecha_ayer,
        fecha_hasta=fecha_hoy,
        limite=10
    )
    
    if recientes['success']:
        print(f"   Ejecuciones últimas 24h: {recientes['total']}")
    
    print(f"\n=== DEMO COMPLETADA ===")
    print(f"Base de datos guardada en: {db_path}")
    print("Puedes examinar los datos usando cualquier cliente SQLite")


if __name__ == "__main__":
    main()