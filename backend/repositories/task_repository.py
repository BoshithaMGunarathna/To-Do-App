"""
Repository layer for Task data access.
Follows Repository Pattern for data access abstraction.
"""
from typing import List, Optional, Dict, Any
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict


class TaskRepository:
    """
    Task Repository - handles all database operations for tasks.
    Follows Single Responsibility Principle (SRP).
    """
    
    def __init__(self, db_connection: MySQLConnection):
        """
        Initialize repository with database connection.
        Uses Dependency Injection for loose coupling.
        """
        self.db = db_connection
    
    def get_cursor(self) -> MySQLCursorDict:
        """Get a new cursor for database operations."""
        return self.db.cursor(dictionary=True)
    
    def find_all(self) -> List[Dict[str, Any]]:
        """
        Retrieve all tasks ordered by creation date (newest first).
        
        Returns:
            List of task dictionaries
        """
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT * FROM task ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def find_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        """
        Find a task by its ID.
        
        Args:
            task_id: The task ID to search for
            
        Returns:
            Task dictionary if found, None otherwise
        """
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def create(self, title: str, description: str, completed: bool = False, 
               priority: str = 'normal', due_date: Optional[str] = None) -> int:
        """
        Create a new task.
        
        Args:
            title: Task title
            description: Task description
            completed: Initial completion status (default: False)
            priority: Task priority - 'low', 'normal', or 'urgent' (default: 'normal')
            due_date: Optional due date in ISO format (YYYY-MM-DD HH:MM:SS)
            
        Returns:
            ID of the newly created task
        """
        cursor = self.get_cursor()
        try:
            cursor.execute(
                "INSERT INTO task (title, description, completed, priority, due_date) VALUES (%s, %s, %s, %s, %s)",
                (title, description, completed, priority, due_date)
            )
            self.db.commit()
            return cursor.lastrowid
        finally:
            cursor.close()
    
    def update(self, task_id: int, title: Optional[str] = None, 
               description: Optional[str] = None, completed: Optional[bool] = None,
               priority: Optional[str] = None, due_date: Optional[str] = None) -> bool:
        """
        Update an existing task.
        
        Args:
            task_id: ID of the task to update
            title: New title (optional)
            description: New description (optional)
            completed: New completion status (optional)
            priority: New priority - 'low', 'normal', or 'urgent' (optional)
            due_date: New due date in ISO format or None to clear (optional)
            
        Returns:
            True if task was updated, False if not found
        """
        cursor = self.get_cursor()
        try:
            # Build dynamic update query based on provided fields
            update_fields = []
            params = []
            
            if title is not None:
                update_fields.append("title = %s")
                params.append(title)
            
            if description is not None:
                update_fields.append("description = %s")
                params.append(description)
            
            if completed is not None:
                update_fields.append("completed = %s")
                params.append(completed)
            
            if priority is not None:
                update_fields.append("priority = %s")
                params.append(priority)
            
            if due_date is not None:
                update_fields.append("due_date = %s")
                params.append(due_date if due_date else None)
            
            if not update_fields:
                return False  # No fields to update
            
            params.append(task_id)
            query = f"UPDATE task SET {', '.join(update_fields)} WHERE id = %s"
            
            cursor.execute(query, tuple(params))
            self.db.commit()
            
            return cursor.rowcount > 0
        finally:
            cursor.close()
    
    def delete(self, task_id: int) -> bool:
        """
        Delete a task by ID.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False if not found
        """
        cursor = self.get_cursor()
        try:
            cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
    
    def count_all(self) -> int:
        """Get total count of all tasks."""
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM task")
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
    
    def count_by_status(self, completed: bool) -> int:
        """
        Get count of tasks by completion status.
        
        Args:
            completed: True for completed tasks, False for active tasks
            
        Returns:
            Count of tasks
        """
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM task WHERE completed = %s", (completed,))
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
