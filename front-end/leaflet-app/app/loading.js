'use client';

import { useState, useEffect } from 'react';

const Loading = ({ text }) => {
  const [displayText, setDisplayText] = useState('Loading...');
  const routeLabels = [
    'Finding your cool route...',
    'Visualizing your cool route...',
    'Finding your direct route...',
    'Visualizing your direct route...',
    'Almost there...'
  ];

  useEffect(() => {
    let i = 0;
    let interval;

    if (text === 'locate') {
      setDisplayText('Finding your location...');
    } else if (text === 'search') {
      setDisplayText('Finding addresses...');
    } else if (text === 'calculate') {
      setDisplayText(routeLabels[0]);

      interval = setInterval(() => {
        i++;
        if (i < routeLabels.length) {
          setDisplayText(routeLabels[i]);
        } else {
          clearInterval(interval);
        }
      }, 5000);
    }

    return () => clearInterval(interval);
  }, [text]);

  return (
    <label className="loading-label">{displayText}</label>
  );
};

export default Loading;
