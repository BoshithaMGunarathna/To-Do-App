"""
Service layer for Task business logic.
Follows Service Pattern for business logic abstraction.
"""
from typing import List, Optional, Dict, Any
from repositories.task_repository import TaskRepository


class TaskService:
    """
    Task Service - handles business logic for task operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self, task_repository: TaskRepository):
        """
        Initialize service with task repository.
        Uses Dependency Injection for loose coupling.
        
        Args:
            task_repository: Repository for task data access
        """
        self.repository = task_repository
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        """
        Get all tasks.
        
        Returns:
            List of all tasks
        """
        return self.repository.find_all()
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Get a specific task by ID.
        
        Args:
            task_id: The task ID
            
        Returns:
            Task if found, None otherwise
        """
        return self.repository.find_by_id(task_id)
    
    def create_task(self, title: str, description: str = "", priority: str = 'normal', 
                    due_date: Optional[str] = None) -> Dict[str, Any]:
        """
        Create a new task with validation.
        
        Args:
            title: Task title (required)
            description: Task description (optional)
            priority: Task priority - 'low', 'normal', or 'urgent' (default: 'normal')
            due_date: Optional due date in ISO format
            
        Returns:
            Created task with ID
            
        Raises:
            ValueError: If title is empty or invalid
        """
        # Validation
        if not title or not title.strip():
            raise ValueError("Task title is required")
        
        if len(title.strip()) > 255:
            raise ValueError("Task title must be 255 characters or less")
        
        if len(description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")
        
        if priority not in ['low', 'normal', 'urgent']:
            raise ValueError("Priority must be 'low', 'normal', or 'urgent'")
        
        # Create task
        task_id = self.repository.create(
            title=title.strip(),
            description=description.strip(),
            completed=False,
            priority=priority,
            due_date=due_date
        )
        
        # Return created task
        return self.repository.find_by_id(task_id)
    
    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, 
                   completed: Optional[bool] = None,
                   priority: Optional[str] = None,
                   due_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            priority: New priority - 'low', 'normal', or 'urgent' (optional)
            due_date: New due date in ISO format or '' to clear (optional)
            
        Returns:
            Updated task if found, None otherwise
            
        Raises:
            ValueError: If validation fails
        """
        # Check if task exists
        existing_task = self.repository.find_by_id(task_id)
        if not existing_task:
            return None
        
        # Validation
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title.strip()) > 255:
                raise ValueError("Task title must be 255 characters or less")
        
        if description is not None and len(description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")
        
        if priority is not None and priority not in ['low', 'normal', 'urgent']:
            raise ValueError("Priority must be 'low', 'normal', or 'urgent'")
        
        # Update task
        success = self.repository.update(
            task_id=task_id,
            title=title.strip() if title else None,
            description=description.strip() if description else None,
            completed=completed,
            priority=priority,
            due_date=due_date if due_date != '' else None
        )
        
        if success:
            return self.repository.find_by_id(task_id)
        return None
    
    def toggle_task_completion(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Toggle the completion status of a task.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self.repository.find_by_id(task_id)
        if not task:
            return None
        
        new_status = not task['completed']
        self.repository.update(task_id, completed=new_status)
        
        return self.repository.find_by_id(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        """
        Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        return self.repository.delete(task_id)
    
    def get_task_statistics(self) -> Dict[str, int]:
        """
        Get task statistics.
        
        Returns:
            Dictionary with task counts (total, active, completed)
        """
        total = self.repository.count_all()
        completed = self.repository.count_by_status(True)
        active = self.repository.count_by_status(False)
        
        return {
            'total': total,
            'active': active,
            'completed': completed
        }
