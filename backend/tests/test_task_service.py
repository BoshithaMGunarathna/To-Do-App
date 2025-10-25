import pytest
from unittest.mock import Mock
from services.task_service import TaskService


@pytest.fixture
def mock_repository():
    return Mock()


@pytest.fixture
def service(mock_repository):
    return TaskService(mock_repository)


class TestTaskService:
    
    def test_get_all_tasks_returns_all(self, service, mock_repository):
        expected_tasks = [{'id': 1, 'title': 'Task 1'}, {'id': 2, 'title': 'Task 2'}]
        mock_repository.find_all.return_value = expected_tasks
        
        result = service.get_all_tasks()
        
        assert result == expected_tasks
        mock_repository.find_all.assert_called_once()
    
    def test_get_task_by_id_returns_task(self, service, mock_repository):
        expected_task = {'id': 1, 'title': 'Task 1'}
        mock_repository.find_by_id.return_value = expected_task
        
        result = service.get_task_by_id(1)
        
        assert result == expected_task
        mock_repository.find_by_id.assert_called_once_with(1)
    
    def test_create_task_success(self, service, mock_repository):
        created_task = {'id': 1, 'title': 'New Task', 'description': 'Description'}
        mock_repository.create.return_value = 1
        mock_repository.find_by_id.return_value = created_task
        
        result = service.create_task("New Task", "Description")
        
        assert result == created_task
        mock_repository.create.assert_called_once_with(
            title="New Task",
            description="Description",
            completed=False,
            priority='normal',
            due_date=None
        )
    
    def test_create_task_trims_whitespace(self, service, mock_repository):
        mock_repository.create.return_value = 1
        mock_repository.find_by_id.return_value = {'id': 1}
        
        service.create_task("  Spaced Title  ", "  Spaced Description  ")
        
        mock_repository.create.assert_called_once_with(
            title="Spaced Title",
            description="Spaced Description",
            completed=False,
            priority='normal',
            due_date=None
        )
    
    def test_create_task_fails_with_empty_title(self, service, mock_repository):
        with pytest.raises(ValueError, match="Task title is required"):
            service.create_task("", "Description")
        
        mock_repository.create.assert_not_called()
    
    def test_create_task_fails_with_whitespace_only_title(self, service, mock_repository):
        with pytest.raises(ValueError, match="Task title is required"):
            service.create_task("   ", "Description")
    
    def test_create_task_fails_with_title_too_long(self, service, mock_repository):
        long_title = "a" * 256
        
        with pytest.raises(ValueError, match="Task title must be 255 characters or less"):
            service.create_task(long_title, "Description")
    
    def test_create_task_fails_with_description_too_long(self, service, mock_repository):
        long_description = "a" * 1001
        
        with pytest.raises(ValueError, match="Task description must be 1000 characters or less"):
            service.create_task("Title", long_description)
    
    def test_update_task_success(self, service, mock_repository):
        existing_task = {'id': 1, 'title': 'Old', 'completed': False}
        updated_task = {'id': 1, 'title': 'New', 'completed': True}
        mock_repository.find_by_id.side_effect = [existing_task, updated_task]
        mock_repository.update.return_value = True
        
        result = service.update_task(1, title="New", completed=True)
        
        assert result == updated_task
        mock_repository.update.assert_called_once_with(
            task_id=1,
            title="New",
            description=None,
            completed=True,
            priority=None,
            due_date=None
        )
    
    def test_update_task_returns_none_when_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None
        
        result = service.update_task(999, title="New")
        
        assert result is None
        mock_repository.update.assert_not_called()
    
    def test_update_task_fails_with_empty_title(self, service, mock_repository):
        mock_repository.find_by_id.return_value = {'id': 1}
        
        with pytest.raises(ValueError, match="Task title cannot be empty"):
            service.update_task(1, title="  ")
    
    def test_toggle_task_completion_changes_status(self, service, mock_repository):
        task = {'id': 1, 'completed': False}
        toggled_task = {'id': 1, 'completed': True}
        mock_repository.find_by_id.side_effect = [task, toggled_task]
        
        result = service.toggle_task_completion(1)
        
        assert result == toggled_task
        mock_repository.update.assert_called_once_with(1, completed=True)
    
    def test_toggle_task_completion_returns_none_when_not_found(self, service, mock_repository):
        mock_repository.find_by_id.return_value = None
        
        result = service.toggle_task_completion(999)
        
        assert result is None
        mock_repository.update.assert_not_called()
    
    def test_delete_task_success(self, service, mock_repository):
        mock_repository.delete.return_value = True
        
        result = service.delete_task(1)
        
        assert result is True
        mock_repository.delete.assert_called_once_with(1)
    
    def test_delete_task_returns_false_when_not_found(self, service, mock_repository):
        mock_repository.delete.return_value = False
        
        result = service.delete_task(999)
        
        assert result is False
    
    def test_get_task_statistics(self, service, mock_repository):
        mock_repository.count_all.return_value = 10
        mock_repository.count_by_status.side_effect = [3, 7]
        
        result = service.get_task_statistics()
        
        assert result == {
            'total': 10,
            'active': 7,
            'completed': 3
        }
        mock_repository.count_all.assert_called_once()
        assert mock_repository.count_by_status.call_count == 2
