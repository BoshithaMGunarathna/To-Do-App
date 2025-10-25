import React, { useEffect, useState } from 'react';
import axios from 'axios';
import { toast } from 'react-toastify';
import { 
  FaCheck, 
  FaEdit, 
  FaTrash, 
  FaUndo, 
  FaPlus,
  FaFlag,
  FaClock
} from 'react-icons/fa';
import { getTaskListStyles } from './TaskList.styles';
import EditTaskModal from './components/EditTaskModal';

interface Task {
  id: number;
  title: string;
  description: string;
  completed: boolean;
  priority: 'low' | 'normal' | 'urgent';
  due_date: string | null;
  created_at: string;
  updated_at: string;
}

type FilterType = 'all' | 'active' | 'completed';
type PriorityType = 'low' | 'normal' | 'urgent';

const TaskList: React.FC = () => {
  const [tasks, setTasks] = useState<Task[]>([]);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');
  const [priority, setPriority] = useState<PriorityType>('normal');
  const [dueDate, setDueDate] = useState('');
  const [filter, setFilter] = useState<FilterType>('all');
  const [loading, setLoading] = useState(false);
  const [, setWindowWidth] = useState(window.innerWidth);
  const [editingTask, setEditingTask] = useState<Task | null>(null);
  const [showEditModal, setShowEditModal] = useState(false);

  // Handle window resize 
  useEffect(() => {
    const handleResize = () => setWindowWidth(window.innerWidth);
    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  const fetchTasks = async () => {
    try {
      const res = await axios.get('http://localhost:5000/tasks');
      setTasks(res.data);
    } catch (error) {
      console.error('Error fetching tasks:', error);
    }
  };

  useEffect(() => {
    fetchTasks();
  }, []);

  const addTask = async () => {
    if (!title.trim()) {
      toast.error('Please enter a task title', {
        position: 'top-right',
        autoClose: 3000,
      });
      return;
    }

    setLoading(true);
    try {
      await axios.post('http://localhost:5000/tasks', { 
        title: title.trim(), 
        description: description.trim(),
        priority,
        due_date: dueDate || null
      });
      setTitle('');
      setDescription('');
      setPriority('normal');
      setDueDate('');
      await fetchTasks();
      toast.success('Task added successfully!', {
        position: 'top-right',
        autoClose: 3000,
      });
    } catch (error: any) {
      console.error('Error adding task:', error);
      const errorMessage = error.response?.data?.error || 'Failed to add task';
      toast.error(errorMessage, {
        position: 'top-right',
        autoClose: 4000,
      });
    } finally {
      setLoading(false);
    }
  };

  const updateTask = async (taskData: Partial<Task>) => {
    if (!editingTask) return;

    try {
      await axios.put(`http://localhost:5000/tasks/${editingTask.id}`, taskData);
      await fetchTasks();
      setShowEditModal(false);
      setEditingTask(null);
      toast.success('Task updated successfully! ✅', {
        position: 'top-right',
        autoClose: 2000,
      });
    } catch (error: any) {
      console.error('Error updating task:', error);
      const errorMessage = error.response?.data?.error || 'Failed to update task';
      toast.error(errorMessage, {
        position: 'top-right',
        autoClose: 4000,
      });
    }
  };

  const toggleTask = async (task: Task) => {
    try {
      await axios.put(`http://localhost:5000/tasks/${task.id}`, { 
        completed: !task.completed 
      });
      await fetchTasks();
      toast.success(
        !task.completed ? 'Task completed! ✅' : 'Task reopened! ',
        {
          position: 'top-right',
          autoClose: 2000,
        }
      );
    } catch (error: any) {
      console.error('Error updating task:', error);
      const errorMessage = error.response?.data?.error || 'Failed to update task';
      toast.error(errorMessage, {
        position: 'top-right',
        autoClose: 4000,
      });
    }
  };

  const deleteTask = async (id: number, taskTitle: string) => {
    toast.info(
      <div style={{ display: 'flex', flexDirection: 'column', gap: '12px' }}>
        <div>Delete "{taskTitle}"?</div>
        <div style={{ display: 'flex', gap: '8px', justifyContent: 'flex-end' }}>
          <button
            onClick={() => toast.dismiss()}
            style={{
              padding: '6px 12px',
              backgroundColor: '#e1e8ed',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 600,
            }}
          >
            Cancel
          </button>
          <button
            onClick={async () => {
              toast.dismiss();
              try {
                await axios.delete(`http://localhost:5000/tasks/${id}`);
                await fetchTasks();
                toast.success('Task deleted successfully! ', {
                  position: 'top-right',
                  autoClose: 3000,
                });
              } catch (error: any) {
                console.error('Error deleting task:', error);
                const errorMessage = error.response?.data?.error || 'Failed to delete task';
                toast.error(errorMessage, {
                  position: 'top-right',
                  autoClose: 4000,
                });
              }
            }}
            style={{
              padding: '6px 12px',
              backgroundColor: '#e0245e',
              color: 'white',
              border: 'none',
              borderRadius: '6px',
              cursor: 'pointer',
              fontSize: '13px',
              fontWeight: 600,
            }}
          >
            Delete
          </button>
        </div>
      </div>,
      {
        position: 'top-center',
        autoClose: false,
        closeButton: false,
        closeOnClick: false,
        draggable: false,
      }
    );
  };

  const openEditModal = (task: Task) => {
    setEditingTask(task);
    setShowEditModal(true);
  };

  const isUrgent = (task: Task) => {
    if (!task.due_date || task.completed) return false;
    const now = new Date();
    const dueDate = new Date(task.due_date);
    const hoursUntilDue = (dueDate.getTime() - now.getTime()) / (1000 * 60 * 60);
    return hoursUntilDue <= 24 && hoursUntilDue >= 0;
  };

  const isOverdue = (task: Task) => {
    if (!task.due_date || task.completed) return false;
    const now = new Date();
    const dueDate = new Date(task.due_date);
    return dueDate < now;
  };

  const filteredTasks = tasks.filter(task => {
    if (filter === 'active') return !task.completed;
    if (filter === 'completed') return task.completed;
    return true;
  });

  const activeTasks = tasks.filter(t => !t.completed);
  const completedTasks = tasks.filter(t => t.completed);

  const priorityColors = {
    low: { bg: '#e8f5e9', text: '#2e7d32', icon: '#4caf50' },
    normal: { bg: '#e3f2fd', text: '#1565c0', icon: '#2196f3' },
    urgent: { bg: '#ffebee', text: '#c62828', icon: '#f44336' }
  };

  const styles = getTaskListStyles(loading);

  return (
    <div style={styles.container}>
      <div style={styles.leftPanel}>
        <div style={styles.title}>Create Task</div>
        <div style={styles.subtitle}>Add a new task to your list</div>
        
        <div style={styles.inputGroup}>
          <label style={styles.label}>Task Title *</label>
          <input 
            type="text"
            value={title} 
            onChange={e => setTitle(e.target.value)}
            onKeyPress={e => e.key === 'Enter' && !e.shiftKey && addTask()}
            placeholder="Enter task title" 
            style={styles.input}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>Description</label>
          <textarea 
            value={description} 
            onChange={e => setDescription(e.target.value)}
            placeholder="Add more details about your task" 
            style={styles.textarea}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>
            <FaFlag style={{ marginRight: '6px' }} />
            Priority
          </label>
          <select
            value={priority}
            onChange={e => setPriority(e.target.value as PriorityType)}
            style={{
              ...styles.input,
              cursor: 'pointer'
            }}
          >
            <option value="low">🟢 Low Priority</option>
            <option value="normal">🔵 Normal Priority</option>
            <option value="urgent">🔴 Urgent Priority</option>
          </select>
        </div>

        <div style={styles.inputGroup}>
          <label style={styles.label}>
            <FaClock style={{ marginRight: '6px' }} />
            Due Date (Optional)
          </label>
          <input
            type="datetime-local"
            value={dueDate}
            onChange={e => setDueDate(e.target.value)}
            style={styles.input}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <button 
          onClick={addTask}
          disabled={loading}
          style={{
            ...styles.addButton,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            gap: '8px',
            transition: 'all 0.3s ease'
          }}
          onMouseEnter={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = '#1a91da';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(29, 161, 242, 0.3)';
            }
          }}
          onMouseLeave={(e) => {
            if (!loading) {
              e.currentTarget.style.backgroundColor = '#1da1f2';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }
          }}
        >
          <FaPlus />
          {loading && <span style={{ marginLeft: '8px' }}>Adding...</span>}
        </button>

        <div style={styles.statsCard}>
          <div style={styles.statsTitle}>Statistics</div>
          <div style={styles.statItem}>
            <span>Total Tasks</span>
            <strong>{tasks.length}</strong>
          </div>
          <div style={styles.statItem}>
            <span>Active</span>
            <strong style={{ color: '#1da1f2' }}>{activeTasks.length}</strong>
          </div>
          <div style={styles.statItem}>
            <span>Completed</span>
            <strong style={{ color: '#17bf63' }}>{completedTasks.length}</strong>
          </div>
        </div>
      </div>

      <div style={styles.rightPanel}>
        <div style={styles.header}>
          <div style={styles.title}>Tasks</div>
          <div style={styles.filterContainer}>
            <button
              onClick={() => setFilter('all')}
              style={{
                ...styles.filterButton(filter === 'all'),
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                if (filter !== 'all') {
                  e.currentTarget.style.backgroundColor = '#f7f9fc';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }
              }}
              onMouseLeave={(e) => {
                if (filter !== 'all') {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.transform = 'translateY(0)';
                }
              }}
            >
              All ({tasks.length})
            </button>
            <button
              onClick={() => setFilter('active')}
              style={{
                ...styles.filterButton(filter === 'active'),
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                if (filter !== 'active') {
                  e.currentTarget.style.backgroundColor = '#f7f9fc';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }
              }}
              onMouseLeave={(e) => {
                if (filter !== 'active') {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.transform = 'translateY(0)';
                }
              }}
            >
              Active ({activeTasks.length})
            </button>
            <button
              onClick={() => setFilter('completed')}
              style={{
                ...styles.filterButton(filter === 'completed'),
                transition: 'all 0.2s ease'
              }}
              onMouseEnter={(e) => {
                if (filter !== 'completed') {
                  e.currentTarget.style.backgroundColor = '#f7f9fc';
                  e.currentTarget.style.transform = 'translateY(-1px)';
                }
              }}
              onMouseLeave={(e) => {
                if (filter !== 'completed') {
                  e.currentTarget.style.backgroundColor = 'transparent';
                  e.currentTarget.style.transform = 'translateY(0)';
                }
              }}
            >
              Completed ({completedTasks.length})
            </button>
          </div>
        </div>

        <div style={styles.taskListContainer}>
          {filteredTasks.length === 0 ? (
            <div style={styles.emptyState}>
              <div style={styles.emptyIcon}>
                {filter === 'all' && '📋'}
                {filter === 'active' && '✨'}
                {filter === 'completed' && '🎉'}
              </div>
              <div style={styles.emptyText}>
                {filter === 'all' && 'No tasks yet. Create your first task!'}
                {filter === 'active' && 'No active tasks. All done!'}
                {filter === 'completed' && 'No completed tasks yet.'}
              </div>
            </div>
          ) : (
            filteredTasks.map(task => {
              const urgent = isUrgent(task);
              const overdue = isOverdue(task);
              const priorityColor = priorityColors[task.priority];

              return (
                <div 
                  key={task.id}
                  style={{
                    ...styles.taskCard(task.completed),
                    borderLeft: `4px solid ${
                      overdue ? '#d32f2f' : 
                      urgent ? '#ff9800' : 
                      priorityColor.icon
                    }`,
                    backgroundColor: overdue ? '#ffebee' : urgent ? '#fff3e0' : '#ffffff',
                    transition: 'all 0.3s ease',
                    animation: 'slideIn 0.3s ease-out'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.boxShadow = '0 6px 20px rgba(0,0,0,0.12)';
                    e.currentTarget.style.transform = 'translateY(-2px)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.boxShadow = 'none';
                    e.currentTarget.style.transform = 'translateY(0)';
                  }}
                >
                  <div style={styles.taskHeader}>
                    <div style={styles.taskContent}>
                      <div style={{
                        display: 'flex',
                        alignItems: 'center',
                        gap: '8px',
                        flexWrap: 'wrap',
                        marginBottom: '8px'
                      }}>
                        <span
                          style={{
                            display: 'inline-flex',
                            alignItems: 'center',
                            gap: '4px',
                            padding: '4px 10px',
                            backgroundColor: priorityColor.bg,
                            color: priorityColor.text,
                            borderRadius: '12px',
                            fontSize: '11px',
                            fontWeight: 600,
                            textTransform: 'uppercase',
                            letterSpacing: '0.5px'
                          }}
                        >
                          <FaFlag size={10} />
                          {task.priority}
                        </span>
                        
                        {task.due_date && (
                          <span
                            style={{
                              display: 'inline-flex',
                              alignItems: 'center',
                              gap: '4px',
                              padding: '4px 10px',
                              backgroundColor: overdue ? '#ffcdd2' : urgent ? '#ffe0b2' : '#e3f2fd',
                              color: overdue ? '#c62828' : urgent ? '#e65100' : '#1565c0',
                              borderRadius: '12px',
                              fontSize: '11px',
                              fontWeight: 600
                            }}
                          >
                            <FaClock size={10} />
                            {overdue ? 'OVERDUE' : urgent ? 'DUE SOON' : 
                              new Date(task.due_date).toLocaleDateString('en-US', {
                                month: 'short',
                                day: 'numeric',
                                hour: '2-digit',
                                minute: '2-digit'
                              })
                            }
                          </span>
                        )}
                      </div>

                      <div style={styles.taskTitle(task.completed)}>
                        {task.title}
                      </div>
                      {task.description && (
                        <div style={styles.taskDescription(task.completed)}>
                          {task.description}
                        </div>
                      )}
                      <div style={styles.taskMeta}>
                        Created {new Date(task.created_at).toLocaleDateString('en-US', { 
                          month: 'short', 
                          day: 'numeric', 
                          year: 'numeric'
                        })}
                      </div>
                    </div>
                    
                    <div style={{
                      ...styles.actionButtons,
                      flexDirection: 'column'
                    }}>
                      <button
                        onClick={() => toggleTask(task)}
                        style={{
                          ...styles.actionButton(task.completed ? 'undo' : 'complete'),
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                          transition: 'all 0.2s ease',
                          minWidth: '100px'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'scale(1.05)';
                          e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                        title={task.completed ? 'Mark as active' : 'Mark as completed'}
                      >
                        {task.completed ? <FaUndo size={12} /> : <FaCheck size={12} />}
                      </button>
                      
                      <button
                        onClick={() => openEditModal(task)}
                        style={{
                          ...styles.actionButton('complete'),
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                          transition: 'all 0.2s ease',
                          backgroundColor: '#1da1f2',
                          minWidth: '100px'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'scale(1.05)';
                          e.currentTarget.style.boxShadow = '0 4px 8px rgba(0,0,0,0.2)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                        title="Edit task"
                      >
                        <FaEdit size={12} />
                      </button>
                      
                      <button
                        onClick={() => deleteTask(task.id, task.title)}
                        style={{
                          ...styles.actionButton('delete'),
                          display: 'flex',
                          alignItems: 'center',
                          justifyContent: 'center',
                          gap: '6px',
                          transition: 'all 0.2s ease',
                          minWidth: '100px'
                        }}
                        onMouseEnter={(e) => {
                          e.currentTarget.style.transform = 'scale(1.05)';
                          e.currentTarget.style.boxShadow = '0 4px 8px rgba(224, 36, 94, 0.3)';
                        }}
                        onMouseLeave={(e) => {
                          e.currentTarget.style.transform = 'scale(1)';
                          e.currentTarget.style.boxShadow = 'none';
                        }}
                        title="Delete task"
                      >
                        <FaTrash size={12} />
                      </button>
                    </div>
                  </div>
                </div>
              );
            })
          )}
        </div>
      </div>

      {/* Edit Task Modal */}
      {showEditModal && editingTask && (
        <EditTaskModal
          task={editingTask}
          onClose={() => {
            setShowEditModal(false);
            setEditingTask(null);
          }}
          onSave={(updatedTask) => {
            updateTask(updatedTask);
            setShowEditModal(false);
            setEditingTask(null);
          }}
          styles={styles}
        />
      )}

      <style>
        {`
          @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
          }

          @keyframes slideUp {
            from {
              opacity: 0;
              transform: translateY(20px);
            }
            to {
              opacity: 1;
              transform: translateY(0);
            }
          }

          @keyframes slideIn {
            from {
              opacity: 0;
              transform: translateX(-10px);
            }
            to {
              opacity: 1;
              transform: translateX(0);
            }
          }
        `}
      </style>
    </div>
  );
};

export default TaskList;
