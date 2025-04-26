#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gio, GLib, Pango, Gdk
from data_manager import DataManager
from dialogs import ProjectDialog, NoteDialog, TaskDialog

class WorkStationApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.workstation.app',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.data_manager = DataManager()
        self.current_project = None
        
        # Cargar el CSS
        self.load_css()

    def load_css(self):
        css = """
        .task-row {
            padding: 5px 0;
            border-bottom: 1px solid rgba(141, 141, 141, 0.2);
        }
        .selected {
            background-color: rgba(141, 141, 141, 0.2);
            color: @theme_fg_color;
        }
        .task-description {
            color: rgba(141, 141, 141, 0.8);
            font-size: 0.9em;
            margin-top: 4px;
        }
        button.suggested-action {
            background-color: @theme_selected_bg_color;
            color: @theme_selected_fg_color;
        }
        button.suggested-action:hover {
            background-color: shade(@theme_selected_bg_color, 1.1);
        }
        /* Quitar el reborde de foco */
        list row:focus {
            box-shadow: none;
            outline: none;
        }
        /* Estilos para los íconos de navegación */
        .clickable {
            opacity: 0.7;
            transition: opacity 0.2s ease-in-out;
        }
        .clickable:hover {
            opacity: 1;
        }
        """
        css_provider = Gtk.CssProvider()
        css_provider.load_from_data(css.encode())
        Gtk.StyleContext.add_provider_for_screen(
            Gdk.Screen.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
        )

    def on_activate(self, app):
        # Crear la ventana principal
        self.win = Gtk.ApplicationWindow(application=app,
                                       title="Work Station")
        self.win.set_default_size(1200, 768)
        
        # Crear el layout principal con paned
        self.main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.win.add(self.main_paned)
        
        # Crear la sidebar
        self.setup_sidebar()
        
        # Crear el contenido principal
        self.setup_main_content()
        
        # Cargar el último proyecto seleccionado o el primero
        self.load_last_project()
        
        self.win.show_all()

    def setup_sidebar(self):
        # Contenedor de la sidebar
        sidebar_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        sidebar_box.set_size_request(220, -1)
        
        # Título de la sidebar
        title_label = Gtk.Label(label="Proyectos")
        title_label.set_margin_top(6)
        title_label.set_margin_bottom(6)
        title_label.set_margin_start(12)
        title_label.set_margin_end(12)
        
        # Aplicar negrita al título usando CSS
        title_label.get_style_context().add_class('bold-title')
        
        sidebar_box.pack_start(title_label, False, False, 0)
        
        # Separador
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        sidebar_box.pack_start(separator, False, False, 0)
        
        # Lista de proyectos
        self.projects_list = Gtk.ListBox()
        self.projects_list.connect('row-selected', self.on_project_selected)
        self.projects_list.set_margin_start(6)
        self.projects_list.set_margin_end(6)
        sidebar_box.pack_start(self.projects_list, True, True, 0)
        
        # Botón para añadir proyecto
        add_project_btn = Gtk.Button(label="Añadir Proyecto")
        add_project_btn.connect('clicked', self.on_add_project)
        add_project_btn.set_margin_start(6)
        add_project_btn.set_margin_end(6)
        add_project_btn.set_margin_bottom(6)
        sidebar_box.pack_start(add_project_btn, False, False, 0)
        
        # Añadir la sidebar al paned
        self.main_paned.pack1(sidebar_box, False, False)

    def setup_main_content(self):
        # Contenedor principal
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        # Notebook para las diferentes secciones
        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_start(6)
        self.notebook.set_margin_end(6)
        self.notebook.set_margin_bottom(6)
        
        # Añadir las pestañas principales (Tareas primero)
        self.setup_tasks_tab()
        self.setup_notes_tab()
        
        self.main_box.pack_start(self.notebook, True, True, 0)
        
        # Añadir el contenido principal al paned
        self.main_paned.pack2(self.main_box, True, True)

    def setup_tasks_tab(self):
        tasks_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=0)
        self.notebook.append_page(tasks_box, Gtk.Label(label="Tareas"))
        
        # Columnas del Kanban
        self.task_lists = {}
        columns = ["Por Hacer", "En Progreso", "Completado"]
        
        for i, column in enumerate(columns):
            # Contenedor de columna
            column_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
            column_box.set_size_request(300, -1)
            
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
            column_box.pack_start(add_task_btn, False, False, 0)
            
            tasks_box.pack_start(column_box, True, True, 0)
            
            # Añadir separador entre columnas
            if i < len(columns) - 1:
                separator = Gtk.Separator(orientation=Gtk.Orientation.VERTICAL)
                tasks_box.pack_start(separator, False, False, 0)

    def setup_notes_tab(self):
        notes_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.notebook.append_page(notes_box, Gtk.Label(label="Notas"))
        
        # Lista de notas
        self.notes_list = Gtk.ListBox()
        self.notes_list.connect('row-activated', self.on_note_activated)
        notes_box.pack_start(self.notes_list, True, True, 0)
        
        # Botón para añadir nota
        add_note_btn = Gtk.Button(label="Añadir Nota")
        add_note_btn.connect('clicked', self.on_add_note)
        add_note_btn.set_margin_start(6)
        add_note_btn.set_margin_end(6)
        add_note_btn.set_margin_bottom(6)
        notes_box.pack_start(add_note_btn, False, False, 0)
        
        # Cargar notas existentes
        self.refresh_notes()

    def load_last_project(self):
        # Cargar proyectos
        self.refresh_projects()
        
        # Intentar cargar el último proyecto seleccionado
        if self.data_manager.get_projects():
            self.current_project = self.data_manager.get_projects()[0]
            self.refresh_notes()
            self.refresh_tasks()

    def refresh_projects(self):
        # Limpiar lista actual
        for child in self.projects_list.get_children():
            self.projects_list.remove(child)
        
        # Añadir proyectos
        for project in self.data_manager.get_projects():
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.set_margin_start(12)
            box.set_margin_end(12)
            row.get_style_context().add_class('task-row')
            row.add(box)
            
            name_label = Gtk.Label(label=project['name'])
            name_label.set_xalign(0)
            box.pack_start(name_label, False, False, 0)
            
            if project['description']:
                desc_label = Gtk.Label(label=project['description'])
                desc_label.set_xalign(0)
                box.pack_start(desc_label, False, False, 0)
            
            self.projects_list.add(row)
        
        self.projects_list.show_all()
        
        # Seleccionar el primer proyecto por defecto
        if self.projects_list.get_children():
            first_row = self.projects_list.get_row_at_index(0)
            self.projects_list.select_row(first_row)
            first_row.get_style_context().add_class('selected')
            project_id = self.data_manager.get_projects()[0]['id']
            self.current_project = self.data_manager.get_project(project_id)
            self.refresh_notes()
            self.refresh_tasks()

    def refresh_notes(self):
        # Limpiar lista actual
        for child in self.notes_list.get_children():
            self.notes_list.remove(child)
        
        # Añadir notas
        project_id = self.current_project['id'] if self.current_project else None
        for note in self.data_manager.get_notes(project_id):
            row = Gtk.ListBoxRow()
            box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
            box.set_margin_start(12)
            box.set_margin_end(12)
            row.get_style_context().add_class('task-row')
            row.add(box)
            
            title_label = Gtk.Label(label=note['title'])
            title_label.set_xalign(0)
            box.pack_start(title_label, False, False, 0)
            
            if note['content']:
                content_label = Gtk.Label(label=note['content'])
                content_label.set_xalign(0)
                box.pack_start(content_label, False, False, 0)
            
            row.note_id = note['id']
            self.notes_list.add(row)
        
        self.notes_list.show_all()
        
        # Seleccionar la primera nota por defecto
        if self.notes_list.get_children():
            first_row = self.notes_list.get_row_at_index(0)
            self.notes_list.select_row(first_row)
            first_row.get_style_context().add_class('selected')

    def refresh_tasks(self):
        # Limpiar todas las listas
        for task_list in self.task_lists.values():
            for child in task_list.get_children():
                task_list.remove(child)
        
        # Añadir tareas a sus respectivas columnas
        project_id = self.current_project['id'] if self.current_project else None
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
                right_arrow.connect('button-press-event', self.on_move_task_right, task['id'])
                
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
            self.refresh_tasks()
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
            self.refresh_tasks()
        return True

    def on_project_selected(self, listbox, row):
        if row:
            # Remover la clase selected de todas las filas
            for child in self.projects_list.get_children():
                child.get_style_context().remove_class('selected')
            
            # Aplicar la clase selected a la fila seleccionada
            row.get_style_context().add_class('selected')
            
            project_id = self.data_manager.get_projects()[row.get_index()]['id']
            self.current_project = self.data_manager.get_project(project_id)
            self.refresh_notes()
            self.refresh_tasks()

    def on_note_activated(self, listbox, row):
        if row:
            note_id = row.note_id
            note = next((n for n in self.data_manager.get_notes() if n['id'] == note_id), None)

            # Remover la clase selected de todas las filas
            for child in self.notes_list.get_children():
                child.get_style_context().remove_class('selected')
            
            # Aplicar la clase selected a la fila seleccionada
            row.get_style_context().add_class('selected')

            if note:
                dialog = NoteDialog(self.win, note)
                response = dialog.run()
                
                if response == Gtk.ResponseType.OK:
                    title, content = dialog.get_note_data()
                    if title:
                        self.data_manager.update_note(note_id, title, content)
                        self.refresh_notes()
                
                dialog.destroy()

    def on_task_activated(self, listbox, row):
        if row:
            task_id = row.task_id
            task = next((t for t in self.data_manager.get_tasks() if t['id'] == task_id), None)

            # Remover la clase selected y deseleccionar todas las filas en todas las listas
            for task_list in self.task_lists.values():
                task_list.unselect_all()
                for child in task_list.get_children():
                    child.get_style_context().remove_class('selected')
            
            # Aplicar la clase selected a la fila seleccionada
            row.get_style_context().add_class('selected')

            if task:
                dialog = TaskDialog(self.win, task)
                response = dialog.run()
                
                if response == Gtk.ResponseType.OK:
                    title, description, status = dialog.get_task_data()
                    if title:
                        self.data_manager.update_task_status(task_id, status)
                        self.refresh_tasks()
                
                dialog.destroy()

    def on_add_project(self, button):
        dialog = ProjectDialog(self.win)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            name, description = dialog.get_project_data()
            if name:
                self.data_manager.add_project(name, description)
                self.refresh_projects()
        
        dialog.destroy()

    def on_add_note(self, button):
        if not self.current_project:
            dialog = Gtk.MessageDialog(
                transient_for=self.win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Selecciona un proyecto primero"
            )
            dialog.run()
            dialog.destroy()
            return

        dialog = NoteDialog(self.win)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            title, content = dialog.get_note_data()
            if title:
                self.data_manager.add_note(title, content, self.current_project['id'])
                self.refresh_notes()
        
        dialog.destroy()

    def on_add_task(self, button):
        if not self.current_project:
            dialog = Gtk.MessageDialog(
                transient_for=self.win,
                flags=0,
                message_type=Gtk.MessageType.INFO,
                buttons=Gtk.ButtonsType.OK,
                text="Selecciona un proyecto primero"
            )
            dialog.run()
            dialog.destroy()
            return

        # Obtener el estado de la columna donde se hizo clic
        status = "Por Hacer"  # Estado por defecto
        
        # Buscar la columna que contiene el botón
        for column_status, task_list in self.task_lists.items():
            if task_list.get_parent().get_parent() == button.get_parent().get_parent():
                status = column_status
                break

        dialog = TaskDialog(self.win, status=status)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            title, description, status = dialog.get_task_data()
            if title:
                self.data_manager.add_task(title, description, status, self.current_project['id'])
                self.refresh_tasks()
        
        dialog.destroy()

if __name__ == '__main__':
    app = WorkStationApp()
    app.run(None) 