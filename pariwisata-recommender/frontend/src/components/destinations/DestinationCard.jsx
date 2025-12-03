import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/cards.css';
import SmartImage from '../common/SmartImage';
import placeholder from '../../assets/placeholder.svg';

const DestinationCard = ({ destination }) => {
  return (
    <div className="card destination-card">
      <div className="card-image">
        <SmartImage publicSrc={destination.image} bundledSrc={placeholder} alt={destination.name} style={{ width: '100%', height: 180, objectFit: 'cover' }} />
        {destination.region && (
          <div className="card-badge">{destination.region}</div>
        )}
      </div>
      <div className="card-content">
        <h3>{destination.name}</h3>
        {destination.categories && destination.categories.length > 0 && (
          <p className="card-category">📍 {destination.categories.map(cat => cat.name).join(', ')}</p>
        )}
        {destination.address && (
          <p className="card-address">{destination.address}</p>
        )}
        <p className="card-description">{destination.description}</p>
        <Link to={`/destinations/${destination.id}`} className="btn primary">
          Lihat Detail
        </Link>
      </div>
    </div>
  );
};

export default DestinationCard;