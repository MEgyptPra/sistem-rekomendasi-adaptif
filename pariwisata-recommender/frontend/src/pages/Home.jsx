import React, { useState, useEffect } from 'react';
import { useQuery } from 'react-query';
import { TrendingUp, Compass, Users, Brain } from 'lucide-react';
import DestinationCard from '../components/destination/Destinationcard';
import LoadingSpinner from '../components/common/LoadingSpinner';
import { recommendationsAPI, destinationsAPI } from '../services/api';

const Home = ({ currentUser }) => {
  const [selectedAlgorithm, setSelectedAlgorithm] = useState('hybrid');
  
  // Fetch recommendations for current user
  const { data: recommendations, isLoading: loadingRecs } = useQuery(
    ['recommendations', currentUser?.id, selectedAlgorithm],
    () => currentUser 
      ? recommendationsAPI.getForUser(currentUser.id, selectedAlgorithm)
      : destinationsAPI.getAll(),
    {
      enabled: true,
      select: (data) => data.data
    }
  );

  const algorithms = [
    { key: 'hybrid', label: 'Hybrid (Recommended)', icon: Brain, color: 'blue' },
    { key: 'content_based', label: 'Content-Based', icon: Compass, color: 'green' },
    { key: 'collaborative', label: 'Collaborative', icon: Users, color: 'purple' },
  ];

  return (
    <div className="min-h-screen bg-gray-50">
      {/* Hero Section */}
      <section className="bg-gradient-to-r from-blue-600 to-purple-600 text-white py-16">
        <div className="container mx-auto px-4 text-center">
          <h1 className="text-4xl md:text-6xl font-bold mb-4">
            Temukan Destinasi Impianmu
          </h1>
          <p className="text-xl md:text-2xl text-blue-100 mb-8">
            Rekomendasi wisata yang dipersonalisasi dengan AI
          </p>
          {currentUser && (
            <div className="bg-white/10 backdrop-blur-sm rounded-lg p-4 inline-block">
              <p className="text-lg">
                Halo, <span className="font-semibold">{currentUser.name}</span>! 👋
              </p>
              <p className="text-blue-100">
                Kami sudah menyiapkan rekomendasi khusus untukmu
              </p>
            </div>
          )}
        </div>
      </section>

      <div className="container mx-auto px-4 py-8">
        {/* Algorithm Selector */}
        {currentUser && (
          <section className="mb-8">
            <h2 className="text-2xl font-bold text-gray-800 mb-4">
              Pilih Algoritma Rekomendasi
            </h2>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              {algorithms.map((algo) => {
                const Icon = algo.icon;
                const isSelected = selectedAlgorithm === algo.key;
                return (
                  <button
                    key={algo.key}
                    onClick={() => setSelectedAlgorithm(algo.key)}
                    className={`p-4 rounded-lg border-2 transition ${
                      isSelected
                        ? `border-${algo.color}-500 bg-${algo.color}-50`
                        : 'border-gray-200 hover:border-gray-300'
                    }`}
                  >
                    <div className="flex items-center space-x-3">
                      <Icon className={`h-6 w-6 ${isSelected ? `text-${algo.color}-600` : 'text-gray-600'}`} />
                      <div className="text-left">
                        <h3 className={`font-semibold ${isSelected ? `text-${algo.color}-800` : 'text-gray-800'}`}>
                          {algo.label}
                        </h3>
                      </div>
                    </div>
                  </button>
                );
              })}
            </div>
          </section>
        )}

        {/* Recommendations Section */}
        <section>
          <div className="flex items-center space-x-2 mb-6">
            <TrendingUp className="h-6 w-6 text-blue-600" />
            <h2 className="text-2xl font-bold text-gray-800">
              {currentUser ? 'Rekomendasi Untukmu' : 'Destinasi Popular'}
            </h2>
          </div>

          {loadingRecs ? (
            <div className="flex justify-center py-12">
              <LoadingSpinner />
            </div>
          ) : (
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
              {recommendations?.map((destination) => (
                <DestinationCard
                  key={destination.id}
                  destination={destination}
                  currentUser={currentUser}
                  onRate={(destId, rating) => {
                    // Handle rating
                    console.log('Rating:', destId, rating);
                  }}
                />
              ))}
            </div>
          )}
        </section>
      </div>
    </div>
  );
};

export default Home;