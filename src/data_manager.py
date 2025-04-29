import json
import os
import shutil
from pathlib import Path
import sqlite3
from datetime import datetime
import uuid

class DataManager:
    def __init__(self):
        self.data_dir = Path.home() / '.workstation'
        self.data_file = self.data_dir / 'work-station-data.json'
        self.images_dir = self.data_dir / 'images'
        self.data = {
            'projects': [],
            'notes': [],
            'tasks': []
        }
        self._ensure_data_dir()
        self._load_data()

    def _ensure_data_dir(self):
        """Asegura que el directorio de datos existe"""
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.images_dir.mkdir(parents=True, exist_ok=True)

    def _load_data(self):
        """Carga los datos desde el archivo JSON"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
                    # Asegurar que todos los proyectos tengan un color
                    self._ensure_project_colors()
            except json.JSONDecodeError:
                self._save_data()  # Si el archivo está corrupto, lo reescribimos

    def _ensure_project_colors(self):
        """Asegura que todos los proyectos tengan un color asignado"""
        from dialogs.dialogs import PROJECT_COLORS
        for project in self.data['projects']:
            if 'color' not in project:
                # Asignar un color basado en el índice del proyecto
                color_index = len(self.data['projects']) % len(PROJECT_COLORS)
                project['color'] = PROJECT_COLORS[color_index]
        self._save_data()

    def _save_data(self):
        """Guarda los datos en el archivo JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_project(self, name, color=None):
        """Añade un nuevo proyecto"""
        project = {
            'id': len(self.data['projects']) + 1,
            'name': name,
            'color': color or 'rgb(245, 39, 39)'  # Color por defecto
        }
        self.data['projects'].append(project)
        self._save_data()
        return project

    def update_project(self, project_id, name=None, color=None):
        """Actualiza un proyecto existente"""
        for project in self.data['projects']:
            if project['id'] == project_id:
                if name is not None:
                    project['name'] = name
                if color is not None:
                    project['color'] = color
                self._save_data()
                return project
        return None

    def add_note(self, title, content, project_id, images=None):
        """Añade una nueva nota"""
        if not project_id:
            raise ValueError("Se requiere un project_id para crear una nota")
            
        note = {
            'id': len(self.data['notes']) + 1,
            'title': title,
            'content': content,
            'project_id': project_id,
            'images': images or [],
            'created_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'updated_at': None
        }
        self.data['notes'].append(note)
        self._save_data()
        return note

    def update_note(self, note_id, title, content, images=None):
        """Actualiza una nota existente"""
        for note in self.data['notes']:
            if note['id'] == note_id:
                note['title'] = title
                note['content'] = content
                if images is not None:
                    note['images'] = images
                note['updated_at'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                self._save_data()
                return note
        return None

    def add_task(self, title, description="", status="Por Hacer", project_id=None, images=None):
        """Añade una nueva tarea"""
        if not project_id:
            raise ValueError("Se requiere un project_id para crear una tarea")
            
        task = {
            'id': len(self.data['tasks']) + 1,
            'title': title,
            'description': description,
            'status': status,
            'project_id': project_id,
            'images': images or [],
            'created_at': datetime.now().strftime('%d/%m/%Y %H:%M'),
            'updated_at': None
        }
        self.data['tasks'].append(task)
        self._save_data()
        return task

    def update_task_status(self, task_id, new_status):
        """Actualiza el estado de una tarea"""
        for task in self.data['tasks']:
            if task['id'] == task_id:
                task['status'] = new_status
                self._save_data()
                return True
        return False

    def get_projects(self):
        """Obtiene todos los proyectos"""
        return self.data['projects']

    def get_project(self, project_id):
        """Obtiene un proyecto específico"""
        for project in self.data['projects']:
            if project['id'] == project_id:
                return project
        return None

    def get_notes(self, project_id=None):
        """Obtiene todas las notas, opcionalmente filtradas por proyecto"""
        if project_id is None:
            return self.data['notes']
        return [note for note in self.data['notes'] if note['project_id'] == project_id]

    def get_tasks(self, project_id=None):
        """Obtiene todas las tareas, opcionalmente filtradas por proyecto"""
        if project_id is None:
            return self.data['tasks']
        return [task for task in self.data['tasks'] if task['project_id'] == project_id]

    def delete_note(self, note_id):
        """Elimina una nota"""
        self.data['notes'] = [note for note in self.data['notes'] if note['id'] != note_id]
        self._save_data()

    def delete_task(self, task_id):
        """Elimina una tarea"""
        self.data['tasks'] = [task for task in self.data['tasks'] if task['id'] != task_id]
        self._save_data()

    def update_task(self, task_id, title, description, images=None):
        """Actualiza una tarea existente."""
        for task in self.data['tasks']:
            if task['id'] == task_id:
                task['title'] = title
                task['description'] = description
                if images is not None:
                    task['images'] = images
                task['updated_at'] = datetime.now().strftime('%d/%m/%Y %H:%M')
                self._save_data()
                return True
        return False

    def export_data(self):
        """Exporta todos los datos de la aplicación."""
        # Devolver una copia profunda de los datos
        return json.loads(json.dumps(self.data))

    def import_data(self, data):
        """Importa todos los datos de la aplicación, sobrescribiendo los actuales."""
        if not isinstance(data, dict):
            raise ValueError("El formato de datos a importar no es válido.")
        # Validar claves mínimas
        for key in ['projects', 'notes', 'tasks']:
            if key not in data:
                raise ValueError(f"Falta la clave '{key}' en los datos a importar.")
        self.data = data
        self._save_data()

    def delete_project(self, project_id):
        """Elimina un proyecto y todos sus elementos asociados (tareas y notas)"""
        # Eliminar el proyecto
        self.data['projects'] = [p for p in self.data['projects'] if p['id'] != project_id]
        
        # Eliminar todas las notas asociadas al proyecto
        self.data['notes'] = [n for n in self.data['notes'] if n['project_id'] != project_id]
        
        # Eliminar todas las tareas asociadas al proyecto
        self.data['tasks'] = [t for t in self.data['tasks'] if t['project_id'] != project_id]
        
        self._save_data() 

    def save_image(self, image_path):
        """Guarda una imagen en el directorio de imágenes y devuelve su nombre único"""
        if not os.path.exists(image_path):
            raise ValueError("La ruta de la imagen no existe")
        
        # Generar un nombre único para la imagen
        unique_name = f"{uuid.uuid4()}{Path(image_path).suffix}"
        target_path = self.images_dir / unique_name
        
        # Copiar la imagen al directorio de imágenes
        shutil.copy2(image_path, target_path)
        
        return unique_name

    def delete_image(self, image_name):
        """Elimina una imagen del directorio de imágenes"""
        image_path = self.images_dir / image_name
        if image_path.exists():
            image_path.unlink()
            return True
        return False

    def get_image_path(self, image_name):
        """Obtiene la ruta completa de una imagen"""
        return str(self.images_dir / image_name) 