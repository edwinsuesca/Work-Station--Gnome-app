import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, GdkPixbuf
import os

class ImagePreviewGrid(Gtk.Grid):
    def __init__(self, data_manager):
        super().__init__()
        self.data_manager = data_manager
        self.set_column_spacing(4)
        self.set_row_spacing(4)
        
        # Aplicar estilos
        style_context = self.get_style_context()
        style_context.add_class('image-preview-container')
        
        self.current_column = 0
        self.current_row = 0
        self.max_columns = 5

    def add_image(self, image_name):
        try:
            # Verificar si la imagen existe
            image_path = self.data_manager.get_image_path(image_name)
            if not os.path.exists(image_path):
                return False
            
            # Crear el contenedor de la imagen
            container = Gtk.EventBox()
            container.set_size_request(40, 40)
            container.get_style_context().add_class('image-preview-container')
            
            # Cargar la imagen
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)
            
            # Escalar la imagen manteniendo la relación de aspecto
            width = pixbuf.get_width()
            height = pixbuf.get_height()
            if width > height:
                new_width = 40
                new_height = int(height * (40/width))
            else:
                new_height = 40
                new_width = int(width * (40/height))
            
            pixbuf = pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.BILINEAR)
            
            # Crear el widget de imagen
            image = Gtk.Image.new_from_pixbuf(pixbuf)
            image.set_halign(Gtk.Align.CENTER)
            image.set_valign(Gtk.Align.CENTER)
            
            container.add(image)
            
            # Añadir la imagen a la rejilla
            num_children = len(list(self.get_children()))
            row = num_children // 6  # 6 imágenes por fila
            col = num_children % 6
            self.attach(container, col, row, 1, 1)
            
            return True
            
        except Exception as e:
            print(f"Error al cargar la preview de la imagen {image_name}: {str(e)}")
            return False
    
    def clear(self):
        for child in self.get_children():
            self.remove(child) 