import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Header from './components/common/Header';
import Footer from './components/common/Footer';
import ScrollToTop from './components/common/ScrollToTop';
import Home from './pages/Home';
import Login from './pages/Login';
import Register from './pages/Register';
import Destinations from './pages/Destinations';
import DestinationDetail from './pages/DestinationDetail';
import Activities from './pages/Activities';
import ActivityDetail from './pages/ActivityDetail';
import Planning from './pages/Planning';
import PlanningDetail from './pages/PlanningDetail';
import Favorites from './pages/Favorites';
import Resources from './pages/Resources';
import Alert from './components/common/Alert';
import './styles/global.css';

function App() {
  return (
    <Router>
      <ScrollToTop />
      <div className="app">
        <Alert />
        <Header />
        <main>
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/destinations" element={<Destinations />} />
            <Route path="/destinations/:id" element={<DestinationDetail />} />
            <Route path="/activities" element={<Activities />} />
            <Route path="/activities/:id" element={<ActivityDetail />} />
            <Route path="/plan-your-trip" element={<Planning />} />
            <Route path="/planning" element={<Planning />} />
            <Route path="/planning/:id" element={<PlanningDetail />} />
            <Route path="/favorites" element={<Favorites />} />
            <Route path="/resources" element={<Resources />} />
          </Routes>
        </main>
        <Footer />
      </div>
    </Router>
  );
}

export default App;