"""
Main Flask application with clean architecture.
Uses dependency injection and layered architecture:
- Controllers: Handle HTTP requests
- Services: Business logic
- Repositories: Data access
- Config: Configuration management
"""
from flask import Flask
from flask_cors import CORS

from config.database import DatabaseConfig, DatabaseConnection
from repositories.task_repository import TaskRepository
from services.task_service import TaskService
from controllers.task_controller import TaskController


def create_app() -> Flask:
    """
    Application factory pattern.
    Creates and configures the Flask application with all dependencies.
    
    Returns:
        Configured Flask application
    """
    app = Flask(__name__)
    CORS(app)
    
    # Initialize database connection
    db_config = DatabaseConfig()
    db_connection = DatabaseConnection(db_config)
    db = db_connection.connect()
    
    # Initialize layers with dependency injection
    task_repository = TaskRepository(db)
    task_service = TaskService(task_repository)
    task_controller = TaskController(task_service)
    
    # Register blueprints
    app.register_blueprint(task_controller.blueprint)
    
    # Health check endpoint
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'todo-api'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)

