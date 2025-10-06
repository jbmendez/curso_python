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
    
    def __init__(self, parent, control_controller, control_data):
        self.result = None
        self.control_ctrl = control_controller
        self.control_data = control_data
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Control")
        self.dialog.geometry("400x200")
        self.dialog.grab_set()
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea widgets básicos"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5)
        
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=1, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def load_data(self):
        """Carga datos del control"""
        self.nombre_var.set(self.control_data.get('nombre', ''))
        
    def update_control(self):
        """Actualiza el control (simplificado)"""
        messagebox.showinfo("Info", "Funcionalidad de edición de control simplificada")
        self.dialog.destroy()
        
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