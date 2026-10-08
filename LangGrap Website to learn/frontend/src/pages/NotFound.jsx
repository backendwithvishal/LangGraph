import React from 'react';
import { Link } from 'react-router-dom';
import { GitBranch, Home, ArrowLeft } from 'lucide-react';

export const NotFound = () => {
  return (
    <div className="flex flex-col items-center justify-center min-h-[60vh] text-center px-4 space-y-4">
      <div className="w-16 h-16 rounded-2xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400">
        <GitBranch className="w-8 h-8" />
      </div>
      <h1 className="text-3xl font-extrabold text-white">404: Node Not Found</h1>
      <p className="text-xs text-slate-400 max-w-md">
        The requested graph route does not exist in the compiled state machine.
      </p>
      <Link
        to="/"
        className="flex items-center gap-2 px-4 py-2 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold shadow-lg shadow-blue-500/20 transition-all"
      >
        <Home className="w-4 h-4" />
        <span>Return to Dashboard</span>
      </Link>
    </div>
  );
};
