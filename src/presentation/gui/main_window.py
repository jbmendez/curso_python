"""
Ventana principal de la aplicación de gestión de controles
"""
import tkinter as tk
from tkinter import ttk, messagebox
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.infrastructure.repositories.sqlite_usuario_repository import SQLiteUsuarioRepository
from src.infrastructure.repositories.sqlite_control_repository import SQLiteControlRepository
from src.infrastructure.repositories.sqlite_parametro_repository import SQLiteParametroRepository
from src.infrastructure.repositories.sqlite_consulta_repository import SQLiteConsultaRepository
from src.infrastructure.repositories.sqlite_consulta_control_repository import SQLiteConsultaControlRepository
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
from src.infrastructure.repositories.sqlite_control_referente_repository import SQLiteControlReferenteRepository
from src.infrastructure.repositories.sqlite_resultado_ejecucion_repository import SQLiteResultadoEjecucionRepository

from src.domain.services.usuario_service import UsuarioService
from src.domain.services.control_service import ControlService
from src.domain.services.ejecucion_control_service import EjecucionControlService
from src.domain.services.conexion_test_service import ConexionTestFactory
from src.infrastructure.services.postgresql_conexion_test import PostgreSQLConexionTest
from src.infrastructure.services.mysql_conexion_test import MySQLConexionTest
from src.infrastructure.services.sqlserver_conexion_test import SQLServerConexionTest
from src.infrastructure.services.sqlite_conexion_test import SQLiteConexionTest
from src.infrastructure.services.ibmiseries_conexion_test import IBMiSeriesConexionTest
from src.infrastructure.services.ibmiseries_jdbc_conexion_test import IBMiSeriesJDBCConexionTest
from src.infrastructure.services.ibmiseries_selector import IBMiSeriesConexionSelector

from src.application.use_cases.registrar_usuario_use_case import RegistrarUsuarioUseCase
from src.application.use_cases.crear_control_use_case import CrearControlUseCase
from src.application.use_cases.actualizar_control_use_case import ActualizarControlUseCase
from src.application.use_cases.eliminar_control_use_case import EliminarControlUseCase
from src.application.use_cases.listar_controles_use_case import ListarControlesUseCase
from src.application.use_cases.crear_parametro_use_case import CrearParametroUseCase
from src.application.use_cases.crear_consulta_use_case import CrearConsultaUseCase
from src.application.use_cases.listar_consultas_use_case import ListarConsultasUseCase
from src.application.use_cases.actualizar_consulta_use_case import ActualizarConsultaUseCase
from src.application.use_cases.eliminar_consulta_use_case import EliminarConsultaUseCase
from src.application.use_cases.asociar_consulta_control_use_case import AsociarConsultaControlUseCase
from src.application.use_cases.listar_consulta_control_use_case import ListarConsultaControlUseCase
from src.application.use_cases.desasociar_consulta_control_use_case import DesasociarConsultaControlUseCase
from src.application.use_cases.establecer_consulta_disparo_use_case import EstablecerConsultaDisparoUseCase
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.use_cases.actualizar_conexion_use_case import ActualizarConexionUseCase
from src.application.use_cases.listar_conexiones_use_case import ListarConexionesUseCase
from src.application.use_cases.crear_referente_use_case import CrearReferenteUseCase
from src.application.use_cases.listar_referentes_use_case import ListarReferentesUseCase
from src.application.use_cases.actualizar_referente_use_case import ActualizarReferenteUseCase
from src.application.use_cases.eliminar_referente_use_case import EliminarReferenteUseCase
from src.application.use_cases.ejecutar_control_use_case import EjecutarControlUseCase
from src.application.use_cases.obtener_historial_ejecucion_use_case import ObtenerHistorialEjecucionUseCase

from src.presentation.controllers.usuario_controller import UsuarioController
from src.presentation.controllers.control_controller import ControlController
from src.presentation.controllers.parametro_controller import ParametroController
from src.presentation.controllers.consulta_controller import ConsultaController
from src.presentation.controllers.consulta_control_controller import ConsultaControlController
from src.presentation.controllers.conexion_controller import ConexionController
from src.presentation.controllers.referente_controller import ReferenteController
from src.presentation.controllers.control_referente_controller import ControlReferenteController
from src.presentation.controllers.ejecucion_controller import EjecucionController

from src.presentation.gui.dialogs import CreateConnectionDialog, EditConnectionDialog, CreateControlDialog, EditControlDialog, ExecutionParametersDialog
from src.presentation.gui.referente_dialogs import ReferentesListDialog, ControlReferentesDialog


