import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

# Lista de colores predefinidos
PROJECT_COLORS = [
    # Fila 1 (100)
    'rgb(255, 205, 210)', 'rgb(248, 187, 208)', 'rgb(225, 190, 231)', 'rgb(209, 196, 233)', 'rgb(187, 222, 251)', 'rgb(178, 235, 242)', 'rgb(178, 223, 219)', 'rgb(200, 230, 201)', 'rgb(220, 237, 200)', 'rgb(241, 248, 233)',
    # Fila 2 (200)
    'rgb(239, 154, 154)', 'rgb(244, 143, 177)', 'rgb(206, 147, 216)', 'rgb(179, 157, 219)', 'rgb(144, 202, 249)', 'rgb(128, 222, 234)', 'rgb(128, 203, 196)', 'rgb(165, 214, 167)', 'rgb(197, 225, 165)', 'rgb(220, 237, 200)',
    # Fila 3 (300)
    'rgb(229, 115, 115)', 'rgb(240, 98, 146)', 'rgb(186, 104, 200)', 'rgb(149, 117, 205)', 'rgb(100, 181, 246)', 'rgb(77, 208, 225)', 'rgb(77, 182, 172)', 'rgb(129, 199, 132)', 'rgb(174, 213, 129)', 'rgb(197, 225, 165)',
    # Fila 4 (400)
    'rgb(239, 83, 80)', 'rgb(236, 64, 122)', 'rgb(171, 71, 188)', 'rgb(126, 87, 194)', 'rgb(66, 165, 245)', 'rgb(38, 198, 218)', 'rgb(38, 166, 154)', 'rgb(102, 187, 106)', 'rgb(156, 204, 101)', 'rgb(174, 213, 129)',
    # Fila 5 (500)
    'rgb(244, 67, 54)', 'rgb(233, 30, 99)', 'rgb(156, 39, 176)', 'rgb(103, 58, 183)', 'rgb(33, 150, 243)', 'rgb(0, 188, 212)', 'rgb(0, 150, 136)', 'rgb(76, 175, 80)', 'rgb(139, 195, 74)', 'rgb(205, 220, 57)',
    # Fila 6 (600)
    'rgb(229, 57, 53)', 'rgb(216, 27, 96)', 'rgb(123, 31, 162)', 'rgb(94, 53, 177)', 'rgb(30, 136, 229)', 'rgb(0, 172, 193)', 'rgb(0, 137, 123)', 'rgb(67, 160, 71)', 'rgb(124, 179, 66)', 'rgb(192, 202, 51)',
    # Fila 7 (700)
    'rgb(211, 47, 47)', 'rgb(194, 24, 91)', 'rgb(106, 27, 154)', 'rgb(81, 45, 168)', 'rgb(25, 118, 210)', 'rgb(0, 151, 167)', 'rgb(0, 121, 107)', 'rgb(56, 142, 60)', 'rgb(104, 159, 56)', 'rgb(175, 180, 43)',
    # Fila 8 (800)
    'rgb(198, 40, 40)', 'rgb(173, 20, 87)', 'rgb(74, 20, 140)', 'rgb(69, 39, 160)', 'rgb(21, 101, 192)', 'rgb(0, 131, 143)', 'rgb(0, 105, 92)', 'rgb(46, 125, 50)', 'rgb(85, 139, 47)', 'rgb(158, 157, 36)',
    # Fila 9 (900)
    'rgb(183, 28, 28)', 'rgb(136, 14, 79)', 'rgb(49, 27, 146)', 'rgb(40, 53, 147)', 'rgb(13, 71, 161)', 'rgb(0, 96, 100)', 'rgb(0, 77, 64)', 'rgb(27, 94, 32)', 'rgb(51, 105, 30)', 'rgb(130, 119, 23)'
]

