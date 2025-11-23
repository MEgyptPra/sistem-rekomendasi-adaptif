import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000/api';

// Create axios instance
const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Add token to requests if available
api.interceptors.request.use((config) => {
  const token = localStorage.getItem('access_token');
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

// Auth API
export const authAPI = {
  register: (data) => api.post('/auth/register', data),
  login: (data) => api.post('/auth/login', data),
  logout: () => api.post('/auth/logout'),
  getCurrentUser: () => api.get('/auth/me'),
  refreshToken: () => api.post('/auth/refresh'),
};

// Destinations API
export const destinationsAPI = {
  getAll: (params) => api.get('/destinations', { params }),
  getAllDestinations: (params) => api.get('/destinations', { params }),
  getById: (id) => api.get(`/destinations/${id}`),
  getByCategory: (category) => api.get(`/destinations/category/${category}`),
  search: (query) => api.get(`/destinations/search`, { params: { q: query } }),
  getReviews: (id) => api.get(`/destinations/${id}/reviews`),
  submitReview: (id, data) => api.post(`/destinations/${id}/reviews`, data),
};

// Activities API
export const activitiesAPI = {
  getAll: (params) => api.get('/activities', { params }),
  getById: (id) => api.get(`/activities/${id}`),
  getByCategory: (category) => api.get(`/activities/category/${category}`),
  search: (query) => api.get(`/activities/search`, { params: { q: query } }),
  getReviews: (id) => api.get(`/activities/${id}/reviews`),
  submitReview: (id, data) => api.post(`/activities/${id}/reviews`, data),
};

// Recommendations API
export const recommendationsAPI = {
  getPersonalized: (params) => api.get('/recommendations/personalized', { params }),
  getHybridRecommendations: (params) => api.get('/recommendations/hybrid', { params }),
  getForUser: (userId, algorithm = 'hybrid') => 
    api.get(`/recommendations/${userId}`, { params: { algorithm } }),
  explain: (userId, destinationId) => 
    api.get(`/recommendations/explain/${userId}/${destinationId}`),
  train: () => api.post('/ml/train'),
  getAllDestinations: (params) => api.get('/destinations', { params }),
};

// Related Items API
export const relatedAPI = {
  getRelatedDestinations: (id) => api.get(`/destinations/${id}/related`),
  getRelatedActivities: (id) => api.get(`/activities/${id}/related`),
};

// Favorites API
export const favoritesAPI = {
  getAll: () => api.get('/favorites'),
  add: (itemType, itemId) => api.post('/favorites', { item_type: itemType, item_id: itemId }),
  remove: (itemType, itemId) => api.delete('/favorites', { data: { item_type: itemType, item_id: itemId } }),
  check: (itemType, itemId) => api.get(`/favorites/check`, { params: { item_type: itemType, item_id: itemId } }),
};

// Interactions API (MAB tracking)
export const interactionsAPI = {
  trackView: (itemType, itemId, duration) => 
    api.post('/interactions/view', { item_type: itemType, item_id: itemId, duration_seconds: duration }),
  trackClick: (itemType, itemId, context) => 
    api.post('/interactions/click', { item_type: itemType, item_id: itemId, context }),
};

// Itineraries API
export const itinerariesAPI = {
  getAll: () => api.get('/itineraries'),
  getById: (id) => api.get(`/itineraries/${id}`),
  create: (data) => api.post('/itineraries', data),
  update: (id, data) => api.put(`/itineraries/${id}`, data),
  delete: (id) => api.delete(`/itineraries/${id}`),
  // Alias untuk backward compatibility
  list: () => api.get('/itineraries'),
};

// Alias untuk backward compatibility
export const itineraryAPI = itinerariesAPI;

// Search API
export const searchAPI = {
  universal: (query, filters) => api.get('/search', { params: { q: query, ...filters } }),
};

// Users API
export const usersAPI = {
  getProfile: (userId) => api.get(`/users/${userId}`),
  updateProfile: (data) => api.put('/users/profile', data),
  updatePreferences: (userId, preferences) => 
    api.put(`/users/${userId}/preferences`, { preferences }),
  getRatings: (userId) => api.get(`/user/${userId}/ratings`),
};

// Ratings API
export const ratingsAPI = {
  add: (userId, destinationId, rating) => 
    api.post(`/ratings`, { user_id: userId, destination_id: destinationId, rating }),
  update: (ratingId, rating) => 
    api.put(`/ratings/${ratingId}`, { rating }),
};

// [BARU] Categories API - Mengambil daftar kategori dinamis
export const categoriesAPI = {
  getAll: () => api.get('/categories'),
};

export default api;