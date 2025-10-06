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
from src.infrastructure.repositories.sqlite_conexion_repository import SQLiteConexionRepository
from src.infrastructure.repositories.sqlite_referente_repository import SQLiteReferenteRepository
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
from src.application.use_cases.crear_conexion_use_case import CrearConexionUseCase
from src.application.use_cases.actualizar_conexion_use_case import ActualizarConexionUseCase
from src.application.use_cases.listar_conexiones_use_case import ListarConexionesUseCase
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

from src.presentation.gui.dialogs import CreateConnectionDialog, EditConnectionDialog, CreateControlDialog, EditControlDialog, ExecutionParametersDialog


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
        referente_repo = SQLiteReferenteRepository(self.db_path)
        resultado_repo = SQLiteResultadoEjecucionRepository(self.db_path)
        
        # Servicios
        usuario_service = UsuarioService(usuario_repo)
        self.control_service = ControlService(
            control_repo, consulta_repo, conexion_repo, parametro_repo, referente_repo
        )
        ejecucion_service = EjecucionControlService(
            control_repo, parametro_repo, consulta_repo, referente_repo, conexion_repo
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
        crear_referente_uc = CrearReferenteUseCase(referente_repo)
        ejecutar_control_uc = EjecutarControlUseCase(control_repo, conexion_repo, resultado_repo, ejecucion_service)
        historial_uc = ObtenerHistorialEjecucionUseCase(resultado_repo, control_repo)
        
        # Controladores
        self.usuario_ctrl = UsuarioController(registrar_usuario_uc)
        self.conexion_ctrl = ConexionController(crear_conexion_uc, listar_conexiones_uc, actualizar_conexion_uc)
        self.control_ctrl = ControlController(crear_control_uc, listar_controles_uc, actualizar_control_uc, eliminar_control_uc)
        self.parametro_ctrl = ParametroController(crear_parametro_uc)
        self.consulta_ctrl = ConsultaController(crear_consulta_uc)
        self.referente_ctrl = ReferenteController(crear_referente_uc)
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
        
        # Pestaña de ejecución
        self.create_execution_tab(notebook)
        
        # Pestaña de historial
        self.create_history_tab(notebook)
        
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
        
        ttk.Label(filters_frame, text="Estado:").grid(row=0, column=2, padx=5, pady=5)
        self.filter_estado = ttk.Combobox(filters_frame, values=["Todos", "EXITOSO", "ERROR", "CONTROL_DISPARADO", "SIN_DATOS"])
        self.filter_estado.set("Todos")
        self.filter_estado.grid(row=0, column=3, padx=5, pady=5)
        
        ttk.Button(filters_frame, text="Filtrar", command=self.filter_history).grid(row=0, column=4, padx=5, pady=5)
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
        
    def refresh_controls(self):
        """Actualiza la lista de controles"""
        # Limpiar lista actual
        for item in self.controls_tree.get_children():
            self.controls_tree.delete(item)
        
        try:
            # Obtener controles desde el controlador
            response = self.control_ctrl.obtener_todas()
            if response.get('success', False):
                controles = response.get('data', [])
                for control in controles:
                    descripcion = control.get('descripcion', '')
                    if len(descripcion) > 50:
                        descripcion = descripcion[:50] + "..."
                    
                    self.controls_tree.insert("", "end", values=(
                        control.get('id', ''),
                        control.get('nombre', ''),
                        descripcion,
                        control.get('tipo_motor', ''),
                        "Activo" if control.get('activo', False) else "Inactivo",
                        control.get('fecha_creacion', '')
                    ))
        except Exception as e:
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
            # TODO: Implementar cuando exista controlador de historial
            # Por ahora, agregar datos de ejemplo
            import datetime
            ejemplo_datos = [
                (1, "Control Ventas", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 "EXITOSO", "250.5", "1500", "Ejecución completada"),
                (2, "Control Inventario", datetime.datetime.now().strftime("%Y-%m-%d %H:%M"), 
                 "ERROR", "120.0", "0", "Error de conexión"),
            ]
            
            for dato in ejemplo_datos:
                self.history_tree.insert("", "end", values=dato)
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar historial: {str(e)}")
    
    # ===== MÉTODOS DE EVENTOS =====
    
    def new_control(self):
        """Abre ventana para crear nuevo control"""
        dialog = CreateControlDialog(self.root, self.control_ctrl, self.conexion_ctrl, self.usuario_ctrl)
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
            self.conexion_ctrl,
            control_data
        )
        
        # Esperar a que se cierre el diálogo
        self.root.wait_window(dialog.dialog)
        
        # Si se editó exitosamente, actualizar la lista
        if dialog.result:
            self.refresh_controls()
    
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
        messagebox.showinfo("Función", "Probar conexión - Por implementar")
    
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
        parametros_ejemplo = [
            {'nombre': 'umbral_ventas', 'valor_por_defecto': 10000, 'descripcion': 'Umbral máximo de ventas'}
        ]
        
        dialog = ExecutionParametersDialog(self.root, control_id, control_nombre, parametros_ejemplo)
        self.root.wait_window(dialog.dialog)
        
        if not dialog.result:
            return  # Usuario canceló
        
        config = dialog.result
        self.results_text.insert("end", f"\n=== Ejecutando Control: {control_nombre} ===\n")
        
        try:
            response = self.ejecucion_ctrl.ejecutar_control(
                control_id=int(config['control_id']),
                parametros_adicionales=config['parametros'],
                ejecutar_solo_disparo=config['ejecutar_solo_disparo'],
                mock_execution=config['mock_execution']
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
                ejecutar_solo_disparo=True,
                mock_execution=True
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
    
    def filter_history(self):
        """Filtra el historial según los criterios seleccionados"""
        messagebox.showinfo("Función", "Filtrar historial - Por implementar")
    
    def clear_filters(self):
        """Limpia los filtros del historial"""
        self.filter_control.set("")
        self.filter_estado.set("Todos")
        self.refresh_history()
    
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