"""
Configuración y inicialización de la base de datos

Proporciona utilidades para inicializar todas las tablas necesarias
para el sistema de controles y programaciones.
"""
import sqlite3
from pathlib import Path
from typing import List


class DatabaseSetup:
    """Clase para configurar e inicializar la base de datos del sistema"""
    
    def __init__(self, db_path: str = "sistema_controles.db"):
        """
        Inicializa la configuración de base de datos
        
        Args:
            db_path: Ruta al archivo de base de datos SQLite
        """
        self.db_path = db_path
    
    def initialize_database(self) -> None:
        """
        Verifica que la base de datos existe y está lista para usar
        
        No crea tablas nuevas, solo verifica que el archivo de BD existe
        """
        try:
            # Verificar que el archivo de BD existe
            db_file = Path(self.db_path)
            if not db_file.exists():
                raise Exception(f"Base de datos no encontrada: {self.db_path}")
            
            # Verificar conexión básica
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table' LIMIT 1")
                result = cursor.fetchone()
                if not result:
                    raise Exception("Base de datos sin tablas")
                    
        except Exception as e:
            raise Exception(f"Error al verificar la base de datos: {str(e)}")
    
    def _crear_tabla_usuarios(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de usuarios"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                email TEXT UNIQUE NOT NULL,
                fecha_creacion TEXT NOT NULL,
                activo BOOLEAN DEFAULT 1
            )
        """)
    
    def _crear_tabla_conexiones(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de conexiones"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS conexiones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                servidor TEXT,
                puerto INTEGER,
                base_datos TEXT,
                usuario TEXT,
                password_encriptado TEXT,
                fecha_creacion TEXT NOT NULL,
                activo BOOLEAN DEFAULT 1
            )
        """)
    
    def _crear_tabla_consultas(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de consultas"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                conexion_id INTEGER NOT NULL,
                sql_texto TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                activo BOOLEAN DEFAULT 1,
                FOREIGN KEY (conexion_id) REFERENCES conexiones (id)
            )
        """)
    
    def _crear_tabla_controles(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de controles"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS controles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                tipo TEXT NOT NULL,
                fecha_creacion TEXT NOT NULL,
                activo BOOLEAN DEFAULT 1,
                configuracion TEXT
            )
        """)
    
    def _crear_tabla_parametros(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de parámetros"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parametros (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                valor_defecto TEXT,
                descripcion TEXT,
                activo BOOLEAN DEFAULT 1
            )
        """)
    
    def _crear_tabla_referentes(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de referentes"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS referentes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nombre TEXT NOT NULL,
                tipo TEXT NOT NULL,
                configuracion TEXT,
                activo BOOLEAN DEFAULT 1
            )
        """)
    
    def _crear_tabla_control_referente(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de asociación control-referente"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS control_referente (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_id INTEGER NOT NULL,
                referente_id INTEGER NOT NULL,
                orden INTEGER DEFAULT 0,
                FOREIGN KEY (control_id) REFERENCES controles (id),
                FOREIGN KEY (referente_id) REFERENCES referentes (id),
                UNIQUE(control_id, referente_id)
            )
        """)
    
    def _crear_tabla_consultas_controles(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de asociación consulta-control"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS consultas_controles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                consulta_id INTEGER NOT NULL,
                control_id INTEGER NOT NULL,
                orden INTEGER DEFAULT 0,
                FOREIGN KEY (consulta_id) REFERENCES consultas (id),
                FOREIGN KEY (control_id) REFERENCES controles (id),
                UNIQUE(consulta_id, control_id)
            )
        """)
    
    def _crear_tabla_resultados_ejecucion(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de resultados de ejecución"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS resultados_ejecucion (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_id INTEGER NOT NULL,
                fecha_ejecucion TEXT NOT NULL,
                estado TEXT NOT NULL,
                mensaje TEXT,
                tiempo_ejecucion_ms INTEGER,
                registros_procesados INTEGER DEFAULT 0,
                FOREIGN KEY (control_id) REFERENCES controles (id)
            )
        """)
    
    def _crear_tabla_programaciones(self, cursor: sqlite3.Cursor) -> None:
        """Crea la tabla de programaciones"""
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS programaciones (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                control_id INTEGER NOT NULL,
                nombre TEXT NOT NULL,
                descripcion TEXT,
                tipo_programacion TEXT NOT NULL,
                activo BOOLEAN NOT NULL DEFAULT 1,
                
                -- Configuración de horario
                hora_ejecucion TEXT,
                fecha_inicio TEXT,
                fecha_fin TEXT,
                
                -- Configuración específica por tipo (JSON)
                dias_semana TEXT,
                dias_mes TEXT,
                intervalo_minutos INTEGER,
                
                -- Estado de ejecución
                ultima_ejecucion TEXT,
                proxima_ejecucion TEXT,
                total_ejecuciones INTEGER DEFAULT 0,
                
                -- Metadatos
                fecha_creacion TEXT NOT NULL,
                fecha_modificacion TEXT,
                creado_por TEXT,
                
                FOREIGN KEY (control_id) REFERENCES controles (id)
            )
        """)
    
    def _crear_indices(self, cursor: sqlite3.Cursor) -> None:
        """Crea índices para optimización de consultas"""
        indices = [
            "CREATE INDEX IF NOT EXISTS idx_programaciones_activo ON programaciones(activo)",
            "CREATE INDEX IF NOT EXISTS idx_programaciones_proxima_ejecucion ON programaciones(proxima_ejecucion)",
            "CREATE INDEX IF NOT EXISTS idx_programaciones_control_id ON programaciones(control_id)",
            "CREATE INDEX IF NOT EXISTS idx_programaciones_tipo ON programaciones(tipo_programacion)",
            "CREATE INDEX IF NOT EXISTS idx_resultados_fecha ON resultados_ejecucion(fecha_ejecucion)",
            "CREATE INDEX IF NOT EXISTS idx_resultados_control ON resultados_ejecucion(control_id)"
        ]
        
        for indice in indices:
            try:
                cursor.execute(indice)
            except sqlite3.OperationalError as e:
                # Ignorar errores de columnas inexistentes en BD antigua
                if "no such column" not in str(e):
                    raise
    
    def verificar_integridad(self) -> List[str]:
        """
        Verifica la integridad de la base de datos
        
        Returns:
            Lista de problemas encontrados (vacía si todo está bien)
        """
        problemas = []
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Verificar integridad de claves foráneas
                cursor.execute("PRAGMA foreign_key_check")
                errores_fk = cursor.fetchall()
                
                if errores_fk:
                    problemas.extend([f"Error FK: {error}" for error in errores_fk])
                
                # Verificar que las tablas principales existen
                cursor.execute("""
                    SELECT name FROM sqlite_master 
                    WHERE type='table' AND name IN (
                        'usuarios', 'conexiones', 'consultas', 'controles',
                        'parametros', 'referentes', 'programaciones'
                    )
                """)
                tablas_existentes = {row[0] for row in cursor.fetchall()}
                tablas_requeridas = {
                    'usuarios', 'conexiones', 'consultas', 'controles',
                    'parametros', 'referentes', 'programaciones'
                }
                
                tablas_faltantes = tablas_requeridas - tablas_existentes
                if tablas_faltantes:
                    problemas.append(f"Tablas faltantes: {', '.join(tablas_faltantes)}")
                
        except Exception as e:
            problemas.append(f"Error al verificar integridad: {str(e)}")
        
        return problemas