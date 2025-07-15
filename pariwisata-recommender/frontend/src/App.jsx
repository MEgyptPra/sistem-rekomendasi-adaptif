import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import { Toaster } from 'react-hot-toast';

// Components
import Header from './components/layout/Header';
import Footer from './components/layout/Footer';

// Pages
import Home from './pages/Home';
import Destinations from './pages/Destinations';
import Profile from './pages/Profile';
import Admin from './pages/Admin';

// Styles
import './index.css';

const queryClient = new QueryClient();

function App() {
  const [currentUser, setCurrentUser] = useState({
    id: 1, // Mock user for development
    name: 'Ahmad Pratama',
    email: 'ahmad@example.com',
    preferences: 'alam,kuliner'
  });

  return (
    <QueryClientProvider client={queryClient}>
      <Router>
        <div className="min-h-screen bg-gray-50">
          <Header currentUser={currentUser} />
          
          <main>
            <Routes>
              <Route path="/" element={<Home currentUser={currentUser} />} />
              <Route path="/destinations" element={<Destinations currentUser={currentUser} />} />
              <Route path="/profile" element={<Profile currentUser={currentUser} setCurrentUser={setCurrentUser} />} />
              <Route path="/admin" element={<Admin />} />
            </Routes>
          </main>
          
          <Footer />
        </div>
        
        <Toaster 
          position="top-right"
          toastOptions={{
            duration: 4000,
            style: {
              background: '#363636',
              color: '#fff',
            },
          }}
        />
      </Router>
    </QueryClientProvider>
  );
}

export default App;