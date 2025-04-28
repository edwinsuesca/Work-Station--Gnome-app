import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class NotesView(Gtk.Box):
    def __init__(self, data_manager, on_note_activated, on_add_note):
        super().__init__(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        self.data_manager = data_manager
        self.on_note_activated = on_note_activated
        self.on_add_note = on_add_note
        
        # Lista de notas
        self.notes_list = Gtk.ListBox()
        self.notes_list.connect('row-activated', self.on_note_activated)
        self.pack_start(self.notes_list, True, True, 0)
        
        # Botón para añadir nota
        add_note_btn = Gtk.Button(label="Añadir Nota")
        add_note_btn.connect('clicked', self.on_add_note)
        add_note_btn.set_margin_start(6)
        add_note_btn.set_margin_end(6)
        add_note_btn.set_margin_bottom(6)
        self.pack_start(add_note_btn, False, False, 0)
        
        # Conectar el evento de clic derecho
        self.notes_list.connect('button-press-event', self.on_button_press)
        
        self.show_all()
    
    def on_button_press(self, widget, event):
        if event.button == 3:  # Clic derecho
            # Obtener la fila bajo el cursor
            row = widget.get_row_at_y(event.y)
            
            # Crear el menú contextual
            menu = Gtk.Menu()
            
            if row:
                # Seleccionar la fila
                widget.select_row(row)
                
                # Opción de eliminar
                delete_item = Gtk.MenuItem(label="Eliminar")
                delete_item.connect('activate', self.on_delete_note, row)
                menu.append(delete_item)
            else:
                # Opción de crear nota
                new_note_item = Gtk.MenuItem(label="Crear Nota")
                new_note_item.connect('activate', self.on_add_note)
                menu.append(new_note_item)
            
            # Mostrar el menú
            menu.show_all()
            menu.popup(None, None, None, None, event.button, event.time)
            return True
        return False
    
    def on_delete_note(self, menu_item, row):
        # Obtener la nota seleccionada
        note_id = row.note_id
        note = next((n for n in self.data_manager.get_notes() if n['id'] == note_id), None)
        
        if note:
            # Crear diálogo de confirmación
            dialog = Gtk.MessageDialog(
                transient_for=self.get_toplevel(),
                flags=0,
                message_type=Gtk.MessageType.WARNING,
                buttons=Gtk.ButtonsType.OK_CANCEL,
                text=f"¿Estás seguro de eliminar la nota '{note['title']}'?"
            )
            dialog.format_secondary_text("Esta acción no se puede deshacer.")
            
            # Hacer que el botón OK sea el botón de acento
            ok_button = dialog.get_widget_for_response(Gtk.ResponseType.OK)
            ok_button.get_style_context().add_class('destructive-action')
            
            # Ejecutar el diálogo
            response = dialog.run()
            
            if response == Gtk.ResponseType.OK:
                # Eliminar la nota
                self.data_manager.delete_note(note_id)
                self.refresh_notes(note['project_id'])
            
            dialog.destroy()
    
    def refresh_notes(self, project_id):
        # Limpiar lista actual
        for child in self.notes_list.get_children():
            self.notes_list.remove(child)
        
        # Obtener el color del proyecto
        project = self.data_manager.get_project(project_id)
        project_color = project.get('color', 'rgb(245, 39, 39)')
        
        # Añadir notas
        for note in self.data_manager.get_notes(project_id):
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
            
            title_label = Gtk.Label(label=note['title'])
            title_label.set_xalign(0)
            box.pack_start(title_label, False, False, 0)
            
            if note['content']:
                content_label = Gtk.Label(label=note['content'])
                content_label.set_xalign(0)
                box.pack_start(content_label, False, False, 0)
            
            # Contenedor para las fechas
            dates_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=12)
            dates_box.set_margin_top(6)
            box.pack_start(dates_box, False, False, 0)
            
            # Fecha de creación
            created_at = note.get('created_at', 'No disponible')
            created_label = Gtk.Label(label=f"Creada: {created_at}")
            created_label.set_xalign(0)
            created_label.get_style_context().add_class('task-description')
            dates_box.pack_start(created_label, False, False, 0)
            
            # Fecha de actualización si existe
            updated_at = note.get('updated_at')
            if updated_at:
                updated_label = Gtk.Label(label=f"Actualizada: {updated_at}")
                updated_label.set_xalign(0)
                updated_label.get_style_context().add_class('task-description')
                dates_box.pack_start(updated_label, False, False, 0)
            
            row.note_id = note['id']
            self.notes_list.add(row)
        
        self.notes_list.show_all()
        
        # Seleccionar la primera nota por defecto
        if self.notes_list.get_children():
            first_row = self.notes_list.get_row_at_index(0)
            self.notes_list.select_row(first_row)
            first_row.get_style_context().add_class('selected') 