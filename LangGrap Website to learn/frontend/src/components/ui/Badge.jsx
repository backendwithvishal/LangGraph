import React from 'react';

export const Badge = ({ children, variant = 'default', size = 'sm', className = '' }) => {
  const base = "inline-flex items-center font-medium rounded-full transition-colors";
  
  const sizeStyles = {
    xs: "px-2 py-0.5 text-xs",
    sm: "px-2.5 py-1 text-xs",
    md: "px-3 py-1.5 text-sm"
  };

  const variantStyles = {
    default: "bg-dark-700 text-slate-300 border border-dark-600",
    primary: "bg-blue-500/10 text-blue-400 border border-blue-500/20",
    beginner: "bg-emerald-500/10 text-emerald-400 border border-emerald-500/20",
    intermediate: "bg-cyan-500/10 text-cyan-400 border border-cyan-500/20",
    advanced: "bg-violet-500/10 text-violet-400 border border-violet-500/20",
    production: "bg-amber-500/10 text-amber-400 border border-amber-500/20",
    danger: "bg-rose-500/10 text-rose-400 border border-rose-500/20",
    real: "bg-emerald-500/20 text-emerald-300 border border-emerald-500/40 font-semibold"
  };

  const variantKey = variant.toLowerCase();
  const selectedVariant = variantStyles[variantKey] || variantStyles.default;

  return (
    <span className={`${base} ${sizeStyles[size]} ${selectedVariant} ${className}`}>
      {children}
    </span>
  );
};
