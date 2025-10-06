"""
Ventanas de diálogo para crear y editar entidades
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Dict, Any, Optional


class CreateConnectionDialog:
    """Diálogo para crear nueva conexión"""
    
    def __init__(self, parent, conexion_controller):
        self.parent = parent
        self.conexion_ctrl = conexion_controller
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nueva Conexión")
        self.dialog.geometry("400x350")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (350 // 2)
        self.dialog.geometry(f"400x350+{x}+{y}")
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Motor:").grid(row=1, column=0, sticky="w", pady=5)
        self.motor_var = tk.StringVar()
        motor_combo = ttk.Combobox(main_frame, textvariable=self.motor_var, width=27)
        motor_combo['values'] = ('postgresql', 'mysql', 'sqlite', 'sqlserver', 'iseries')
        motor_combo.set('postgresql')
        motor_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Servidor:").grid(row=2, column=0, sticky="w", pady=5)
        self.servidor_var = tk.StringVar(value="localhost")
        ttk.Entry(main_frame, textvariable=self.servidor_var, width=30).grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Puerto:").grid(row=3, column=0, sticky="w", pady=5)
        self.puerto_var = tk.StringVar(value="5432")
        ttk.Entry(main_frame, textvariable=self.puerto_var, width=30).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Base de Datos:").grid(row=4, column=0, sticky="w", pady=5)
        self.bd_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.bd_var, width=30).grid(row=4, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Usuario:").grid(row=5, column=0, sticky="w", pady=5)
        self.usuario_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.usuario_var, width=30).grid(row=5, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Contraseña:").grid(row=6, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.password_var, width=30, show="*").grid(row=6, column=1, pady=5, padx=(10, 0))
        
        # Botón probar conexión
        test_frame = ttk.Frame(main_frame)
        test_frame.grid(row=7, column=0, columnspan=2, pady=10)
        ttk.Button(test_frame, text="Probar Conexión", command=self.test_connection).pack()
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=8, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Crear", command=self.create_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def create_connection(self):
        """Crea la conexión"""
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
            response = self.conexion_ctrl.crear_conexion(
                nombre=self.nombre_var.get().strip(),
                motor=self.motor_var.get(),
                servidor=self.servidor_var.get().strip(),
                puerto=puerto,
                base_datos=self.bd_var.get().strip(),
                usuario=self.usuario_var.get().strip(),
                password=self.password_var.get()
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", "Conexión creada exitosamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear conexión: {str(e)}")
    
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
                datos = response.get('data', {})
                mensaje = f"✅ Conexión exitosa\n\n"
                mensaje += f"Tiempo de respuesta: {datos.get('tiempo_respuesta', 0):.2f}s\n"
                if datos.get('version_servidor'):
                    mensaje += f"Versión del servidor: {datos.get('version_servidor')}"
                messagebox.showinfo("Prueba de Conexión", mensaje)
            else:
                error_msg = response.get('error', 'Error desconocido')
                messagebox.showerror("Error de Conexión", f"❌ {error_msg}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al probar conexión: {str(e)}")
    
    def cancel(self):
        """Cancela la creación"""
        self.dialog.destroy()


class EditConnectionDialog:
    """Diálogo para editar conexión existente"""
    
    def __init__(self, parent, conexion_controller, conexion_data):
        self.parent = parent
        self.conexion_ctrl = conexion_controller
        self.conexion_data = conexion_data
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Conexión")
        self.dialog.geometry("600x420")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (420 // 2)
        self.dialog.geometry(f"600x420+{x}+{y}")
        
        self.create_widgets()
        self.load_connection_data()
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=30).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Motor:").grid(row=1, column=0, sticky="w", pady=5)
        self.motor_var = tk.StringVar()
        motor_combo = ttk.Combobox(main_frame, textvariable=self.motor_var, width=42)
        motor_combo['values'] = ('postgresql', 'mysql', 'sqlite', 'sqlserver', 'iseries')
        motor_combo.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Servidor:").grid(row=2, column=0, sticky="w", pady=5)
        self.servidor_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.servidor_var, width=45).grid(row=2, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Puerto:").grid(row=3, column=0, sticky="w", pady=5)
        self.puerto_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.puerto_var, width=45).grid(row=3, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Base de Datos:").grid(row=4, column=0, sticky="w", pady=5)
        self.bd_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.bd_var, width=45).grid(row=4, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Usuario:").grid(row=5, column=0, sticky="w", pady=5)
        self.usuario_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.usuario_var, width=45).grid(row=5, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Contraseña:").grid(row=6, column=0, sticky="w", pady=5)
        self.password_var = tk.StringVar()
        password_entry = ttk.Entry(main_frame, textvariable=self.password_var, width=45, show="*")
        password_entry.grid(row=6, column=1, pady=5, padx=(10, 0))
        
        # Nota explicativa sobre la contraseña
        ttk.Label(main_frame, text="(Dejar vacío para mantener la contraseña actual)", 
                 foreground="gray", font=("Arial", 8)).grid(row=6, column=2, sticky="w", padx=5)
        
        # Campo activo
        ttk.Label(main_frame, text="Estado:").grid(row=7, column=0, sticky="w", pady=5)
        self.activa_var = tk.BooleanVar()
        ttk.Checkbutton(main_frame, text="Conexión activa", variable=self.activa_var).grid(row=7, column=1, sticky="w", pady=5, padx=(10, 0))
        
        # Botón probar conexión
        test_frame = ttk.Frame(main_frame)
        test_frame.grid(row=8, column=0, columnspan=3, pady=10)
        ttk.Button(test_frame, text="Probar Conexión", command=self.test_connection).pack()
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=9, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_connection).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def load_connection_data(self):
        """Carga los datos de la conexión en los campos"""
        self.nombre_var.set(self.conexion_data.get('nombre', ''))
        self.motor_var.set(self.conexion_data.get('motor', 'postgresql'))
        self.servidor_var.set(self.conexion_data.get('servidor', ''))
        self.puerto_var.set(str(self.conexion_data.get('puerto', '')))
        self.bd_var.set(self.conexion_data.get('base_datos', ''))
        self.usuario_var.set(self.conexion_data.get('usuario', ''))
        self.activa_var.set(self.conexion_data.get('activa', True))
        # No cargamos la contraseña por seguridad, el usuario debe reintroducirla
        
    def update_connection(self):
        """Actualiza la conexión"""
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
        
        # La contraseña es opcional - si está vacía, se mantiene la actual
        nueva_password = self.password_var.get().strip()
        if not nueva_password:
            # Usar una cadena especial para indicar que no se debe cambiar la contraseña
            nueva_password = "***KEEP_CURRENT***"
        
        try:
            puerto = int(self.puerto_var.get())
        except ValueError:
            messagebox.showerror("Error", "El puerto debe ser un número")
            return
        
        try:
            response = self.conexion_ctrl.actualizar_conexion(
                conexion_id=self.conexion_data['id'],
                nombre=self.nombre_var.get().strip(),
                motor=self.motor_var.get(),
                servidor=self.servidor_var.get().strip(),
                puerto=puerto,
                base_datos=self.bd_var.get().strip(),
                usuario=self.usuario_var.get().strip(),
                password=nueva_password,
                activa=self.activa_var.get()
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
        
        # Para editar, si no se proporciona contraseña, usar una especial
        password = self.password_var.get().strip()
        if not password:
            messagebox.showwarning("Advertencia", "Para probar la conexión necesitas introducir la contraseña")
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
                password=password
            )
            
            if response.get('success', False):
                datos = response.get('data', {})
                mensaje = f"✅ Conexión exitosa\n\n"
                mensaje += f"Tiempo de respuesta: {datos.get('tiempo_respuesta', 0):.2f}s\n"
                if datos.get('version_servidor'):
                    mensaje += f"Versión del servidor: {datos.get('version_servidor')}"
                messagebox.showinfo("Prueba de Conexión", mensaje)
            else:
                error_msg = response.get('error', 'Error desconocido')
                messagebox.showerror("Error de Conexión", f"❌ {error_msg}")
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al probar conexión: {str(e)}")
    
    def cancel(self):
        """Cancela la edición"""
        self.dialog.destroy()


class CreateControlDialog:
    """Diálogo para crear nuevo control"""
    
    def __init__(self, parent, control_controller, conexion_controller, usuario_controller):
        self.parent = parent
        self.control_ctrl = control_controller
        self.conexion_ctrl = conexion_controller
        self.usuario_ctrl = usuario_controller
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Control")
        self.dialog.geometry("500x400")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (500 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (400 // 2)
        self.dialog.geometry(f"500x400+{x}+{y}")
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=40).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Descripción:").grid(row=1, column=0, sticky="nw", pady=5)
        self.descripcion_text = tk.Text(main_frame, width=35, height=4)
        self.descripcion_text.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Conexión:").grid(row=2, column=0, sticky="w", pady=5)
        self.conexion_var = tk.StringVar()
        self.conexion_combo = ttk.Combobox(main_frame, textvariable=self.conexion_var, width=37)
        self.conexion_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones")
        options_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.disparar_si_hay_datos_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Disparar si hay datos", variable=self.disparar_si_hay_datos_var).pack(anchor="w", padx=10, pady=5)
        
        self.activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Control activo", variable=self.activo_var).pack(anchor="w", padx=10, pady=5)
        
        # Información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información")
        info_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Label(info_frame, text="Nota: Después de crear el control, podrás agregar parámetros,\nconsultas y referentes desde la ventana principal.", 
                 foreground="gray").pack(padx=10, pady=5)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Crear", command=self.create_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def load_data(self):
        """Carga datos necesarios para el formulario"""
        try:
            # Cargar conexiones reales desde el controlador
            response = self.conexion_ctrl.obtener_todas()
            if response.get('success', False):
                conexiones = response.get('data', [])
                conexiones_list = []
                for conexion in conexiones:
                    if conexion.get('activa', True):  # Solo conexiones activas
                        conexiones_list.append(f"{conexion['id']} - {conexion['nombre']} ({conexion['motor']})")
                
                self.conexion_combo['values'] = conexiones_list
                if conexiones_list:
                    self.conexion_combo.set(conexiones_list[0])
                else:
                    self.conexion_combo['values'] = ['No hay conexiones disponibles']
            else:
                self.conexion_combo['values'] = ['Error al cargar conexiones']
                
        except Exception as e:
            print(f"Error al cargar conexiones: {e}")
            self.conexion_combo['values'] = ['Error al cargar conexiones']
    
    def create_control(self):
        """Crea el control"""
        # Validar campos obligatorios
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
            
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()
        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return
        
        conexion_seleccionada = self.conexion_var.get()
        if not conexion_seleccionada:
            messagebox.showerror("Error", "Selecciona una conexión")
            return
        
        # Extraer ID de conexión (formato: "1 - Nombre")
        try:
            conexion_id = int(conexion_seleccionada.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Conexión inválida")
            return
        
        try:
            # Por ahora usamos usuario fijo (ID 1)
            # TODO: Implementar selección de usuario o usar usuario actual
            usuario_id = 1
            
            response = self.control_ctrl.crear_control_simple(
                nombre=self.nombre_var.get().strip(),
                descripcion=descripcion,
                conexion_id=conexion_id,
                usuario_creador_id=usuario_id
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", "Control creado exitosamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al crear control: {str(e)}")
    
    def cancel(self):
        """Cancela la creación"""
        self.dialog.destroy()


class ExecutionParametersDialog:
    """Diálogo para configurar parámetros de ejecución"""
    
    def __init__(self, parent, control_id, control_name, parametros=None):
        self.parent = parent
        self.control_id = control_id
        self.control_name = control_name
        self.parametros = parametros or []
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Parámetros - {control_name}")
        self.dialog.geometry("400x300")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
        self.create_widgets()
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        ttk.Label(main_frame, text=f"Configurar parámetros para: {self.control_name}", 
                 font=("Arial", 10, "bold")).pack(pady=(0, 10))
        
        # Frame para parámetros
        params_frame = ttk.LabelFrame(main_frame, text="Parámetros")
        params_frame.pack(fill="both", expand=True, pady=10)
        
        # Si no hay parámetros, mostrar mensaje
        if not self.parametros:
            ttk.Label(params_frame, text="Este control no tiene parámetros configurados").pack(pady=20)
        else:
            # Crear campos para cada parámetro
            self.param_vars = {}
            for i, param in enumerate(self.parametros):
                ttk.Label(params_frame, text=f"{param['nombre']}:").grid(row=i, column=0, sticky="w", padx=10, pady=5)
                
                var = tk.StringVar(value=str(param.get('valor_por_defecto', '')))
                entry = ttk.Entry(params_frame, textvariable=var, width=20)
                entry.grid(row=i, column=1, padx=10, pady=5)
                
                self.param_vars[param['nombre']] = var
                
                # Mostrar descripción si existe
                if param.get('descripcion'):
                    ttk.Label(params_frame, text=param['descripcion'], 
                             foreground="gray", font=("Arial", 8)).grid(row=i, column=2, sticky="w", padx=5)
        
        # Opciones de ejecución
        options_frame = ttk.LabelFrame(main_frame, text="Opciones de Ejecución")
        options_frame.pack(fill="x", pady=10)
        
        self.solo_disparo_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Ejecutar solo consulta de disparo", 
                       variable=self.solo_disparo_var).pack(anchor="w", padx=10, pady=5)
        
        self.mock_execution_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(options_frame, text="Simulación (recomendado para pruebas)", 
                       variable=self.mock_execution_var).pack(anchor="w", padx=10, pady=5)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=10)
        
        ttk.Button(buttons_frame, text="Ejecutar", command=self.execute).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def execute(self):
        """Prepara los parámetros y ejecuta"""
        parametros = {}
        if hasattr(self, 'param_vars'):
            for nombre, var in self.param_vars.items():
                value = var.get().strip()
                if value:
                    # Intentar convertir a número si es posible
                    try:
                        if '.' in value:
                            parametros[nombre] = float(value)
                        else:
                            parametros[nombre] = int(value)
                    except ValueError:
                        parametros[nombre] = value
        
        self.result = {
            'control_id': self.control_id,
            'parametros': parametros,
            'ejecutar_solo_disparo': self.solo_disparo_var.get(),
            'mock_execution': self.mock_execution_var.get()
        }
        
        self.dialog.destroy()
    
    def cancel(self):
        """Cancela la ejecución"""
        self.dialog.destroy()


class EditControlDialog:
    """Diálogo para editar control existente"""
    
    def __init__(self, parent, control_controller, conexion_controller, control_data):
        self.parent = parent
        self.control_ctrl = control_controller
        self.conexion_ctrl = conexion_controller
        self.control_data = control_data
        self.result = None
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Control")
        self.dialog.geometry("600x450")
        self.dialog.transient(parent)
        self.dialog.grab_set()
        
        # Centrar ventana
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (600 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (450 // 2)
        self.dialog.geometry(f"600x450+{x}+{y}")
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(main_frame, text="Nombre:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(main_frame, textvariable=self.nombre_var, width=45).grid(row=0, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Descripción:").grid(row=1, column=0, sticky="nw", pady=5)
        self.descripcion_text = tk.Text(main_frame, width=40, height=4)
        self.descripcion_text.grid(row=1, column=1, pady=5, padx=(10, 0))
        
        ttk.Label(main_frame, text="Conexión:").grid(row=2, column=0, sticky="w", pady=5)
        self.conexion_var = tk.StringVar()
        self.conexion_combo = ttk.Combobox(main_frame, textvariable=self.conexion_var, width=42)
        self.conexion_combo.grid(row=2, column=1, pady=5, padx=(10, 0))
        
        # Frame para opciones
        options_frame = ttk.LabelFrame(main_frame, text="Opciones")
        options_frame.grid(row=3, column=0, columnspan=2, sticky="ew", pady=10)
        
        self.disparar_si_hay_datos_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Disparar si hay datos", variable=self.disparar_si_hay_datos_var).pack(anchor="w", padx=10, pady=5)
        
        self.activo_var = tk.BooleanVar()
        ttk.Checkbutton(options_frame, text="Control activo", variable=self.activo_var).pack(anchor="w", padx=10, pady=5)
        
        # Información adicional
        info_frame = ttk.LabelFrame(main_frame, text="Información")
        info_frame.grid(row=4, column=0, columnspan=2, sticky="ew", pady=10)
        
        ttk.Label(info_frame, text="Nota: Los parámetros, consultas y referentes se gestionan\nseparadamente desde la ventana principal.", 
                 foreground="gray").pack(padx=10, pady=5)
        
        # Botones
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.grid(row=5, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.update_control).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
        # Configurar grid
        main_frame.columnconfigure(1, weight=1)
        
    def load_data(self):
        """Carga datos necesarios para el formulario"""
        # Cargar datos del control
        self.nombre_var.set(self.control_data.get('nombre', ''))
        self.descripcion_text.delete("1.0", "end")
        self.descripcion_text.insert("1.0", self.control_data.get('descripcion', ''))
        self.disparar_si_hay_datos_var.set(self.control_data.get('disparar_si_hay_datos', True))
        self.activo_var.set(self.control_data.get('activo', True))
        
        # Cargar conexiones disponibles
        try:
            response = self.conexion_ctrl.obtener_todas()
            if response.get('success', False):
                conexiones = response.get('data', [])
                conexiones_list = []
                conexion_actual = None
                
                for conexion in conexiones:
                    if conexion.get('activa', True):
                        display_text = f"{conexion['id']} - {conexion['nombre']} ({conexion['motor']})"
                        conexiones_list.append(display_text)
                        
                        # Si esta es la conexión actual del control, la marcamos
                        if conexion['id'] == self.control_data.get('conexion_id'):
                            conexion_actual = display_text
                
                self.conexion_combo['values'] = conexiones_list
                if conexion_actual:
                    self.conexion_combo.set(conexion_actual)
                elif conexiones_list:
                    self.conexion_combo.set(conexiones_list[0])
            else:
                self.conexion_combo['values'] = ['Error al cargar conexiones']
                
        except Exception as e:
            print(f"Error al cargar conexiones: {e}")
            self.conexion_combo['values'] = ['Error al cargar conexiones']
    
    def update_control(self):
        """Actualiza el control"""
        # Validar campos obligatorios
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "El nombre es obligatorio")
            return
            
        descripcion = self.descripcion_text.get("1.0", "end-1c").strip()
        if not descripcion:
            messagebox.showerror("Error", "La descripción es obligatoria")
            return
        
        conexion_seleccionada = self.conexion_var.get()
        if not conexion_seleccionada:
            messagebox.showerror("Error", "Selecciona una conexión")
            return
        
        # Extraer ID de conexión (formato: "1 - Nombre")
        try:
            conexion_id = int(conexion_seleccionada.split(' - ')[0])
        except (ValueError, IndexError):
            messagebox.showerror("Error", "Conexión inválida")
            return
        
        try:
            response = self.control_ctrl.actualizar_control(
                control_id=self.control_data['id'],
                nombre=self.nombre_var.get().strip(),
                descripcion=descripcion,
                conexion_id=conexion_id,
                disparar_si_hay_datos=self.disparar_si_hay_datos_var.get(),
                activo=self.activo_var.get()
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", "Control actualizado exitosamente")
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar control: {str(e)}")
    
    def cancel(self):
        """Cancela la edición"""
        self.dialog.destroy()