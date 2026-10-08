import React from 'react';

export const Card = ({ children, className = '', hover = false, onClick = null }) => {
  const hoverClass = hover ? "hover:border-blue-500/40 hover:shadow-lg hover:shadow-blue-500/5 transition-all duration-200 cursor-pointer" : "";
  return (
    <div
      onClick={onClick}
      className={`glass-panel rounded-xl p-5 border border-dark-700/80 bg-dark-850/80 ${hoverClass} ${className}`}
    >
      {children}
    </div>
  );
};
