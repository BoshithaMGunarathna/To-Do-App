"""
Task routes/controllers.
Handles HTTP requests and responses.
Follows Single Responsibility Principle (SRP).
"""
from flask import Blueprint, request, jsonify
from services.task_service import TaskService
from typing import Tuple


class TaskController:
    """
    Task Controller - handles HTTP requests for task operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self, task_service: TaskService):
        """
        Initialize controller with task service.
        Uses Dependency Injection for loose coupling.
        
        Args:
            task_service: Service for task business logic
        """
        self.service = task_service
        self.blueprint = Blueprint('tasks', __name__, url_prefix='/tasks')
        self._register_routes()
    
    def _register_routes(self):
        """Register all routes for this controller."""
        self.blueprint.add_url_rule('', view_func=self.get_all_tasks, methods=['GET'])
        self.blueprint.add_url_rule('', view_func=self.create_task, methods=['POST'])
        self.blueprint.add_url_rule('/<int:task_id>', view_func=self.update_task, methods=['PUT'])
        self.blueprint.add_url_rule('/<int:task_id>', view_func=self.delete_task, methods=['DELETE'])
        self.blueprint.add_url_rule('/stats', view_func=self.get_statistics, methods=['GET'])
    
    def get_all_tasks(self):
        """
        GET /tasks - Retrieve all tasks.
        
        Returns:
            JSON array of tasks with 200 status
        """
        try:
            tasks = self.service.get_all_tasks()
            return jsonify(tasks), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def create_task(self) -> Tuple:
        """
        POST /tasks - Create a new task.
        
        Request body:
            {
                "title": "Task title (required)",
                "description": "Task description (optional)",
                "priority": "normal|low|urgent (optional, default: normal)",
                "due_date": "ISO datetime string (optional)"
            }
        
        Returns:
            JSON of created task with 201 status, or error with 400/500 status
        """
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
        """
        PUT /tasks/<id> - Update an existing task.
        
        Args:
            task_id: ID of the task to update
        
        Request body (all fields optional):
            {
                "title": "New title",
                "description": "New description",
                "completed": true/false,
                "priority": "normal|low|urgent",
                "due_date": "ISO datetime string or '' to clear"
            }
        
        Returns:
            JSON of updated task with 200 status, or error with 400/404/500 status
        """
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
        """
        DELETE /tasks/<id> - Delete a task.
        
        Args:
            task_id: ID of the task to delete
        
        Returns:
            Success message with 200 status, or error with 404/500 status
        """
        try:
            success = self.service.delete_task(task_id)
            
            if not success:
                return jsonify({'error': 'Task not found'}), 404
            
            return jsonify({'message': 'Task deleted successfully'}), 200
            
        except Exception as e:
            return jsonify({'error': str(e)}), 500
    
    def get_statistics(self) -> Tuple:
        """
        GET /tasks/stats - Get task statistics.
        
        Returns:
            JSON with task counts (total, active, completed) with 200 status
        """
        try:
            stats = self.service.get_task_statistics()
            return jsonify(stats), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500
