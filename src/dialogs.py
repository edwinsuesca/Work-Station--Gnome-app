import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class ProjectDialog(Gtk.Dialog):
    def __init__(self, parent):
        super().__init__(title="Nuevo Proyecto", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')

        self.set_default_size(400, 200)

        box = self.get_content_area()
        box.set_spacing(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)

        # Nombre del proyecto
        name_label = Gtk.Label(label="Nombre:")
        self.name_entry = Gtk.Entry()
        name_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        name_box.pack_start(name_label, False, False, 0)
        name_box.pack_start(self.name_entry, True, True, 0)
        box.pack_start(name_box, False, False, 0)

        # Descripción del proyecto
        desc_label = Gtk.Label(label="Descripción:")
        self.desc_text = Gtk.TextView()
        self.desc_text.set_size_request(-1, 100)
        self.desc_text.set_margin_start(8)
        self.desc_text.set_margin_end(8)
        self.desc_text.set_margin_top(8)
        self.desc_text.set_margin_bottom(8)
        desc_scroll = Gtk.ScrolledWindow()
        desc_scroll.add(self.desc_text)
        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        desc_box.pack_start(desc_label, False, False, 0)
        desc_box.pack_start(desc_scroll, True, True, 0)
        box.pack_start(desc_box, True, True, 0)

        self.show_all()

    def get_project_data(self):
        name = self.name_entry.get_text()
        buffer = self.desc_text.get_buffer()
        description = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        return name, description

class NoteDialog(Gtk.Dialog):
    def __init__(self, parent, note=None):
        super().__init__(title="Nueva Nota" if not note else "Editar Nota", 
                        transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')

        self.set_default_size(400, 300)
        self.note = note

        box = self.get_content_area()
        box.set_spacing(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)

        # Título de la nota
        title_label = Gtk.Label(label="Título:")
        self.title_entry = Gtk.Entry()
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title_box.pack_start(title_label, False, False, 0)
        title_box.pack_start(self.title_entry, True, True, 0)
        box.pack_start(title_box, False, False, 0)

        # Contenido de la nota
        content_label = Gtk.Label(label="Contenido:")
        self.content_text = Gtk.TextView()
        self.content_text.set_size_request(-1, 200)
        self.content_text.set_margin_start(8)
        self.content_text.set_margin_end(8)
        self.content_text.set_margin_top(8)
        self.content_text.set_margin_bottom(8)
        content_scroll = Gtk.ScrolledWindow()
        content_scroll.add(self.content_text)
        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        content_box.pack_start(content_label, False, False, 0)
        content_box.pack_start(content_scroll, True, True, 0)
        box.pack_start(content_box, True, True, 0)

        # Si estamos editando, cargar los datos
        if note:
            self.title_entry.set_text(note['title'])
            buffer = self.content_text.get_buffer()
            buffer.set_text(note['content'])

        self.show_all()

    def get_note_data(self):
        title = self.title_entry.get_text()
        buffer = self.content_text.get_buffer()
        content = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        return title, content

class TaskDialog(Gtk.Dialog):
    def __init__(self, parent, task=None, status=None):
        super().__init__(title="Nueva Tarea" if not task else "Editar Tarea", 
                        transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )

        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')

        self.set_default_size(400, 300)
        self.task = task

        box = self.get_content_area()
        box.set_spacing(12)
        box.set_margin_start(12)
        box.set_margin_end(12)
        box.set_margin_top(12)
        box.set_margin_bottom(12)

        # Título de la tarea
        title_label = Gtk.Label(label="Título:")
        self.title_entry = Gtk.Entry()
        title_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        title_box.pack_start(title_label, False, False, 0)
        title_box.pack_start(self.title_entry, True, True, 0)
        box.pack_start(title_box, False, False, 0)

        # Estado de la tarea
        status_label = Gtk.Label(label="Estado:")
        self.status_combo = Gtk.ComboBoxText()
        for status in ["Por Hacer", "En Progreso", "Completado"]:
            self.status_combo.append(status, status)
        status_box = Gtk.Box(orientation=Gtk.Orientation.HORIZONTAL, spacing=6)
        status_box.pack_start(status_label, False, False, 0)
        status_box.pack_start(self.status_combo, True, True, 0)
        box.pack_start(status_box, False, False, 0)

        # Descripción de la tarea
        desc_label = Gtk.Label(label="Descripción:")
        self.desc_text = Gtk.TextView()
        self.desc_text.set_size_request(-1, 200)
        self.desc_text.set_margin_start(8)
        self.desc_text.set_margin_end(8)
        self.desc_text.set_margin_top(8)
        self.desc_text.set_margin_bottom(8)
        desc_scroll = Gtk.ScrolledWindow()
        desc_scroll.add(self.desc_text)
        desc_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        desc_box.pack_start(desc_label, False, False, 0)
        desc_box.pack_start(desc_scroll, True, True, 0)
        box.pack_start(desc_box, True, True, 0)

        # Si estamos editando, cargar los datos
        if task:
            self.title_entry.set_text(task['title'])
            buffer = self.desc_text.get_buffer()
            buffer.set_text(task['description'])
            self.status_combo.set_active_id(task['status'])
        elif status:
            self.status_combo.set_active_id(status)

        self.show_all()

    def get_task_data(self):
        title = self.title_entry.get_text()
        buffer = self.desc_text.get_buffer()
        description = buffer.get_text(buffer.get_start_iter(), buffer.get_end_iter(), False)
        status = self.status_combo.get_active_id()
        return title, description, status 