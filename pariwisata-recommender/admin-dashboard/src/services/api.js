import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor to add auth token
api.interceptors.request.use(
  (config) => {
    const token = localStorage.getItem('adminToken');
    if (token) {
      config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor to handle errors
api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      // Token expired or invalid
      localStorage.removeItem('adminToken');
      window.location.href = '/login';
    }
    return Promise.reject(error);
  }
);

// API methods
const apiService = {
  // Auth
  login: (email, password) => api.post('/admin/login', { email, password }),
  
  // Dashboard stats
  getStats: () => api.get('/admin/stats'),
  getActivityStats: () => api.get('/admin/activity-stats'),
  
  // Destinations
  getDestinations: () => api.get('/admin/destinations'),
  getDestination: (id) => api.get(`/admin/destinations/${id}`),
  createDestination: (data) => api.post('/admin/destinations', data),
  updateDestination: (id, data) => api.put(`/admin/destinations/${id}`, data),
  deleteDestination: (id) => api.delete(`/admin/destinations/${id}`),
  
  // Activities
  getActivities: () => api.get('/admin/activities'),
  getActivity: (id) => api.get(`/admin/activities/${id}`),
  createActivity: (data) => api.post('/admin/activities', data),
  updateActivity: (id, data) => api.put(`/admin/activities/${id}`, data),
  deleteActivity: (id) => api.delete(`/admin/activities/${id}`),

  // Test API
  testApi: (data) => api.post('/admin/test-api', data),
  
  // Users
  getUsers: () => api.get('/admin/users'),
  getUser: (id) => api.get(`/admin/users/${id}`),
  updateUser: (id, data) => api.put(`/admin/users/${id}`, data),
  deleteUser: (id) => api.delete(`/admin/users/${id}`),
  
  // Analytics
  getAnalytics: () => api.get('/admin/analytics'),
  getRecommendationStats: () => api.get('/admin/analytics/recommendations'),
  getUserGrowth: () => api.get('/admin/analytics/user-growth'),
  
  // Model Management
  getModelStatus: () => api.get('/admin/model/status'),
  getDriftDetection: () => api.get('/admin/model/drift-detection'),
  retrainModel: (data) => api.post('/admin/model/retrain', data),
  setRetrainSchedule: (data) => api.post('/admin/model/schedule', data),
  getTrainingHistory: () => api.get('/admin/model/training-history'),
  getRealtimeStats: () => api.get('/admin/model/realtime-stats'),
  getRealtimeConfig: () => api.get('/admin/model/realtime-config'),
  setRealtimeConfig: (data) => api.post('/admin/model/realtime-config', data),
  
  // Realtime API Config
  listRealtimeApiConfig: () => api.get('/admin/model/realtime-api-config'),
  getRealtimeApiConfig: (id) => api.get(`/admin/model/realtime-api-config/${id}`),
  createRealtimeApiConfig: (data) => api.post('/admin/model/realtime-api-config', data),
  updateRealtimeApiConfig: (id, data) => api.put(`/admin/model/realtime-api-config/${id}`, data),
  deleteRealtimeApiConfig: (id) => api.delete(`/admin/model/realtime-api-config/${id}`),
};

export default apiService;
