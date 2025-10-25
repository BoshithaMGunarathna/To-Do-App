import pytest
from unittest.mock import Mock, MagicMock, call
from repositories.task_repository import TaskRepository


@pytest.fixture
def mock_db():
    """Create a mock database connection."""
    return Mock()


@pytest.fixture
def mock_cursor():
    """Create a mock database cursor."""
    cursor = Mock()
    cursor.fetchall = Mock(return_value=[])
    cursor.fetchone = Mock(return_value=None)
    cursor.lastrowid = 1
    cursor.rowcount = 1
    return cursor


@pytest.fixture
def repository(mock_db, mock_cursor):
    """Create TaskRepository with mocked database."""
    mock_db.cursor.return_value = mock_cursor
    return TaskRepository(mock_db)


class TestTaskRepository:
    """Test suite for TaskRepository."""
    
    def test_find_all_returns_all_tasks(self, repository, mock_cursor):
        """Test finding all tasks returns correct data."""
        # Arrange
        expected_tasks = [
            {'id': 1, 'title': 'Task 1', 'description': 'Desc 1', 'completed': False},
            {'id': 2, 'title': 'Task 2', 'description': 'Desc 2', 'completed': True}
        ]
        mock_cursor.fetchall.return_value = expected_tasks
        
        # Act
        result = repository.find_all()
        
        # Assert
        assert result == expected_tasks
        mock_cursor.execute.assert_called_once_with("SELECT * FROM task ORDER BY created_at DESC")
        mock_cursor.close.assert_called_once()
    
    def test_find_by_id_returns_task_when_found(self, repository, mock_cursor):
        """Test finding task by ID returns task when it exists."""
        # Arrange
        expected_task = {'id': 1, 'title': 'Task 1', 'description': 'Desc 1', 'completed': False}
        mock_cursor.fetchone.return_value = expected_task
        
        # Act
        result = repository.find_by_id(1)
        
        # Assert
        assert result == expected_task
        mock_cursor.execute.assert_called_once_with("SELECT * FROM task WHERE id = %s", (1,))
        mock_cursor.close.assert_called_once()
    
    def test_find_by_id_returns_none_when_not_found(self, repository, mock_cursor):
        """Test finding task by ID returns None when not found."""
        # Arrange
        mock_cursor.fetchone.return_value = None
        
        # Act
        result = repository.find_by_id(999)
        
        # Assert
        assert result is None
        mock_cursor.execute.assert_called_once()
    
    def test_create_inserts_task_and_returns_id(self, repository, mock_cursor, mock_db):
        """Test creating task inserts into database and returns ID."""
        # Arrange
        mock_cursor.lastrowid = 42
        
        # Act
        result = repository.create("New Task", "Description", False)
        
        # Assert
        assert result == 42
        mock_cursor.execute.assert_called_once_with(
            "INSERT INTO task (title, description, completed) VALUES (%s, %s, %s)",
            ("New Task", "Description", False)
        )
        mock_db.commit.assert_called_once()
        mock_cursor.close.assert_called_once()
    
    def test_update_with_all_fields(self, repository, mock_cursor, mock_db):
        """Test updating task with all fields."""
        # Arrange
        mock_cursor.rowcount = 1
        
        # Act
        result = repository.update(1, title="Updated", description="New desc", completed=True)
        
        # Assert
        assert result is True
        mock_cursor.execute.assert_called_once()
        assert "UPDATE task SET" in mock_cursor.execute.call_args[0][0]
        mock_db.commit.assert_called_once()
    
    def test_update_with_partial_fields(self, repository, mock_cursor, mock_db):
        """Test updating task with only some fields."""
        # Arrange
        mock_cursor.rowcount = 1
        
        # Act
        result = repository.update(1, completed=True)
        
        # Assert
        assert result is True
        mock_cursor.execute.assert_called_once()
        call_args = mock_cursor.execute.call_args[0]
        assert "completed = %s" in call_args[0]
        assert call_args[1] == (True, 1)
    
    def test_update_returns_false_when_no_fields(self, repository, mock_cursor):
        """Test update returns False when no fields provided."""
        # Act
        result = repository.update(1)
        
        # Assert
        assert result is False
        mock_cursor.execute.assert_not_called()
    
    def test_update_returns_false_when_task_not_found(self, repository, mock_cursor, mock_db):
        """Test update returns False when task doesn't exist."""
        # Arrange
        mock_cursor.rowcount = 0
        
        # Act
        result = repository.update(999, title="Updated")
        
        # Assert
        assert result is False
    
    def test_delete_removes_task_and_returns_true(self, repository, mock_cursor, mock_db):
        """Test deleting task removes it and returns True."""
        # Arrange
        mock_cursor.rowcount = 1
        
        # Act
        result = repository.delete(1)
        
        # Assert
        assert result is True
        mock_cursor.execute.assert_called_once_with("DELETE FROM task WHERE id = %s", (1,))
        mock_db.commit.assert_called_once()
    
    def test_delete_returns_false_when_not_found(self, repository, mock_cursor):
        """Test delete returns False when task doesn't exist."""
        # Arrange
        mock_cursor.rowcount = 0
        
        # Act
        result = repository.delete(999)
        
        # Assert
        assert result is False
    
    def test_count_all_returns_total_count(self, repository, mock_cursor):
        """Test counting all tasks returns correct count."""
        # Arrange
        mock_cursor.fetchone.return_value = {'count': 5}
        
        # Act
        result = repository.count_all()
        
        # Assert
        assert result == 5
        mock_cursor.execute.assert_called_once_with("SELECT COUNT(*) as count FROM task")
    
    def test_count_by_status_completed(self, repository, mock_cursor):
        """Test counting completed tasks."""
        # Arrange
        mock_cursor.fetchone.return_value = {'count': 3}
        
        # Act
        result = repository.count_by_status(True)
        
        # Assert
        assert result == 3
        mock_cursor.execute.assert_called_once_with(
            "SELECT COUNT(*) as count FROM task WHERE completed = %s", (True,)
        )
    
    def test_count_by_status_active(self, repository, mock_cursor):
        """Test counting active tasks."""
        # Arrange
        mock_cursor.fetchone.return_value = {'count': 2}
        
        # Act
        result = repository.count_by_status(False)
        
        # Assert
        assert result == 2
