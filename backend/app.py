from flask import Flask
from flask_cors import CORS

from config.database import DatabaseConfig, DatabaseConnection
from repositories.task_repository import TaskRepository
from services.task_service import TaskService
from controllers.task_controller import TaskController


def create_app() -> Flask:
    app = Flask(__name__)
    CORS(app)
    
    db_config = DatabaseConfig()
    db_connection = DatabaseConnection(db_config)
    db = db_connection.connect()
    
    task_repository = TaskRepository(db)
    task_service = TaskService(task_repository)
    task_controller = TaskController(task_service)
    
    app.register_blueprint(task_controller.blueprint)
    
    @app.route('/health', methods=['GET'])
    def health_check():
        return {'status': 'healthy', 'service': 'todo-api'}, 200
    
    return app


if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=5000, debug=False)

