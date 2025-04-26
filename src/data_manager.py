import json
import os
from pathlib import Path

class DataManager:
    def __init__(self):
        self.data_dir = Path.home() / '.workstation'
        self.data_file = self.data_dir / 'data.json'
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

    def _load_data(self):
        """Carga los datos desde el archivo JSON"""
        if self.data_file.exists():
            try:
                with open(self.data_file, 'r') as f:
                    self.data = json.load(f)
            except json.JSONDecodeError:
                self._save_data()  # Si el archivo está corrupto, lo reescribimos

    def _save_data(self):
        """Guarda los datos en el archivo JSON"""
        with open(self.data_file, 'w') as f:
            json.dump(self.data, f, indent=4)

    def add_project(self, name, description=""):
        """Añade un nuevo proyecto"""
        project = {
            'id': len(self.data['projects']) + 1,
            'name': name,
            'description': description
        }
        self.data['projects'].append(project)
        self._save_data()
        return project

    def add_note(self, title, content, project_id):
        """Añade una nueva nota"""
        if not project_id:
            raise ValueError("Se requiere un project_id para crear una nota")
            
        note = {
            'id': len(self.data['notes']) + 1,
            'title': title,
            'content': content,
            'project_id': project_id
        }
        self.data['notes'].append(note)
        self._save_data()
        return note

    def update_note(self, note_id, title, content):
        """Actualiza una nota existente"""
        for note in self.data['notes']:
            if note['id'] == note_id:
                note['title'] = title
                note['content'] = content
                self._save_data()
                return note
        return None

    def add_task(self, title, description="", status="Por Hacer", project_id=None):
        """Añade una nueva tarea"""
        if not project_id:
            raise ValueError("Se requiere un project_id para crear una tarea")
            
        task = {
            'id': len(self.data['tasks']) + 1,
            'title': title,
            'description': description,
            'status': status,
            'project_id': project_id
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