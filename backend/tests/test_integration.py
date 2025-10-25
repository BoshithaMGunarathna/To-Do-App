"""
Integration tests for Task API endpoints.
Tests the full stack with test database.
"""
import pytest
import json
from app import create_app


@pytest.fixture
def app():
    """Create test application."""
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()


class TestTaskAPI:
    """Integration tests for Task API."""
    
    def test_health_check(self, client):
        """Test health check endpoint."""
        # Act
        response = client.get('/health')
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_get_all_tasks(self, client):
        """Test GET /tasks returns list of tasks."""
        # Act
        response = client.get('/tasks')
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_create_task_success(self, client):
        """Test POST /tasks creates new task."""
        # Arrange
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }
        
        # Act
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        # Assert
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['title'] == 'Test Task'
        assert data['description'] == 'Test Description'
        assert data['completed'] == 0  # MySQL returns 0/1 for boolean
    
    def test_create_task_without_title_fails(self, client):
        """Test POST /tasks without title returns 400."""
        # Arrange
        task_data = {
            'description': 'Test Description'
        }
        
        # Act
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        # Assert
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_with_empty_title_fails(self, client):
        """Test POST /tasks with empty title returns 400."""
        # Arrange
        task_data = {
            'title': '',
            'description': 'Test Description'
        }
        
        # Act
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        # Assert
        assert response.status_code == 400
    
    def test_update_task_success(self, client):
        """Test PUT /tasks/<id> updates task."""
        # Arrange - Create a task first
        create_data = {'title': 'Original', 'description': 'Desc'}
        create_response = client.post('/tasks',
                                    data=json.dumps(create_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        update_data = {
            'title': 'Updated',
            'completed': True
        }
        
        # Act
        response = client.put(f'/tasks/{task_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated'
        assert data['completed'] == 1  # MySQL returns 0/1 for boolean
    
    def test_update_nonexistent_task_returns_404(self, client):
        """Test PUT /tasks/<id> with invalid ID returns 404."""
        # Arrange
        update_data = {'title': 'Updated'}
        
        # Act
        response = client.put('/tasks/99999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        # Assert
        assert response.status_code == 404
    
    def test_delete_task_success(self, client):
        """Test DELETE /tasks/<id> removes task."""
        # Arrange - Create a task first
        create_data = {'title': 'To Delete', 'description': 'Desc'}
        create_response = client.post('/tasks',
                                    data=json.dumps(create_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        # Act
        response = client.delete(f'/tasks/{task_id}')
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        # Verify task is deleted
        get_response = client.get('/tasks')
        tasks = json.loads(get_response.data)
        task_ids = [task['id'] for task in tasks]
        assert task_id not in task_ids
    
    def test_delete_nonexistent_task_returns_404(self, client):
        """Test DELETE /tasks/<id> with invalid ID returns 404."""
        # Act
        response = client.delete('/tasks/99999')
        
        # Assert
        assert response.status_code == 404
    
    def test_get_statistics(self, client):
        """Test GET /tasks/stats returns correct statistics."""
        # Act
        response = client.get('/tasks/stats')
        
        # Assert
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total' in data
        assert 'active' in data
        assert 'completed' in data
        assert isinstance(data['total'], int)
        assert isinstance(data['active'], int)
        assert isinstance(data['completed'], int)
