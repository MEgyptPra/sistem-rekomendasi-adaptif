import React, { useState } from 'react';
import '../../styles/alert.css';

const Alert = () => {
  const [isVisible, setIsVisible] = useState(true);
  
  // Example alert - in a real app, this would come from an API or context
  const alertData = {
    type: 'warning',
    title: 'Travel Advisory',
    message: 'Winter weather conditions affecting mountain passes. Check road conditions before traveling.',
    link: '/plan-your-trip#alerts'
  };
  
  if (!isVisible) return null;
  
  return (
    <div className={`site-alert ${alertData.type}`}>
      <div className="container alert-container">
        <div className="alert-content">
          <span className="alert-icon">⚠️</span>
          <div>
            <strong>{alertData.title}: </strong>
            <span>{alertData.message}</span>
            {alertData.link && (
              <a href={alertData.link} className="alert-link">Learn More</a>
            )}
          </div>
        </div>
        <button 
          className="alert-close"
          onClick={() => setIsVisible(false)}
          aria-label="Close alert"
        >
          ×
        </button>
      </div>
    </div>
  );
};

export default Alert;