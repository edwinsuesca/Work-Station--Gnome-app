import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Pango

class Kanban(Gtk.Box):
    def __init__(self, data_manager, on_task_activated, on_add_task):
        super().__init__(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.data_manager = data_manager
        self.on_task_activated = on_task_activated
        self.on_add_task = on_add_task
        
        # Columnas del Kanban
        self.task_lists = {}
        columns = ["Por Hacer", "En Progreso", "Completado"]
        
        for i, column in enumerate(columns):
            # Contenedor de columna
            column_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            column_box.set_size_request(300, -1)
            column_box.column_status = column  # Agregar el estado como propiedad
            
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
            
            # Añadir separador entre columnas
            if i < len(columns) - 1:
                separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                self.pack_start(separator, False, False, 0)
        
        self.show_all()
    
    def refresh_tasks(self, project_id):
        # Limpiar todas las listas
        for task_list in self.task_lists.values():
            for child in task_list.get_children():
                task_list.remove(child)
        
        # Añadir tareas a sus respectivas columnas
        for task in self.data_manager.get_tasks(project_id):
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
            box.set_margin_start(12)
            box.set_margin_end(12)
            row.get_style_context().add_class('task-row')
            row.add(box)
            
            # Contenedor para el contenido de la tarea
            content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            content_box.set_hexpand(True)
            box.pack_start(content_box, True, True, 0)
            
            title_label = Gtk.Label(label=task['title'])
            title_label.set_xalign(0)
            content_box.pack_start(title_label, False, False, 0)
            
            if task['description']:
                # Limitar la descripción a 100 caracteres
                description = task['description']
                if len(description) > 100:
                    description = description[:97] + "..."
                
                desc_label = Gtk.Label(label=description)
                desc_label.set_xalign(0)
                desc_label.get_style_context().add_class('task-description')
                desc_label.set_line_wrap(True)
                desc_label.set_line_wrap_mode(Pango.WrapMode.WORD_CHAR)
                content_box.pack_start(desc_label, False, False, 0)
            
            row.task_id = task['id']
            
            # Asegurarse de que la tarea tenga un estado válido
            status = task.get('status', 'Por Hacer')
            if status not in self.task_lists:
                status = 'Por Hacer'
            
            # Agregar íconos según la columna
            if status == 'Por Hacer':
                # Ícono para mover a la derecha
                right_arrow = Gtk.Image.new_from_icon_name('go-next-symbolic', Gtk.IconSize.BUTTON)
                right_arrow.set_margin_start(6)
                right_arrow.set_margin_end(6)
                right_arrow.set_valign(Gtk.Align.CENTER)
                right_arrow.set_halign(Gtk.Align.END)
                right_arrow.get_style_context().add_class('clickable')
                
                # Crear un contenedor para el ícono que capture los eventos
                right_arrow_box = Gtk.EventBox()
                right_arrow_box.add(right_arrow)
                right_arrow_box.connect('button-press-event', self.on_move_task_right, task['id'])
                box.pack_start(right_arrow_box, False, False, 0)
                
            elif status == 'En Progreso':
                # Ícono para mover a la izquierda
                left_arrow = Gtk.Image.new_from_icon_name('go-previous-symbolic', Gtk.IconSize.BUTTON)
                left_arrow.set_margin_start(6)
                left_arrow.set_margin_end(6)
                left_arrow.set_valign(Gtk.Align.CENTER)
                left_arrow.set_halign(Gtk.Align.START)
                left_arrow.get_style_context().add_class('clickable')
                
                # Crear un contenedor para el ícono que capture los eventos
                left_arrow_box = Gtk.EventBox()
                left_arrow_box.add(left_arrow)
                left_arrow_box.connect('button-press-event', self.on_move_task_left, task['id'])
                box.pack_start(left_arrow_box, False, False, 0)
                
                # Ícono para mover a la derecha
                right_arrow = Gtk.Image.new_from_icon_name('go-next-symbolic', Gtk.IconSize.BUTTON)
                right_arrow.set_margin_start(6)
                right_arrow.set_margin_end(6)
                right_arrow.set_valign(Gtk.Align.CENTER)
                right_arrow.set_halign(Gtk.Align.END)
                right_arrow.get_style_context().add_class('clickable')
                
                # Crear un contenedor para el ícono que capture los eventos
                right_arrow_box = Gtk.EventBox()
                right_arrow_box.add(right_arrow)
                right_arrow_box.connect('button-press-event', self.on_move_task_right, task['id'])
                box.pack_start(right_arrow_box, False, False, 0)
                
            elif status == 'Completado':
                # Ícono para mover a la izquierda
                left_arrow = Gtk.Image.new_from_icon_name('go-previous-symbolic', Gtk.IconSize.BUTTON)
                left_arrow.set_margin_start(6)
                left_arrow.set_margin_end(6)
                left_arrow.set_valign(Gtk.Align.CENTER)
                left_arrow.set_halign(Gtk.Align.END)
                left_arrow.get_style_context().add_class('clickable')
                
                # Crear un contenedor para el ícono que capture los eventos
                left_arrow_box = Gtk.EventBox()
                left_arrow_box.add(left_arrow)
                left_arrow_box.connect('button-press-event', self.on_move_task_left, task['id'])
                box.pack_start(left_arrow_box, False, False, 0)
            
            self.task_lists[status].add(row)
        
        # Mostrar todas las listas
        for task_list in self.task_lists.values():
            task_list.show_all()
            
        # Seleccionar la primera tarea por defecto
        for task_list in self.task_lists.values():
            if task_list.get_children():
                first_row = task_list.get_row_at_index(0)
                task_list.select_row(first_row)
                first_row.get_style_context().add_class('selected')
                break
    
    def on_move_task_left(self, widget, event, task_id):
        task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)
        if task:
            current_status = task.get('status', 'Por Hacer')
            if current_status == 'En Progreso':
                new_status = 'Por Hacer'
            elif current_status == 'Completado':
                new_status = 'En Progreso'
            else:
                return
            
            self.data_manager.update_task_status(task_id, new_status)
            self.refresh_tasks(task['project_id'])
        return True

    def on_move_task_right(self, widget, event, task_id):
        task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)
        if task:
            current_status = task.get('status', 'Por Hacer')
            if current_status == 'Por Hacer':
                new_status = 'En Progreso'
            elif current_status == 'En Progreso':
                new_status = 'Completado'
            else:
                return
            
            self.data_manager.update_task_status(task_id, new_status)
            self.refresh_tasks(task['project_id'])
        return True 