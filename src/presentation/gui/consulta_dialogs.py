"""
Diálogos adicionales para consultas - Parte 2
Este archivo contiene diálogos complementarios que son importados por dialogs.py
"""
import tkinter as tk
from tkinter import ttk, messagebox


class EditConsultaDialog:
    """Diálogo para editar consulta existente"""
    
    def __init__(self, parent, consulta_controller, conexion_controller, consulta_data):
        self.result = None
        self.consulta_ctrl = consulta_controller
        self.conexion_ctrl = conexion_controller
        self.consulta_data = consulta_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Consulta")
        self.dialog.geometry("600x500")
        self.dialog.grab_set()
        
        self.create_widgets()
        self._cargar_conexiones()
        self.load_data()
        
    def create_widgets(self):
        """Crea widgets del formulario"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información básica
        ttk.Label(main_frame, text="Información de la Consulta", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=40).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Descripción:").grid(row=2, column=0, sticky="nw", pady=5)
        self.descripcion_text = tk.Text(main_frame, width=35, height=2)
        self.descripcion_text.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Conexión específica (opcional)
        ttk.Label(main_frame, text="Conexión específica:").grid(row=3, column=0, sticky="w", pady=5)
        self.conexion_var = tk.StringVar()
        self.conexion_combo = ttk.Combobox(main_frame, textvariable=self.conexion_var, width=37, state="readonly")
        self.conexion_combo.grid(row=3, column=1, pady=5, padx=(10, 0))
        
        # SQL Editor
        ttk.Label(main_frame, text="Consulta SQL:", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=(20, 5))
        
        # Frame para el SQL con scrollbars
        sql_frame = ttk.Frame(main_frame)
        sql_frame.grid(row=5, column=0, columnspan=2, sticky="ew", pady=5)
        sql_frame.grid_columnconfigure(0, weight=1)
        
        self.sql_text = tk.Text(sql_frame, width=60, height=8, font=("Consolas", 10))
        sql_scrollbar = ttk.Scrollbar(sql_frame, orient="vertical", command=self.sql_text.yview)
        self.sql_text.configure(yscrollcommand=sql_scrollbar.set)
        
        self.sql_text.grid(row=0, column=0, sticky="ew")
        sql_scrollbar.grid(row=0, column=1, sticky="ns")
        
        # Estado
        ttk.Label(main_frame, text="Estado:").grid(row=6, column=0, sticky="w", pady=5)
        self.activa_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Consulta activa", variable=self.activa_var).grid(row=6, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Información adicional
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=8, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.id_label = ttk.Label(info_frame, text="N/A", foreground="gray")
        self.id_label.grid(row=0, column=1, sticky="w")
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=9, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_consulta).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def _cargar_conexiones(self):
        """Carga la lista de conexiones disponibles"""
        try:
            if self.conexion_ctrl:
                response = self.conexion_ctrl.obtener_todas()
                if response.get('success', False):
                    conexiones_bd = response.get('data', [])
                    self.conexiones_disponibles = [{"id": None, "nombre": "(Usar conexión del control)"}]
                    
                    for conn in conexiones_bd:
                        self.conexiones_disponibles.append({
                            "id": conn.get('id'),
                            "nombre": f"{conn.get('nombre')} (ID: {conn.get('id')})"
                        })
                else:
                    self.conexiones_disponibles = [{"id": None, "nombre": "(Sin conexiones disponibles)"}]
            else:
                self.conexiones_disponibles = [{"id": None, "nombre": "(Sin controlador de conexiones)"}]
            
            valores_combo = [f"{conn['nombre']}" for conn in self.conexiones_disponibles]
            self.conexion_combo['values'] = valores_combo
            
        except Exception as e:
            print(f"Error cargando conexiones: {e}")
            self.conexiones_disponibles = [{"id": None, "nombre": "Error al cargar conexiones"}]
            self.conexion_combo['values'] = ["Error al cargar conexiones"]
            
    def load_data(self):
        """Carga datos de la consulta en el formulario"""
        if self.consulta_data:
            self.nombre_var.set(self.consulta_data.get('nombre', ''))
            
            # Descripción
            descripcion = self.consulta_data.get('descripcion', '')
            self.descripcion_text.delete('1.0', tk.END)
            self.descripcion_text.insert('1.0', descripcion)
            
            # SQL
            sql = self.consulta_data.get('sql', '')
            self.sql_text.delete('1.0', tk.END)
            self.sql_text.insert('1.0', sql)
            
            # Estado activo
            self.activa_var.set(self.consulta_data.get('activa', True))
            
            # Conexión
            conexion_id_actual = self.consulta_data.get('conexion_id')
            for i, conn in enumerate(self.conexiones_disponibles):
                if conn['id'] == conexion_id_actual:
                    self.conexion_combo.current(i)
                    break
            else:
                self.conexion_combo.current(0)  # Seleccionar primera opción si no encuentra
            
            # ID
            consulta_id = self.consulta_data.get('id', 'N/A')
            self.id_label.config(text=str(consulta_id))
            
    def update_consulta(self):
        """Actualiza la consulta con los datos del formulario"""
        try:
            # Validaciones básicas
            nombre = self.nombre_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre de la consulta es requerido")
                return
            
            sql = self.sql_text.get('1.0', tk.END).strip()
            if not sql:
                messagebox.showerror("Error", "La consulta SQL es requerida")
                return
            
            # Obtener ID de la consulta
            consulta_id = self.consulta_data.get('id')
            if not consulta_id:
                messagebox.showerror("Error", "No se pudo obtener el ID de la consulta")
                return
            
            # Obtener datos del formulario
            descripcion = self.descripcion_text.get('1.0', tk.END).strip()
            activa = self.activa_var.get()
            
            # Obtener conexión seleccionada
            conexion_seleccionada_idx = self.conexion_combo.current()
            conexion_id = None
            if conexion_seleccionada_idx >= 0 and conexion_seleccionada_idx < len(self.conexiones_disponibles):
                conexion_id = self.conexiones_disponibles[conexion_seleccionada_idx]['id']
            
            # Verificar que el controlador esté disponible
            if not self.consulta_ctrl:
                messagebox.showerror("Error", "Controlador de consultas no está disponible")
                return
            
            # Llamar al controlador para actualizar
            response = self.consulta_ctrl.actualizar_consulta(
                consulta_id=int(consulta_id),
                nombre=nombre,
                sql=sql,
                descripcion=descripcion,
                conexion_id=conexion_id,
                activa=activa
            )
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Consulta '{nombre}' actualizada exitosamente")
                
                self.result = {
                    'success': True,
                    'data': response.get('data', {}),
                    'nombre': nombre,
                    'sql': sql,
                    'descripcion': descripcion,
                    'conexion_id': conexion_id,
                    'activa': activa
                }
                
                self.dialog.destroy()
            else:
                error = response.get('error', 'Error desconocido')
                messagebox.showerror("Error", f"No se pudo actualizar la consulta: {error}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar la consulta: {str(e)}")
            
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class CreateConsultaDialog:
    """Diálogo para crear nueva consulta"""
    
    def __init__(self, parent, consulta_controller, conexion_controller, control_controller):
        self.result = None
        self.consulta_ctrl = consulta_controller
        self.conexion_ctrl = conexion_controller
        self.control_ctrl = control_controller
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Consulta")
        self.dialog.geometry("600x500")
        self.dialog.grab_set()
        
        self.create_widgets()
        self._cargar_conexiones()
        
    def create_widgets(self):
        """Crea widgets del formulario"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Campo Nombre (requerido)
        ttk.Label(main_frame, text="Nombre *:").pack(anchor="w", pady=(0, 5))
        self.nombre_entry = ttk.Entry(main_frame, width=50)
        self.nombre_entry.pack(fill="x", pady=(0, 10))
        
        # Campo Descripción (opcional)
        ttk.Label(main_frame, text="Descripción:").pack(anchor="w", pady=(0, 5))
        self.descripcion_entry = ttk.Entry(main_frame, width=50)
        self.descripcion_entry.pack(fill="x", pady=(0, 10))
        
        # Campo Conexión (opcional)
        ttk.Label(main_frame, text="Conexión (opcional):").pack(anchor="w", pady=(0, 5))
        self.conexion_combo = ttk.Combobox(main_frame, state="readonly")
        self.conexion_combo.pack(fill="x", pady=(0, 10))
        
        # Campo SQL (requerido)
        ttk.Label(main_frame, text="Sentencia SQL *:").pack(anchor="w", pady=(0, 5))
        
        # Frame para el texto SQL con scrollbar
        sql_frame = ttk.Frame(main_frame)
        sql_frame.pack(fill="both", expand=True, pady=(0, 10))
        
        self.sql_text = tk.Text(sql_frame, height=12, wrap=tk.WORD)
        sql_scrollbar = ttk.Scrollbar(sql_frame, orient="vertical", command=self.sql_text.yview)
        self.sql_text.configure(yscrollcommand=sql_scrollbar.set)
        
        self.sql_text.pack(side="left", fill="both", expand=True)
        sql_scrollbar.pack(side="right", fill="y")
        
        # Checkbox Activa
        self.activa_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(main_frame, text="Consulta activa", variable=self.activa_var).pack(anchor="w", pady=(0, 10))
        
        # Botones
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Crear", command=self.save).pack(side="right", padx=5)
        ttk.Button(button_frame, text="Cancelar", command=self.cancel).pack(side="right", padx=5)
        
        # Nota
        ttk.Label(main_frame, text="* Campos requeridos", font=("Arial", 8), foreground="gray").pack(anchor="w")
    
    def _cargar_conexiones(self):
        """Carga las conexiones disponibles en el combobox"""
        try:
            response = self.conexion_ctrl.obtener_todas()
            if response.get('success', False):
                conexiones = response.get('data', [])
                nombres = ["Sin conexión"] + [conn.get('nombre', '') for conn in conexiones]
                self.conexion_combo['values'] = nombres
                self.conexion_combo.set("Sin conexión")
        except Exception as e:
            print(f"Error al cargar conexiones: {e}")
            self.conexion_combo['values'] = ["Sin conexión"]
            self.conexion_combo.set("Sin conexión")
    
    def save(self):
        """Guarda la nueva consulta"""
        try:
            # Obtener valores del formulario
            nombre = self.nombre_entry.get().strip()
            descripcion = self.descripcion_entry.get().strip()
            sql = self.sql_text.get("1.0", tk.END).strip()
            activa = self.activa_var.get()
            
            # Validaciones
            if not nombre:
                messagebox.showerror("Error", "El nombre es requerido")
                return
            
            if not sql:
                messagebox.showerror("Error", "La sentencia SQL es requerida")
                return
            
            # Determinar conexión ID
            conexion_id = None
            conexion_seleccionada = self.conexion_combo.get()
            if conexion_seleccionada and conexion_seleccionada != "Sin conexión":
                # Buscar el ID de la conexión
                response = self.conexion_ctrl.obtener_todas()
                if response.get('success', False):
                    for conn in response.get('data', []):
                        if conn.get('nombre') == conexion_seleccionada:
                            conexion_id = conn.get('id')
                            break
            
            # Crear consulta
            response = self.consulta_ctrl.crear_consulta(
                nombre=nombre,
                sql=sql,
                descripcion=descripcion,
                conexion_id=conexion_id,
                activa=activa
            )
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Consulta '{nombre}' creada exitosamente")
                
                self.result = {
                    'success': True,
                    'data': response.get('data', {}),
                    'nombre': nombre,
                    'sql': sql,
                    'descripcion': descripcion,
                    'conexion_id': conexion_id,
                    'activa': activa
                }
                
                self.dialog.destroy()
            else:
                error = response.get('error', 'Error desconocido')
                messagebox.showerror("Error", f"No se pudo crear la consulta: {error}")
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear la consulta: {str(e)}")
            
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()