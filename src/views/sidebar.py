import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import json
import os
from dialogs.dialogs import ProjectDialog

class Sidebar(Gtk.Box):
    def __init__(self, data_manager, on_project_selected, on_add_project):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        self.set_size_request(220, -1)
        self.get_style_context().add_class('sidebar')
        self.data_manager = data_manager
        self.on_project_selected = on_project_selected
        self.on_add_project = on_add_project
        
        # Sección del logo
        logo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        logo_box.set_margin_top(12)
        logo_box.set_margin_bottom(12)
        logo_box.set_margin_start(12)
        logo_box.set_margin_end(12)
        
        def get_logo_path():
            # Ruta estándar de instalación global
            system_path = "/usr/local/share/work-station/assets/logo.png"
            # Ruta relativa para desarrollo
            dev_path = os.path.join(os.path.dirname(__file__), '../assets/logo.png')
            if os.path.exists(system_path):
                return system_path
            elif os.path.exists(dev_path):
                return dev_path
            else:
                return None

        logo_path = get_logo_path()
        if logo_path:
            logo_img = Gtk.Image.new_from_file(logo_path)
            logo_box.set_size_request(140, 28)
            logo_box.pack_start(logo_img, False, False, 0)
        else:
            logo_placeholder = Gtk.Label(label="LOGO")
            logo_placeholder.get_style_context().add_class('bold-title')
            logo_box.pack_start(logo_placeholder, False, False, 0)
        
        self.pack_start(logo_box, False, False, 0)
        
        # Separador
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(separator, False, False, 0)
        
        # Título de la sidebar
        title_label = Gtk.Label(label='Proyectos')
        title_label.set_margin_top(3)
        title_label.set_margin_bottom(6)
        title_label.set_margin_start(6)
        title_label.set_margin_end(6)
        
        # Aplicar negrita al título usando CSS
        title_label.get_style_context().add_class('bold-title')
        
        self.pack_start(title_label, False, False, 0)
        
        # Lista de proyectos
        self.projects_list = Gtk.ListBox()
        self.projects_list.connect('row-selected', self.on_project_selected)
        self.pack_start(self.projects_list, True, True, 0)
        
        # Botón para añadir proyecto
        add_project_btn = Gtk.Button(label="Añadir Proyecto")
        add_project_btn.connect('clicked', self.on_add_project)
        add_project_btn.set_margin_start(6)
        add_project_btn.set_margin_end(6)
        add_project_btn.set_margin_bottom(6)
        self.pack_start(add_project_btn, False, False, 0)
        
        # Separador
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(separator, False, False, 0)
        
        # Sección de opciones
        options_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        options_box.set_margin_start(6)
        options_box.set_margin_end(6)
        options_box.set_margin_bottom(6)
        
        # Botón de importar
        import_btn = Gtk.Button(label="Importar")
        import_btn.connect('clicked', self.on_import)
        options_box.pack_start(import_btn, False, False, 0)
        
        # Botón de exportar
        export_btn = Gtk.Button(label="Exportar")
        export_btn.connect('clicked', self.on_export)
        options_box.pack_start(export_btn, False, False, 0)
        
        self.pack_start(options_box, False, False, 0)
        
        # Conectar el evento de clic derecho
        self.projects_list.connect('button-press-event', self.on_button_press)
        
        self.show_all()
    
    def on_import(self, widget):
        # Crear el diálogo de selección de archivo
        dialog = Gtk.FileChooserDialog(
            title="Importar datos",
            transient_for=self.get_toplevel(),
            action=Gtk.FileChooserAction.OPEN
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OPEN, Gtk.ResponseType.OK
        )
        
        # Filtrar por archivos JSON
        filter_json = Gtk.FileFilter()
        filter_json.set_name("Archivos JSON")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)
        
        # Ejecutar el diálogo
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                with open(dialog.get_filename(), 'r') as f:
                    data = json.load(f)
                    self.data_manager.import_data(data)
                    self.refresh_projects()
            except Exception as e:
                # Mostrar mensaje de error
                error_dialog = Gtk.MessageDialog(
                    transient_for=self.get_toplevel(),
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Error al importar datos"
                )
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
        
        dialog.destroy()
    
    def on_export(self, widget):
        # Crear el diálogo de selección de archivo
        dialog = Gtk.FileChooserDialog(
            title="Exportar datos",
            transient_for=self.get_toplevel(),
            action=Gtk.FileChooserAction.SAVE
        )
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_SAVE, Gtk.ResponseType.OK
        )
        
        # Filtrar por archivos JSON
        filter_json = Gtk.FileFilter()
        filter_json.set_name("Archivos JSON")
        filter_json.add_mime_type("application/json")
        dialog.add_filter(filter_json)
        
        # Establecer nombre de archivo por defecto
        dialog.set_current_name("datos_exportados.json")
        
        # Ejecutar el diálogo
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            try:
                data = self.data_manager.export_data()
                with open(dialog.get_filename(), 'w') as f:
                    json.dump(data, f, indent=4)
            except Exception as e:
                # Mostrar mensaje de error
                error_dialog = Gtk.MessageDialog(
                    transient_for=self.get_toplevel(),
                    flags=0,
                    message_type=Gtk.MessageType.ERROR,
                    buttons=Gtk.ButtonsType.OK,
                    text="Error al exportar datos"
                )
                error_dialog.format_secondary_text(str(e))
                error_dialog.run()
                error_dialog.destroy()
        
        dialog.destroy()
    
    def on_button_press(self, widget, event):
        if event.button == 3:  # Clic derecho
            # Obtener la fila bajo el cursor
            row = self.projects_list.get_row_at_y(event.y)
            
            # Crear el menú contextual
            menu = Gtk.Menu()
            
            if row:
                # Si hay una fila bajo el cursor, mostrar opciones para el proyecto
                # Seleccionar la fila
                self.projects_list.select_row(row)
                
                # Remover la clase selected de todas las filas
                for child in self.projects_list.get_children():
                    child.get_style_context().remove_class('selected')
                
                # Aplicar la clase selected a la fila seleccionada
                row.get_style_context().add_class('selected')
                
                # Opción de Editar
                edit_item = Gtk.MenuItem(label="Editar")
                edit_item.connect('activate', self.on_rename_project, row)
                menu.append(edit_item)
                
                # Separador
                separator = Gtk.SeparatorMenuItem()
                menu.append(separator)
                
                # Opción de eliminar
                delete_item = Gtk.MenuItem(label="Eliminar")
                delete_item.connect('activate', self.on_delete_project, row)
                menu.append(delete_item)
            else:
                # Si no hay fila bajo el cursor, mostrar opción de nuevo proyecto
                new_project_item = Gtk.MenuItem(label="Nuevo Proyecto")
                new_project_item.connect('activate', self.on_add_project)
                menu.append(new_project_item)
            
            # Mostrar el menú
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False
    
    def on_delete_project(self, menu_item, row):
        # Obtener el proyecto seleccionado
        project = self.data_manager.get_projects()[row.get_index()]
        
        # Crear diálogo de confirmación
        dialog = Gtk.MessageDialog(
            transient_for=self.get_toplevel(),
            flags=0,
            message_type=Gtk.MessageType.WARNING,
            buttons=Gtk.ButtonsType.OK_CANCEL,
            text=f"¿Estás seguro de eliminar el proyecto '{project['name']}'?"
        )
        dialog.format_secondary_text("Esta acción eliminará el proyecto y todas sus tareas y notas asociadas. No se puede deshacer.")
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('destructive-action')
        
        # Ejecutar el diálogo
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Guardar el índice actual
            current_index = row.get_index()
            
            # Eliminar el proyecto y todos sus elementos asociados
            self.data_manager.delete_project(project['id'])
            
            # Actualizar la lista de proyectos
            self.refresh_projects()
            
            # Obtener la lista actualizada de proyectos
            projects = self.data_manager.get_projects()
            
            if projects:
                # Si hay proyectos, seleccionar el siguiente o el anterior
                if current_index < len(projects):
                    next_row = self.projects_list.get_row_at_index(current_index)
                else:
                    next_row = self.projects_list.get_row_at_index(current_index - 1)
                
                if next_row:
                    self.projects_list.select_row(next_row)
                    self.on_project_selected(self.projects_list, next_row)
            else:
                # Si no hay proyectos, crear uno temporal
                temp_project = self.data_manager.add_project("Proyecto Temporal")
                self.refresh_projects()
                
                # Seleccionar el proyecto temporal
                temp_row = self.projects_list.get_row_at_index(0)
                if temp_row:
                    self.projects_list.select_row(temp_row)
                    self.on_project_selected(self.projects_list, temp_row)
                
                # Eliminar el proyecto temporal
                self.data_manager.delete_project(temp_project['id'])
                self.refresh_projects()
        
        dialog.destroy()
    
    def on_rename_project(self, menu_item, row):
        # Obtener el proyecto seleccionado
        project_id = self.data_manager.get_projects()[row.get_index()]['id']
        project = self.data_manager.get_project(project_id)
        
        # Crear el diálogo de edición
        dialog = ProjectDialog(self.get_toplevel(), project)
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            name, color = dialog.get_project_data()
            if name:
                # Actualizar el proyecto
                self.data_manager.update_project(project['id'], name, color)
                self.refresh_projects()
        
        dialog.destroy()
    
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
            row.get_style_context().add_class('item')
            row.add(box)
            
            # Aplicar el color del proyecto como borde izquierdo
            color = project.get('color', 'rgb(245, 39, 39)')  # Color por defecto si no existe
            provider = Gtk.CssProvider()
            provider.load_from_data(f'.item {{ border-left: 7px solid {color}; }}'.encode())
            row.get_style_context().add_provider(
                provider,
                Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
            )
            
            name_label = Gtk.Label(label=project['name'])
            name_label.set_xalign(0)
            box.pack_start(name_label, False, False, 0)
            
            self.projects_list.add(row)
        
        self.projects_list.show_all()
        
        # Seleccionar el primer proyecto por defecto
        if self.projects_list.get_children():
            first_row = self.projects_list.get_row_at_index(0)
            self.projects_list.select_row(first_row)
            first_row.get_style_context().add_class('selected') 