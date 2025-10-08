"""
Ventana de gestión de programaciones

Permite crear, editar, eliminar y gestionar programaciones de controles
"""
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, time
from typing import Optional, Dict, Any
import sys
import os

# Agregar el directorio src al path para importar módulos
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', '..')))

from src.domain.entities.programacion import TipoProgramacion, DiaSemana


class ProgramacionesWindow:
    """Ventana para gestión de programaciones"""
    
    def __init__(self, parent, programacion_controller, control_controller):
        self.parent = parent
        self.programacion_ctrl = programacion_controller
        self.control_ctrl = control_controller
        
        self.window = None
        self.controles = []
        self.programaciones = []
        
        # Variables para formulario
        self.control_var = tk.StringVar()
        self.nombre_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()
        self.tipo_var = tk.StringVar()
        self.activo_var = tk.BooleanVar(value=True)
        self.hora_var = tk.StringVar()
        self.intervalo_var = tk.StringVar()
        
        # Variable para controlar si estamos editando
        self.programacion_editando = None
        
        # Variables para días de semana
        self.dias_semana_vars = {}
        for dia in DiaSemana:
            self.dias_semana_vars[dia] = tk.BooleanVar()
        
        # Variables para días del mes (1-31)
        self.dias_mes_vars = {}
        for dia in range(1, 32):
            self.dias_mes_vars[dia] = tk.BooleanVar()
        
        # Variable especial para fin de mes
        self.fin_mes_var = tk.BooleanVar()
    
    def show(self):
        """Muestra la ventana de gestión de programaciones"""
        if self.window and self.window.winfo_exists():
            self.window.lift()
            return
        
        self.create_window()
        self.load_data()
    
    def create_window(self):
        """Crea la ventana principal"""
        self.window = tk.Toplevel(self.parent)
        self.window.title("Gestión de Programaciones")
        self.window.geometry("900x700")
        self.window.transient(self.parent)
        self.window.grab_set()
        
        # Frame principal con pestañas
        notebook = ttk.Notebook(self.window)
        notebook.pack(fill="both", expand=True, padx=10, pady=10)
        
        # Pestaña de listado
        self.create_lista_tab(notebook)
        
        # Pestaña de creación/edición
        self.create_form_tab(notebook)
    
    def create_lista_tab(self, notebook):
        """Crea la pestaña de listado de programaciones"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Programaciones")
        
        # Frame superior con filtros
        filter_frame = ttk.LabelFrame(frame, text="Filtros")
        filter_frame.pack(fill="x", padx=5, pady=5)
        
        # Filtro por control
        ttk.Label(filter_frame, text="Control:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
        self.filter_control_combo = ttk.Combobox(filter_frame, state="readonly", width=30)
        self.filter_control_combo.grid(row=0, column=1, padx=5, pady=5, sticky="ew")
        self.filter_control_combo.bind("<<ComboboxSelected>>", self.filter_programaciones)
        
        # Filtro solo activas
        self.filter_activas_var = tk.BooleanVar()
        ttk.Checkbutton(
            filter_frame, 
            text="Solo activas", 
            variable=self.filter_activas_var,
            command=self.filter_programaciones
        ).grid(row=0, column=2, padx=5, pady=5)
        
        # Botón refrescar
        ttk.Button(
            filter_frame, 
            text="Refrescar", 
            command=self.load_data
        ).grid(row=0, column=3, padx=5, pady=5)
        
        # Botón limpiar filtros
        ttk.Button(
            filter_frame, 
            text="Limpiar filtros", 
            command=self.clear_filters
        ).grid(row=0, column=4, padx=5, pady=5)
        
        filter_frame.columnconfigure(1, weight=1)
        
        # Lista de programaciones
        self.create_programaciones_list(frame)
        
        # Frame inferior con botones
        buttons_frame = ttk.Frame(frame)
        buttons_frame.pack(fill="x", padx=5, pady=5)
        
        ttk.Button(
            buttons_frame, 
            text="Nueva Programación", 
            command=self.nueva_programacion
        ).pack(side="left", padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Editar", 
            command=self.editar_programacion
        ).pack(side="left", padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Eliminar", 
            command=self.eliminar_programacion
        ).pack(side="left", padx=5)
        
        ttk.Button(
            buttons_frame, 
            text="Activar/Desactivar", 
            command=self.toggle_programacion
        ).pack(side="left", padx=5)
    
    def create_programaciones_list(self, parent):
        """Crea la lista de programaciones con TreeView"""
        # Frame para TreeView con scrollbars
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill="both", expand=True, padx=5, pady=5)
        
        # Crear TreeView
        columns = ("ID", "Control", "Nombre", "Tipo", "Descripción", "Estado", "Próxima Ejecución")
        self.programaciones_tree = ttk.Treeview(tree_frame, columns=columns, show="headings")
        
        # Configurar columnas
        self.programaciones_tree.heading("ID", text="ID")
        self.programaciones_tree.heading("Control", text="Control")
        self.programaciones_tree.heading("Nombre", text="Nombre")
        self.programaciones_tree.heading("Tipo", text="Tipo")
        self.programaciones_tree.heading("Descripción", text="Descripción")
        self.programaciones_tree.heading("Estado", text="Estado")
        self.programaciones_tree.heading("Próxima Ejecución", text="Próxima Ejecución")
        
        # Configurar ancho de columnas
        self.programaciones_tree.column("ID", width=50)
        self.programaciones_tree.column("Control", width=150)
        self.programaciones_tree.column("Nombre", width=150)
        self.programaciones_tree.column("Tipo", width=100)
        self.programaciones_tree.column("Descripción", width=200)
        self.programaciones_tree.column("Estado", width=80)
        self.programaciones_tree.column("Próxima Ejecución", width=150)
        
        # Scrollbars
        v_scrollbar = ttk.Scrollbar(tree_frame, orient="vertical", command=self.programaciones_tree.yview)
        h_scrollbar = ttk.Scrollbar(tree_frame, orient="horizontal", command=self.programaciones_tree.xview)
        self.programaciones_tree.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # Grid layout
        self.programaciones_tree.grid(row=0, column=0, sticky="nsew")
        v_scrollbar.grid(row=0, column=1, sticky="ns")
        h_scrollbar.grid(row=1, column=0, sticky="ew")
        
        tree_frame.grid_rowconfigure(0, weight=1)
        tree_frame.grid_columnconfigure(0, weight=1)
    
    def create_form_tab(self, notebook):
        """Crea la pestaña de formulario"""
        frame = ttk.Frame(notebook)
        notebook.add(frame, text="Nueva/Editar")
        
        # Crear formulario
        self.create_form(frame)
    
    def create_form(self, parent):
        """Crea el formulario de programación"""
        # Frame principal del formulario
        form_frame = ttk.LabelFrame(parent, text="Datos de Programación")
        form_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        row = 0
        
        # Control
        ttk.Label(form_frame, text="Control:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.control_combo = ttk.Combobox(form_frame, textvariable=self.control_var, state="readonly", width=40)
        self.control_combo.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        row += 1
        
        # Nombre
        ttk.Label(form_frame, text="Nombre:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.nombre_var, width=40).grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        row += 1
        
        # Descripción
        ttk.Label(form_frame, text="Descripción:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        ttk.Entry(form_frame, textvariable=self.descripcion_var, width=40).grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        row += 1
        
        # Tipo de programación
        ttk.Label(form_frame, text="Tipo:").grid(row=row, column=0, padx=5, pady=5, sticky="w")
        self.tipo_combo = ttk.Combobox(form_frame, textvariable=self.tipo_var, state="readonly", width=40)
        self.tipo_combo.grid(row=row, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
        self.tipo_combo.bind("<<ComboboxSelected>>", self.on_tipo_changed)
        row += 1
        
        # Activo
        ttk.Checkbutton(form_frame, text="Activo", variable=self.activo_var).grid(row=row, column=1, padx=5, pady=5, sticky="w")
        row += 1
        
        # Configuración específica por tipo (se mostrará/ocultará según el tipo)
        self.config_frame = ttk.LabelFrame(form_frame, text="Configuración")
        self.config_frame.grid(row=row, column=0, columnspan=3, padx=5, pady=10, sticky="ew")
        row += 1
        
        # Botones
        buttons_frame = ttk.Frame(form_frame)
        buttons_frame.grid(row=row, column=0, columnspan=3, pady=10)
        
        self.save_button = ttk.Button(buttons_frame, text="Guardar", command=self.save_programacion)
        self.save_button.pack(side="left", padx=5)
        
        self.update_button = ttk.Button(buttons_frame, text="Actualizar", command=self.update_programacion)
        self.update_button.pack(side="left", padx=5)
        self.update_button.pack_forget()  # Ocultar inicialmente
        
        ttk.Button(buttons_frame, text="Limpiar", command=self.clear_form).pack(side="left", padx=5)
        
        form_frame.columnconfigure(1, weight=1)
    
    def on_tipo_changed(self, event=None):
        """Maneja el cambio de tipo de programación"""
        # Limpiar frame de configuración
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        
        tipo = self.tipo_var.get()
        if " - " in tipo:
            tipo = tipo.split(" - ")[0].lower()
        
        if tipo in ["diaria", "semanal", "mensual", "unica_vez"]:
            # Hora de ejecución
            ttk.Label(self.config_frame, text="Hora (HH:MM):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ttk.Entry(self.config_frame, textvariable=self.hora_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
        
        if tipo == "semanal":
            # Días de la semana
            ttk.Label(self.config_frame, text="Días de la semana:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            dias_frame = ttk.Frame(self.config_frame)
            dias_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
            
            col = 0
            for dia in DiaSemana:
                ttk.Checkbutton(
                    dias_frame, 
                    text=dia.name.capitalize(), 
                    variable=self.dias_semana_vars[dia]
                ).grid(row=0, column=col, padx=2)
                col += 1
        
        elif tipo == "mensual":
            # Días del mes
            ttk.Label(self.config_frame, text="Días del mes:").grid(row=1, column=0, padx=5, pady=5, sticky="nw")
            dias_mes_frame = ttk.Frame(self.config_frame)
            dias_mes_frame.grid(row=1, column=1, columnspan=2, padx=5, pady=5, sticky="w")
            
            # Opción especial para fin de mes
            ttk.Checkbutton(
                dias_mes_frame,
                text="🗓️ Fin de mes",
                variable=self.fin_mes_var
            ).grid(row=0, column=0, columnspan=3, padx=2, pady=2, sticky="w")
            
            # Separador visual
            ttk.Separator(dias_mes_frame, orient="horizontal").grid(row=1, column=0, columnspan=8, sticky="ew", pady=2)
            
            # Crear checkboxes para días del mes en una grilla
            for dia in range(1, 32):
                row_pos = ((dia - 1) // 8) + 2  # +2 para dejar espacio a la opción fin de mes
                col_pos = (dia - 1) % 8
                ttk.Checkbutton(
                    dias_mes_frame,
                    text=str(dia),
                    variable=self.dias_mes_vars[dia],
                    width=3
                ).grid(row=row_pos, column=col_pos, padx=1, pady=1, sticky="w")
        
        elif tipo == "intervalo":
            # Intervalo en minutos
            ttk.Label(self.config_frame, text="Intervalo (minutos):").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            ttk.Entry(self.config_frame, textvariable=self.intervalo_var, width=10).grid(row=0, column=1, padx=5, pady=5, sticky="w")
    
    def load_data(self):
        """Carga los datos iniciales"""
        print("DEBUG - Iniciando load_data...")
        self.load_controles()
        self.load_tipos_programacion()
        self.load_programaciones()
        print("DEBUG - load_data completado")
    
    def load_controles(self):
        """Carga la lista de controles"""
        try:
            print("DEBUG - Cargando controles...")
            response = self.control_ctrl.listar_controles()
            print(f"DEBUG - Respuesta controles: {response}")
            
            if response['success']:
                self.controles = response['data']
                print(f"DEBUG - {len(self.controles)} controles cargados")
                
                # Actualizar combos
                control_names = [""] + [f"{c['id']} - {c['nombre']}" for c in self.controles]
                self.control_combo['values'] = control_names
                self.filter_control_combo['values'] = ["Todos"] + control_names[1:]
                self.filter_control_combo.set("Todos")
                
                print(f"DEBUG - Combos actualizados: {control_names}")
            else:
                print(f"DEBUG - Error en respuesta: {response['message']}")
                messagebox.showerror("Error", f"Error al cargar controles: {response['message']}")
        except Exception as e:
            print(f"DEBUG - Excepción al cargar controles: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al cargar controles: {str(e)}")
    
    def load_tipos_programacion(self):
        """Carga los tipos de programación"""
        try:
            response = self.programacion_ctrl.obtener_tipos_programacion()
            if response['success']:
                tipos = []
                for t in response['data']:
                    # Crear formato más legible: DIARIA - Ejecutar todos los días a hora específica
                    tipo_display = f"{t['value'].upper()} - {t['description']}"
                    tipos.append(tipo_display)
                self.tipo_combo['values'] = tipos
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar tipos: {str(e)}")
    
    def load_programaciones(self):
        """Carga la lista de programaciones"""
        try:
            print("DEBUG - Iniciando carga de programaciones...")
            response = self.programacion_ctrl.listar_programaciones()
            print(f"DEBUG - Respuesta del controlador: {response}")
            
            if response['success']:
                self.programaciones = response['data']
                print(f"DEBUG - {len(self.programaciones)} programaciones cargadas")
                self.update_programaciones_tree()
            else:
                print(f"DEBUG - Error en respuesta: {response['message']}")
                messagebox.showerror("Error", f"Error al cargar programaciones: {response['message']}")
        except Exception as e:
            print(f"DEBUG - Excepción al cargar programaciones: {e}")
            import traceback
            traceback.print_exc()
            messagebox.showerror("Error", f"Error al cargar programaciones: {str(e)}")
    
    def update_programaciones_tree(self, programaciones_filtradas=None):
        """Actualiza el TreeView de programaciones"""
        # Limpiar TreeView
        for item in self.programaciones_tree.get_children():
            self.programaciones_tree.delete(item)
        
        # Usar programaciones filtradas o todas
        programaciones_a_mostrar = programaciones_filtradas if programaciones_filtradas is not None else self.programaciones
        
        # Agregar programaciones
        for prog in programaciones_a_mostrar:
            # Buscar nombre del control
            control_nombre = "Control no encontrado"
            for control in self.controles:
                if control['id'] == prog['control_id']:
                    control_nombre = control['nombre']
                    break
            
            estado = "🟢 Activa" if prog['activo'] else "🔴 Inactiva"
            proxima = prog.get('proxima_ejecucion', 'No programada')
            if proxima and proxima != 'No programada':
                try:
                    # Formatear fecha si es válida
                    proxima = datetime.fromisoformat(proxima).strftime('%d/%m/%Y %H:%M')
                except:
                    pass
            
            self.programaciones_tree.insert("", "end", values=(
                prog['id'],
                control_nombre,
                prog['nombre'],
                prog['tipo_programacion'],
                prog['descripcion_programacion'],
                estado,
                proxima
            ))
    
    def filter_programaciones(self, event=None):
        """Filtra las programaciones según los criterios seleccionados"""
        if not hasattr(self, 'programaciones') or not self.programaciones:
            return
        
        # Obtener criterios de filtro
        control_filtro = self.filter_control_combo.get() if hasattr(self, 'filter_control_combo') else "Todos"
        solo_activas = self.filter_activas_var.get() if hasattr(self, 'filter_activas_var') else False
        
        # Filtrar programaciones
        programaciones_filtradas = []
        
        for prog in self.programaciones:
            # Filtro por control
            if control_filtro != "Todos":
                control_id_filtro = int(control_filtro.split(" - ")[0]) if " - " in control_filtro else None
                if control_id_filtro and prog.get('control_id') != control_id_filtro:
                    continue
            
            # Filtro por activas
            if solo_activas and not prog.get('activo', True):
                continue
            
            programaciones_filtradas.append(prog)
        
        # Actualizar la vista con programaciones filtradas
        self.update_programaciones_tree(programaciones_filtradas)
    
    def clear_filters(self):
        """Limpia todos los filtros y muestra todas las programaciones"""
        if hasattr(self, 'filter_control_combo'):
            self.filter_control_combo.set("Todos")
        if hasattr(self, 'filter_activas_var'):
            self.filter_activas_var.set(False)
        
        # Mostrar todas las programaciones
        self.update_programaciones_tree()
    
    def nueva_programacion(self):
        """Prepara el formulario para nueva programación"""
        self.clear_form()
        self.programacion_editando = None
        # Cambiar a la pestaña de formulario
        notebook = self.window.children['!notebook']
        notebook.select(1)  # Seleccionar pestaña "Nueva/Editar"
    
    def editar_programacion(self):
        """Edita la programación seleccionada"""
        selection = self.programaciones_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una programación para editar")
            return
        
        # Obtener datos de la programación seleccionada
        item = self.programaciones_tree.item(selection[0])
        prog_id = item['values'][0]
        
        # Buscar la programación en la lista
        programacion = None
        for prog in self.programaciones:
            if prog['id'] == prog_id:
                programacion = prog
                break
        
        if not programacion:
            messagebox.showerror("Error", "No se pudo encontrar la programación seleccionada")
            return
        
        # Cargar datos en el formulario
        self.cargar_programacion_en_formulario(programacion)
        
        # Cambiar a la pestaña de formulario
        notebook = self.window.children['!notebook']
        notebook.select(1)  # Seleccionar pestaña "Nueva/Editar"
    
    def eliminar_programacion(self):
        """Elimina la programación seleccionada"""
        selection = self.programaciones_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una programación para eliminar")
            return
        
        item = self.programaciones_tree.item(selection[0])
        prog_id = item['values'][0]
        prog_nombre = item['values'][2]
        
        if messagebox.askyesno("Confirmar", f"¿Está seguro de eliminar la programación '{prog_nombre}'?"):
            try:
                response = self.programacion_ctrl.eliminar_programacion(prog_id)
                if response['success']:
                    messagebox.showinfo("Éxito", response['message'])
                    self.load_programaciones()
                else:
                    messagebox.showerror("Error", response['message'])
            except Exception as e:
                messagebox.showerror("Error", f"Error al eliminar: {str(e)}")
    
    def toggle_programacion(self):
        """Activa/desactiva la programación seleccionada"""
        selection = self.programaciones_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Seleccione una programación")
            return
        
        item = self.programaciones_tree.item(selection[0])
        prog_id = item['values'][0]
        estado_actual = "Activa" in item['values'][5]
        nuevo_estado = not estado_actual
        
        try:
            response = self.programacion_ctrl.activar_desactivar_programacion(prog_id, nuevo_estado)
            if response['success']:
                messagebox.showinfo("Éxito", response['message'])
                self.load_programaciones()
            else:
                messagebox.showerror("Error", response['message'])
        except Exception as e:
            messagebox.showerror("Error", f"Error al cambiar estado: {str(e)}")
    
    def save_programacion(self):
        """Guarda la programación"""
        # Validar campos básicos
        if not self.control_var.get():
            messagebox.showerror("Error", "Seleccione un control")
            return
        
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "Ingrese un nombre")
            return
        
        if not self.tipo_var.get():
            messagebox.showerror("Error", "Seleccione un tipo de programación")
            return
        
        try:
            # Extraer ID del control
            control_id = int(self.control_var.get().split(" - ")[0])
            
            # Extraer tipo de programación
            tipo = self.tipo_var.get().split(" - ")[0].lower()
            
            # Preparar datos
            datos = {
                'control_id': control_id,
                'nombre': self.nombre_var.get().strip(),
                'descripcion': self.descripcion_var.get().strip(),
                'tipo_programacion': tipo,
                'activo': self.activo_var.get()
            }
            
            # Agregar configuración específica según el tipo
            if tipo in ["diaria", "semanal", "mensual", "unica_vez"]:
                if self.hora_var.get():
                    datos['hora_ejecucion'] = self.hora_var.get()
            
            if tipo == "semanal":
                dias_seleccionados = []
                for dia, var in self.dias_semana_vars.items():
                    if var.get():
                        dias_seleccionados.append(dia.value)
                if dias_seleccionados:
                    datos['dias_semana'] = dias_seleccionados
            
            elif tipo == "mensual":
                dias_seleccionados = []
                
                # Verificar si se seleccionó fin de mes
                if self.fin_mes_var.get():
                    dias_seleccionados.append(-1)  # Valor especial para fin de mes
                
                # Agregar días específicos seleccionados
                for dia, var in self.dias_mes_vars.items():
                    if var.get():
                        dias_seleccionados.append(dia)
                
                if dias_seleccionados:
                    datos['dias_mes'] = dias_seleccionados
            
            elif tipo == "intervalo":
                if self.intervalo_var.get():
                    datos['intervalo_minutos'] = int(self.intervalo_var.get())
            
            # Crear programación
            response = self.programacion_ctrl.crear_programacion(datos)
            if response['success']:
                messagebox.showinfo("Éxito", response['message'])
                self.clear_form()
                self.load_programaciones()
            else:
                messagebox.showerror("Error", response['message'])
                
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al guardar: {str(e)}")
    
    def update_programacion(self):
        """Actualiza una programación existente"""
        if not self.programacion_editando:
            messagebox.showerror("Error", "No hay programación seleccionada para actualizar")
            return
        
        # Validar campos básicos
        if not self.control_var.get():
            messagebox.showerror("Error", "Seleccione un control")
            return
        
        if not self.nombre_var.get().strip():
            messagebox.showerror("Error", "Ingrese un nombre")
            return
        
        if not self.tipo_var.get():
            messagebox.showerror("Error", "Seleccione un tipo de programación")
            return
        
        try:
            # Extraer ID del control
            control_id = int(self.control_var.get().split(" - ")[0])
            
            # Extraer tipo de programación
            tipo = self.tipo_var.get().split(" - ")[0].lower()
            
            # Preparar datos para actualización
            datos = {
                'id': self.programacion_editando['id'],
                'control_id': control_id,  # ← AGREGADO: control_id faltante
                'nombre': self.nombre_var.get().strip(),
                'descripcion': self.descripcion_var.get().strip(),
                'tipo_programacion': tipo,
                'activo': self.activo_var.get()
            }
            
            # Agregar configuración específica según el tipo
            if tipo in ["diaria", "semanal", "mensual", "unica_vez"]:
                if self.hora_var.get():
                    datos['hora_ejecucion'] = self.hora_var.get()
            
            if tipo == "semanal":
                dias_seleccionados = []
                for dia, var in self.dias_semana_vars.items():
                    if var.get():
                        dias_seleccionados.append(dia.value)
                if dias_seleccionados:
                    datos['dias_semana'] = dias_seleccionados
            
            elif tipo == "mensual":
                dias_seleccionados = []
                
                # Verificar si se seleccionó fin de mes
                if self.fin_mes_var.get():
                    dias_seleccionados.append(-1)  # Valor especial para fin de mes
                
                # Agregar días específicos seleccionados
                for dia, var in self.dias_mes_vars.items():
                    if var.get():
                        dias_seleccionados.append(dia)
                
                if dias_seleccionados:
                    datos['dias_mes'] = dias_seleccionados
            
            elif tipo == "intervalo":
                if self.intervalo_var.get():
                    datos['intervalo_minutos'] = int(self.intervalo_var.get())
            
            # Actualizar programación
            response = self.programacion_ctrl.actualizar_programacion(datos)
            if response['success']:
                messagebox.showinfo("Éxito", response['message'])
                self.clear_form()
                self.load_programaciones()
            else:
                messagebox.showerror("Error", response['message'])
                
        except ValueError as e:
            messagebox.showerror("Error", f"Error en los datos: {str(e)}")
        except Exception as e:
            messagebox.showerror("Error", f"Error al actualizar: {str(e)}")
    
    def cargar_programacion_en_formulario(self, programacion):
        """Carga los datos de una programación en el formulario para edición"""
        self.programacion_editando = programacion
        
        # Cargar datos básicos
        # Buscar el control correspondiente
        for control in self.controles:
            if control['id'] == programacion['control_id']:
                self.control_var.set(f"{control['id']} - {control['nombre']}")
                break
        
        self.nombre_var.set(programacion['nombre'])
        self.descripcion_var.set(programacion['descripcion'])
        self.activo_var.set(programacion['activo'])
        
        # Cargar tipo de programación
        tipo_programacion = programacion['tipo_programacion'].upper()
        for value in self.tipo_combo['values']:
            if value.startswith(tipo_programacion):
                self.tipo_var.set(value)
                break
        
        # Disparar el evento de cambio de tipo para mostrar configuración
        self.on_tipo_changed()
        
        # Cargar configuración específica
        if programacion.get('hora_ejecucion'):
            self.hora_var.set(programacion['hora_ejecucion'])
        
        if programacion.get('intervalo_minutos'):
            self.intervalo_var.set(str(programacion['intervalo_minutos']))
        
        # Cargar días de semana
        if programacion.get('dias_semana'):
            # Limpiar selecciones previas
            for var in self.dias_semana_vars.values():
                var.set(False)
            
            # Marcar días seleccionados
            for dia_nombre in programacion['dias_semana']:
                for dia, var in self.dias_semana_vars.items():
                    if dia.name.capitalize() == dia_nombre:
                        var.set(True)
                        break
        
        # Cargar días del mes
        if programacion.get('dias_mes'):
            # Limpiar selecciones previas
            for var in self.dias_mes_vars.values():
                var.set(False)
            self.fin_mes_var.set(False)
            
            # Marcar días seleccionados
            for dia in programacion['dias_mes']:
                if dia == -1:
                    self.fin_mes_var.set(True)
                elif dia in self.dias_mes_vars:
                    self.dias_mes_vars[dia].set(True)
        
        # Cambiar botones para modo edición
        self.save_button.pack_forget()
        self.update_button.pack(side="left", padx=5)
    
    def clear_form(self):
        """Limpia el formulario"""
        self.control_var.set("")
        self.nombre_var.set("")
        self.descripcion_var.set("")
        self.tipo_var.set("")
        self.activo_var.set(True)
        self.hora_var.set("")
        self.intervalo_var.set("")
        
        # Limpiar días de semana
        for var in self.dias_semana_vars.values():
            var.set(False)
        
        # Limpiar días del mes
        for var in self.dias_mes_vars.values():
            var.set(False)
        
        # Limpiar fin de mes
        self.fin_mes_var.set(False)
        
        # Limpiar frame de configuración
        for widget in self.config_frame.winfo_children():
            widget.destroy()
        
        # Resetear modo edición
        self.programacion_editando = None
        self.update_button.pack_forget()
        self.save_button.pack(side="left", padx=5)