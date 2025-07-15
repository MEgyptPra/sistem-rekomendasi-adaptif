import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MapPin, User, Search, Home } from 'lucide-react';

const Header = ({ currentUser }) => {
  const location = useLocation();
  
  const isActive = (path) => location.pathname === path;
  
  return (
    <header className="bg-white shadow-md border-b">
      <div className="container mx-auto px-4 py-4">
        <div className="flex items-center justify-between">
          {/* Logo */}
          <Link to="/" className="flex items-center space-x-2">
            <MapPin className="h-8 w-8 text-blue-600" />
            <span className="text-2xl font-bold text-gray-800">
              WisataKu
            </span>
          </Link>
          
          {/* Navigation */}
          <nav className="hidden md:flex space-x-8">
            <Link 
              to="/" 
              className={`flex items-center space-x-1 px-3 py-2 rounded-md transition ${
                isActive('/') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              <Home className="h-4 w-4" />
              <span>Beranda</span>
            </Link>
            
            <Link 
              to="/destinations" 
              className={`flex items-center space-x-1 px-3 py-2 rounded-md transition ${
                isActive('/destinations') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              <Search className="h-4 w-4" />
              <span>Destinasi</span>
            </Link>
            
            <Link 
              to="/profile" 
              className={`flex items-center space-x-1 px-3 py-2 rounded-md transition ${
                isActive('/profile') 
                  ? 'bg-blue-100 text-blue-700' 
                  : 'text-gray-600 hover:text-blue-600'
              }`}
            >
              <User className="h-4 w-4" />
              <span>Profil</span>
            </Link>
          </nav>
          
          {/* User Info */}
          <div className="flex items-center space-x-4">
            {currentUser ? (
              <div className="flex items-center space-x-2">
                <div className="w-8 h-8 bg-blue-600 rounded-full flex items-center justify-center">
                  <span className="text-white text-sm font-medium">
                    {currentUser.name?.[0]?.toUpperCase()}
                  </span>
                </div>
                <span className="text-gray-700">{currentUser.name}</span>
              </div>
            ) : (
              <button className="bg-blue-600 text-white px-4 py-2 rounded-md hover:bg-blue-700 transition">
                Login
              </button>
            )}
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;