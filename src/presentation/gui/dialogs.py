"""
Ventanas de diálogo simples para crear y editar entidades
"""
import tkinter as tk
from tkinter import ttk, messagebox


class CreateConnectionDialog:
    """Diálogo para crear nueva conexión"""
    
    def __init__(self, parent, conexion_controller):
        self.result = None
        self.conexion_ctrl = conexion_controller
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Conexión")
        self.dialog.geometry("400x350")
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets básicos del diálogo"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos básicos
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5)
        
        ttk.Label(frame, text="Motor:").grid(row=1, column=0, sticky="w", pady=5)
        self.motor_var = tk.StringVar()
        motor_combo = ttk.Combobox(frame, textvariable=self.motor_var, width=27)
        motor_combo['values'] = ('postgresql', 'mysql', 'sqlite', 'sqlserver', 'iseries')
        motor_combo.set('postgresql')
        motor_combo.grid(row=1, column=1, pady=5)
        motor_combo.bind('<<ComboboxSelected>>', self.on_motor_change)
        
        # Campo Driver Type
        ttk.Label(frame, text="Tipo Driver:").grid(row=2, column=0, sticky="w", pady=5)
        self.driver_type_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(frame, textvariable=self.driver_type_var, width=27)
        self.driver_combo['values'] = ('auto', 'jdbc', 'odbc')
        self.driver_combo.set('auto')
        self.driver_combo.grid(row=2, column=1, pady=5)
        self.driver_combo.grid_remove()
        
        ttk.Label(frame, text="Servidor:").grid(row=3, column=0, sticky="w", pady=5)
        self.servidor_var = tk.StringVar(value="localhost")
        ttk.Entry(frame, textvariable=self.servidor_var, width=30).grid(row=3, column=1, pady=5)
        
        ttk.Label(frame, text="Puerto:").grid(row=4, column=0, sticky="w", pady=5)
        self.puerto_var = tk.StringVar(value="5432")
        ttk.Entry(frame, textvariable=self.puerto_var, width=30).grid(row=4, column=1, pady=5)
        
        ttk.Label(frame, text="Base de Datos:").grid(row=5, column=0, sticky="w", pady=5)
        self.bd_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.bd_var, width=30).grid(row=5, column=1, pady=5)
        
        ttk.Label(frame, text="Usuario:").grid(row=6, column=0, sticky="w", pady=5)
        self.usuario_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.usuario_var, width=30).grid(row=6, column=1, pady=5)
        
        ttk.Label(frame, text="Contraseña:").grid(row=7, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=30, show="*").grid(row=7, column=1, pady=5)
        
        # Botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Crear", command=self.create_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def on_motor_change(self, event=None):
        """Maneja el cambio de motor"""
        motor = self.motor_var.get()
        if motor == 'iseries':
            self.driver_combo.grid()
        else:
            self.driver_combo.grid_remove()
            self.driver_type_var.set('default')
        
    def create_connection(self):
        """Crea la conexión"""
        try:
            driver_type = self.driver_type_var.get() if self.motor_var.get() == 'iseries' else 'default'
            
            response = self.conexion_ctrl.crear_conexion(
                nombre=self.nombre_var.get(),
                motor=self.motor_var.get(),
                servidor=self.servidor_var.get(),
                puerto=int(self.puerto_var.get()),
                base_datos=self.bd_var.get(),
                usuario=self.usuario_var.get(),
                password=self.password_var.get(),
                driver_type=driver_type
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", "Conexión creada exitosamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
        except Exception as e:
            messagebox.showerror("Error", f"Error: {str(e)}")
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class EditConnectionDialog:
    """Diálogo para editar conexión existente"""
    
    def __init__(self, parent, conexion_controller, conexion_data):
        self.result = None
        self.conexion_ctrl = conexion_controller
        self.conexion_data = conexion_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Conexión: {conexion_data.get('nombre', '')}")
        self.dialog.geometry("400x450")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"400x450+{x}+{y}")
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea todos los widgets necesarios para editar conexión"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario completos
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Motor:").grid(row=1, column=0, sticky="w", pady=5)
        self.motor_var = tk.StringVar()
        motor_combo = ttk.Combobox(frame, textvariable=self.motor_var, width=27)
        motor_combo['values'] = ('postgresql', 'mysql', 'sqlite', 'sqlserver', 'iseries')
        motor_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        motor_combo.bind('<<ComboboxSelected>>', self.on_motor_change)
        
        # Campo Driver Type (solo visible para IBM i Series)
        ttk.Label(frame, text="Tipo Driver:").grid(row=2, column=0, sticky="w", pady=5)
        self.driver_type_var = tk.StringVar()
        self.driver_combo = ttk.Combobox(frame, textvariable=self.driver_type_var, width=27)
        self.driver_combo['values'] = ('auto', 'jdbc', 'odbc')
        self.driver_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Servidor:").grid(row=3, column=0, sticky="w", pady=5)
        self.servidor_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.servidor_var, width=30).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Puerto:").grid(row=4, column=0, sticky="w", pady=5)
        self.puerto_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.puerto_var, width=30).grid(row=4, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Base de Datos:").grid(row=5, column=0, sticky="w", pady=5)
        self.bd_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.bd_var, width=30).grid(row=5, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Usuario:").grid(row=6, column=0, sticky="w", pady=5)
        self.usuario_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.usuario_var, width=30).grid(row=6, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(frame, text="Nueva Contraseña:").grid(row=7, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.password_var, width=30, show="*").grid(row=7, column=1, pady=5, padx=(10, 0))
        
        # Checkbox activa
        self.activa_var = tk.BooleanVar()
        ttk.Checkbutton(frame, text="Conexión activa", variable=self.activa_var).grid(row=8, column=0, columnspan=2, pady=10)
        
        # Botón probar conexión
        test_frame = ttk.Frame(frame)
        test_frame.grid(row=9, column=0, columnspan=2, pady=10)
        ttk.Button(test_frame, text="Probar Conexión", command=self.test_connection).pack()
        
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=10, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        frame.columnconfigure(1, weight=1)
        
    def load_data(self):
        """Carga todos los datos de la conexión en el formulario"""
        self.nombre_var.set(self.conexion_data.get('nombre', ''))
        motor = self.conexion_data.get('motor', 'postgresql')
        self.motor_var.set(motor)
        self.servidor_var.set(self.conexion_data.get('servidor', ''))
        self.puerto_var.set(str(self.conexion_data.get('puerto', '')))
        self.bd_var.set(self.conexion_data.get('base_datos', ''))
        self.usuario_var.set(self.conexion_data.get('usuario', ''))
        self.activa_var.set(self.conexion_data.get('activa', True))
        
        # Cargar driver_type si existe
        driver_type = self.conexion_data.get('driver_type', 'auto')
        self.driver_type_var.set(driver_type)
        
        # Mostrar/ocultar campo driver_type según el motor
        self.on_motor_change()
        
        # No cargamos la contraseña por seguridad, el usuario debe reintroducirla
    
    def on_motor_change(self, event=None):
        """Maneja el cambio de motor para mostrar/ocultar el campo driver_type"""
        motor = self.motor_var.get()
        if motor == 'iseries':
            # Mostrar campo driver_type para IBM i Series
            self.driver_combo.grid()
        else:
            # Ocultar campo driver_type para otros motores
            self.driver_combo.grid_remove()
            self.driver_type_var.set('default')
        
    def update_connection(self):
        """Actualiza la conexión con validaciones"""
        # Validar campos obligatorios
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
            
        if not self.bd_var.get().strip():
            messagebox.showerror("Error", "La base de datos es obligatoria")
            return
            
        if not self.usuario_var.get().strip():
            messagebox.showerror("Error", "El usuario es obligatorio")
            return
        
        try:
            puerto = int(self.puerto_var.get())
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
            return
        
        try:
            # Determinar driver_type
            driver_type = self.driver_type_var.get() if self.motor_var.get() == 'iseries' else 'default'
            
            response = self.conexion_ctrl.actualizar_conexion(
                conexion_id=self.conexion_data['id'],
                nombre=self.nombre_var.get().strip(),
                motor=self.motor_var.get(),
                servidor=self.servidor_var.get().strip(),
                puerto=puerto,
                base_datos=self.bd_var.get().strip(),
                usuario=self.usuario_var.get().strip(),
                password=self.password_var.get() if self.password_var.get().strip() else None,
                activa=self.activa_var.get(),
                driver_type=driver_type
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", "Conexión actualizada exitosamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar conexión: {str(e)}")
    
    def test_connection(self):
        """Prueba la conexión sin guardarla"""
        # Validar campos obligatorios
        if not self.bd_var.get().strip():
            messagebox.showerror("Error", "La base de datos es obligatoria para probar la conexión")
            return
            
        if not self.usuario_var.get().strip():
            messagebox.showerror("Error", "El usuario es obligatorio para probar la conexión")
            return
        
        if not self.password_var.get().strip():
            messagebox.showerror("Error", "La contraseña es obligatoria para probar la conexión")
            return
        
        try:
            puerto = int(self.puerto_var.get())
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
            return
        
        try:
            # Llamar al controlador para probar la conexión
            response = self.conexion_ctrl.probar_conexion(
                motor=self.motor_var.get(),
                servidor=self.servidor_var.get().strip(),
                puerto=puerto,
                base_datos=self.bd_var.get().strip(),
                usuario=self.usuario_var.get().strip(),
                password=self.password_var.get()
            )
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", "Conexión establecida exitosamente")
            else:
                messagebox.showerror("Error", response.get('error', 'Error al conectar'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al probar conexión: {str(e)}")
        
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class CreateControlDialog:
    """Diálogo para crear nuevo control"""
    
    def __init__(self, parent, control_controller):
        self.result = None
        self.control_ctrl = control_controller
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Control")
        self.dialog.geometry("400x200")
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea widgets básicos"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5)
        
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Crear", command=self.create_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def create_control(self):
        """Crea el control (simplificado)"""
        messagebox.showinfo("Info", "Funcionalidad de control simplificada")
        self.dialog.destroy()
        
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class EditControlDialog:
    """Diálogo para editar control existente"""
    
    def __init__(self, parent, control_controller, conexion_controller, control_data):
        self.result = None
        self.control_ctrl = control_controller
        self.conexion_ctrl = conexion_controller  # Agregar controlador de conexiones
        self.control_data = control_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Control")
        self.dialog.geometry("500x400")
        self.dialog.grab_set()
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea widgets completos del formulario"""
        # Frame principal con scroll
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Información básica
        ttk.Label(main_frame, text="Información del Control", font=("Arial", 10, "bold")).grid(row=0, column=0, columnspan=2, sticky="w", pady=(0, 10))
        
        ttk.Label(main_frame, text="Nombre:").grid(row=1, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=40).grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Descripción:").grid(row=2, column=0, sticky="nw", pady=5)
        self.descripcion_var = tk.StringVar()
        descripcion_entry = tk.Text(main_frame, width=35, height=3)
        descripcion_entry.grid(row=2, column=1, pady=5, padx=(10, 0))
        self.descripcion_text = descripcion_entry
        
        # Estado del control
        ttk.Label(main_frame, text="Estado:").grid(row=3, column=0, sticky="w", pady=5)
        self.activo_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Control activo", variable=self.activo_var).grid(row=3, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Configuración de disparo
        ttk.Label(main_frame, text="Configuración de Disparo", font=("Arial", 10, "bold")).grid(row=4, column=0, columnspan=2, sticky="w", pady=(20, 10))
        
        ttk.Label(main_frame, text="Disparar cuando:").grid(row=5, column=0, sticky="w", pady=5)
        self.disparo_var = tk.StringVar()
        disparo_frame = ttk.Frame(main_frame)
        disparo_frame.grid(row=5, column=1, sticky="w", pady=5, padx=(10, 0))
        
        ttk.Radiobutton(disparo_frame, text="HAY datos", variable=self.disparo_var, value="true").pack(side="left", padx=(0, 10))
        ttk.Radiobutton(disparo_frame, text="NO hay datos", variable=self.disparo_var, value="false").pack(side="left")
        
        # Conexión asociada
        ttk.Label(main_frame, text="Conexión:").grid(row=6, column=0, sticky="w", pady=5)
        self.conexion_var = tk.StringVar()
        self.conexion_combo = ttk.Combobox(main_frame, textvariable=self.conexion_var, width=37, state="readonly")
        self.conexion_combo.grid(row=6, column=1, pady=5, padx=(10, 0))
        
        # Información adicional
        info_frame = ttk.Frame(main_frame)
        info_frame.grid(row=7, column=0, columnspan=2, pady=(20, 0), sticky="ew")
        
        ttk.Label(info_frame, text="ID:").grid(row=0, column=0, sticky="w", padx=(0, 10))
        self.id_label = ttk.Label(info_frame, text="N/A", foreground="gray")
        self.id_label.grid(row=0, column=1, sticky="w")
        
        ttk.Label(info_frame, text="Fecha creación:").grid(row=0, column=2, sticky="w", padx=(20, 10))
        self.fecha_label = ttk.Label(info_frame, text="N/A", foreground="gray")
        self.fecha_label.grid(row=0, column=3, sticky="w")
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
        # Cargar lista de conexiones
        self._cargar_conexiones()
        
    def _cargar_conexiones(self):
        """Carga la lista de conexiones disponibles"""
        try:
            # Obtener conexiones reales desde el controlador
            if self.conexion_ctrl:
                response = self.conexion_ctrl.obtener_todas()
                if response.get('success', False):
                    conexiones_bd = response.get('data', [])
                    self.conexiones_disponibles = []
                    
                    for conn in conexiones_bd:
                        self.conexiones_disponibles.append({
                            "id": conn.get('id'),
                            "nombre": f"{conn.get('nombre')} (ID: {conn.get('id')})"
                        })
                else:
                    # Fallback si no se pueden obtener las conexiones
                    self.conexiones_disponibles = [{"id": 1, "nombre": "Conexión no disponible (ID: 1)"}]
            else:
                # Fallback si no hay controlador de conexiones
                self.conexiones_disponibles = [{"id": 1, "nombre": "Sin controlador de conexiones (ID: 1)"}]
            
            # Configurar valores del combobox
            valores_combo = [f"{conn['nombre']}" for conn in self.conexiones_disponibles]
            self.conexion_combo['values'] = valores_combo
            
            # Seleccionar la conexión actual si existe
            conexion_id_actual = self.control_data.get('conexion_id', 1)
            for i, conn in enumerate(self.conexiones_disponibles):
                if conn['id'] == conexion_id_actual:
                    self.conexion_combo.current(i)
                    break
            
            print(f"DEBUG EditControlDialog - Conexiones cargadas: {self.conexiones_disponibles}")
            print(f"DEBUG EditControlDialog - Conexión actual ID: {conexion_id_actual}")
            
        except Exception as e:
            print(f"Error cargando conexiones: {e}")
            import traceback
            traceback.print_exc()
            # Fallback
            self.conexiones_disponibles = [{"id": 1, "nombre": "Error al cargar conexiones (ID: 1)"}]
            self.conexion_combo['values'] = ["Error al cargar conexiones (ID: 1)"]
            self.conexion_combo.current(0)
        
    def load_data(self):
        """Carga datos del control en el formulario"""
        if self.control_data:
            self.nombre_var.set(self.control_data.get('nombre', ''))
            
            # Descripción
            descripcion = self.control_data.get('descripcion', '')
            self.descripcion_text.delete('1.0', tk.END)
            self.descripcion_text.insert('1.0', descripcion)
            
            # Estado activo
            self.activo_var.set(self.control_data.get('activo', True))
            
            # Configuración de disparo
            disparar_si_hay_datos = self.control_data.get('disparar_si_hay_datos', True)
            self.disparo_var.set("true" if disparar_si_hay_datos else "false")
            
            # Conexión
            conexion_nombre = self.control_data.get('conexion_nombre', '')
            if conexion_nombre:
                self.conexion_var.set(conexion_nombre)
            
            # Información adicional
            control_id = self.control_data.get('id', 'N/A')
            self.id_label.config(text=str(control_id))
            
            fecha_creacion = self.control_data.get('fecha_creacion', 'N/A')
            self.fecha_label.config(text=str(fecha_creacion))
        
    def update_control(self):
        """Actualiza el control con los datos del formulario"""
        try:
            # Validaciones básicas
            nombre = self.nombre_var.get().strip()
            if not nombre:
                messagebox.showerror("Error", "El nombre del control es requerido")
                return
            
            # Obtener datos del formulario
            descripcion = self.descripcion_text.get('1.0', tk.END).strip()
            activo = self.activo_var.get()
            disparar_si_hay_datos = self.disparo_var.get() == "true"
            
            # Obtener ID del control
            control_id = self.control_data.get('id')
            if not control_id:
                messagebox.showerror("Error", "No se pudo obtener el ID del control")
                return
            
            # Debug: mostrar datos que se van a enviar
            print(f"DEBUG - Actualizando control:")
            print(f"  ID: {control_id}")
            print(f"  Nombre: {nombre}")
            print(f"  Descripción: {descripcion}")
            print(f"  Activo: {activo}")
            print(f"  Disparar si hay datos: {disparar_si_hay_datos}")
            
            # Obtener el ID real de la conexión seleccionada
            conexion_seleccionada_idx = self.conexion_combo.current()
            if conexion_seleccionada_idx >= 0 and conexion_seleccionada_idx < len(self.conexiones_disponibles):
                conexion_id = self.conexiones_disponibles[conexion_seleccionada_idx]['id']
            else:
                conexion_id = self.control_data.get('conexion_id', 1)  # Fallback
                
            print(f"  Conexión seleccionada índice: {conexion_seleccionada_idx}")
            print(f"  Conexión ID: {conexion_id}")
            
            # Verificar que el controlador esté disponible
            if not self.control_ctrl:
                messagebox.showerror("Error", "Controlador de control no está disponible")
                return
            
            print("DEBUG - Llamando al controlador...")
            
            # Llamar al controlador para actualizar
            response = self.control_ctrl.actualizar_control(
                control_id=int(control_id),
                nombre=nombre,
                descripcion=descripcion,
                conexion_id=int(conexion_id),
                disparar_si_hay_datos=disparar_si_hay_datos,
                activo=activo
            )
            
            print(f"DEBUG - Respuesta del controlador: {response}")
            
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Control '{nombre}' actualizado exitosamente")
                
                self.result = {
                    'success': True,
                    'data': response.get('data', {}),
                    'nombre': nombre,
                    'descripcion': descripcion,
                    'activo': activo,
                    'disparar_si_hay_datos': disparar_si_hay_datos
                }
                
                self.dialog.destroy()
            else:
                error = response.get('error', 'Error desconocido')
                messagebox.showerror("Error", f"No se pudo actualizar el control: {error}")
            
        except Exception as e:
            print(f"DEBUG - Excepción: {str(e)}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al actualizar el control: {str(e)}")
        
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class ExecutionParametersDialog:
    """Diálogo para parámetros de ejecución"""
    
    def __init__(self, parent, parametros):
        self.result = None
        self.parametros = parametros
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Parámetros de Ejecución")
        self.dialog.geometry("400x300")
        self.dialog.grab_set()
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea widgets básicos"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Parámetros:").grid(row=0, column=0, sticky="w", pady=5)
        
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Ejecutar", command=self.execute).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def execute(self):
        """Ejecuta con parámetros (simplificado)"""
        messagebox.showinfo("Info", "Funcionalidad de ejecución simplificada")
        self.dialog.destroy()
        
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()