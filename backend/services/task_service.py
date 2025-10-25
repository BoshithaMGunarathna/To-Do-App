from typing import List, Optional, Dict, Any
from repositories.task_repository import TaskRepository


class TaskService:
    
    def __init__(self, task_repository: TaskRepository):
        self.repository = task_repository
    
    def get_all_tasks(self) -> List[Dict[str, Any]]:
        return self.repository.find_all()
    
    def get_task_by_id(self, task_id: int) -> Optional[Dict[str, Any]]:
        return self.repository.find_by_id(task_id)
    
    def create_task(self, title: str, description: str = "", priority: str = 'normal', 
                    due_date: Optional[str] = None) -> Dict[str, Any]:
        
        if not title or not title.strip():
            raise ValueError("Task title is required")
        
        if len(title.strip()) > 255:
            raise ValueError("Task title must be 255 characters or less")
        
        if len(description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")
        
        if priority not in ['low', 'normal', 'urgent']:
            raise ValueError("Priority must be 'low', 'normal', or 'urgent'")
        
        task_id = self.repository.create(
            title=title.strip(),
            description=description.strip(),
            completed=False,
            priority=priority,
            due_date=due_date
        )
        
        return self.repository.find_by_id(task_id)
    
    def update_task(self, task_id: int, title: Optional[str] = None,
                   description: Optional[str] = None, 
                   completed: Optional[bool] = None,
                   priority: Optional[str] = None,
                   due_date: Optional[str] = None) -> Optional[Dict[str, Any]]:
        
        existing_task = self.repository.find_by_id(task_id)
        if not existing_task:
            return None
        
        if title is not None:
            if not title.strip():
                raise ValueError("Task title cannot be empty")
            if len(title.strip()) > 255:
                raise ValueError("Task title must be 255 characters or less")
        
        if description is not None and len(description) > 1000:
            raise ValueError("Task description must be 1000 characters or less")
        
        if priority is not None and priority not in ['low', 'normal', 'urgent']:
            raise ValueError("Priority must be 'low', 'normal', or 'urgent'")
        
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
        task = self.repository.find_by_id(task_id)
        if not task:
            return None
        
        new_status = not task['completed']
        self.repository.update(task_id, completed=new_status)
        
        return self.repository.find_by_id(task_id)
    
    def delete_task(self, task_id: int) -> bool:
        return self.repository.delete(task_id)
    
    def get_task_statistics(self) -> Dict[str, int]:
        total = self.repository.count_all()
        completed = self.repository.count_by_status(True)
        active = self.repository.count_by_status(False)
        
        return {
            'total': total,
            'active': active,
            'completed': completed
        }
