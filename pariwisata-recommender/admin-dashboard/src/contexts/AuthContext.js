import React, { createContext, useContext, useState, useEffect } from 'react';
import { jwtDecode as jwt_decode } from 'jwt-decode';
import apiService from '../services/api';

const AuthContext = createContext();

export function useAuth() {
  return useContext(AuthContext);
}

export function AuthProvider({ children }) {
  const [currentUser, setCurrentUser] = useState(null);
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');

  useEffect(() => {
    // Check if there's a token stored in localStorage
    const token = localStorage.getItem('adminToken');
    
    if (token) {
      try {
        // Check if token is expired
        const decodedToken = jwt_decode(token);
        const currentTime = Date.now() / 1000;
        
        if (decodedToken.exp > currentTime) {
          setCurrentUser(decodedToken);
          setIsAuthenticated(true);
        } else {
          // Token expired, remove it
          localStorage.removeItem('adminToken');
        }
      } catch (err) {
        // Invalid token, remove it
        localStorage.removeItem('adminToken');
      }
    }
    
    setLoading(false);
  }, []);

  async function login(email, password) {
    try {
      setError('');
      const response = await apiService.login(email, password);
      
      const { access_token } = response.data;
      
      localStorage.setItem('adminToken', access_token);
      
      const decodedToken = jwt_decode(access_token);
      setCurrentUser(decodedToken);
      setIsAuthenticated(true);
      
      return true;
    } catch (err) {
      console.error('Login error:', err);
      setError(err.response?.data?.detail || 'Login failed. Please check your credentials.');
      return false;
    }
  }

  function logout() {
    localStorage.removeItem('adminToken');
    setCurrentUser(null);
    setIsAuthenticated(false);
  }

  const value = {
    currentUser,
    isAuthenticated,
    login,
    logout,
    error,
  };

  return (
    <AuthContext.Provider value={value}>
      {!loading && children}
    </AuthContext.Provider>
  );
}