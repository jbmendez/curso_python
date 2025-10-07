"""
Diálogos para gestión de referentes

Contiene los formularios para crear, editar y gestionar
referentes y sus asociaciones con controles
"""
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from typing import Optional, List, Dict, Any
import os


class CreateReferenteDialog:
    """Diálogo para crear nuevo referente"""
    
    def __init__(self, parent, referente_controller):
        self.result = None
        self.referente_ctrl = referente_controller
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Nuevo Referente")
        self.dialog.geometry("450x250")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"450x250+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(frame, text="Nombre del Referente:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=40).grid(row=0, column=1, pady=5, sticky="w")
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=40).grid(row=1, column=1, pady=5, sticky="w")
        
        ttk.Label(frame, text="Ruta de Archivos:").grid(row=2, column=0, sticky="w", pady=5)
        path_frame = ttk.Frame(frame)
        path_frame.grid(row=2, column=1, pady=5, sticky="ew")
        
        self.path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.path_var, width=30).pack(side="left", fill="x", expand=True)
        ttk.Button(path_frame, text="Explorar", command=self.browse_path, width=10).pack(side="right", padx=(5, 0))
        
        ttk.Label(frame, text="Activo:").grid(row=3, column=0, sticky="w", pady=5)
        self.activo_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, variable=self.activo_var).grid(row=3, column=1, pady=5, sticky="w")
        
        # Configurar expansión de columnas
        frame.columnconfigure(1, weight=1)
        
        # Botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Crear", command=self.create_referente).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def browse_path(self):
        """Abre el diálogo para seleccionar carpeta"""
        folder = filedialog.askdirectory(title="Seleccionar carpeta para archivos de reportes")
        if folder:
            self.path_var.set(folder)
        
    def create_referente(self):
        """Crea el referente"""
        try:
            # Validaciones básicas
            nombre = self.nombre_var.get().strip()
            email = self.email_var.get().strip()
            path_archivos = self.path_var.get().strip()
            activo = self.activo_var.get()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
                
            if not email:
                messagebox.showerror("Error", "El email es obligatorio")
                return
            
            # Validar email básico
            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "El formato del email no es válido")
                return
            
            # Validar ruta si se proporciona
            if path_archivos and not os.path.exists(path_archivos):
                response = messagebox.askyesno(
                    "Ruta no existe", 
                    f"La ruta '{path_archivos}' no existe. ¿Desea crearla?"
                )
                if response:
                    try:
                        os.makedirs(path_archivos, exist_ok=True)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo crear la carpeta: {str(e)}")
                        return
                else:
                    return
            
            # Llamar al controlador
            response = self.referente_ctrl.crear_referente(
                nombre=nombre,
                email=email,
                path_archivos=path_archivos,
                activo=activo
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", response.get('message', 'Referente creado exitosamente'))
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class EditReferenteDialog:
    """Diálogo para editar referente existente"""
    
    def __init__(self, parent, referente_controller, referente_data):
        self.result = None
        self.referente_ctrl = referente_controller
        self.referente_data = referente_data
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Editar Referente: {referente_data.get('nombre', '')}")
        self.dialog.geometry("450x250")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
        self.load_data()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (450 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (250 // 2)
        self.dialog.geometry(f"450x250+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos del formulario
        ttk.Label(frame, text="Nombre del Referente:").grid(row=0, column=0, sticky="w", pady=5)
        self.nombre_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.nombre_var, width=40).grid(row=0, column=1, pady=5, sticky="w")
        
        ttk.Label(frame, text="Email:").grid(row=1, column=0, sticky="w", pady=5)
        self.email_var = tk.StringVar()
        ttk.Entry(frame, textvariable=self.email_var, width=40).grid(row=1, column=1, pady=5, sticky="w")
        
        ttk.Label(frame, text="Ruta de Archivos:").grid(row=2, column=0, sticky="w", pady=5)
        path_frame = ttk.Frame(frame)
        path_frame.grid(row=2, column=1, pady=5, sticky="ew")
        
        self.path_var = tk.StringVar()
        ttk.Entry(path_frame, textvariable=self.path_var, width=30).pack(side="left", fill="x", expand=True)
        ttk.Button(path_frame, text="Explorar", command=self.browse_path, width=10).pack(side="right", padx=(5, 0))
        
        ttk.Label(frame, text="Activo:").grid(row=3, column=0, sticky="w", pady=5)
        self.activo_var = tk.BooleanVar()
        ttk.Checkbutton(frame, variable=self.activo_var).grid(row=3, column=1, pady=5, sticky="w")
        
        # Configurar expansión de columnas
        frame.columnconfigure(1, weight=1)
        
        # Botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        ttk.Button(buttons_frame, text="Guardar", command=self.save_referente).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def browse_path(self):
        """Abre el diálogo para seleccionar carpeta"""
        folder = filedialog.askdirectory(
            title="Seleccionar carpeta para archivos de reportes",
            initialdir=self.path_var.get() or "/"
        )
        if folder:
            self.path_var.set(folder)
    
    def load_data(self):
        """Carga los datos del referente en el formulario"""
        self.nombre_var.set(self.referente_data.get('nombre', ''))
        self.email_var.set(self.referente_data.get('email', ''))
        self.path_var.set(self.referente_data.get('path_archivos', ''))
        self.activo_var.set(self.referente_data.get('activo', True))
        
    def save_referente(self):
        """Guarda los cambios del referente"""
        try:
            # Validaciones básicas
            nombre = self.nombre_var.get().strip()
            email = self.email_var.get().strip()
            path_archivos = self.path_var.get().strip()
            activo = self.activo_var.get()
            
            if not nombre:
                messagebox.showerror("Error", "El nombre es obligatorio")
                return
                
            if not email:
                messagebox.showerror("Error", "El email es obligatorio")
                return
            
            # Validar email básico
            if "@" not in email or "." not in email:
                messagebox.showerror("Error", "El formato del email no es válido")
                return
            
            # Validar ruta si se proporciona
            if path_archivos and not os.path.exists(path_archivos):
                response = messagebox.askyesno(
                    "Ruta no existe", 
                    f"La ruta '{path_archivos}' no existe. ¿Desea crearla?"
                )
                if response:
                    try:
                        os.makedirs(path_archivos, exist_ok=True)
                    except Exception as e:
                        messagebox.showerror("Error", f"No se pudo crear la carpeta: {str(e)}")
                        return
                else:
                    return
            
            # Llamar al controlador para actualizar
            referente_id = self.referente_data.get('id')
            response = self.referente_ctrl.actualizar_referente(
                referente_id=referente_id,
                nombre=nombre,
                email=email,
                path_archivos=path_archivos,
                activo=activo
            )
            
            if response.get('success', False):
                self.result = response['data']
                messagebox.showinfo("Éxito", response.get('message', 'Referente actualizado exitosamente'))
                self.dialog.destroy()
            else:
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()


class ReferentesListDialog:
    """Diálogo para listar y gestionar referentes"""
    
    def __init__(self, parent, referente_controller, control_referente_controller=None):
        self.referente_ctrl = referente_controller
        self.control_referente_ctrl = control_referente_controller
        self.selected_referentes = []
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Gestión de Referentes")
        self.dialog.geometry("800x500")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
        self.load_referentes()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (800 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (500 // 2)
        self.dialog.geometry(f"800x500+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Barra de herramientas
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill="x", pady=(0, 10))
        
        ttk.Button(toolbar, text="Nuevo Referente", command=self.new_referente).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="Editar", command=self.edit_referente).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Eliminar", command=self.delete_referente).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Actualizar", command=self.load_referentes).pack(side="left", padx=5)
        
        # Separador
        ttk.Separator(toolbar, orient="vertical").pack(side="left", fill="y", padx=10)
        
        # Filtros
        ttk.Label(toolbar, text="Filtros:").pack(side="left", padx=(0, 5))
        self.filter_activos = tk.BooleanVar(value=False)
        ttk.Checkbutton(toolbar, text="Solo activos", variable=self.filter_activos, 
                       command=self.load_referentes).pack(side="left", padx=5)
        
        # Lista de referentes
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill="both", expand=True)
        
        # Configurar treeview
        columns = ("ID", "Nombre", "Email", "Ruta Archivos", "Activo")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Nombre", text="Nombre")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Ruta Archivos", text="Ruta Archivos")
        self.tree.heading("Activo", text="Activo")
        
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Nombre", width=150, minwidth=100)
        self.tree.column("Email", width=200, minwidth=150)
        self.tree.column("Ruta Archivos", width=300, minwidth=200)
        self.tree.column("Activo", width=80, minwidth=60)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar componentes
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Eventos del tree
        self.tree.bind("<Double-1>", lambda e: self.edit_referente())
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Seleccionar", command=self.select_referentes).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Cerrar", command=self.close_dialog).pack(side="right", padx=5)
        
    def load_referentes(self):
        """Carga la lista de referentes"""
        try:
            # Limpiar lista actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            # Obtener referentes
            response = self.referente_ctrl.obtener_todos(solo_activos=self.filter_activos.get())
            
            if response.get('success', False):
                referentes = response.get('data', [])
                
                for referente in referentes:
                    valores = (
                        referente.get('id', ''),
                        referente.get('nombre', ''),
                        referente.get('email', ''),
                        referente.get('path_archivos', ''),
                        "Sí" if referente.get('activo', False) else "No"
                    )
                    
                    self.tree.insert("", "end", values=valores)
                    
            else:
                messagebox.showerror("Error", response.get('error', 'Error al cargar referentes'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def new_referente(self):
        """Abre diálogo para crear nuevo referente"""
        dialog = CreateReferenteDialog(self.dialog, self.referente_ctrl)
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.result:
            self.load_referentes()
    
    def edit_referente(self):
        """Abre diálogo para editar referente seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un referente para editar")
            return
        
        item = self.tree.item(selection[0])
        referente_id = item['values'][0]
        
        # Obtener datos completos del referente
        response = self.referente_ctrl.obtener_por_id(referente_id)
        if response.get('success', False):
            referente_data = response['data']
            dialog = EditReferenteDialog(self.dialog, self.referente_ctrl, referente_data)
            self.dialog.wait_window(dialog.dialog)
            
            if dialog.result:
                self.load_referentes()
        else:
            messagebox.showerror("Error", response.get('error', 'Error al obtener referente'))
    
    def delete_referente(self):
        """Elimina el referente seleccionado"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione un referente para eliminar")
            return
        
        item = self.tree.item(selection[0])
        referente_id = item['values'][0]
        referente_nombre = item['values'][1]
        
        # Confirmar eliminación
        response = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar el referente '{referente_nombre}'?\n\n"
            "Esta acción también eliminará todas las asociaciones con controles."
        )
        
        if response:
            try:
                result = self.referente_ctrl.eliminar_referente(referente_id)
                
                if result.get('success', False):
                    messagebox.showinfo("Éxito", result.get('message', 'Referente eliminado exitosamente'))
                    self.load_referentes()
                else:
                    messagebox.showerror("Error", result.get('error', 'Error al eliminar referente'))
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def select_referentes(self):
        """Selecciona los referentes marcados"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione al menos un referente")
            return
        
        self.selected_referentes = []
        for item_id in selection:
            item = self.tree.item(item_id)
            referente_data = {
                'id': item['values'][0],
                'nombre': item['values'][1],
                'email': item['values'][2],
                'path_archivos': item['values'][3],
                'activo': item['values'][4] == "Sí"
            }
            self.selected_referentes.append(referente_data)
        
        self.dialog.destroy()
    
    def close_dialog(self):
        """Cierra el diálogo sin seleccionar"""
        self.dialog.destroy()


class ControlReferentesDialog:
    """Diálogo para gestionar asociaciones de referentes de un control"""
    
    def __init__(self, parent, control_data, control_referente_controller, referente_controller):
        self.control_data = control_data
        self.control_referente_ctrl = control_referente_controller
        self.referente_ctrl = referente_controller
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Referentes del Control: {control_data.get('nombre', '')}")
        self.dialog.geometry("900x600")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
        self.load_asociaciones()
        
        # Configurar eventos para mantener el foco
        self.dialog.protocol("WM_DELETE_WINDOW", self.close_dialog)
        self.dialog.focus_force()
        
    def ensure_focus(self):
        """Asegura que esta ventana mantenga el foco"""
        self.dialog.lift()
        self.dialog.focus_force()
        self.dialog.grab_set()
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (900 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (600 // 2)
        self.dialog.geometry(f"900x600+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        main_frame = ttk.Frame(self.dialog)
        main_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Información del control
        info_frame = ttk.LabelFrame(main_frame, text="Control", padding=10)
        info_frame.pack(fill="x", pady=(0, 10))
        
        ttk.Label(info_frame, text=f"Nombre: {self.control_data.get('nombre', '')}", font=("TkDefaultFont", 10, "bold")).pack(anchor="w")
        ttk.Label(info_frame, text=f"Descripción: {self.control_data.get('descripcion', '')}").pack(anchor="w")
        
        # Barra de herramientas
        toolbar = ttk.Frame(main_frame)
        toolbar.pack(fill="x", pady=(0, 10))
        
        ttk.Button(toolbar, text="Agregar Referente", command=self.add_referente).pack(side="left", padx=(0, 5))
        ttk.Button(toolbar, text="Editar Asociación", command=self.edit_asociacion).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Eliminar Asociación", command=self.delete_asociacion).pack(side="left", padx=5)
        ttk.Button(toolbar, text="Actualizar", command=self.load_asociaciones).pack(side="left", padx=5)
        
        # Lista de referentes asociados
        list_frame = ttk.LabelFrame(main_frame, text="Referentes Asociados", padding=5)
        list_frame.pack(fill="both", expand=True)
        
        # Configurar treeview
        columns = ("ID", "Referente", "Email", "Ruta", "Activa", "Fecha", "Email Notif", "Archivo Notif", "Observaciones")
        self.tree = ttk.Treeview(list_frame, columns=columns, show="headings", height=15)
        
        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Referente", text="Referente")
        self.tree.heading("Email", text="Email")
        self.tree.heading("Ruta", text="Ruta Archivos")
        self.tree.heading("Activa", text="Activa")
        self.tree.heading("Fecha", text="Fecha Asociación")
        self.tree.heading("Email Notif", text="Notif Email")
        self.tree.heading("Archivo Notif", text="Notif Archivo")
        self.tree.heading("Observaciones", text="Observaciones")
        
        self.tree.column("ID", width=50, minwidth=50)
        self.tree.column("Referente", width=120, minwidth=100)
        self.tree.column("Email", width=150, minwidth=120)
        self.tree.column("Ruta", width=200, minwidth=150)
        self.tree.column("Activa", width=60, minwidth=50)
        self.tree.column("Fecha", width=100, minwidth=80)
        self.tree.column("Email Notif", width=80, minwidth=60)
        self.tree.column("Archivo Notif", width=80, minwidth=60)
        self.tree.column("Observaciones", width=150, minwidth=100)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=self.tree.yview)
        h_scrollbar = ttk.Scrollbar(list_frame, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Empaquetar componentes
        tree_frame = ttk.Frame(list_frame)
        tree_frame.pack(fill="both", expand=True)
        
        self.tree.pack(side="left", fill="both", expand=True)
        v_scrollbar.pack(side="right", fill="y")
        
        h_scrollbar.pack(side="bottom", fill="x")
        
        # Eventos del tree
        self.tree.bind("<Double-1>", lambda e: self.edit_asociacion())
        
        # Botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(button_frame, text="Cerrar", command=self.close_dialog).pack(side="right", padx=5)
        
    def load_asociaciones(self):
        """Carga las asociaciones del control"""
        try:
            print(f"DEBUG ControlReferentesDialog - load_asociaciones iniciado")
            
            # Limpiar lista actual
            for item in self.tree.get_children():
                self.tree.delete(item)
            
            print(f"DEBUG ControlReferentesDialog - Tree limpiado")
            
            # Obtener asociaciones
            control_id = self.control_data.get('id')
            print(f"DEBUG ControlReferentesDialog - Obteniendo asociaciones para control_id: {control_id}")
            
            response = self.control_referente_ctrl.obtener_asociaciones_control(control_id)
            print(f"DEBUG ControlReferentesDialog - Respuesta del controlador: {response}")
            
            if response.get('success', False):
                asociaciones = response.get('data', [])
                print(f"DEBUG ControlReferentesDialog - {len(asociaciones)} asociaciones encontradas")
                
                for i, asoc in enumerate(asociaciones):
                    print(f"DEBUG ControlReferentesDialog - Procesando asociación {i+1}: {asoc}")
                    
                    fecha_str = ""
                    if asoc.get('fecha_asociacion'):
                        try:
                            from datetime import datetime
                            fecha = datetime.fromisoformat(asoc['fecha_asociacion'].replace('Z', '+00:00'))
                            fecha_str = fecha.strftime("%d/%m/%Y")
                        except Exception as date_error:
                            print(f"DEBUG ControlReferentesDialog - Error procesando fecha: {date_error}")
                            fecha_str = asoc.get('fecha_asociacion', '')[:10]
                    
                    valores = (
                        asoc.get('id', ''),
                        asoc.get('referente_nombre', ''),
                        asoc.get('referente_email', ''),
                        asoc.get('referente_path_archivos', ''),
                        "Sí" if asoc.get('activa', False) else "No",
                        fecha_str,
                        "Sí" if asoc.get('notificar_por_email', False) else "No",
                        "Sí" if asoc.get('notificar_por_archivo', False) else "No",
                        asoc.get('observaciones', '')
                    )
                    
                    print(f"DEBUG ControlReferentesDialog - Insertando valores: {valores}")
                    self.tree.insert("", "end", values=valores)
                    print(f"DEBUG ControlReferentesDialog - Asociación {i+1} insertada exitosamente")
                    
                print(f"DEBUG ControlReferentesDialog - load_asociaciones completado exitosamente")
            else:
                error_msg = response.get('error', 'Error al cargar asociaciones')
                print(f"DEBUG ControlReferentesDialog - Error en respuesta: {error_msg}")
                messagebox.showerror("Error", error_msg)
                
        except Exception as e:
            print(f"DEBUG ControlReferentesDialog - Excepción en load_asociaciones: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def add_referente(self):
        """Abre diálogo para agregar referente al control"""
        # Abrir lista de referentes para seleccionar
        dialog = ReferentesListDialog(self.dialog, self.referente_ctrl)
        self.dialog.wait_window(dialog.dialog)
        
        if dialog.selected_referentes:
            for referente in dialog.selected_referentes:
                # Crear asociación
                response = self.control_referente_ctrl.asociar_control_referente(
                    control_id=self.control_data.get('id'),
                    referente_id=referente['id'],
                    notificar_por_email=True,
                    notificar_por_archivo=False,
                    observaciones=""
                )
                
                if not response.get('success', False):
                    messagebox.showerror("Error", 
                        f"Error al asociar referente '{referente['nombre']}': {response.get('error', 'Error desconocido')}")
            
            # Recargar lista
            self.load_asociaciones()
    
    def edit_asociacion(self):
        """Edita la asociación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una asociación para editar")
            return
        
        item = self.tree.item(selection[0])
        asociacion_id = item['values'][0]
        
        print(f"DEBUG ControlReferentesDialog - Abriendo edición de asociación ID: {asociacion_id}")
        
        # Crear diálogo de edición de asociación
        dialog = EditAsociacionDialog(self.dialog, self.control_referente_ctrl, asociacion_id)
        self.dialog.wait_window(dialog.dialog)
        
        print(f"DEBUG ControlReferentesDialog - Diálogo cerrado. Result: {dialog.result}")
        
        # Asegurar que esta ventana mantenga el foco después de cerrar el diálogo
        self.dialog.lift()
        self.dialog.focus_force()
        self.dialog.grab_set()
        
        if dialog.result:
            print("DEBUG ControlReferentesDialog - Recargando asociaciones...")
            self.load_asociaciones()
            # Asegurar foco después de recargar
            self.ensure_focus()
        else:
            print("DEBUG ControlReferentesDialog - No hay result, no se recarga")
    
    def delete_asociacion(self):
        """Elimina la asociación seleccionada"""
        selection = self.tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una asociación para eliminar")
            return
        
        item = self.tree.item(selection[0])
        asociacion_id = item['values'][0]
        referente_nombre = item['values'][1]
        
        # Confirmar eliminación
        response = messagebox.askyesno(
            "Confirmar eliminación",
            f"¿Está seguro de que desea eliminar la asociación con '{referente_nombre}'?"
        )
        
        if response:
            try:
                result = self.control_referente_ctrl.eliminar_asociacion_por_id(asociacion_id)
                
                if result.get('success', False):
                    messagebox.showinfo("Éxito", result.get('message', 'Asociación eliminada exitosamente'))
                    self.load_asociaciones()
                else:
                    messagebox.showerror("Error", result.get('error', 'Error al eliminar asociación'))
                    
            except Exception as e:
                messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def close_dialog(self):
        """Cierra el diálogo"""
        self.dialog.destroy()


