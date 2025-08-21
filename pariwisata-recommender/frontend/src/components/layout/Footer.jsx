import React from 'react';
import { Link, useLocation } from 'react-router-dom';
import { MapPin, User, Search, Home } from 'lucide-react';

const Header = ({ currentUser }) => {
  const location = useLocation();   
  return (
    <footer>
      {/* Footer content goes here */}
    </footer>
  );
};

export default Header;