class MainWindow:
    """Ventana principal de la aplicación"""
    
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sistema de Gestión de Controles SQL")
        self.root.geometry("1200x800")
        
        # Configurar base de datos centralizada
        self.db_path = "sistema_controles.db"
        
        # Inicializar servicios de conexión
        from src.infrastructure.config.conexion_config import inicializar_servicios_conexion
        inicializar_servicios_conexion()
        
        self.setup_controllers()
        
        # Crear interfaz
        self.create_widgets()
        
    def setup_controllers(self):
        """Configura todos los controladores siguiendo Clean Architecture"""
        # Inicializar servicios de prueba de conexión
        self._inicializar_servicios_conexion()
        
        # Repositorios
        usuario_repo = SQLiteUsuarioRepository(self.db_path)
        conexion_repo = SQLiteConexionRepository(self.db_path)
        control_repo = SQLiteControlRepository(self.db_path)
        parametro_repo = SQLiteParametroRepository(self.db_path)
        consulta_repo = SQLiteConsultaRepository(self.db_path)
        consulta_control_repo = SQLiteConsultaControlRepository(self.db_path)
        referente_repo = SQLiteReferenteRepository(self.db_path)
        control_referente_repo = SQLiteControlReferenteRepository(self.db_path)
        resultado_repo = SQLiteResultadoEjecucionRepository(self.db_path)
        
        # Servicios
        usuario_service = UsuarioService(usuario_repo)
        self.control_service = ControlService(
            control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo
        )
        ejecucion_service = EjecucionControlService(
            control_repo, parametro_repo, consulta_repo, referente_repo, conexion_repo, consulta_control_repo
        )
        
        # Casos de uso
        registrar_usuario_uc = RegistrarUsuarioUseCase(usuario_repo, usuario_service)
        crear_conexion_uc = CrearConexionUseCase(conexion_repo)
        actualizar_conexion_uc = ActualizarConexionUseCase(conexion_repo)
        listar_conexiones_uc = ListarConexionesUseCase(conexion_repo)
        crear_control_uc = CrearControlUseCase(self.control_service)
        actualizar_control_uc = ActualizarControlUseCase(self.control_service, control_repo)
        eliminar_control_uc = EliminarControlUseCase(self.control_service, control_repo)
        listar_controles_uc = ListarControlesUseCase(self.control_service)
        crear_parametro_uc = CrearParametroUseCase(parametro_repo)
        crear_consulta_uc = CrearConsultaUseCase(consulta_repo)
        listar_consultas_uc = ListarConsultasUseCase(consulta_repo)
        actualizar_consulta_uc = ActualizarConsultaUseCase(consulta_repo)
        eliminar_consulta_uc = EliminarConsultaUseCase(consulta_repo)
        # Use cases de asociaciones consulta-control
        asociar_consulta_control_uc = AsociarConsultaControlUseCase(consulta_control_repo)
        listar_consulta_control_uc = ListarConsultaControlUseCase(consulta_control_repo)
        desasociar_consulta_control_uc = DesasociarConsultaControlUseCase(consulta_control_repo)
        establecer_consulta_disparo_uc = EstablecerConsultaDisparoUseCase(consulta_control_repo)
        crear_referente_uc = CrearReferenteUseCase(referente_repo)
        listar_referentes_uc = ListarReferentesUseCase(referente_repo)
        actualizar_referente_uc = ActualizarReferenteUseCase(referente_repo)
        eliminar_referente_uc = EliminarReferenteUseCase(referente_repo)
        ejecutar_control_uc = EjecutarControlUseCase(control_repo, conexion_repo, resultado_repo, ejecucion_service)
        historial_uc = ObtenerHistorialEjecucionUseCase(resultado_repo, control_repo)
        
        # Controladores
        self.usuario_ctrl = UsuarioController(registrar_usuario_uc)
        self.conexion_ctrl = ConexionController(crear_conexion_uc, listar_conexiones_uc, actualizar_conexion_uc)
        self.control_ctrl = ControlController(crear_control_uc, listar_controles_uc, actualizar_control_uc, eliminar_control_uc)
        self.parametro_ctrl = ParametroController(crear_parametro_uc)
        self.consulta_ctrl = ConsultaController(crear_consulta_uc, listar_consultas_uc, actualizar_consulta_uc, eliminar_consulta_uc)
        self.consulta_control_ctrl = ConsultaControlController(
            asociar_consulta_control_uc, listar_consulta_control_uc, 
            desasociar_consulta_control_uc, establecer_consulta_disparo_uc
        )
        self.referente_ctrl = ReferenteController(
            crear_referente_uc, listar_referentes_uc, actualizar_referente_uc, 
            eliminar_referente_uc, referente_repo, control_referente_repo
        )
        self.control_referente_ctrl = ControlReferenteController(
            control_referente_repo, control_repo, referente_repo
        )
        self.ejecucion_ctrl = EjecucionController(ejecutar_control_uc, historial_uc)
        
    def create_widgets(self):
        """Crea la interfaz gráfica"""
        # Barra de menú
        self.create_menu()
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.root)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de controles
        self.create_controls_tab(notebook)
        
        # Pestaña de conexiones
        self.create_connections_tab(notebook)
        
        # Pestaña de consultas
        self.create_consultas_tab(notebook)
        
        # Pestaña de ejecución
        self.create_execution_tab(notebook)
        
        # Pestaña de historial
        self.create_history_tab(notebook)
        
        # Cargar datos iniciales
        self.load_initial_data()
        
    def load_initial_data(self):
        """Carga todos los datos iniciales de la aplicación"""
        try:
            # Cargar controles (usado en múltiples lugares)
            self.refresh_controls()
            self.refresh_execution_controls()
            
            # Cargar filtros de historial
            self.load_filter_controls()
            
            # Cargar historial
            self.refresh_history()
            
            print("DEBUG - Datos iniciales cargados exitosamente")
        except Exception as e:
            print(f"DEBUG - Error cargando datos iniciales: {e}")
            import traceback
            traceback.print_exc()
        
    def create_menu(self):
        """Crea la barra de menú"""
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)
        
        # Menú Archivo
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Archivo", menu=file_menu)
        file_menu.add_command(label="Nuevo Control", command=self.new_control)
        file_menu.add_command(label="Nueva Conexión", command=self.new_connection)
        file_menu.add_separator()
        file_menu.add_command(label="Gestionar Referentes", command=self.manage_referentes)
        file_menu.add_separator()
        file_menu.add_command(label="Salir", command=self.root.quit)
        
        # Menú Herramientas
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Herramientas", menu=tools_menu)
        tools_menu.add_command(label="Ejecutar Control", command=self.execute_control)
        tools_menu.add_command(label="Ver Historial", command=self.view_history)
        
        # Menú Ayuda
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Ayuda", menu=help_menu)
        help_menu.add_command(label="Acerca de", command=self.show_about)
        
    def create_controls_tab(self, notebook):
        """Crea la pestaña de gestión de controles"""
        controls_frame = ttk.Frame(notebook)
        notebook.add(controls_frame, text="Controles")
        
        # Frame superior para botones
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Nuevo Control", command=self.new_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Editar Control", command=self.edit_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Gestionar Consultas", command=self.manage_control_consultas).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Gestionar Referentes", command=self.manage_control_referentes).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Eliminar Control", command=self.delete_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Actualizar", command=self.refresh_controls).pack(side="left", padx=5)
        
        # Lista de controles
        columns = ("ID", "Nombre", "Descripción", "Conexión", "Estado", "Fecha Creación")
        self.controls_tree = ttk.Treeview(controls_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.controls_tree.heading(col, text=col)
            self.controls_tree.column(col, width=150)
        
        # Scrollbar para la lista
        scrollbar_controls = ttk.Scrollbar(controls_frame, orient="vertical", command=self.controls_tree.yview)
        self.controls_tree.configure(yscrollcommand=scrollbar_controls.set)
        
        # Empaquetar lista y scrollbar
        self.controls_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_controls.pack(side="right", fill="y")
        
        # Cargar controles iniciales
        self.refresh_controls()
        
    def create_connections_tab(self, notebook):
        """Crea la pestaña de gestión de conexiones"""
        connections_frame = ttk.Frame(notebook)
        notebook.add(connections_frame, text="Conexiones")
        
        # Frame superior para botones
        buttons_frame = ttk.Frame(connections_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Nueva Conexión", command=self.new_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Editar Conexión", command=self.edit_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Probar Conexión", command=self.test_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Actualizar", command=self.refresh_connections).pack(side="left", padx=5)
        
        # Lista de conexiones
        columns = ("ID", "Nombre", "Motor", "Servidor", "Puerto", "Base Datos", "Usuario", "Estado")
        self.connections_tree = ttk.Treeview(connections_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.connections_tree.heading(col, text=col)
            self.connections_tree.column(col, width=120)
        
        # Scrollbar
        scrollbar_connections = ttk.Scrollbar(connections_frame, orient="vertical", command=self.connections_tree.yview)
        self.connections_tree.configure(yscrollcommand=scrollbar_connections.set)
        
        # Empaquetar
        self.connections_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_connections.pack(side="right", fill="y")
        
        # Cargar conexiones iniciales
        self.refresh_connections()
        
    def create_consultas_tab(self, notebook):
        """Crea la pestaña de gestión de consultas"""
        consultas_frame = ttk.Frame(notebook)
        notebook.add(consultas_frame, text="Consultas")
        
        # Frame superior para botones
        buttons_frame = ttk.Frame(consultas_frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(buttons_frame, text="Nueva Consulta", command=self.new_consulta).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Editar Consulta", command=self.edit_consulta).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Eliminar Consulta", command=self.delete_consulta).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Ejecutar Consulta", command=self.execute_consulta).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Actualizar", command=self.refresh_consultas).pack(side="left", padx=5)
        
        # Lista de consultas
        columns = ("ID", "Nombre", "Descripción", "Conexión", "Control", "Fecha Creación")
        self.consultas_tree = ttk.Treeview(consultas_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        for col in columns:
            self.consultas_tree.heading(col, text=col)
            self.consultas_tree.column(col, width=130)
        
        # Scrollbar para la lista
        scrollbar_consultas = ttk.Scrollbar(consultas_frame, orient="vertical", command=self.consultas_tree.yview)
        self.consultas_tree.configure(yscrollcommand=scrollbar_consultas.set)
        
        # Empaquetar lista y scrollbar
        self.consultas_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_consultas.pack(side="right", fill="y")
        
        # Cargar consultas iniciales
        self.refresh_consultas()
        
    def create_execution_tab(self, notebook):
        """Crea la pestaña de ejecución de controles"""
        execution_frame = ttk.Frame(notebook)
        notebook.add(execution_frame, text="Ejecución")
        
        # Frame izquierdo para selección
        left_frame = ttk.LabelFrame(execution_frame, text="Seleccionar Control")
        left_frame.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        
        # Lista de controles para ejecutar
        self.execution_tree = ttk.Treeview(left_frame, columns=("ID", "Nombre", "Estado"), show="headings", height=10)
        self.execution_tree.heading("ID", text="ID")
        self.execution_tree.heading("Nombre", text="Nombre")
        self.execution_tree.heading("Estado", text="Estado")
        self.execution_tree.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Botones de ejecución
        buttons_exec_frame = ttk.Frame(left_frame)
        buttons_exec_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(buttons_exec_frame, text="Ejecutar Control", command=self.execute_selected_control).pack(side="left", padx=5)
        ttk.Button(buttons_exec_frame, text="Solo Disparo", command=self.execute_trigger_only).pack(side="left", padx=5)
        
        # Frame derecho para resultados
        right_frame = ttk.LabelFrame(execution_frame, text="Resultados de Ejecución")
        right_frame.pack(side="right", fill="both", expand=True, padx=5, pady=5)
        
        # Área de texto para mostrar resultados
        self.results_text = tk.Text(right_frame, height=20, width=50)
        results_scrollbar = ttk.Scrollbar(right_frame, orient="vertical", command=self.results_text.yview)
        self.results_text.configure(yscrollcommand=results_scrollbar.set)
        
        self.results_text.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        results_scrollbar.pack(side="right", fill="y")
        
        # Cargar controles para ejecución
        self.refresh_execution_controls()
        
    def create_history_tab(self, notebook):
        """Crea la pestaña de historial de ejecuciones"""
        history_frame = ttk.Frame(notebook)
        notebook.add(history_frame, text="Historial")
        
        # Frame superior para filtros
        filters_frame = ttk.LabelFrame(history_frame, text="Filtros")
        filters_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Label(filters_frame, text="Control:").grid(row=0, column=0, padx=5, pady=5)
        self.filter_control = ttk.Combobox(filters_frame, width=20)
        self.filter_control.grid(row=0, column=1, padx=5, pady=5)
        self.filter_control.bind('<<ComboboxSelected>>', self.filter_history)
        
        ttk.Label(filters_frame, text="Estado:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_estado = ttk.Combobox(filters_frame, values=["Todos", "EXITOSO", "ERROR", "CONTROL_DISPARADO", "SIN_DATOS"])
        self.filter_estado.set("Todos")
        self.filter_estado.grid(row=0, column=3, padx=5, pady=5)
        self.filter_estado.bind('<<ComboboxSelected>>', self.filter_history)
        
        ttk.Button(filters_frame, text="Filtrar", command=lambda: self.filter_history()).grid(row=0, column=4, padx=5, pady=5)
        ttk.Button(filters_frame, text="Limpiar", command=self.clear_filters).grid(row=0, column=5, padx=5, pady=5)
        
        # Lista de historial
        columns = ("ID", "Control", "Fecha", "Estado", "Tiempo (ms)", "Filas Disparo", "Mensaje")
        self.history_tree = ttk.Treeview(history_frame, columns=columns, show="headings", height=20)
        
        # Configurar columnas
        for col in columns:
            self.history_tree.heading(col, text=col)
            self.history_tree.column(col, width=130)
        
        # Scrollbar para historial
        scrollbar_history = ttk.Scrollbar(history_frame, orient="vertical", command=self.history_tree.yview)
        self.history_tree.configure(yscrollcommand=scrollbar_history.set)
        
        # Empaquetar
        self.history_tree.pack(side="left", fill="both", expand=True, padx=5, pady=5)
        scrollbar_history.pack(side="right", fill="y")
        
        # Cargar historial inicial
        self.refresh_history()
        
    def load_filter_controls(self):
        """Carga los controles disponibles en el combo de filtro"""
        try:
            response = self.control_ctrl.obtener_todas()
            
            if response.get('success', False):
                controles = response.get('data', [])
                
                # Crear lista de nombres para el combo
                control_names = ["Todos"]  # Opción para mostrar todos
                control_mapping = {"Todos": None}  # Mapeo nombre -> ID
                
                for control in controles:
                    nombre = control.get('nombre', f"Control ID {control.get('id', 'N/A')}")
                    control_names.append(nombre)
                    control_mapping[nombre] = control.get('id')
                
                # Configurar valores del combo
                self.filter_control['values'] = control_names
                self.filter_control.set("Todos")  # Seleccionar "Todos" por defecto
                
                # Guardar el mapeo para uso posterior en filtros
                self.control_filter_mapping = control_mapping
                
                print(f"DEBUG - Controles cargados en filtro: {len(controles)} controles")
            else:
                print(f"DEBUG - Error obteniendo controles para filtro: {response.get('error', 'Error desconocido')}")
                self.filter_control['values'] = ["Todos"]
                self.filter_control.set("Todos")
                self.control_filter_mapping = {"Todos": None}
                
        except Exception as e:
            print(f"DEBUG - Excepción en load_filter_controls: {e}")
            import traceback
            traceback.print_exc()
            self.filter_control['values'] = ["Todos"]
            self.filter_control.set("Todos")
            self.control_filter_mapping = {"Todos": None}
        
    def refresh_controls(self):
        """Actualiza la lista de controles"""
        print("DEBUG MainWindow - refresh_controls iniciado")
        
        # Limpiar lista actual
        for item in self.controls_tree.get_children():
            self.controls_tree.delete(item)
        
        print("DEBUG MainWindow - Lista limpiada, obteniendo controles...")
        
        try:
            # Obtener controles desde el controlador
            response = self.control_ctrl.obtener_todas()
            print(f"DEBUG MainWindow - Respuesta del controlador: {response}")
            
            if response.get('success', False):
                controles = response.get('data', [])
                print(f"DEBUG MainWindow - {len(controles)} controles encontrados")
                
                for control in controles:
                    descripcion = control.get('descripcion', '')
                    if len(descripcion) > 50:
                        descripcion = descripcion[:50] + "..."
                    
                    print(f"DEBUG MainWindow - Insertando control: {control.get('id')} - {control.get('nombre')}")
                    
                    self.controls_tree.insert("", "end", values=(
                        control.get('id', ''),
                        control.get('nombre', ''),
                        descripcion,
                        control.get('tipo_motor', ''),
                        "Activo" if control.get('activo', False) else "Inactivo",
                        control.get('fecha_creacion', '')
                    ))
                print("DEBUG MainWindow - refresh_controls completado exitosamente")
            else:
                print(f"DEBUG MainWindow - Error en respuesta del controlador: {response}")
                
        except Exception as e:
            print(f"DEBUG MainWindow - Excepción en refresh_controls: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al cargar controles: {str(e)}")
    
    def refresh_connections(self):
        """Actualiza la lista de conexiones"""
        # Limpiar lista actual
        for item in self.connections_tree.get_children():
            self.connections_tree.delete(item)
            
        try:
            # Obtener conexiones desde el controlador
            response = self.conexion_ctrl.obtener_todas()
            if response.get('success', False):
                conexiones = response.get('data', [])
                for conexion in conexiones:
                    self.connections_tree.insert("", "end", values=(
                        conexion.get('id', ''),
                        conexion.get('nombre', ''),
                        conexion.get('motor', ''),
                        conexion.get('servidor', ''),
                        conexion.get('puerto', ''),
                        conexion.get('base_datos', ''),
                        conexion.get('usuario', ''),
                        "Activa" if conexion.get('activa', False) else "Inactiva"
                    ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar conexiones: {str(e)}")
    
    def refresh_execution_controls(self):
        """Actualiza la lista de controles para ejecución"""
        # Limpiar lista actual
        for item in self.execution_tree.get_children():
            self.execution_tree.delete(item)
        
        try:
            # Obtener solo controles activos
            response = self.control_ctrl.obtener_todas()
            if response.get('success', False):
                controles = response.get('data', [])
                for control in controles:
                    if control.get('activo', False):
                        self.execution_tree.insert("", "end", values=(
                            control.get('id', ''),
                            control.get('nombre', ''),
                            control.get('tipo_motor', '')
                        ))
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar controles para ejecución: {str(e)}")
    
    def refresh_history(self):
        """Actualiza el historial de ejecuciones"""
        # Limpiar lista actual
        for item in self.history_tree.get_children():
            self.history_tree.delete(item)
        
        try:
            # Obtener historial real desde el controlador
            response = self.ejecucion_ctrl.obtener_historial(
                limite=100,  # Últimas 100 ejecuciones
                incluir_detalles=False
            )
            
            if response.get('success', False):
                historial_data = response.get('data', [])
                
                for ejecucion in historial_data:
                    # Formatear fecha para mostrar
                    fecha_str = ""
                    try:
                        from datetime import datetime
                        fecha = datetime.fromisoformat(ejecucion['fecha_ejecucion'].replace('Z', '+00:00'))
                        fecha_str = fecha.strftime("%Y-%m-%d %H:%M:%S")
                    except:
                        fecha_str = ejecucion.get('fecha_ejecucion', '')[:19]
                    
                    # Formatear estado para mostrar
                    estado = ejecucion.get('estado', '').upper()
                    
                    valores = (
                        ejecucion.get('id', ''),
                        ejecucion.get('control_nombre', 'N/A'),
                        fecha_str,
                        estado,
                        f"{ejecucion.get('tiempo_total_ejecucion_ms', 0):.1f}",
                        ejecucion.get('total_filas_disparadas', 0),
                        ejecucion.get('mensaje', '')[:50] + "..." if len(ejecucion.get('mensaje', '')) > 50 else ejecucion.get('mensaje', '')
                    )
                    
                    self.history_tree.insert("", "end", values=valores)
                    
                print(f"DEBUG - Historial cargado: {len(historial_data)} ejecuciones")
            else:
                error_msg = response.get('error', 'Error al obtener historial')
                print(f"DEBUG - Error obteniendo historial: {error_msg}")
                # Si hay error, mostrar mensaje en el historial
                self.history_tree.insert("", "end", values=("", "Error", "", "ERROR", "", "", error_msg))
                
        except Exception as e:
            print(f"DEBUG - Excepción en refresh_history: {e}")
            import traceback
            traceback.print_exc()
            # Si hay excepción, mostrar mensaje en el historial
            self.history_tree.insert("", "end", values=("", "Error", "", "ERROR", "", "", f"Error: {str(e)}"))
    
    def filter_history(self, event=None):
        """Filtra el historial según los criterios seleccionados"""
        try:
            # Obtener valores de los filtros
            selected_control = self.filter_control.get()
            selected_estado = self.filter_estado.get()
            
            print(f"DEBUG - Filtrando historial: Control={selected_control}, Estado={selected_estado}")
            
            # Obtener el ID del control seleccionado
            control_id = None
            if hasattr(self, 'control_filter_mapping') and selected_control in self.control_filter_mapping:
                control_id = self.control_filter_mapping[selected_control]
            
            # Preparar estado para el filtro
            estado = None
            if selected_estado and selected_estado != "Todos":
                estado = selected_estado
            
            # Limpiar la vista
            for item in self.history_tree.get_children():
                self.history_tree.delete(item)
            
            # Obtener historial con filtros
            response = self.ejecucion_ctrl.obtener_historial(
                control_id=control_id,
                estado=estado,
                limite=100  # Aumentar límite para ver más resultados
            )
            
            if response.get('success', False):
                historial_data = response.get('data', [])
                
                for ejecucion in historial_data:
                    self.history_tree.insert("", "end", values=(
                        ejecucion.get('id', ''),
                        ejecucion.get('control_nombre', ''),
                        ejecucion.get('fecha_ejecucion', ''),
                        ejecucion.get('estado', ''),
                        ejecucion.get('tiempo_ejecucion_ms', ''),
                        ejecucion.get('filas_disparo', ''),
                        ejecucion.get('mensaje', '')
                    ))
                
                print(f"DEBUG - Historial filtrado: {len(historial_data)} ejecuciones")
            else:
                print(f"DEBUG - Error filtrando historial: {response.get('error', '')}")
                
        except Exception as e:
            print(f"DEBUG - Error en filter_history: {e}")
            import traceback
            traceback.print_exc()
    
    def clear_filters(self):
        """Limpia todos los filtros y recarga el historial completo"""
        try:
            self.filter_control.set("Todos")
            self.filter_estado.set("Todos")
            self.refresh_history()
            print("DEBUG - Filtros limpiados")
        except Exception as e:
            print(f"DEBUG - Error limpiando filtros: {e}")
    
    # ===== MÉTODOS DE EVENTOS =====
    
    def new_control(self):
        """Abre ventana para crear nuevo control"""
        dialog = CreateControlDialog(self.root, self.control_ctrl, self.conexion_ctrl)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_controls()
            self.refresh_execution_controls()
            messagebox.showinfo("Éxito", f"Control '{dialog.result['nombre']}' creado exitosamente")
    
    def edit_control(self):
        """Edita el control seleccionado"""
        selection = self.controls_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un control para editar")
            return
        
        # Obtener datos del control seleccionado
        item = self.controls_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos del control")
            return
        
        control_id = values[0]
        
        # Obtener los datos completos del control desde el backend
        try:
            # Usar el servicio para cargar el control completo
            control_completo = self.control_service.cargar_control_completo(control_id)
            
            # Crear diccionario con los datos completos del control
            control_data = {
                'id': control_completo.id,
                'nombre': control_completo.nombre,
                'descripcion': control_completo.descripcion,
                'activo': control_completo.activo,
                'fecha_creacion': control_completo.fecha_creacion.isoformat() if control_completo.fecha_creacion else '',
                'disparar_si_hay_datos': control_completo.disparar_si_hay_datos,
                'conexion_id': control_completo.conexion_id
            }
            
        except Exception as e:
            # Fallback: usar datos básicos del TreeView
            control_data = {
                'id': values[0],
                'nombre': values[1],
                'descripcion': values[2],
                'activo': values[4] == "Activo",
                'fecha_creacion': values[5],
                'disparar_si_hay_datos': True,  # Por defecto como fallback
                'conexion_id': None
            }
        
        # Abrir diálogo de edición
        dialog = EditControlDialog(
            self.root, 
            self.control_ctrl,
            self.conexion_ctrl,  # Pasar también el controlador de conexiones
            control_data
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si se editó exitosamente, actualizar la lista
        print(f"DEBUG MainWindow - dialog.result: {dialog.result}")
        if dialog.result:
            print("DEBUG MainWindow - Refrescando controles después de edición...")
            self.refresh_controls()
            print("DEBUG MainWindow - Controles refrescados")
        else:
            print("DEBUG MainWindow - No hay result del dialog, no se refresca")
    
    def delete_control(self):
        """Elimina el control seleccionado"""
        selection = self.controls_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un control para eliminar")
            return
        
        # Obtener datos del control seleccionado
        item = self.controls_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos del control")
            return
        
        control_id = values[0]
        control_nombre = values[1]
        
        # Confirmar eliminación
        resultado = messagebox.askyesno(
            "Confirmar eliminación", 
            f"¿Estás seguro de que deseas eliminar el control '{control_nombre}'?\n\n"
            f"Esta acción no se puede deshacer.",
            icon='warning'
        )
        
        if not resultado:
            return
        
        try:
            # Ejecutar eliminación
            response = self.control_ctrl.eliminar_control(control_id)
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", response.get('message', 'Control eliminado exitosamente'))
                # Actualizar la lista de controles
                self.refresh_controls()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido al eliminar el control'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def manage_control_consultas(self):
        """Gestiona las consultas asociadas a un control"""
        selection = self.controls_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un control para gestionar sus consultas")
            return
        
        # Obtener datos del control seleccionado
        item = self.controls_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos del control")
            return
        
        control_id = values[0]
        control_nombre = values[1]
        
        # Abrir diálogo de gestión de consultas
        from .control_consultas_dialog import ControlConsultasDialog
        
        dialog = ControlConsultasDialog(
            self.root,
            control_id,
            control_nombre,
            self.consulta_ctrl,
            self.consulta_control_ctrl
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si hubo cambios, actualizar la vista si es necesario
        if dialog.result:
            self.refresh_controls()
    
    def new_connection(self):
        """Abre ventana para crear nueva conexión"""
        dialog = CreateConnectionDialog(self.root, self.conexion_ctrl)
        self.root.wait_window(dialog.dialog)
        
        if dialog.result:
            self.refresh_connections()
            messagebox.showinfo("Éxito", f"Conexión '{dialog.result['nombre']}' creada exitosamente")
    
    def edit_connection(self):
        """Edita la conexión seleccionada"""
        selection = self.connections_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una conexión para editar")
            return
        
        # Obtener datos de la conexión seleccionada
        item = self.connections_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la conexión")
            return
        
        # Crear diccionario con los datos de la conexión
        conexion_data = {
            'id': values[0],
            'nombre': values[1],
            'motor': values[2],
            'servidor': values[3],
            'puerto': values[4],
            'base_datos': values[5],
            'usuario': values[6],
            'activa': values[7] == "Activa",  # Convertir texto a booleano
            # No incluimos la contraseña por seguridad
        }
        
        # Abrir diálogo de edición
        dialog = EditConnectionDialog(
            self.root, 
            self.conexion_ctrl, 
            conexion_data
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si se editó exitosamente, actualizar la lista
        if dialog.result:
            self.refresh_connections()
    
    def test_connection(self):
        """Prueba la conexión seleccionada"""
        selection = self.connections_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una conexión para probar")
            return
        
        # Obtener datos de la conexión seleccionada
        item = self.connections_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la conexión")
            return
        
        # Extraer datos de la conexión
        conexion_id = values[0]
        nombre = values[1]
        motor = values[2]
        servidor = values[3]
        puerto = int(values[4]) if values[4] else 5432
        base_datos = values[5]
        usuario = values[6]
        
        # Obtener la conexión completa para tener la contraseña y driver_type
        try:
            # Obtener todas las conexiones para encontrar la completa
            response = self.conexion_ctrl.obtener_todas()
            if not response.get('success', False):
                messagebox.showerror("Error", "No se pudieron obtener los datos completos de la conexión")
                return
            
            # Buscar la conexión específica
            conexion_completa = None
            for conexion in response.get('data', []):
                if str(conexion.get('id')) == str(conexion_id):
                    conexion_completa = conexion
                    break
            
            if not conexion_completa:
                messagebox.showerror("Error", "No se encontró la conexión seleccionada")
                return
            
            # Solicitar contraseña al usuario
            from tkinter import simpledialog
            password = simpledialog.askstring("Contraseña", 
                                             f"Ingresa la contraseña para la conexión '{nombre}':", 
                                             show='*')
            
            if password is None:  # Usuario canceló
                return
            
            # Mostrar ventana de progreso
            progress_window = tk.Toplevel(self.root)
            progress_window.title("Probando Conexión")
            progress_window.geometry("400x150")
            progress_window.grab_set()
            progress_window.resizable(False, False)
            
            # Centrar la ventana
            progress_window.transient(self.root)
            
            # Contenido de la ventana de progreso
            ttk.Label(progress_window, text=f"Probando conexión a '{nombre}'...", 
                     font=("Arial", 12)).pack(pady=20)
            
            progress_bar = ttk.Progressbar(progress_window, mode='indeterminate')
            progress_bar.pack(pady=10, padx=40, fill='x')
            progress_bar.start()
            
            status_label = ttk.Label(progress_window, text="Conectando...", foreground="blue")
            status_label.pack(pady=5)
            
            # Actualizar la ventana
            progress_window.update()
            
            # Realizar la prueba de conexión
            driver_type = conexion_completa.get('driver_type', 'default')
            response = self.conexion_ctrl.probar_conexion(
                motor=motor,
                servidor=servidor,
                puerto=puerto,
                base_datos=base_datos,
                usuario=usuario,
                password=password,
                driver_type=driver_type
            )
            
            # Cerrar ventana de progreso
            progress_window.destroy()
            
            # Mostrar resultado
            if response.get('success', False):
                data = response.get('data', {})
                mensaje = data.get('mensaje', 'Conexión exitosa')
                tiempo = data.get('tiempo_respuesta', 'N/A')
                version = data.get('version_servidor', 'N/A')
                
                resultado_texto = f"""✅ CONEXIÓN EXITOSA

Conexión: {nombre}
Servidor: {servidor}:{puerto}
Tiempo de respuesta: {tiempo:.2f}s
Versión del servidor: {version}

Mensaje: {mensaje}"""
                
                messagebox.showinfo("Conexión Exitosa", resultado_texto)
            else:
                error = response.get('error', 'Error desconocido')
                messagebox.showerror("Error de Conexión", 
                                   f"❌ No se pudo conectar a '{nombre}'\n\nError: {error}")
        
        except Exception as e:
            # Cerrar ventana de progreso si existe
            try:
                progress_window.destroy()
            except:
                pass
            
            messagebox.showerror("Error", f"Error al probar la conexión: {str(e)}")
    
    # Métodos para gestión de consultas
    def refresh_consultas(self):
        """Actualiza la lista de consultas"""
        try:
            response = self.consulta_ctrl.obtener_todas()
            
            # Limpiar lista actual
            for item in self.consultas_tree.get_children():
                self.consultas_tree.delete(item)
            
            if response.get('success', False):
                for consulta in response.get('data', []):
                    # Obtener nombres de conexión y control
                    conexion_nombre = "Sin conexión"
                    if consulta.get('conexion_id'):
                        try:
                            conn_response = self.conexion_ctrl.obtener_por_id(consulta['conexion_id'])
                            if conn_response.get('success', False):
                                conexion_nombre = conn_response['data'].get('nombre', 'N/A')
                        except:
                            pass
                    
                    control_nombre = "Sin control"
                    if consulta.get('control_id'):
                        try:
                            ctrl_response = self.control_ctrl.obtener_por_id(consulta['control_id'])
                            if ctrl_response.get('success', False):
                                control_nombre = ctrl_response['data'].get('nombre', 'N/A')
                        except:
                            pass
                    
                    self.consultas_tree.insert("", "end", values=(
                        consulta.get('id', ''),
                        consulta.get('nombre', ''),
                        consulta.get('descripcion', ''),
                        conexion_nombre,
                        control_nombre,
                        consulta.get('fecha_creacion', '')
                    ))
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar consultas: {str(e)}")
    
    def new_consulta(self):
        """Crea una nueva consulta"""
        from .consulta_dialogs import CreateConsultaDialog
        
        dialog = CreateConsultaDialog(
            self.root,
            self.consulta_ctrl,
            self.conexion_ctrl,
            self.control_ctrl
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si se creó exitosamente, actualizar la lista
        if dialog.result:
            self.refresh_consultas()
    
    def edit_consulta(self):
        """Edita la consulta seleccionada"""
        selection = self.consultas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para editar")
            return
        
        # Obtener datos de la consulta seleccionada
        item = self.consultas_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la consulta")
            return
        
        consulta_id = values[0]
        
        # Obtener datos completos de la consulta
        response = self.consulta_ctrl.obtener_por_id(consulta_id)
        if not response.get('success', False):
            messagebox.showerror("Error", "No se pudieron obtener los datos de la consulta")
            return
        
        consulta_data = response.get('data', {})
        
        # Abrir diálogo de edición
        from .consulta_dialogs import EditConsultaDialog
        
        dialog = EditConsultaDialog(
            self.root,
            self.consulta_ctrl,
            self.conexion_ctrl,
            consulta_data
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si se editó exitosamente, actualizar la lista
        if dialog.result:
            self.refresh_consultas()
    
    def delete_consulta(self):
        """Elimina la consulta seleccionada"""
        selection = self.consultas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para eliminar")
            return
        
        # Obtener datos de la consulta seleccionada
        item = self.consultas_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la consulta")
            return
        
        consulta_id = values[0]
        consulta_nombre = values[1]
        
        # Confirmar eliminación
        respuesta = messagebox.askyesno(
            "Confirmar Eliminación",
            f"¿Estás seguro de que quieres eliminar la consulta '{consulta_nombre}'?\n\nEsta acción no se puede deshacer."
        )
        
        if not respuesta:
            return
        
        try:
            response = self.consulta_ctrl.eliminar_consulta(consulta_id)
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", "Consulta eliminada exitosamente")
                self.refresh_consultas()
            else:
                error = response.get('error', 'Error desconocido')
                messagebox.showerror("Error", f"Error al eliminar la consulta: {error}")
        
        except Exception as e:
            messagebox.showerror("Error", f"Error al eliminar la consulta: {str(e)}")
    
    def execute_consulta(self):
        """Ejecuta la consulta seleccionada"""
        selection = self.consultas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para ejecutar")
            return
        
        # Obtener datos de la consulta seleccionada
        item = self.consultas_tree.item(selection[0])
        values = item['values']
        
        if not values:
            messagebox.showerror("Error", "No se pudieron obtener los datos de la consulta")
            return
        
        consulta_id = values[0]
        consulta_nombre = values[1]
        
        # Obtener datos completos de la consulta
        response = self.consulta_ctrl.obtener_por_id(consulta_id)
        if not response.get('success', False):
            messagebox.showerror("Error", "No se pudieron obtener los datos de la consulta")
            return
        
        consulta_data = response.get('data', {})
        sql_sentence = consulta_data.get('sql', '')  # Cambiado de 'sql_sentence' a 'sql'
        
        if not sql_sentence.strip():
            messagebox.showerror("Error", "La consulta no tiene una sentencia SQL válida")
            return
        
        # Mostrar ventana de confirmación con la SQL
        from tkinter import scrolledtext
        
        confirm_window = tk.Toplevel(self.root)
        confirm_window.title(f"Ejecutar Consulta: {consulta_nombre}")
        confirm_window.geometry("800x500")
        confirm_window.grab_set()
        confirm_window.resizable(True, True)
        confirm_window.transient(self.root)
        
        # Título
        ttk.Label(confirm_window, text=f"Consulta: {consulta_nombre}", font=("Arial", 12, "bold")).pack(pady=10)
        
        # SQL Text Area
        ttk.Label(confirm_window, text="Sentencia SQL:").pack(anchor="w", padx=10)
        sql_text = scrolledtext.ScrolledText(confirm_window, height=15, wrap=tk.WORD)
        sql_text.pack(fill="both", expand=True, padx=10, pady=5)
        sql_text.insert("1.0", sql_sentence)
        sql_text.configure(state="disabled")
        
        # Botones
        button_frame = ttk.Frame(confirm_window)
        button_frame.pack(fill="x", padx=10, pady=10)
        
        def ejecutar():
            confirm_window.destroy()
            self._ejecutar_consulta_sql(consulta_id, consulta_nombre, sql_sentence, consulta_data)
        
        ttk.Button(button_frame, text="Ejecutar", command=ejecutar).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=confirm_window.destroy).pack(side="right", padx=5)
    
    def _ejecutar_consulta_sql(self, consulta_id, consulta_nombre, sql_sentence, consulta_data):
        """Ejecuta la sentencia SQL de la consulta"""
        try:
            # Obtener la consulta completa
            consulta_response = self.consulta_ctrl.obtener_por_id(consulta_id)
            if not consulta_response.get('success', False):
                messagebox.showerror("Error", "No se pudo obtener la consulta")
                return
            
            consulta_info = consulta_response.get('data', {})
            
            # Determinar la conexión a usar
            conexion_id = consulta_info.get('conexion_id')
            print(f"DEBUG: conexion_id de la consulta: {conexion_id}")
            
            if not conexion_id:
                # Si la consulta no tiene conexión específica, usar la primera disponible
                print("DEBUG: No hay conexion_id, buscando primera disponible...")
                conexiones_response = self.conexion_ctrl.obtener_todas()
                print(f"DEBUG: Respuesta obtener_todas: {conexiones_response}")
                if not conexiones_response.get('success', False) or not conexiones_response.get('data'):
                    messagebox.showerror("Error", "No hay conexiones disponibles")
                    return
                conexion_id = conexiones_response['data'][0]['id']
                print(f"DEBUG: Usando primera conexión disponible: {conexion_id}")
            
            # Obtener la conexión
            print(f"DEBUG: Intentando obtener conexión ID: {conexion_id}")
            conexion_response = self.conexion_ctrl.obtener_por_id(conexion_id)
            print(f"DEBUG: Respuesta obtener_por_id: {conexion_response}")
            if not conexion_response.get('success', False):
                error_msg = conexion_response.get('error', 'Error desconocido')
                messagebox.showerror("Error", f"No se pudo obtener la conexión: {error_msg}")
                return
            
            conexion_data = conexion_response.get('data', {})
            
            # Crear entidades para la simulación
            from src.domain.entities.consulta import Consulta
            from src.domain.entities.conexion import Conexion
            
            consulta_entity = Consulta(
                id=consulta_id,
                nombre=consulta_nombre,
                sql=sql_sentence,
                descripcion=consulta_info.get('descripcion', ''),
                conexion_id=conexion_id,
                activa=True
            )
            
            # Debug: mostrar datos de conexión
            print(f"DEBUG: Datos de conexión recibidos: {conexion_data}")
            
            conexion_entity = Conexion(
                id=conexion_data.get('id'),
                nombre=conexion_data.get('nombre', ''),
                tipo_motor=conexion_data.get('motor', 'postgresql'),  # Usar 'motor'
                servidor=conexion_data.get('servidor', ''),          # Usar 'servidor'
                puerto=conexion_data.get('puerto', 0),
                base_datos=conexion_data.get('base_datos', ''),
                usuario=conexion_data.get('usuario', ''),
                contraseña=conexion_data.get('contraseña', ''),     # Agregar contraseña
                activa=True
            )
            
            print(f"DEBUG: Entidad conexión creada: motor={conexion_entity.tipo_motor}, servidor={conexion_entity.servidor}")
            
            # Ejecutar la consulta usando el servicio (en modo simulación)
            # Acceder al servicio de ejecución directamente desde el use case
            ejecucion_service = self.ejecucion_ctrl.ejecutar_use_case.ejecucion_service
            resultado_consulta = ejecucion_service._ejecutar_consulta(
                consulta_entity, 
                {},  # Sin parámetros por ahora
                conexion_entity,
                mock_execution=False,  # Cambiar a False para ejecución real
                es_disparo=False
            )
            
            # Mostrar resultados
            self._mostrar_resultado_consulta(consulta_nombre, resultado_consulta)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al ejecutar la consulta: {str(e)}")
            import traceback
            print(f"Error detallado: {traceback.format_exc()}")
    
    def _mostrar_resultado_consulta(self, consulta_nombre, resultado):
        """Muestra los resultados de la ejecución de una consulta"""
        # Crear ventana de resultados
        result_window = tk.Toplevel(self.root)
        result_window.title(f"Resultados: {consulta_nombre}")
        result_window.geometry("800x600")
        result_window.grab_set()
        result_window.resizable(True, True)
        
        # Frame principal
        main_frame = ttk.Frame(result_window)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Título
        ttk.Label(main_frame, text=f"Resultados de: {consulta_nombre}", 
                  font=("Arial", 12, "bold")).pack(pady=(0, 10))
        
        # Información de ejecución
        info_frame = ttk.LabelFrame(main_frame, text="Información de Ejecución")
        info_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Tiempo de ejecución: {resultado.tiempo_ejecucion_ms:.1f} ms").pack(anchor="w", padx=10, pady=2)
        ttk.Label(info_frame, text=f"Filas afectadas: {resultado.filas_afectadas}").pack(anchor="w", padx=10, pady=2)
        
        if resultado.error:
            ttk.Label(info_frame, text=f"Error: {resultado.error}", foreground="red").pack(anchor="w", padx=10, pady=2)
        
        # SQL ejecutado
        sql_frame = ttk.LabelFrame(main_frame, text="SQL Ejecutado")
        sql_frame.pack(fill="x", pady=(0, 10))
        
        from tkinter import scrolledtext
        sql_text = scrolledtext.ScrolledText(sql_frame, height=4, wrap=tk.WORD)
        sql_text.pack(fill="x", padx=10, pady=10)
        sql_text.insert("1.0", resultado.sql_ejecutado)
        sql_text.config(state="disabled")
        
        # Datos resultantes
        if resultado.datos and not resultado.error:
            data_frame = ttk.LabelFrame(main_frame, text="Datos Resultantes")
            data_frame.pack(fill="both", expand=True, pady=(0, 10))
            
            # Crear frame para el treeview y scrollbars
            tree_frame = ttk.Frame(data_frame)
            tree_frame.pack(fill="both", expand=True, padx=10, pady=10)
            
            # Crear Treeview para mostrar datos
            columns = list(resultado.datos[0].keys()) if resultado.datos else []
            tree = ttk.Treeview(tree_frame, columns=columns, show="headings", height=15)
            
            # Configurar columnas con mejor ancho
            for col in columns:
                tree.heading(col, text=col)
                # Calcular ancho basado en el contenido
                max_width = max(
                    len(col) * 8,  # Ancho del header
                    max(len(str(row.get(col, ''))) for row in resultado.datos[:10]) * 8  # Ancho del contenido (sample)
                )
                tree.column(col, width=min(max_width, 200), minwidth=50)  # Máximo 200px, mínimo 50px
            
            # Insertar datos
            for row_data in resultado.datos[:100]:  # Mostrar hasta 100 filas
                values = []
                for col in columns:
                    value = row_data.get(col, '')
                    # Truncar valores muy largos para mejor visualización
                    if isinstance(value, str) and len(value) > 50:
                        value = value[:47] + "..."
                    values.append(str(value))
                tree.insert("", "end", values=values)
            
            # Scrollbars
            v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=tree.yview)
            h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=tree.xview)
            tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
            
            # Pack con grid para mejor control
            tree.grid(row=0, column=0, sticky="nsew")
            v_scrollbar.grid(row=0, column=1, sticky="ns")
            h_scrollbar.grid(row=1, column=0, sticky="ew")
            
            # Configurar grid weights
            tree_frame.grid_rowconfigure(0, weight=1)
            tree_frame.grid_columnconfigure(0, weight=1)
            
            # Información adicional
            info_text = f"Mostrando {min(len(resultado.datos), 100)} filas de {len(resultado.datos)} totales"
            if len(columns) > 10:
                info_text += f" - {len(columns)} columnas (use scroll horizontal para ver todas)"
            
            ttk.Label(data_frame, text=info_text, font=("Arial", 9)).pack(pady=(0, 5))
        
        # Botón cerrar
        ttk.Button(main_frame, text="Cerrar", command=result_window.destroy).pack(pady=10)
    
    def execute_selected_control(self):
        """Ejecuta el control seleccionado"""
        selection = self.execution_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un control para ejecutar")
            return
        
        item = self.execution_tree.item(selection[0])
        control_id = item['values'][0]
        control_nombre = item['values'][1]
        
        # Abrir diálogo de parámetros
        # TODO: Cargar parámetros reales del control
        # Crear diálogo simple solo con opciones básicas
        dialog = ExecutionParametersDialog(self.root, [])  # Sin parámetros adicionales
        self.root.wait_window(dialog.dialog)
        
        if not dialog.result:
            return  # Usuario canceló
        
        config = dialog.result
        # Usar el control_id real en lugar del del config
        config['control_id'] = control_id
        
        self.results_text.insert("end", f"\n=== Ejecutando Control: {control_nombre} ===\n")
        
        try:
            response = self.ejecucion_ctrl.ejecutar_control(
                control_id=int(config['control_id']),
                ejecutar_solo_disparo=config['ejecutar_solo_disparo']
            )
            
            if response.get('success', False):
                data = response['data']
                self.results_text.insert("end", f"✅ Estado: {data['estado']}\n")
                self.results_text.insert("end", f"⏱️ Tiempo: {data['tiempo_total_ejecucion_ms']:.1f} ms\n")
                self.results_text.insert("end", f"📊 Filas disparo: {data['total_filas_disparo']}\n")
                if not config['ejecutar_solo_disparo']:
                    self.results_text.insert("end", f"📋 Filas disparadas: {data['total_filas_disparadas']}\n")
                self.results_text.insert("end", f"💬 Mensaje: {data['mensaje']}\n")
            else:
                self.results_text.insert("end", f"❌ Error: {response.get('error', 'Error desconocido')}\n")
        
        except Exception as e:
            self.results_text.insert("end", f"❌ Excepción: {str(e)}\n")
        
        self.results_text.see("end")
        self.refresh_history()  # Actualizar historial
    
    def execute_trigger_only(self):
        """Ejecuta solo el disparo del control seleccionado"""
        selection = self.execution_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona un control para ejecutar")
            return
        
        item = self.execution_tree.item(selection[0])
        control_id = item['values'][0]
        control_nombre = item['values'][1]
        
        self.results_text.insert("end", f"\n=== Ejecutando Solo Disparo: {control_nombre} ===\n")
        
        try:
            response = self.ejecucion_ctrl.ejecutar_control(
                control_id=int(control_id),
                ejecutar_solo_disparo=True
            )
            
            if response.get('success', False):
                data = response['data']
                self.results_text.insert("end", f"✅ Estado: {data['estado']}\n")
                self.results_text.insert("end", f"⏱️ Tiempo: {data['tiempo_total_ejecucion_ms']:.1f} ms\n")
                self.results_text.insert("end", f"📊 Filas encontradas: {data['total_filas_disparo']}\n")
                self.results_text.insert("end", f"📋 Mensaje: {data['mensaje']}\n")
            else:
                self.results_text.insert("end", f"❌ Error: {response.get('error', 'Error desconocido')}\n")
        
        except Exception as e:
            self.results_text.insert("end", f"❌ Excepción: {str(e)}\n")
        
        self.results_text.see("end")
        self.refresh_history()
    
    def execute_control(self):
        """Placeholder para ejecutar control desde menú"""
        messagebox.showinfo("Función", "Ir a pestaña Ejecución para ejecutar controles")
    
    def view_history(self):
        """Placeholder para ver historial desde menú"""
        messagebox.showinfo("Función", "Ir a pestaña Historial para ver ejecuciones")
    
    def clear_filters_old(self):
        """Limpia los filtros del historial"""
        self.filter_control.set("")
        self.filter_estado.set("Todos")
        self.refresh_history()
    
    def manage_referentes(self):
        """Abre el diálogo de gestión de referentes"""
        try:
            dialog = ReferentesListDialog(self.root, self.referente_ctrl, self.control_referente_ctrl)
            self.root.wait_window(dialog.dialog)
        except Exception as e:
            messagebox.showerror("Error", f"Error al abrir gestión de referentes: {str(e)}")
    
    def manage_control_referentes(self):
        """Abre el diálogo de gestión de referentes para el control seleccionado"""
        try:
            selection = self.controls_tree.selection()
            if not selection:
                messagebox.showwarning("Advertencia", "Seleccione un control para gestionar sus referentes")
                return
            
            # Obtener datos del control seleccionado
            item = self.controls_tree.item(selection[0])
            control_id = item['values'][0]
            control_nombre = item['values'][1]
            control_descripcion = item['values'][2]
            
            # Crear diccionario con datos del control
            control_data = {
                'id': control_id,
                'nombre': control_nombre,
                'descripcion': control_descripcion
            }
            
            # Abrir diálogo de gestión de referentes del control
            dialog = ControlReferentesDialog(
                self.root, 
                control_data, 
                self.control_referente_ctrl, 
                self.referente_ctrl
            )
            self.root.wait_window(dialog.dialog)
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al gestionar referentes del control: {str(e)}")

    def show_about(self):
        """Muestra información sobre la aplicación"""
        messagebox.showinfo(
            "Acerca de",
            "Sistema de Gestión de Controles SQL\n\n"
            "Versión: 1.0\n"
            "Arquitectura: Clean Architecture\n"
            "Base de datos: SQLite\n"
            "Interface: Tkinter\n\n"
            "Desarrollado para entornos bancarios"
        )
    
    def _inicializar_servicios_conexion(self):
        """Inicializa y registra los servicios de prueba de conexión"""
        # Registrar servicio PostgreSQL
        postgresql_service = PostgreSQLConexionTest()
        ConexionTestFactory.registrar_servicio(
            postgresql_service.tipos_soportados(), 
            postgresql_service
        )
        
        # Registrar servicio MySQL
        mysql_service = MySQLConexionTest()
        ConexionTestFactory.registrar_servicio(
            mysql_service.tipos_soportados(), 
            mysql_service
        )
        
        # Registrar servicio SQL Server
        sqlserver_service = SQLServerConexionTest()
        ConexionTestFactory.registrar_servicio(
            sqlserver_service.tipos_soportados(), 
            sqlserver_service
        )
        
        # Registrar servicio SQLite
        sqlite_service = SQLiteConexionTest()
        ConexionTestFactory.registrar_servicio(
            sqlite_service.tipos_soportados(), 
            sqlite_service
        )
        
        # Registrar servicio IBM i Series (Selector inteligente)
        ibmiseries_selector = IBMiSeriesConexionSelector()
        ConexionTestFactory.registrar_servicio(
            ibmiseries_selector.tipos_soportados(), 
            ibmiseries_selector
        )
        
        # Registrar servicios específicos para acceso directo si es necesario
        ibmiseries_jdbc_service = IBMiSeriesJDBCConexionTest()
        ConexionTestFactory.registrar_servicio(
            ibmiseries_jdbc_service.tipos_soportados(), 
            ibmiseries_jdbc_service
        )
        
        print(f"✅ Servicios de conexión registrados: {ConexionTestFactory.tipos_soportados()}")
    
    def run(self):
        """Inicia la aplicación"""
        self.root.mainloop()


def main():
    """Función principal"""
    app = MainWindow()
    app.run()


if __name__ == "__main__":
    main()