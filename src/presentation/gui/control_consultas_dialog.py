"""
Diálogo para gestionar las consultas asociadas a un control
"""
import tkinter as tk
from tkinter import ttk, messagebox
from typing import Optional, Dict, Any, List


class ControlConsultasDialog:
    """Diálogo para gestionar consultas de un control específico"""
    
    def __init__(self, parent, control_id: int, control_nombre: str, consulta_ctrl, consulta_control_ctrl):
        self.result = None
        self.control_id = control_id
        self.control_nombre = control_nombre
        self.consulta_ctrl = consulta_ctrl
        self.consulta_control_ctrl = consulta_control_ctrl
        
        # Datos
        self.todas_consultas = []
        self.consultas_asociadas = []
        
        self.dialog = tk.Toplevel(parent)
        self.dialog.title(f"Gestionar Consultas - Control: {control_nombre}")
        self.dialog.geometry("900x600")
        self.dialog.grab_set()
        self.dialog.resizable(True, True)
        
        self.create_widgets()
        self.load_data()
        
    def create_widgets(self):
        """Crea widgets del diálogo"""
        # Frame principal
        main_frame = ttk.Frame(self.dialog, padding="10")
        main_frame.pack(fill="both", expand=True)
        
        # Título
        title_label = ttk.Label(main_frame, text=f"Gestión de Consultas - Control: {self.control_nombre}", 
                               font=("Arial", 12, "bold"))
        title_label.pack(pady=(0, 10))
        
        # Frame de contenido con dos columnas
        content_frame = ttk.Frame(main_frame)
        content_frame.pack(fill="both", expand=True)
        content_frame.grid_columnconfigure(0, weight=1)
        content_frame.grid_columnconfigure(1, weight=1)
        
        # Columna izquierda: Consultas disponibles
        left_frame = ttk.LabelFrame(content_frame, text="Consultas Disponibles", padding="5")
        left_frame.grid(row=0, column=0, sticky="nsew", padx=(0, 5))
        
        # Lista de consultas disponibles
        self.disponibles_tree = ttk.Treeview(left_frame, columns=("ID", "Nombre", "Descripción"), 
                                            show="headings", height=12)
        self.disponibles_tree.heading("ID", text="ID")
        self.disponibles_tree.heading("Nombre", text="Nombre")
        self.disponibles_tree.heading("Descripción", text="Descripción")
        self.disponibles_tree.column("ID", width=50)
        self.disponibles_tree.column("Nombre", width=150)
        self.disponibles_tree.column("Descripción", width=200)
        self.disponibles_tree.pack(fill="both", expand=True, pady=(0, 5))
        
        # Botones para consultas disponibles
        disp_buttons_frame = ttk.Frame(left_frame)
        disp_buttons_frame.pack(fill="x")
        ttk.Button(disp_buttons_frame, text="Asociar >>", command=self.asociar_consulta).pack(side="left", padx=5)
        ttk.Button(disp_buttons_frame, text="Nueva Consulta", command=self.nueva_consulta).pack(side="left", padx=5)
        
        # Columna derecha: Consultas asociadas
        right_frame = ttk.LabelFrame(content_frame, text="Consultas Asociadas al Control", padding="5")
        right_frame.grid(row=0, column=1, sticky="nsew", padx=(5, 0))
        
        # Lista de consultas asociadas
        self.asociadas_tree = ttk.Treeview(right_frame, columns=("ID", "Nombre", "Orden", "Disparo"), 
                                          show="headings", height=12)
        self.asociadas_tree.heading("ID", text="ID")
        self.asociadas_tree.heading("Nombre", text="Nombre")
        self.asociadas_tree.heading("Orden", text="Orden")
        self.asociadas_tree.heading("Disparo", text="Disparo")
        self.asociadas_tree.column("ID", width=50)
        self.asociadas_tree.column("Nombre", width=150)
        self.asociadas_tree.column("Orden", width=60)
        self.asociadas_tree.column("Disparo", width=60)
        self.asociadas_tree.pack(fill="both", expand=True, pady=(0, 5))
        
        # Botones para consultas asociadas
        asoc_buttons_frame = ttk.Frame(right_frame)
        asoc_buttons_frame.pack(fill="x")
        ttk.Button(asoc_buttons_frame, text="<< Desasociar", command=self.desasociar_consulta).pack(side="left", padx=5)
        ttk.Button(asoc_buttons_frame, text="Marcar Disparo", command=self.marcar_disparo).pack(side="left", padx=5)
        ttk.Button(asoc_buttons_frame, text="Cambiar Orden", command=self.cambiar_orden).pack(side="left", padx=5)
        
        # Frame de botones principales
        buttons_frame = ttk.Frame(main_frame)
        buttons_frame.pack(fill="x", pady=(10, 0))
        
        ttk.Button(buttons_frame, text="Actualizar", command=self.load_data).pack(side="left", padx=5)
        ttk.Button(buttons_frame, text="Cerrar", command=self.close).pack(side="right", padx=5)
        
    def load_data(self):
        """Carga los datos de consultas"""
        try:
            # Cargar todas las consultas
            response = self.consulta_ctrl.obtener_todas()
            if response.get('success', False):
                self.todas_consultas = response.get('data', [])
            else:
                self.todas_consultas = []
                messagebox.showerror("Error", "No se pudieron cargar las consultas")
            
            # Cargar consultas asociadas al control
            try:
                response = self.consulta_control_ctrl.obtener_consultas_por_control(self.control_id)
                if response.get('success', False):
                    self.consultas_asociadas = response.get('data', [])
                else:
                    self.consultas_asociadas = []
            except Exception as e:
                print(f"Error cargando asociaciones: {e}")
                self.consultas_asociadas = []
            
            self.update_trees()
            
        except Exception as e:
            messagebox.showerror("Error", f"Error al cargar datos: {str(e)}")
    
    def update_trees(self):
        """Actualiza las listas de consultas"""
        # Limpiar árboles
        for item in self.disponibles_tree.get_children():
            self.disponibles_tree.delete(item)
        for item in self.asociadas_tree.get_children():
            self.asociadas_tree.delete(item)
        
        # IDs de consultas asociadas
        ids_asociadas = [c.get('consulta_id') for c in self.consultas_asociadas]
        
        # Llenar consultas disponibles (las que no están asociadas)
        for consulta in self.todas_consultas:
            if consulta.get('id') not in ids_asociadas:
                self.disponibles_tree.insert("", "end", values=(
                    consulta.get('id', ''),
                    consulta.get('nombre', ''),
                    consulta.get('descripcion', '')[:50] + "..." if len(consulta.get('descripcion', '')) > 50 else consulta.get('descripcion', '')
                ))
        
        # Llenar consultas asociadas
        for asociacion in sorted(self.consultas_asociadas, key=lambda x: x.get('orden', 1)):
            consulta = next((c for c in self.todas_consultas if c.get('id') == asociacion.get('consulta_id')), {})
            disparo_text = "SÍ" if asociacion.get('es_disparo', False) else "NO"
            self.asociadas_tree.insert("", "end", values=(
                consulta.get('id', ''),
                consulta.get('nombre', ''),
                asociacion.get('orden', 1),
                disparo_text
            ))
    
    def asociar_consulta(self):
        """Asocia una consulta al control"""
        selection = self.disponibles_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para asociar")
            return
        
        item = self.disponibles_tree.item(selection[0])
        values = item['values']
        consulta_id = values[0]
        consulta_nombre = values[1]
        
        try:
            # Crear la asociación
            response = self.consulta_control_ctrl.asociar_consulta(
                control_id=self.control_id,
                consulta_id=consulta_id,
                es_disparo=False,
                orden=len(self.consultas_asociadas) + 1
            )
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Consulta '{consulta_nombre}' asociada correctamente")
                self.load_data()  # Recargar datos
            else:
                messagebox.showerror("Error", response.get('message', 'Error al asociar consulta'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al asociar consulta: {str(e)}")
    
    def desasociar_consulta(self):
        """Desasocia una consulta del control"""
        selection = self.asociadas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para desasociar")
            return
        
        item = self.asociadas_tree.item(selection[0])
        values = item['values']
        consulta_id = values[0]
        consulta_nombre = values[1]
        
        # Confirmar desasociación
        if not messagebox.askyesno("Confirmar", f"¿Desea desasociar la consulta '{consulta_nombre}' del control?"):
            return
        
        try:
            response = self.consulta_control_ctrl.desasociar_consulta(self.control_id, consulta_id)
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Consulta '{consulta_nombre}' desasociada correctamente")
                self.load_data()  # Recargar datos
            else:
                messagebox.showerror("Error", response.get('message', 'Error al desasociar consulta'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al desasociar consulta: {str(e)}")
    
    def marcar_disparo(self):
        """Marca una consulta como de disparo"""
        selection = self.asociadas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para marcar como disparo")
            return
        
        item = self.asociadas_tree.item(selection[0])
        values = item['values']
        consulta_id = values[0]
        consulta_nombre = values[1]
        
        # Confirmar acción
        if not messagebox.askyesno("Confirmar", f"¿Desea marcar la consulta '{consulta_nombre}' como consulta de disparo?\\n\\nEsto desmarcará cualquier otra consulta de disparo existente."):
            return
        
        try:
            response = self.consulta_control_ctrl.establecer_consulta_disparo(self.control_id, consulta_id)
            if response.get('success', False):
                messagebox.showinfo("Éxito", f"Consulta '{consulta_nombre}' marcada como disparo")
                self.load_data()  # Recargar datos
            else:
                messagebox.showerror("Error", response.get('message', 'Error al marcar como disparo'))
                
        except Exception as e:
            messagebox.showerror("Error", f"Error al marcar como disparo: {str(e)}")
    
    def cambiar_orden(self):
        """Cambia el orden de una consulta"""
        selection = self.asociadas_tree.selection()
        if not selection:
            messagebox.showwarning("Advertencia", "Selecciona una consulta para cambiar el orden")
            return
        
        item = self.asociadas_tree.item(selection[0])
        values = item['values']
        consulta_nombre = values[1]
        orden_actual = values[2]
        
        # Solicitar nuevo orden
        from tkinter import simpledialog
        nuevo_orden = simpledialog.askinteger(
            "Cambiar Orden", 
            f"Orden actual de '{consulta_nombre}': {orden_actual}\\nIngresa el nuevo orden:",
            minvalue=1,
            maxvalue=99
        )
        
        if nuevo_orden is not None:
            # TODO: Implementar cambio de orden
            messagebox.showinfo("Pendiente", f"Funcionalidad de cambio de orden pendiente de implementar\\nNuevo orden: {nuevo_orden}")
    
    def nueva_consulta(self):
        """Crea una nueva consulta"""
        from .consulta_dialogs import CreateConsultaDialog
        
        dialog = CreateConsultaDialog(
            self.dialog,
            self.consulta_ctrl,
            None,  # conexion_ctrl
            None   # control_ctrl  
        )
        
        # Esperar a que se cierre el diálogo
        self.dialog.wait_window(dialog.dialog)
        
        # Si se creó exitosamente, recargar datos
        if dialog.result:
            self.load_data()
    
    def close(self):
        """Cierra el diálogo"""
        self.dialog.destroy()