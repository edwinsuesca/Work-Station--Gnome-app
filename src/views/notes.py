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
        
        self.show_all()
    
    def refresh_notes(self, project_id):
        # Limpiar lista actual
        for child in self.notes_list.get_children():
            self.notes_list.remove(child)
        
        # Añadir notas
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