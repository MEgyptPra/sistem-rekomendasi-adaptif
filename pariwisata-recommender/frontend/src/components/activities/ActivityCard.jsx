import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/cards.css';

const ActivityCard = ({ activity }) => {
  const handleImgError = (e) => {
    e.target.onerror = null;
    e.target.src = '/assets/images/placeholder.webp';
  };
  return (
    <div className="card activity-card">
      <div className="card-image">
        <img
          src={activity.image}
          alt={activity.name}
          onError={handleImgError}
        />
        {activity.category && (
          <div className="card-badge">{activity.category}</div>
        )}
      </div>
      <div className="card-content">
        <h3>{activity.name}</h3>
        <p>{activity.description}</p>
        <Link to={`/activities/${activity.id}`} className="btn primary">
          Lihat Detail
        </Link>
      </div>
    </div>
  );
};

export default ActivityCard;