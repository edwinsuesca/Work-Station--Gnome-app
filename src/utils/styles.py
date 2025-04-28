import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

def load_styles():
    css = """
    .item {
        padding: 5px 0;
        border: none;
        border-bottom: 1px solid rgba(141, 141, 141, 0.2);
    }
    .selected {
        background-color: rgba(0, 142, 255, 0.2);
        border-bottom-color: rgba(0, 142, 255, 0.7);
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
    /* Estilos para los placeholders */
    entry {
        padding: 8px;
    }
    entry placeholder {
        color: rgba(141, 141, 141, 0.6);
    }
    
    textview {
        padding: 8px;
    }

    .p-8 {
        padding: 8px;
    }

    .bold-title {
        font-weight: bold;
    }

    button {
        border: none;
    }
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css.encode())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    ) 