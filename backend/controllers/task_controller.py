from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from typing import Tuple


class TaskController:
    def __init__(self, task_service: TaskService):
        self.service = task_service
        self.blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')
        self._register_routes()
    
    def _register_routes(self):
        self.blueprint.add_url_rule('', view_func=self.get_all_tasks, methods=['GET'])
        self.blueprint.add_url_rule('', view_func=self.create_task, methods=['POST'])
        self.blueprint.add_url_rule('/<int:task_id>', view_func=self.update_task, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:task_id>', view_func=self.delete_task, methods=['DELETE'])
        self.blueprint.add_url_rule('/stats', view_func=self.get_statistics, methods=['GET'])
    
    def get_all_tasks(self):
        try:
            tasks = self.service.get_all_tasks()
            return jsonify(tasks), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create_task(self) -> Tuple:
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            title = data.get('title', '')
            description = data.get('description', '')
            priority = data.get('priority', 'normal')
            due_date = data.get('due_date')
            
            task = self.service.create_task(title, description, priority, due_date)
            return jsonify(task), 201
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def update_task(self, task_id: int) -> Tuple:
        try:
            data = request.get_json()
            
            if not data:
                return jsonify({'error': 'Request body is required'}), 400
            
            title = data.get('title')
            description = data.get('description')
            completed = data.get('completed')
            priority = data.get('priority')
            due_date = data.get('due_date')
            
            task = self.service.update_task(task_id, title, description, completed, priority, due_date)
            
            if task is None:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify(task), 200
            
        except ValueError as e:
            return jsonify({'error': str(e)}), 400
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def delete_task(self, task_id: int) -> Tuple:
        try:
            success = self.service.delete_task(task_id)
            
            if not success:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify({'message': 'Task deleted successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_statistics(self) -> Tuple:
        try:
            stats = self.service.get_task_statistics()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