class EditAsociacionDialog:
    """Diálogo para editar una asociación Control-Referente"""
    
    def __init__(self, parent, control_referente_controller, asociacion_id):
        self.result = None
        self.control_referente_ctrl = control_referente_controller
        self.asociacion_id = asociacion_id
        
        # Crear ventana modal
        self.dialog = tk.Toplevel(parent)
        self.dialog.title("Editar Asociación")
        self.dialog.geometry("400x300")
        self.dialog.grab_set()
        
        # Centrar ventana
        self.center_window()
        
        self.create_widgets()
        self.load_asociacion_data()  # Cargar datos reales de la asociación
        
    def center_window(self):
        """Centra la ventana en la pantalla"""
        self.dialog.update_idletasks()
        x = (self.dialog.winfo_screenwidth() // 2) - (400 // 2)
        y = (self.dialog.winfo_screenheight() // 2) - (300 // 2)
        self.dialog.geometry(f"400x300+{x}+{y}")
        
    def create_widgets(self):
        """Crea los widgets del diálogo"""
        frame = ttk.Frame(self.dialog)
        frame.pack(fill="both", expand=True, padx=20, pady=20)
        
        # Campos de la asociación
        ttk.Label(frame, text="Estado de la Asociación:").grid(row=0, column=0, sticky="w", pady=5)
        self.activa_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(frame, text="Activa", variable=self.activa_var).grid(row=0, column=1, pady=5, sticky="w")
        
        ttk.Label(frame, text="Notificaciones:").grid(row=1, column=0, sticky="nw", pady=5)
        notif_frame = ttk.Frame(frame)
        notif_frame.grid(row=1, column=1, pady=5, sticky="w")
        
        self.email_notif_var = tk.BooleanVar(value=True)
        ttk.Checkbutton(notif_frame, text="Por Email", variable=self.email_notif_var).pack(anchor="w")
        
        self.archivo_notif_var = tk.BooleanVar(value=False)
        ttk.Checkbutton(notif_frame, text="Por Archivo", variable=self.archivo_notif_var).pack(anchor="w")
        
        ttk.Label(frame, text="Observaciones:").grid(row=2, column=0, sticky="nw", pady=5)
        self.observaciones_text = tk.Text(frame, height=6, width=35, wrap="word")
        self.observaciones_text.grid(row=2, column=1, pady=5, sticky="ew")
        
        # Scrollbar para observaciones
        obs_scrollbar = ttk.Scrollbar(frame, orient="vertical", command=self.observaciones_text.yview)
        self.observaciones_text.configure(yscrollcommand=obs_scrollbar.set)
        obs_scrollbar.grid(row=2, column=2, sticky="ns", pady=5)
        
        # Configurar expansión
        frame.columnconfigure(1, weight=1)
        frame.rowconfigure(2, weight=1)
        
        # Botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.grid(row=3, column=0, columnspan=3, pady=20)
        
        ttk.Button(buttons_frame, text="Guardar", command=self.save_asociacion).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cancelar", command=self.cancel).pack(side="left", padx=5)
        
    def load_asociacion_data(self):
        """Carga los datos actuales de la asociación desde la base de datos"""
        try:
            response = self.control_referente_ctrl.obtener_asociacion_por_id(self.asociacion_id)
            
            if response.get('success', False):
                data = response.get('data', {})
                
                # Cargar valores reales en los campos
                self.activa_var.set(data.get('activa', True))
                self.email_notif_var.set(data.get('notificar_por_email', True))
                self.archivo_notif_var.set(data.get('notificar_por_archivo', False))
                
                # Cargar observaciones
                observaciones = data.get('observaciones', '')
                self.observaciones_text.delete("1.0", tk.END)
                self.observaciones_text.insert("1.0", observaciones)
                
                print(f"DEBUG EditAssociationDialog - Datos cargados:")
                print(f"  Activa: {data.get('activa')}")
                print(f"  Email: {data.get('notificar_por_email')}")
                print(f"  Archivo: {data.get('notificar_por_archivo')}")
                print(f"  Observaciones: '{observaciones}'")
            else:
                error_msg = response.get('error', 'Error al cargar datos de la asociación')
                messagebox.showerror("Error", error_msg)
                print(f"ERROR - {error_msg}")
                
        except Exception as e:
            error_msg = f"Error inesperado al cargar asociación: {str(e)}"
            messagebox.showerror("Error", error_msg)
            print(f"ERROR - {error_msg}")
            import traceback
            traceback.print_exc()
        
    def save_asociacion(self):
        """Guarda los cambios de la asociación"""
        try:
            observaciones = self.observaciones_text.get("1.0", "end-1c").strip()
            
            print(f"DEBUG EditAsociacionDialog - Guardando asociación ID: {self.asociacion_id}")
            print(f"  Activa: {self.activa_var.get()}")
            print(f"  Email: {self.email_notif_var.get()}")
            print(f"  Archivo: {self.archivo_notif_var.get()}")
            print(f"  Observaciones: '{observaciones}'")
            
            response = self.control_referente_ctrl.actualizar_asociacion(
                asociacion_id=self.asociacion_id,
                activa=self.activa_var.get(),
                notificar_por_email=self.email_notif_var.get(),
                notificar_por_archivo=self.archivo_notif_var.get(),
                observaciones=observaciones
            )
            
            print(f"DEBUG EditAsociacionDialog - Respuesta del controlador: {response}")
            
            if response.get('success', False):
                self.result = response['data']
                print(f"DEBUG EditAsociacionDialog - Estableciendo result: {self.result}")
                messagebox.showinfo("Éxito", response.get('message', 'Asociación actualizada exitosamente'))
                
                # Asegurar que la ventana padre mantenga el foco
                parent = self.dialog.master
                self.dialog.destroy()
                
                # Traer la ventana padre al frente
                if parent:
                    parent.lift()
                    parent.focus_force()
                    parent.grab_set()
            else:
                print(f"DEBUG EditAsociacionDialog - Error en respuesta: {response.get('error')}")
                messagebox.showerror("Error", response.get('error', 'Error desconocido'))
                
        except Exception as e:
            print(f"DEBUG EditAsociacionDialog - Excepción: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error inesperado: {str(e)}")
    
    def cancel(self):
        """Cancela la operación"""
        self.dialog.destroy()