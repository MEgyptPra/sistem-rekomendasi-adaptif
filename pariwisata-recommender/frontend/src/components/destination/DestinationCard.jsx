import React, { useState } from 'react';
import { Star, MapPin, Heart, ExternalLink } from 'lucide-react';
import RatingModal from './RatingModal';

const DestinationCard = ({ destination, currentUser, onRate }) => {
  const [showRatingModal, setShowRatingModal] = useState(false);
  const [isLiked, setIsLiked] = useState(false);
  
  const handleRate = async (rating) => {
    if (currentUser && onRate) {
      await onRate(destination.id, rating);
      setShowRatingModal(false);
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md overflow-hidden hover:shadow-lg transition-shadow">
      {/* Image */}
      <div className="relative h-48 bg-gray-200">
        <img 
          src={destination.image_url || '/placeholder-destination.jpg'} 
          alt={destination.name}
          className="w-full h-full object-cover"
        />
        <button 
          onClick={() => setIsLiked(!isLiked)}
          className="absolute top-3 right-3 p-2 rounded-full bg-white/80 hover:bg-white transition"
        >
          <Heart 
            className={`h-5 w-5 ${isLiked ? 'text-red-500 fill-current' : 'text-gray-600'}`} 
          />
        </button>
      </div>
      
      {/* Content */}
      <div className="p-4">
        <div className="flex items-start justify-between mb-2">
          <h3 className="text-lg font-semibold text-gray-800 line-clamp-2">
            {destination.name}
          </h3>
          <span className="text-sm text-blue-600 bg-blue-100 px-2 py-1 rounded-full">
            {destination.category}
          </span>
        </div>
        
        <div className="flex items-center text-gray-600 mb-2">
          <MapPin className="h-4 w-4 mr-1" />
          <span className="text-sm">{destination.location}</span>
        </div>
        
        <p className="text-gray-600 text-sm mb-3 line-clamp-2">
          {destination.description}
        </p>
        
        {/* Rating */}
        <div className="flex items-center justify-between">
          <div className="flex items-center space-x-2">
            <div className="flex items-center">
              <Star className="h-4 w-4 text-yellow-400 fill-current" />
              <span className="text-sm font-medium ml-1">
                {destination.average_rating?.toFixed(1) || 'N/A'}
              </span>
              <span className="text-xs text-gray-500 ml-1">
                ({destination.rating_count || 0})
              </span>
            </div>
          </div>
          
          <div className="flex space-x-2">
            <button 
              onClick={() => setShowRatingModal(true)}
              className="text-sm bg-blue-600 text-white px-3 py-1 rounded-md hover:bg-blue-700 transition"
            >
              Beri Rating
            </button>
            <button className="text-sm border border-gray-300 px-3 py-1 rounded-md hover:bg-gray-50 transition">
              <ExternalLink className="h-3 w-3" />
            </button>
          </div>
        </div>
      </div>
      
      {/* Rating Modal */}
      <RatingModal 
        isOpen={showRatingModal}
        onClose={() => setShowRatingModal(false)}
        onRate={handleRate}
        destination={destination}
      />
    </div>
  );
};

export default DestinationCard;