class ProjectDialog(Gtk.Dialog):
    def __init__(self, parent, project=None):
        super().__init__(title="Proyecto", transient_for=parent, flags=0)
        self.add_buttons(
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL,
            Gtk.STOCK_OK, Gtk.ResponseType.OK
        )
        
        # Hacer que el botón OK sea el botón de acento
        ok_button = self.get_widget_for_response(Gtk.ResponseType.OK)
        ok_button.get_style_context().add_class('suggested-action')
        
        # Establecer un tamaño mínimo para el diálogo
        self.set_default_size(300, 200)
        
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
        self.name_entry.connect("activate", self.on_enter_pressed)
        name_box.pack_start(self.name_entry, True, True, 0)
        
        # Contenedor para los colores
        colors_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=6)
        colors_box.set_margin_top(12)
        box.pack_start(colors_box, True, True, 0)
        
        # Título de la sección de colores
        colors_label = Gtk.Label(label="Color del proyecto")
        colors_label.set_xalign(0)
        colors_box.pack_start(colors_label, False, False, 0)
        
        # Grid para los colores
        colors_grid = Gtk.Grid()
        colors_grid.set_column_spacing(6)
        colors_grid.set_row_spacing(6)
        colors_box.pack_start(colors_grid, True, True, 0)
        
        # Crear botones de color organizados por filas y columnas (9 filas x 10 columnas)
        self.color_buttons = []
        num_cols = 10
        num_rows = 9
        for row in range(num_rows):
            for col in range(num_cols):
                i = row * num_cols + col
                if i >= len(PROJECT_COLORS):
                    break
                color = PROJECT_COLORS[i]
                button = Gtk.Button()
                button.set_size_request(30, 30)
                button.get_style_context().add_class('color-button')
                button.color = color
                button.connect('clicked', self.on_color_selected)
                button.set_name(f'color-button-{i}')
                provider = Gtk.CssProvider()
                provider.load_from_data(f'#{button.get_name()} {{ background-color: {color}; }}'.encode())
                button.get_style_context().add_provider(
                    provider,
                    Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
                )
                if project and project['color'] == color:
                    button.get_style_context().add_class('selected-color')
                colors_grid.attach(button, col, row, 1, 1)
                self.color_buttons.append(button)
        
        # Color seleccionado por defecto
        self.selected_color = project['color'] if project else PROJECT_COLORS[0]
        
        # Aumentar el ancho del diálogo para que quepan los botones
        self.set_default_size(420, 300)
        
        # Agregar clase al contenedor de botones
        action_area = self.get_action_area()
        action_area.get_style_context().add_class('dialog-action-area')
        
        # Si es un proyecto existente, cargar los datos
        if project:
            self.name_entry.set_text(project['name'])
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de nombre
        self.name_entry.grab_focus()

    def on_color_selected(self, button):
        # Remover la clase selected-color de todos los botones
        for btn in self.color_buttons:
            btn.get_style_context().remove_class('selected-color')
        
        # Agregar la clase al botón seleccionado
        button.get_style_context().add_class('selected-color')
        
        # Guardar el color seleccionado
        self.selected_color = button.color

    def on_enter_pressed(self, widget):
        if self.name_entry.get_text().strip():
            self.response(Gtk.ResponseType.OK)

    def get_project_data(self):
        return self.name_entry.get_text(), self.selected_color

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
        self.title_entry.connect("activate", self.on_enter_pressed)
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
        
        # Agregar clase al contenedor de botones
        action_area = self.get_action_area()
        action_area.get_style_context().add_class('dialog-action-area')
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de contenido
        self.content_textview.grab_focus()

    def on_enter_pressed(self, widget):
        if self.title_entry.get_text().strip():
            self.response(Gtk.ResponseType.OK)

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
        self.title_entry.connect("activate", self.on_enter_pressed)
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
        
        # Agregar clase al contenedor de botones
        action_area = self.get_action_area()
        action_area.get_style_context().add_class('dialog-action-area')
        
        # Mostrar el diálogo
        self.show_all()
        
        # Establecer el foco en el campo de descripción
        self.desc_textview.grab_focus()
    
    def on_enter_pressed(self, widget):
        if self.title_entry.get_text().strip():
            self.response(Gtk.ResponseType.OK)
    
    def get_task_data(self):
        title = self.title_entry.get_text()
        description = self.desc_textview.get_buffer().get_text(
            self.desc_textview.get_buffer().get_start_iter(),
            self.desc_textview.get_buffer().get_end_iter(),
            False
        )
        return title, description 