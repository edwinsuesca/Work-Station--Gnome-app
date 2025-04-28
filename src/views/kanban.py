import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class Kanban(Gtk.Box):
    def __init__(self, data_manager, on_task_activated, on_add_task):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.data_manager = data_manager
        self.set_homogeneous(True)
        self.on_task_activated = on_task_activated
        self.on_add_task = on_add_task
        
        # Columnas del Kanban
        self.task_lists = {}
        columns = ["Por Hacer", "En Progreso", "Completado"]
        
        for i, column in enumerate(columns):
            # Contenedor de columna
            column_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            column_box.set_hexpand(True)
            #column_box.set_size_request(300, -1)
            column_box.column_status = column  # Agregar el estado como propiedad
            column_box.get_style_context().add_class('kanban-column')
            
            # Header de la columna
            header_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            header_box.set_margin_start(6)
            header_box.set_margin_end(6)
            header_box.set_margin_top(6)
            header_box.set_margin_bottom(6)
            
            # Título de la columna
            title_label = Gtk.Label(label=column)
            title_label.set_xalign(0.5)  # Centrar el título
            title_label.set_margin_bottom(12)  # Espacio entre el título y la línea
            
            # Aplicar negrita al título usando CSS en lugar de override_font
            title_label.get_style_context().add_class('bold-title')
            
            header_box.pack_start(title_label, False, False, 0)
            
            # Separador del header
            header_separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
            header_box.pack_start(header_separator, False, False, 0)
            
            column_box.pack_start(header_box, False, False, 0)
            
            # Lista de tareas
            task_list = Gtk.ListBox()
            task_list.connect('row-activated', self.on_task_activated)
            task_list.set_margin_start(6)
            task_list.set_margin_end(6)
            task_list.set_margin_bottom(6)
            self.task_lists[column] = task_list
            column_box.pack_start(task_list, True, True, 0)
            
            # Botón para añadir tarea
            add_task_btn = Gtk.Button(label="Añadir Tarea")
            add_task_btn.connect('clicked', self.on_add_task)
            add_task_btn.set_margin_start(6)
            add_task_btn.set_margin_end(6)
            add_task_btn.set_margin_bottom(6)
            add_task_btn.column_status = column  # Agregar el estado como propiedad
            column_box.pack_start(add_task_btn, False, False, 0)
            
            self.pack_start(column_box, True, True, 0)
        
        # Conectar el evento de clic derecho para todas las listas de tareas
        for task_list in self.task_lists.values():
            task_list.connect('button-press-event', self.on_button_press)
        
        
        self.show_all()
    
    def on_button_press(self, widget, event):
        if event.button == 3:  # Clic derecho
            # Obtener la fila bajo el cursor
            row = widget.get_row_at_y(event.y)
            if row:
                # No seleccionar la fila automáticamente
                widget.select_row(row)

                # Remover la clase selected y deseleccionar todas las filas en todas las listas
                for task_list in self.task_lists.values():
                    task_list.unselect_all()
                    for child in task_list.get_children():
                        child.get_style_context().remove_class('selected')
                
                # Aplicar la clase selected a la fila seleccionada
                row.get_style_context().add_class('selected')
                
                # Crear el menú contextual
                menu = Gtk.Menu()
                
                # Submenú para cambiar estado
                status_menu = Gtk.Menu()
                status_item = Gtk.MenuItem(label="Cambiar Estado")
                status_item.set_submenu(status_menu)
                
                # Obtener el estado actual de la tarea
                task_id = row.task_id
                task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)
                
                if task:  # Solo si la tarea existe
                    current_status = task.get('status', 'Por Hacer')
                    
                    # Añadir opciones de estado
                    for status in ["Por Hacer", "En Progreso", "Completado"]:
                        if status != current_status:
                            status_option = Gtk.MenuItem(label=status)
                            status_option.connect('activate', self.on_change_status, task_id, status)
                            status_menu.append(status_option)
                    
                    menu.append(status_item)
                    
                    # Separador
                    menu.append(Gtk.SeparatorMenuItem())
                
                # Opción de eliminar
                delete_item = Gtk.MenuItem(label="Eliminar")
                delete_item.connect('activate', self.on_delete_task, row)
                menu.append(delete_item)
                
                # Mostrar el menú
                menu.show_all()
                menu.popup(None, None, None, None, event.button, event.time)
                return True
        return False
    
    def on_change_status(self, menu_item, task_id, new_status):
        task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)
        if task:
            self.data_manager.update_task_status(task_id, new_status)
            self.refresh_tasks(task['project_id'], selected_task_id=task_id)
    
    def on_delete_task(self, menu_item, row):
        # Obtener la tarea seleccionada
        task_id = row.task_id
        task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)
        
        if task:
            # Crear diálogo de confirmación
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK_CANCEL,
                text=f"¿Estás seguro de eliminar la tarea '{task['title']}'?"
            )
            dialog.format_secondary_text("Esta acción no se puede deshacer.")
            
            # Hacer que el botón OK sea el botón de acento
            ok_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
            ok_button.get_style_context().add_class('destructive-action')
            
            # Ejecutar el diálogo
            response = dialog.run()
            
            if response == Gtk.ResponseType.OK:
                # Eliminar la tarea
                self.data_manager.delete_task(task_id)
                self.refresh_tasks(task['project_id'])
            
            dialog.destroy()
    
    def refresh_tasks(self, project_id, selected_task_id=None):
        # Limpiar todas las listas
        for task_list in self.task_lists.values():
            for child in task_list.get_children():
                task_list.remove(child)
        
        # Obtener el color del proyecto
        project = self.data_manager.get_project(project_id)
        project_color = project.get('color', 'rgb(245, 39, 39)')
        
        # Añadir tareas a sus respectivas columnas
        for task in self.data_manager.get_tasks(project_id):
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.set_margin_start(12)
            box.set_margin_end(12)
            row.get_style_context().add_class('item')
            row.add(box)
            
            # Aplicar el color del proyecto como borde izquierdo
            provider = Gtk.CssProvider()
            provider.load_from_data(f'.item {{ border-left: 7px solid {project_color}; }}'.encode())
            row.get_style_context().add_provider(
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            
            # Contenedor para el contenido de la tarea
            content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            content_box.set_hexpand(True)
            box.pack_start(content_box, True, True, 0)
            
            if task['title']:
                # Limitar la descripción a 100 caracteres
                title = task['title']
                if len(title) > 80:
                    title = title[:77] + "..."
                
                title_label = Gtk.Label(label=title)
                title_label.set_xalign(0)
                title_label.set_line_wrap(True)
                title_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                content_box.pack_start(title_label, False, False, 0)
            
            if task['description']:
                # Limitar la descripción a 100 caracteres
                description = task['description']
                if len(description) > 80:
                    description = description[:77] + "..."
                
                title_label = Gtk.Label(label=description)
                title_label.set_xalign(0)
                title_label.get_style_context().add_class('task-description')
                title_label.set_line_wrap(True)
                title_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                content_box.pack_start(title_label, False, False, 0)
            
            # Contenedor para las fechas
            dates_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            dates_box.set_margin_top(6)
            box.pack_start(dates_box, False, False, 0)
            
            # Fecha de creación
            created_at = task.get('created_at', 'No disponible')
            created_label = Gtk.Label(label=f"Creada: {created_at}")
            created_label.set_xalign(0)
            created_label.get_style_context().add_class('task-description')
            dates_box.pack_start(created_label, False, False, 0)
            
            # Fecha de actualización si existe
            updated_at = task.get('updated_at')
            if updated_at:
                updated_label = Gtk.Label(label=f"Actualizada: {updated_at}")
                updated_label.set_xalign(0)
                updated_label.get_style_context().add_class('task-description')
                dates_box.pack_start(updated_label, False, False, 0)
            
            row.task_id = task['id']
            
            # Asegurarse de que la tarea tenga un estado válido
            status = task.get('status', 'Por Hacer')
            if status not in self.task_lists:
                status = 'Por Hacer'
            
            self.task_lists[status].add(row)
        
        # Mostrar todas las listas
        for task_list in self.task_lists.values():
            task_list.show_all()
        
        # Seleccionar la tarea movida si corresponde
        if selected_task_id is not None:
            for task_list in self.task_lists.values():
                for row in task_list.get_children():
                    if hasattr(row, 'task_id') and row.task_id == selected_task_id:
                        task_list.select_row(row)
                        row.get_style_context().add_class('selected')
                        return
        # Si no, seleccionar la primera tarea por defecto
        for task_list in self.task_lists.values():
            if task_list.get_children():
                first_row = task_list.get_row_at_index(0)
                task_list.select_row(first_row)
                first_row.get_style_context().add_class('selected')
                break 