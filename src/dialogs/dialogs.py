import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ProjectDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Proyecto", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')
        
        # Establecer un tamaño mínimo para el diálogo
        self.set_default_size(600, 100)
        
        # Contenedor principal
        box = self.get_content_area()
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        
        # Contenedor para el nombre
        name_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(name_box, True, True, 0)
        
        # Entrada de nombre
        self.name_entry = Gtk.Entry()
        self.name_entry.set_placeholder_text("Nombre del proyecto")
        self.name_entry.set_hexpand(True)
        name_box.pack_start(self.name_entry, True, True, 0)
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de nombre
        self.name_entry.grab_focus()

    def get_project_data(self):
        name = self.name_entry.get_text()
        return name, ""

class NoteDialog(Gtk.Dialog):
    def __init__(self, parent, note=None):
        super().__init__(title="Nota", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')
        
        # Establecer un tamaño mínimo para el diálogo
        self.set_default_size(600, 400)
        
        # Contenedor principal
        box = self.get_content_area()
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        
        # Contenedor para el título
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        title_box.set_margin_bottom(12)
        box.pack_start(title_box, False, False, 0)
        
        # Entrada de título
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Título de la nota")
        self.title_entry.set_hexpand(True)
        title_box.pack_start(self.title_entry, False, False, 0)
        
        # Contenedor para el contenido
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(content_box, True, True, 0)
        
        # Entrada de contenido
        self.content_textview = Gtk.TextView()
        self.content_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.content_textview.set_hexpand(True)
        self.content_textview.set_vexpand(True)
        
        # Scrolled window para el contenido
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.content_textview)
        scrolled.set_min_content_height(300)
        content_box.pack_start(scrolled, True, True, 0)
        
        # Si es una nota existente, cargar los datos
        if note:
            self.title_entry.set_text(note['title'])
            if note['content']:
                self.content_textview.get_buffer().set_text(note['content'])
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de contenido
        self.content_textview.grab_focus()

    def get_note_data(self):
        title = self.title_entry.get_text()
        content = self.content_textview.get_buffer().get_text(
            self.content_textview.get_buffer().get_start_iter(),
            self.content_textview.get_buffer().get_end_iter(),
            False
        )
        return title, content

class TaskDialog(Gtk.Dialog):
    def __init__(self, parent, task=None, status=None):
        super().__init__(title="Tarea", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')
        
        # Establecer un tamaño mínimo para el diálogo
        self.set_default_size(600, 400)
        
        # Contenedor principal
        box = self.get_content_area()
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)
        
        # Contenedor para el título
        title_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        title_box.set_margin_bottom(12)
        box.pack_start(title_box, False, False, 0)
        
        # Entrada de título
        self.title_entry = Gtk.Entry()
        self.title_entry.set_placeholder_text("Título de la tarea")
        self.title_entry.set_hexpand(True)
        title_box.pack_start(self.title_entry, False, False, 0)
        
        # Contenedor para la descripción
        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        box.pack_start(desc_box, True, True, 0)
        
        # Entrada de descripción
        self.desc_textview = Gtk.TextView()
        self.desc_textview.set_wrap_mode(Gtk.WrapMode.WORD)
        self.desc_textview.set_hexpand(True)
        self.desc_textview.set_vexpand(True)
        
        # Scrolled window para la descripción
        scrolled = Gtk.ScrolledWindow()
        scrolled.set_policy(Gtk.PolicyType.AUTOMATIC, Gtk.PolicyType.AUTOMATIC)
        scrolled.add(self.desc_textview)
        scrolled.set_min_content_height(300)
        desc_box.pack_start(scrolled, True, True, 0)
        
        # Si es una tarea existente, cargar los datos
        if task:
            self.title_entry.set_text(task['title'])
            if task['description']:
                self.desc_textview.get_buffer().set_text(task['description'])
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de descripción
        self.desc_textview.grab_focus()
    
    def get_task_data(self):
        title = self.title_entry.get_text()
        description = self.desc_textview.get_buffer().get_text(
            self.desc_textview.get_buffer().get_start_iter(),
            self.desc_textview.get_buffer().get_end_iter(),
            False
        )
        return title, description 