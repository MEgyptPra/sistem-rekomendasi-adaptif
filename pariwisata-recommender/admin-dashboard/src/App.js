import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import CssBaseline from '@mui/material/CssBaseline';

// Import pages
import Login from './pages/Login';
import Dashboard from './pages/Dashboard';
import Destinations from './pages/Destinations';
import Activities from './pages/Activities';
import Users from './pages/Users';
import Analytics from './pages/Analytics';
import ModelManagement from './pages/ModelManagement';
import Settings from './pages/Settings';
import RealTimeStats from './pages/RealTimeStats';

// Import components
import Layout from './components/Layout';

// Authentication context
import { AuthProvider, useAuth } from './contexts/AuthContext';

// Protected route wrapper
const ProtectedRoute = ({ children }) => {
  const { isAuthenticated } = useAuth();
  return isAuthenticated ? children : <Navigate to="/login" />;
};

// Create a theme
const theme = createTheme({
  palette: {
    primary: {
      main: '#0D6EFD',
    },
    secondary: {
      main: '#036C5F',
    },
    background: {
      default: '#f5f5f5',
    },
  },
});

function AppContent() {
  return (
    <Router>
      <Routes>
        <Route path="/login" element={<Login />} />
        
        <Route path="/" element={
          <ProtectedRoute>
            <Layout>
              <Dashboard />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/destinations" element={
          <ProtectedRoute>
            <Layout>
              <Destinations />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/activities" element={
          <ProtectedRoute>
            <Layout>
              <Activities />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/users" element={
          <ProtectedRoute>
            <Layout>
              <Users />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/analytics" element={
          <ProtectedRoute>
            <Layout>
              <Analytics />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/model-management" element={
          <ProtectedRoute>
            <Layout>
              <ModelManagement />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/settings" element={
          <ProtectedRoute>
            <Layout>
              <Settings />
            </Layout>
          </ProtectedRoute>
        } />
        
        <Route path="/realtime-stats" element={
          <ProtectedRoute>
            <Layout>
              <RealTimeStats />
            </Layout>
          </ProtectedRoute>
        } />
      </Routes>
    </Router>
  );
}

function App() {
  return (
    <ThemeProvider theme={theme}>
      <CssBaseline />
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </ThemeProvider>
  );
}

export default App;