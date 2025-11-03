import React, { createContext, useContext, useState, useEffect } from 'react';
import axios from 'axios';
import { jwtDecode as jwt_decode } from 'jwt-decode';

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
          // Set up axios default header
          axios.defaults.headers.common['Authorization'] = `Bearer ${token}`;
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
      const response = await axios.post('http://localhost:8000/admin/login', {
        email,
        password
      });
      
      const { access_token } = response.data;
      
      localStorage.setItem('adminToken', access_token);
      axios.defaults.headers.common['Authorization'] = `Bearer ${access_token}`;
      
      const decodedToken = jwt_decode(access_token);
      setCurrentUser(decodedToken);
      setIsAuthenticated(true);
      
      return true;
    } catch (err) {
      setError(err.response?.data?.detail || 'Login failed');
      return false;
    }
  }

  function logout() {
    localStorage.removeItem('adminToken');
    delete axios.defaults.headers.common['Authorization'];
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