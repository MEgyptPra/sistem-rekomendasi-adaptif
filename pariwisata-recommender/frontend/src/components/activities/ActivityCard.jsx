import React from 'react';
import { Link } from 'react-router-dom';
import '../../styles/cards.css';
import SmartImage from '../common/SmartImage';
import placeholder from '../../assets/placeholder.svg';

const ActivityCard = ({ activity }) => {
  return (
    <div className="card activity-card">
      <div className="card-image">
        <SmartImage publicSrc={activity.image} bundledSrc={placeholder} alt={activity.name} style={{ width: '100%', height: 160, objectFit: 'cover' }} />
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