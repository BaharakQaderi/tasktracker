import axios from 'axios';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: process.env.REACT_APP_API_URL || '',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor for logging
api.interceptors.request.use(
  (config) => {
    console.log(`Making ${config.method?.toUpperCase()} request to ${config.url}`);
    return config;
  },
  (error) => {
    console.error('Request error:', error);
    return Promise.reject(error);
  }
);

// Response interceptor for error handling
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    console.error('Response error:', error);
    
    if (error.response) {
      // Server responded with error status
      const message = error.response.data?.detail || 
                     error.response.data?.message || 
                     `Server error: ${error.response.status}`;
      throw new Error(message);
    } else if (error.request) {
      // Request was made but no response received
      throw new Error('Network error: Unable to connect to server');
    } else {
      // Something else happened
      throw new Error(error.message || 'An unexpected error occurred');
    }
  }
);

export const taskService = {
  // Get all tasks with optional filtering
  async getTasks(skip = 0, limit = 100, completed = null) {
    const params = { skip, limit };
    if (completed !== null) {
      params.completed = completed;
    }
    
    const response = await api.get('/tasks', { params });
    return response.data;
  },

  // Get a specific task by ID
  async getTask(id) {
    const response = await api.get(`/tasks/${id}`);
    return response.data;
  },

  // Create a new task
  async createTask(taskData) {
    const response = await api.post('/tasks', taskData);
    return response.data;
  },

  // Update an existing task
  async updateTask(id, updateData) {
    const response = await api.put(`/tasks/${id}`, updateData);
    return response.data;
  },

  // Mark a task as completed
  async completeTask(id) {
    const response = await api.post(`/tasks/${id}/complete`);
    return response.data;
  },

  // Delete a task
  async deleteTask(id) {
    await api.delete(`/tasks/${id}`);
    return true;
  },

  // Get task statistics
  async getStats() {
    const response = await api.get('/tasks/stats');
    return response.data;
  },

  // Health check
  async healthCheck() {
    const response = await api.get('/health');
    return response.data;
  },
};

export default api;
