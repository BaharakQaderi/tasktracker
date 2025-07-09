import React, { useState } from 'react';

const TaskItem = ({ task, onUpdate, onComplete, onDelete }) => {
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState('');

  const formatDate = (dateString) => {
    return new Date(dateString).toLocaleDateString('en-US', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    });
  };

  const handleEdit = () => {
    setIsEditing(true);
    setEditTitle(task.title);
    setError('');
  };

  const handleCancelEdit = () => {
    setIsEditing(false);
    setEditTitle(task.title);
    setError('');
  };

  const handleSaveEdit = async () => {
    const trimmedTitle = editTitle.trim();
    if (!trimmedTitle) {
      setError('Task title cannot be empty');
      return;
    }

    if (trimmedTitle.length > 200) {
      setError('Task title must be 200 characters or less');
      return;
    }

    if (trimmedTitle === task.title) {
      setIsEditing(false);
      return;
    }

    setIsLoading(true);
    setError('');

    try {
      await onUpdate(task.id, { title: trimmedTitle });
      setIsEditing(false);
    } catch (err) {
      setError(err.message || 'Failed to update task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleComplete = async () => {
    if (task.completed) return;

    setIsLoading(true);
    try {
      await onComplete(task.id);
    } catch (err) {
      setError(err.message || 'Failed to complete task');
    } finally {
      setIsLoading(false);
    }
  };

  const handleDelete = async () => {
    if (!window.confirm('Are you sure you want to delete this task?')) {
      return;
    }

    setIsLoading(true);
    try {
      await onDelete(task.id);
    } catch (err) {
      setError(err.message || 'Failed to delete task');
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e) => {
    if (e.key === 'Enter') {
      handleSaveEdit();
    } else if (e.key === 'Escape') {
      handleCancelEdit();
    }
  };

  return (
    <div className={`bg-white rounded-lg p-4 shadow-sm border border-gray-200 transition-all duration-200 hover:shadow-md ${task.completed ? 'opacity-75' : ''} fade-in`}>
      <div className="flex items-start space-x-3">
        {/* Completion Checkbox */}
        <button
          onClick={handleComplete}
          disabled={task.completed || isLoading}
          className={`mt-1 flex-shrink-0 w-5 h-5 rounded border-2 flex items-center justify-center transition-all duration-200 ${
            task.completed
              ? 'bg-green-500 border-green-500 text-white'
              : 'border-gray-300 hover:border-primary-500 hover:bg-primary-50'
          } ${isLoading ? 'opacity-50 cursor-not-allowed' : 'cursor-pointer'}`}
        >
          {task.completed && (
            <svg className="w-3 h-3" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={3} d="M5 13l4 4L19 7" />
            </svg>
          )}
        </button>

        {/* Task Content */}
        <div className="flex-1 min-w-0">
          {isEditing ? (
            <div className="space-y-2">
              <input
                type="text"
                value={editTitle}
                onChange={(e) => setEditTitle(e.target.value)}
                onKeyDown={handleKeyPress}
                className="w-full px-2 py-1 border border-gray-300 rounded focus:outline-none focus:ring-2 focus:ring-primary-500 focus:border-primary-500"
                disabled={isLoading}
                maxLength={200}
                autoFocus
              />
              <div className="flex items-center space-x-2">
                <button
                  onClick={handleSaveEdit}
                  disabled={isLoading}
                  className="px-2 py-1 bg-primary-500 text-white text-xs rounded hover:bg-primary-600 disabled:opacity-50"
                >
                  {isLoading ? 'Saving...' : 'Save'}
                </button>
                <button
                  onClick={handleCancelEdit}
                  disabled={isLoading}
                  className="px-2 py-1 bg-gray-300 text-gray-700 text-xs rounded hover:bg-gray-400"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <>
              <h3 className={`text-lg font-medium ${task.completed ? 'line-through text-gray-500' : 'text-gray-900'}`}>
                {task.title}
              </h3>
              <div className="flex items-center space-x-4 mt-1">
                <span className="text-xs text-gray-500">
                  Created: {formatDate(task.created_at)}
                </span>
                {task.updated_at !== task.created_at && (
                  <span className="text-xs text-gray-500">
                    Updated: {formatDate(task.updated_at)}
                  </span>
                )}
                {task.completed && (
                  <span className="inline-flex items-center px-2 py-0.5 rounded-full text-xs font-medium bg-green-100 text-green-800">
                    ✅ Completed
                  </span>
                )}
              </div>
            </>
          )}

          {error && (
            <div className="mt-2 p-2 bg-red-50 border border-red-200 rounded text-xs text-red-600">
              {error}
            </div>
          )}
        </div>

        {/* Action Buttons */}
        {!isEditing && (
          <div className="flex items-center space-x-1">
            {!task.completed && (
              <button
                onClick={handleEdit}
                disabled={isLoading}
                className="p-2 text-gray-400 hover:text-primary-500 hover:bg-primary-50 rounded transition-colors disabled:opacity-50"
                title="Edit task"
              >
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z" />
                </svg>
              </button>
            )}
            
            <button
              onClick={handleDelete}
              disabled={isLoading}
              className="p-2 text-gray-400 hover:text-red-500 hover:bg-red-50 rounded transition-colors disabled:opacity-50"
              title="Delete task"
            >
              {isLoading ? (
                <div className="animate-spin rounded-full h-4 w-4 border-b-2 border-gray-400"></div>
              ) : (
                <svg className="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16" />
                </svg>
              )}
            </button>
          </div>
        )}
      </div>
    </div>
  );
};

export default TaskItem;
