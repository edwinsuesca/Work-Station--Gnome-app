import gi
gi.require_version('Gtk', '3.0')
gi.require_version('Gdk', '3.0')
from gi.repository import Gtk, Gdk

def load_styles():
    css = """
    .item {
        padding: 5px 0;
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }

    .item-project {
        padding: 10px 0;
        border: none;
        border-bottom: 1px solid rgba(0, 0, 0, 0.1);
    }
    .selected {
        background-color: rgba(0, 142, 255, 0.1);
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

    .p-container {
        border: none;
    }
    
    .kanban-column {
        border-right: 1px solid rgba(0, 0, 0, 0.1);
    }

    .kanban-column:last-child {
        border-right: none;
    }

    /* Estilo para el área de botones en diálogos */
    .dialog-action-area {
        margin-top: 25px;
    }

    .dialog-action-area button:first-child {
        margin-right: 10px;
    }

    /* Estilos para los botones de color */
    .color-button {
        border-radius: 20px;
        min-width: 20px;
        min-height: 20px;
        padding: 0;
        background: none;
    }

    .selected-color {
        border: 2px solid @theme_fg_color;
        border-width: 3px;
    }

    /* Eliminar bordes del notebook y tabs */
    notebook {
        border: none;
        background: none;
        padding: 0;
    }
    
    notebook header {
        border: none;
        background: none;
        padding: 0;
    }
    
    notebook header tabs {
        border: none;
        margin: 0;
        padding: 0;
    }
    
    notebook header tab {
        margin: 0;
        padding: 8px 12px;
    }

    /* Eliminar bordes de la sidebar */
    .sidebar {
        padding: 0;
        margin: 0;
        background: none;
        border: none;
    }

    /* Eliminar el borde del separador del paned */
    paned {
        background: none;
    }

    paned separator {
        background: none;
        border: none;
        min-width: 0;
        min-height: 0;
    }
    """
    css_provider = Gtk.CssProvider()
    css_provider.load_from_data(css.encode())
    Gtk.StyleContext.add_provider_for_screen(
        Gdk.Screen.get_default(),
        css_provider,
        Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION
    ) 