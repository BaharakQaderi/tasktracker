import React, { useState, useEffect } from 'react';
import TaskList from './components/TaskList';
import TaskForm from './components/TaskForm';
import TaskStats from './components/TaskStats';
import Header from './components/Header';
import { taskService } from './services/taskService';

function App() {
  const [tasks, setTasks] = useState([]);
  const [stats, setStats] = useState({ total: 0, completed: 0, pending: 0 });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [filter, setFilter] = useState('all'); // 'all', 'pending', 'completed'

  // Load tasks on component mount
  useEffect(() => {
    loadTasks();
  }, [filter]);

  const loadTasks = async () => {
    try {
      setLoading(true);
      setError(null);
      
      const filterParam = filter === 'all' ? null : filter === 'completed';
      const data = await taskService.getTasks(0, 100, filterParam);
      
      setTasks(data.tasks);
      setStats({
        total: data.total,
        completed: data.completed,
        pending: data.pending
      });
    } catch (err) {
      console.error('Error loading tasks:', err);
      setError('Failed to load tasks. Please try again.');
    } finally {
      setLoading(false);
    }
  };

  const handleCreateTask = async (taskData) => {
    try {
      const newTask = await taskService.createTask(taskData);
      setTasks(prevTasks => [newTask, ...prevTasks]);
      
      // Update stats
      setStats(prevStats => ({
        total: prevStats.total + 1,
        completed: prevStats.completed,
        pending: prevStats.pending + 1
      }));
      
      return newTask;
    } catch (err) {
      console.error('Error creating task:', err);
      throw new Error('Failed to create task. Please try again.');
    }
  };

  const handleUpdateTask = async (taskId, updateData) => {
    try {
      const updatedTask = await taskService.updateTask(taskId, updateData);
      
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? updatedTask : task
        )
      );
      
      // Recalculate stats
      await loadTasks();
      
      return updatedTask;
    } catch (err) {
      console.error('Error updating task:', err);
      throw new Error('Failed to update task. Please try again.');
    }
  };

  const handleCompleteTask = async (taskId) => {
    try {
      const completedTask = await taskService.completeTask(taskId);
      
      setTasks(prevTasks =>
        prevTasks.map(task =>
          task.id === taskId ? completedTask : task
        )
      );
      
      // Update stats
      setStats(prevStats => ({
        total: prevStats.total,
        completed: prevStats.completed + 1,
        pending: prevStats.pending - 1
      }));
      
      return completedTask;
    } catch (err) {
      console.error('Error completing task:', err);
      throw new Error('Failed to complete task. Please try again.');
    }
  };

  const handleDeleteTask = async (taskId) => {
    try {
      await taskService.deleteTask(taskId);
      
      const taskToDelete = tasks.find(task => task.id === taskId);
      setTasks(prevTasks => prevTasks.filter(task => task.id !== taskId));
      
      // Update stats
      setStats(prevStats => ({
        total: prevStats.total - 1,
        completed: taskToDelete?.completed ? prevStats.completed - 1 : prevStats.completed,
        pending: taskToDelete?.completed ? prevStats.pending : prevStats.pending - 1
      }));
    } catch (err) {
      console.error('Error deleting task:', err);
      throw new Error('Failed to delete task. Please try again.');
    }
  };

  if (loading && tasks.length === 0) {
    return (
      <div className="min-h-screen bg-gray-50 flex items-center justify-center">
        <div className="text-center">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary-500 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading tasks...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gray-50">
      <Header />
      
      <main className="max-w-4xl mx-auto px-4 py-8">
        {error && (
          <div className="mb-6 bg-red-50 border-l-4 border-red-400 p-4 rounded">
            <div className="flex">
              <div className="ml-3">
                <p className="text-sm text-red-700">{error}</p>
                <button
                  onClick={loadTasks}
                  className="mt-2 text-sm text-red-600 hover:text-red-500 underline"
                >
                  Try again
                </button>
              </div>
            </div>
          </div>
        )}

        {/* Stats Section */}
        <TaskStats stats={stats} />

        {/* Task Creation Form */}
        <div className="mb-8">
          <TaskForm onSubmit={handleCreateTask} />
        </div>

        {/* Filter Controls */}
        <div className="mb-6">
          <div className="flex flex-wrap gap-2">
            <button
              onClick={() => setFilter('all')}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                filter === 'all'
                  ? 'bg-primary-500 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
              }`}
            >
              All Tasks
            </button>
            <button
              onClick={() => setFilter('pending')}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                filter === 'pending'
                  ? 'bg-primary-500 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
              }`}
            >
              Pending ({stats.pending})
            </button>
            <button
              onClick={() => setFilter('completed')}
              className={`px-4 py-2 rounded-full text-sm font-medium transition-colors ${
                filter === 'completed'
                  ? 'bg-primary-500 text-white'
                  : 'bg-white text-gray-700 hover:bg-gray-50 border border-gray-300'
              }`}
            >
              Completed ({stats.completed})
            </button>
          </div>
        </div>

        {/* Task List */}
        <TaskList
          tasks={tasks}
          onUpdate={handleUpdateTask}
          onComplete={handleCompleteTask}
          onDelete={handleDeleteTask}
          loading={loading}
        />

        {/* Empty State */}
        {!loading && tasks.length === 0 && (
          <div className="text-center py-12">
            <div className="mx-auto h-24 w-24 text-gray-400 mb-4">
              <svg fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={1}
                  d="M9 5H7a2 2 0 00-2 2v10a2 2 0 002 2h8a2 2 0 002-2V7a2 2 0 00-2-2h-2M9 5a2 2 0 002 2h2a2 2 0 002-2M9 5a2 2 0 012-2h2a2 2 0 012 2"
                />
              </svg>
            </div>
            <h3 className="text-lg font-medium text-gray-900 mb-2">
              {filter === 'all' ? 'No tasks yet' : 
               filter === 'pending' ? 'No pending tasks' : 
               'No completed tasks'}
            </h3>
            <p className="text-gray-500">
              {filter === 'all' ? 'Create your first task to get started!' :
               filter === 'pending' ? 'All tasks are completed! 🎉' :
               'Complete some tasks to see them here.'}
            </p>
          </div>
        )}
      </main>
    </div>
  );
}

export default App;
