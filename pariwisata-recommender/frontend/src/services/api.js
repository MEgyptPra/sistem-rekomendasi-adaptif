import axios from 'axios';

const API_BASE_URL = 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Destinations API
export const destinationsAPI = {
  getAll: () => api.get('/destinations'),
  getById: (id) => api.get(`/destinations/${id}`),
  getByCategory: (category) => api.get(`/destinations/category/${category}`),
  search: (query) => api.get(`/destinations/search?q=${query}`),
};

// Recommendations API
export const recommendationsAPI = {
  getForUser: (userId, algorithm = 'hybrid') => 
    api.get(`/recommendations/${userId}?algorithm=${algorithm}`),
  explain: (userId, destinationId) => 
    api.get(`/recommendations/explain/${userId}/${destinationId}`),
  train: () => api.post('/ml/train'),
};

// Users API
export const usersAPI = {
  getProfile: (userId) => api.get(`/users/${userId}`),
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