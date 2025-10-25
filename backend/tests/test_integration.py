import pytest
import json
from app import create_app


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True
    return app


@pytest.fixture
def client(app):
    return app.test_client()


class TestTaskAPI:
    
    def test_health_check(self, client):
        response = client.get('/health')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['status'] == 'healthy'
    
    def test_get_all_tasks(self, client):
        response = client.get('/tasks')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert isinstance(data, list)
    
    def test_create_task_success(self, client):
        task_data = {
            'title': 'Test Task',
            'description': 'Test Description'
        }
        
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 201
        data = json.loads(response.data)
        assert 'id' in data
        assert data['title'] == 'Test Task'
        assert data['description'] == 'Test Description'
        assert data['completed'] == 0
    
    def test_create_task_without_title_fails(self, client):
        task_data = {
            'description': 'Test Description'
        }
        
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 400
        data = json.loads(response.data)
        assert 'error' in data
    
    def test_create_task_with_empty_title_fails(self, client):
        task_data = {
            'title': '',
            'description': 'Test Description'
        }
        
        response = client.post('/tasks',
                             data=json.dumps(task_data),
                             content_type='application/json')
        
        assert response.status_code == 400
    
    def test_update_task_success(self, client):
        create_data = {'title': 'Original', 'description': 'Desc'}
        create_response = client.post('/tasks',
                                    data=json.dumps(create_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        update_data = {
            'title': 'Updated',
            'completed': True
        }
        
        response = client.put(f'/tasks/{task_id}',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert data['title'] == 'Updated'
        assert data['completed'] == 1
    
    def test_update_nonexistent_task_returns_404(self, client):
        update_data = {'title': 'Updated'}
        
        response = client.put('/tasks/99999',
                            data=json.dumps(update_data),
                            content_type='application/json')
        
        assert response.status_code == 404
    
    def test_delete_task_success(self, client):
        create_data = {'title': 'To Delete', 'description': 'Desc'}
        create_response = client.post('/tasks',
                                    data=json.dumps(create_data),
                                    content_type='application/json')
        task_id = json.loads(create_response.data)['id']
        
        response = client.delete(f'/tasks/{task_id}')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'message' in data
        
        get_response = client.get('/tasks')
        tasks = json.loads(get_response.data)
        task_ids = [task['id'] for task in tasks]
        assert task_id not in task_ids
    
    def test_delete_nonexistent_task_returns_404(self, client):
        response = client.delete('/tasks/99999')
        
        assert response.status_code == 404
    
    def test_get_statistics(self, client):
        response = client.get('/tasks/stats')
        
        assert response.status_code == 200
        data = json.loads(response.data)
        assert 'total' in data
        assert 'active' in data
        assert 'completed' in data
        assert isinstance(data['total'], int)
        assert isinstance(data['active'], int)
        assert isinstance(data['completed'], int)
