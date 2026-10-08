import React from 'react';

export const ProgressBar = ({ progress = 0, size = 'md', showLabel = false, color = 'blue' }) => {
  const clamped = Math.min(100, Math.max(0, Math.round(progress)));

  const sizeClasses = {
    sm: 'h-1.5',
    md: 'h-2.5',
    lg: 'h-4'
  };

  const colorGradients = {
    blue: 'from-blue-600 to-cyan-500',
    emerald: 'from-emerald-600 to-teal-400',
    violet: 'from-violet-600 to-indigo-400',
    amber: 'from-amber-500 to-orange-500'
  };

  const selectedGradient = colorGradients[color] || colorGradients.blue;

  return (
    <div className="w-full">
      {showLabel && (
        <div className="flex justify-between items-center mb-1.5 text-xs text-slate-400 font-medium">
          <span>Completion</span>
          <span className="text-slate-200">{clamped}%</span>
        </div>
      )}
      <div className={`w-full bg-dark-700/80 rounded-full overflow-hidden ${sizeClasses[size]}`}>
        <div
          className={`h-full bg-gradient-to-r ${selectedGradient} transition-all duration-500 rounded-full`}
          style={{ width: `${clamped}%` }}
        />
      </div>
    </div>
  );
};
