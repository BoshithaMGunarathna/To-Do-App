import pytest
from unittest.mock import Mock, MagicMock, call
from repositories.task_repository import TaskRepository


@pytest.fixture
def mock_db():
    return Mock()


@pytest.fixture
def mock_cursor():
    cursor = Mock()
    cursor.fetchall = Mock(return_value=[])
    cursor.fetchone = Mock(return_value=None)
    cursor.lastrowid = 1
    cursor.rowcount = 1
    return cursor


@pytest.fixture
def repository(mock_db, mock_cursor):
    mock_db.cursor.return_value = mock_cursor
    return TaskRepository(mock_db)


class TestTaskRepository:
    
    def test_find_all_returns_all_tasks(self, repository, mock_cursor):
        expected_tasks = [
            {'id': 1, 'title': 'Task 1', 'description': 'Desc 1', 'completed': False},
            {'id': 2, 'title': 'Task 2', 'description': 'Desc 2', 'completed': True}
        ]
        mock_cursor.fetchall.return_value = expected_tasks
        
        result = repository.find_all()
        
        assert result == expected_tasks
        mock_cursor.execute.assert_called_once_with("SELECT * FROM task ORDER BY created_at DESC")
        mock_cursor.close.assert_called_once()
    
    def test_find_by_id_returns_task_when_found(self, repository, mock_cursor):
        expected_task = {'id': 1, 'title': 'Task 1', 'description': 'Desc 1', 'completed': False}
        mock_cursor.fetchone.return_value = expected_task
        
        result = repository.find_by_id(1)
        
        assert result == expected_task
        mock_cursor.execute.assert_called_once_with("SELECT * FROM task WHERE id = %s", (1,))
        mock_cursor.close.assert_called_once()
    
    def test_find_by_id_returns_none_when_not_found(self, repository, mock_cursor):
        mock_cursor.fetchone.return_value = None
        
        result = repository.find_by_id(999)
        
        assert result is None
        mock_cursor.execute.assert_called_once()
    
    def test_create_inserts_task_and_returns_id(self, repository, mock_cursor, mock_db):
        mock_cursor.lastrowid = 42
        
        result = repository.create("New Task", "Description", False)
        
        assert result == 42
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO task (title, description, completed) VALUES (%s, %s, %s)",
            ("New Task", "Description", False)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_update_with_all_fields(self, repository, mock_cursor, mock_db):
        mock_cursor.rowcount = 1
        
        result = repository.update(1, title="Updated", description="New desc", completed=True)
        
        assert result is True
        mock_cursor.execute.assert_called_once()
        assert "UPDATE task SET" in mock_cursor.execute.call_args[0][0]
        mock_db.commit.assert_called_once()
    
    def test_update_with_partial_fields(self, repository, mock_cursor, mock_db):
        mock_cursor.rowcount = 1
        
        result = repository.update(1, completed=True)
        
        assert result is True
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "completed = %s" in call_args[0]
        assert call_args[1] == (True, 1)
    
    def test_update_returns_false_when_no_fields(self, repository, mock_cursor):
        result = repository.update(1)
        
        assert result is False
        mock_cursor.execute.assert_not_called()
    
    def test_update_returns_false_when_task_not_found(self, repository, mock_cursor, mock_db):
        mock_cursor.rowcount = 0
        
        result = repository.update(999, title="Updated")
        
        assert result is False
    
    def test_delete_removes_task_and_returns_true(self, repository, mock_cursor, mock_db):
        mock_cursor.rowcount = 1
        
        result = repository.delete(1)
        
        assert result is True
        mock_cursor.execute.assert_called_once_with("DELETE FROM task WHERE id = %s", (1,))
        mock_db.commit.assert_called_once()
    
    def test_delete_returns_false_when_not_found(self, repository, mock_cursor):
        mock_cursor.rowcount = 0
        
        result = repository.delete(999)
        
        assert result is False
    
    def test_count_all_returns_total_count(self, repository, mock_cursor):
        mock_cursor.fetchone.return_value = {'count': 5}
        
        result = repository.count_all()
        
        assert result == 5
        mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) as count FROM task")
    
    def test_count_by_status_completed(self, repository, mock_cursor):
        mock_cursor.fetchone.return_value = {'count': 3}
        
        result = repository.count_by_status(True)
        
        assert result == 3
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) as count FROM task WHERE completed = %s", (True,)
        )
    
    def test_count_by_status_active(self, repository, mock_cursor):
        mock_cursor.fetchone.return_value = {'count': 2}
        
        result = repository.count_by_status(False)
        
        assert result == 2
