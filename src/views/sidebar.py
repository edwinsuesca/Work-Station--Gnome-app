import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import json
import os

class Sidebar(Gtk.Box):
    def __init__(self, data_manager, on_project_selected, on_add_project):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.set_size_request(220, -1)
        self.data_manager = data_manager
        self.on_project_selected = on_project_selected
        self.on_add_project = on_add_project
        
        # Sección del logo
        logo_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=0)
        logo_box.set_margin_top(12)
        logo_box.set_margin_bottom(12)
        logo_box.set_margin_start(12)
        logo_box.set_margin_end(12)
        
        # TODO: Agregar el logo de la aplicación aquí
        # Mostrar el logo real
        logo_path = os.path.join(os.path.dirname(__file__), '../assets/logo.svg')
        logo_img = Gtk.Image.new_from_file(logo_path)
        logo_img.set_pixel_size(64)
        #logo_box.set_size_request(70, 14)
        logo_box.pack_start(logo_img, False, False, 0)
        
        self.pack_start(logo_box, False, False, 0)
        
        # Separador
        separator = Gtk.Separator(orientation=Gtk.Orientation.HORIZONTAL)
        self.pack_start(separator, False, False, 0)
        
        # Título de la sidebar
        title_label = Gtk.Label(label="Proyectos")
        title_label.set_margin_top(6)
        title_label.set_margin_bottom(6)
        title_label.set_margin_start(12)
        title_label.set_margin_end(12)
        
        # Aplicar negrita al título usando CSS
        title_label.get_style_context().add_class('bold-title')
        
        self.pack_start(title_label, False, False, 0)
        
        # Lista de proyectos
        self.projects_list = Gtk.ListBox()
        self.projects_list.connect('row-selected', self.on_project_selected)
        self.projects_list.set_margin_start(6)
        self.projects_list.set_margin_end(6)
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
            if row:
                # Seleccionar la fila
                self.projects_list.select_row(row)
                
                # Crear el menú contextual
                menu = Gtk.Menu()
                
                # Opción de renombrar
                rename_item = Gtk.MenuItem(label="Renombrar")
                rename_item.connect('activate', self.on_rename_project, row)
                menu.append(rename_item)
                
                # Separador
                separator = Gtk.SeparatorMenuItem()
                menu.append(separator)
                
                # Opción de eliminar
                delete_item = Gtk.MenuItem(label="Eliminar")
                delete_item.connect('activate', self.on_delete_project, row)
                menu.append(delete_item)
                
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
        dialog.format_secondary_text("Esta acción no se puede deshacer.")
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('destructive-action')
        
        # Ejecutar el diálogo
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            # Eliminar el proyecto
            self.data_manager.get_projects().pop(row.get_index())
            self.data_manager._save_data()
            self.refresh_projects()
        
        dialog.destroy()
    
    def on_rename_project(self, menu_item, row):
        # Obtener el proyecto seleccionado
        project = self.data_manager.get_projects()[row.get_index()]
        
        # Crear el diálogo de edición
        dialog = Gtk.Dialog(title="Renombrar Proyecto", transient_for=self.get_toplevel(), flags=0)
        dialog.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')
        
        # Establecer un tamaño mínimo para el diálogo
        dialog.set_default_size(600, 100)
        
        # Contenedor principal
        box = dialog.get_content_area()
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        
        # Contenedor para el nombre
        name_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(name_box, True, True, 0)
        
        # Entrada de nombre
        name_entry = Gtk.Entry()
        name_entry.set_placeholder_text("Nombre del proyecto")
        name_entry.set_text(project['name'])
        name_entry.set_hexpand(True)
        name_box.pack_start(name_entry, True, True, 0)
        
        # Mostrar el diálogo
        dialog.show_all()
        
        # Establecer el foco en el campo de nombre
        name_entry.grab_focus()
        
        # Ejecutar el diálogo
        response = dialog.run()
        
        if response == Gtk.ResponseType.OK:
            new_name = name_entry.get_text()
            if new_name:
                # Actualizar el proyecto
                project['name'] = new_name
                self.data_manager._save_data()
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