import React from 'react';
import { FaFlag, FaClock, FaTimes } from 'react-icons/fa';

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

type PriorityType = 'low' | 'normal' | 'urgent';

interface EditTaskModalProps {
  task: Task;
  onClose: () => void;
  onSave: (taskData: Partial<Task>) => void;
  styles: any;
}

const EditTaskModal: React.FC<EditTaskModalProps> = ({ task, onClose, onSave, styles }) => {
  const [editingTask, setEditingTask] = React.useState<Task>({
    ...task,
    // Fix the date format for datetime-local input
    due_date: task.due_date ? new Date(task.due_date).toISOString().slice(0, 16) : null
  });

  const handleSave = () => {
    onSave({
      title: editingTask.title,
      description: editingTask.description,
      priority: editingTask.priority,
      due_date: editingTask.due_date || ''
    });
  };

  return (
    <div
      style={{
        position: 'fixed',
        top: 0,
        left: 0,
        right: 0,
        bottom: 0,
        backgroundColor: 'rgba(0, 0, 0, 0.5)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        zIndex: 1000,
        animation: 'fadeIn 0.2s ease-out',
        padding: '20px',
        boxSizing: 'border-box'
      }}
      onClick={onClose}
    >
      <div
        style={{
          backgroundColor: 'white',
          borderRadius: '16px',
          padding: '32px',
          maxWidth: '500px',
          width: '100%',
          maxHeight: '90vh',
          overflowY: 'auto',
          boxShadow: '0 20px 60px rgba(0, 0, 0, 0.3)',
          animation: 'slideUp 0.3s ease-out',
          position: 'relative'
        }}
        onClick={(e) => e.stopPropagation()}
      >
        <div style={{
          display: 'flex',
          justifyContent: 'space-between',
          alignItems: 'center',
          marginBottom: '24px'
        }}>
          <h2 style={{
            margin: 0,
            fontSize: '24px',
            fontWeight: 600,
            color: '#1a1a1a'
          }}>
            Edit Task
          </h2>
          <button
            onClick={onClose}
            style={{
              background: 'none',
              border: 'none',
              fontSize: '24px',
              cursor: 'pointer',
              color: '#657786',
              padding: '4px',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.color = '#1a1a1a';
              e.currentTarget.style.transform = 'rotate(90deg)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.color = '#657786';
              e.currentTarget.style.transform = 'rotate(0deg)';
            }}
          >
            <FaTimes />
          </button>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={styles.label}>Task Title *</label>
          <input
            type="text"
            value={editingTask.title}
            onChange={(e) => setEditingTask({ ...editingTask, title: e.target.value })}
            style={styles.input}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={styles.label}>Description</label>
          <textarea
            value={editingTask.description}
            onChange={(e) => setEditingTask({ ...editingTask, description: e.target.value })}
            style={styles.textarea}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={styles.label}>
            <FaFlag style={{ marginRight: '6px' }} />
            Priority
          </label>
          <select
            value={editingTask.priority}
            onChange={(e) => setEditingTask({ ...editingTask, priority: e.target.value as PriorityType })}
            style={{ ...styles.input, cursor: 'pointer' }}
          >
            <option value="low">🟢 Low Priority</option>
            <option value="normal">🔵 Normal Priority</option>
            <option value="urgent">🔴 Urgent Priority</option>
          </select>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <label style={styles.label}>
            <FaClock style={{ marginRight: '6px' }} />
            Due Date
          </label>
          <input
            type="datetime-local"
            value={editingTask.due_date || ''}
            onChange={(e) => setEditingTask({ ...editingTask, due_date: e.target.value || null })}
            style={styles.input}
            onFocus={(e) => e.target.style.borderColor = '#1da1f2'}
            onBlur={(e) => e.target.style.borderColor = '#e1e8ed'}
          />
        </div>

        <div style={{
          display: 'flex',
          gap: '12px',
          marginTop: '24px'
        }}>
          <button
            onClick={onClose}
            style={{
              flex: 1,
              padding: '12px',
              fontSize: '15px',
              fontWeight: 600,
              color: '#657786',
              backgroundColor: '#f7f9fc',
              border: '1px solid #e1e8ed',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#e1e8ed';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#f7f9fc';
            }}
          >
            Cancel
          </button>
          <button
            onClick={handleSave}
            style={{
              flex: 1,
              padding: '12px',
              fontSize: '15px',
              fontWeight: 600,
              color: 'white',
              backgroundColor: '#1da1f2',
              border: 'none',
              borderRadius: '8px',
              cursor: 'pointer',
              transition: 'all 0.2s'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.backgroundColor = '#1a91da';
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 4px 12px rgba(29, 161, 242, 0.3)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.backgroundColor = '#1da1f2';
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = 'none';
            }}
          >
            Save Changes
          </button>
        </div>

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
          `}
        </style>
      </div>
    </div>
  );
};

export default EditTaskModal;