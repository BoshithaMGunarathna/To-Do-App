from typing import List, Optional, Dict, Any
from mysql.connector import MySQLConnection
from mysql.connector.cursor import MySQLCursorDict


class TaskRepository:
    def __init__(self, db_connection: MySQLConnection):
        self.db = db_connection
    
    def get_cursor(self) -> MySQLCursorDict:
        return self.db.cursor(dictionary=True)
    
    def find_all(self) -> List[Dict[str, Any]]:
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT * FROM task ORDER BY created_at DESC")
            return cursor.fetchall()
        finally:
            cursor.close()
    
    def find_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT * FROM task WHERE id = %s", (task_id,))
            return cursor.fetchone()
        finally:
            cursor.close()
    
    def create(self, title: str, description: str, completed: bool = False, 
               priority: str = 'normal', due_date: Optional[str] = None) -> int:
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
        cursor = self.get_cursor()
        try:
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
                return False
            
            params.append(task_id)
            query = f"UPDATE task SET {', '.join(update_fields)} WHERE id = %s"
            
            cursor.execute(query, tuple(params))
            self.db.commit()
            
            return cursor.rowcount > 0
        finally:
            cursor.close()
    
    def delete(self, task_id: int) -> bool:
        cursor = self.get_cursor()
        try:
            cursor.execute("DELETE FROM task WHERE id = %s", (task_id,))
            self.db.commit()
            return cursor.rowcount > 0
        finally:
            cursor.close()
    
    def count_all(self) -> int:
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM task")
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
    
    def count_by_status(self, completed: bool) -> int:
        cursor = self.get_cursor()
        try:
            cursor.execute("SELECT COUNT(*) as count FROM task WHERE completed = %s", (completed,))
            result = cursor.fetchone()
            return result['count'] if result else 0
        finally:
            cursor.close()
