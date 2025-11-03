import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/cards.css';

const DestinationCard = ({ destination }) => {
  return (
    <div className="card destination-card">
      <div className="card-image">
        <img src={destination.image} alt={destination.name} />
        {destination.region && (
          <div className="card-badge">{destination.region}</div>
        )}
      </div>
      <div className="card-content">
        <h3>{destination.name}</h3>
        <p>{destination.description}</p>
        <Link to={`/destinations/${destination.id}`} className="btn primary">
          Lihat Detail
        </Link>
      </div>
    </div>
  );
};

export default DestinationCard;