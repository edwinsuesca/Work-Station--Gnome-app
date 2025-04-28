#!/usr/bin/env python3

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gio

from data_manager import DataManager
from dialogs.dialogs import ProjectDialog, NoteDialog, TaskDialog
from views.sidebar import Sidebar
from views.kanban import Kanban
from views.notes import NotesView
from utils.styles import load_styles

class WorkStationApp(Gtk.Application):
    def __init__(self):
        super().__init__(application_id='com.workstation.app',
                        flags=Gio.ApplicationFlags.FLAGS_NONE)
        self.connect('activate', self.on_activate)
        self.data_manager = DataManager()
        self.current_project = None
        
        # Cargar los estilos
        load_styles()

    def on_activate(self, app):
        # Crear la ventana principal
        self.win = Gtk.ApplicationWindow(application=app,
                                       title="Work Station")
        self.win.set_default_size(1400, 768)
        
        # Crear el layout principal con paned
        self.main_paned = Gtk.Paned(orientation=Gtk.Orientation.HORIZONTAL)
        self.win.add(self.main_paned)
        
        # Crear la sidebar
        self.sidebar = Sidebar(
            self.data_manager,
            self.on_project_selected,
            self.on_add_project
        )
        self.main_paned.pack1(self.sidebar, False, False)
        
        # Crear el contenido principal
        self.setup_main_content()
        
        # Cargar el último proyecto seleccionado o el primero
        self.load_last_project()
        
        self.win.show_all()

    def setup_main_content(self):
        # Contenedor principal
        self.main_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        
        # Crear ScrolledWindow para permitir scroll en ambas direcciones
        scrolled_window = Gtk.ScrolledWindow()
        scrolled_window.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        
        # Notebook para las diferentes secciones
        self.notebook = Gtk.Notebook()
        self.notebook.set_margin_start(6)
        self.notebook.set_margin_end(6)
        self.notebook.set_margin_bottom(6)
        
        # Añadir las pestañas principales
        self.setup_tasks_tab()
        self.setup_notes_tab()
        
        # Crear un contenedor intermedio para el notebook
        container = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        container.pack_start(self.notebook, True, True, 0)
        
        # Agregar el contenedor al ScrolledWindow
        scrolled_window.add(container)
        
        # Añadir el ScrolledWindow al main_box
        self.main_box.pack_start(scrolled_window, True, True, 0)
        
        # Añadir el contenido principal al paned
        self.main_paned.pack2(self.main_box, True, True)

    def setup_tasks_tab(self):
        self.kanban = Kanban(
            self.data_manager,
            self.on_task_activated,
            self.on_add_task
        )
        self.notebook.append_page(self.kanban, Gtk.Label(label="Tareas"))

    def setup_notes_tab(self):
        self.notes_view = NotesView(
            self.data_manager,
            self.on_note_activated,
            self.on_add_note
        )
        self.notebook.append_page(self.notes_view, Gtk.Label(label="Notas"))

    def load_last_project(self):
        # Cargar proyectos
        self.sidebar.refresh_projects()
        
        # Intentar cargar el último proyecto seleccionado
        if self.data_manager.get_projects():
            self.current_project = self.data_manager.get_projects()[0]
            self.refresh_notes()
            self.refresh_tasks()

    def refresh_notes(self):
        if self.current_project:
            self.notes_view.refresh_notes(self.current_project['id'])

    def refresh_tasks(self):
        if self.current_project:
            self.kanban.refresh_tasks(self.current_project['id'])

    def on_project_selected(self, listbox, row):
        if row:
            # Remover la clase selected de todas las filas
            for child in self.sidebar.projects_list.get_children():
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
            for child in self.notes_view.notes_list.get_children():
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
            for task_list in self.kanban.task_lists.values():
                task_list.unselect_all()
                for child in task_list.get_children():
                    child.get_style_context().remove_class('selected')
            
            # Aplicar la clase selected a la fila seleccionada
            row.get_style_context().add_class('selected')

            if task:
                dialog = TaskDialog(self.win, task)
                response = dialog.run()
                
                if response == Gtk.ResponseType.OK:
                    title, description = dialog.get_task_data()
                    if title:
                        self.data_manager.update_task(task_id, title, description)
                        self.refresh_tasks()
                
                dialog.destroy()

    def on_add_project(self, button):
        dialog = ProjectDialog(self.win)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            name, color = dialog.get_project_data()
            if name:
                self.data_manager.add_project(name, color)
                self.sidebar.refresh_projects()
        
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

        # Obtener el estado directamente del botón
        status = button.column_status

        dialog = TaskDialog(self.win)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            title, description = dialog.get_task_data()
            if title:
                self.data_manager.add_task(title, description, status, self.current_project['id'])
                self.refresh_tasks()
        
        dialog.destroy()

if __name__ == '__main__':
    app = WorkStationApp()
    app.run(None) 