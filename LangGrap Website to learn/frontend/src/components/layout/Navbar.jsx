import React, { useState } from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import {
  GitBranch,
  Search,
  BookOpen,
  Terminal,
  Activity,
  CheckCircle2,
  Bookmark,
  Sun,
  Moon,
  Zap,
  HelpCircle,
  FolderGit2,
  Sparkles
} from 'lucide-react';
import { useProgress } from '../../context/ProgressContext';
import { useTheme } from '../../context/ThemeContext';
import { Badge } from '../ui/Badge';

export const Navbar = ({ onOpenSearch }) => {
  const navigate = useNavigate();
  const location = useLocation();
  const { completedCount, progress, toggleFastTrack } = useProgress();
  const { theme, toggleTheme, isDark } = useTheme();

  const totalLessons = 32; // Total lessons across 14 modules
  const percent = Math.round((completedCount / totalLessons) * 100);

  const navLinks = [
    { path: '/', label: 'Dashboard', icon: Activity },
    { path: '/path', label: 'Learning Path', icon: BookOpen },
    { path: '/playground', label: 'Visual Graph', icon: GitBranch },
    { path: '/code', label: 'Python Lab', icon: Terminal },
    { path: '/practice', label: 'Quiz & Practice', icon: CheckCircle2 },
    { path: '/projects', label: 'Guided Projects', icon: FolderGit2 },
    { path: '/reference', label: 'Reference & Docs', icon: HelpCircle },
  ];

  return (
    <header className="sticky top-0 z-40 w-full border-b border-dark-700/80 bg-dark-900/90 backdrop-blur-md">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 h-16 flex items-center justify-between gap-4">
        
        {/* Brand Logo */}
        <div className="flex items-center gap-6">
          <Link to="/" className="flex items-center gap-2.5 group">
            <div className="w-9 h-9 rounded-lg bg-gradient-to-tr from-blue-600 to-cyan-400 flex items-center justify-center shadow-lg shadow-blue-500/20 group-hover:scale-105 transition-transform">
              <GitBranch className="w-5 h-5 text-white" />
            </div>
            <div>
              <div className="flex items-center gap-1.5">
                <span className="font-extrabold text-lg tracking-tight text-white font-sans">
                  Graph<span className="text-blue-400">Lab</span>
                </span>
                <span className="text-[10px] uppercase font-bold tracking-wider px-1.5 py-0.5 rounded bg-blue-500/10 text-blue-400 border border-blue-500/20">
                  v0.2+
                </span>
              </div>
              <span className="text-[10px] text-slate-400 hidden sm:block tracking-wide">
                Interactive LangGraph Learning
              </span>
            </div>
          </Link>
        </div>

        {/* Global Search Bar Trigger */}
        <button
          onClick={onOpenSearch}
          className="hidden md:flex items-center gap-3 px-3.5 py-1.5 rounded-lg bg-dark-800/90 border border-dark-700 text-slate-400 hover:text-slate-200 hover:border-dark-600 transition-all text-xs w-64 justify-between shadow-inner"
        >
          <span className="flex items-center gap-2">
            <Search className="w-3.5 h-3.5 text-slate-400" />
            <span>Search lessons, APIs, errors...</span>
          </span>
          <kbd className="px-1.5 py-0.5 rounded bg-dark-700 border border-dark-600 text-[10px] font-mono text-slate-400">
            ⌘K
          </kbd>
        </button>

        {/* Action Controls */}
        <div className="flex items-center gap-3">
          
          {/* Fast Track Mode Toggle */}
          <button
            onClick={toggleFastTrack}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              progress.fastTrackMode
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/50 shadow-sm shadow-amber-500/20'
                : 'bg-dark-800 text-slate-400 border-dark-700 hover:text-slate-200'
            }`}
            title="Toggle 5-Day Intensive Bootcamp Mode"
          >
            <Zap className={`w-3.5 h-3.5 ${progress.fastTrackMode ? 'text-amber-400 fill-amber-400' : ''}`} />
            <span className="hidden sm:inline">5-Day Bootcamp</span>
          </button>

          {/* Progress Widget */}
          <Link
            to="/progress"
            className="flex items-center gap-2 px-3 py-1.5 rounded-lg bg-dark-800 border border-dark-700 hover:border-dark-600 transition-all group"
          >
            <div className="w-5 h-5 rounded-full bg-blue-500/20 flex items-center justify-center text-[10px] font-bold text-blue-400">
              {completedCount}
            </div>
            <div className="hidden lg:flex flex-col">
              <span className="text-[11px] font-medium text-slate-300 leading-tight">
                {percent}% Mastered
              </span>
            </div>
          </Link>

          {/* Theme Toggle */}
          <button
            onClick={toggleTheme}
            className="p-2 rounded-lg bg-dark-800 border border-dark-700 text-slate-400 hover:text-slate-200 hover:border-dark-600 transition-all"
            title="Toggle theme"
          >
            {isDark ? <Sun className="w-4 h-4 text-amber-400" /> : <Moon className="w-4 h-4 text-blue-400" />}
          </button>
        </div>
      </div>

      {/* Secondary Horizontal Nav for Mobile / Desktop Quick Navigation */}
      <div className="border-t border-dark-800 bg-dark-900/60 overflow-x-auto scrollbar-none">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 flex items-center gap-1 py-1.5">
          {navLinks.map((item) => {
            const Icon = item.icon;
            const isActive = location.pathname === item.path || (item.path !== '/' && location.pathname.startsWith(item.path));
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`flex items-center gap-1.5 px-3 py-1.5 rounded-md text-xs font-medium whitespace-nowrap transition-colors ${
                  isActive
                    ? 'bg-blue-600/15 text-blue-400 font-semibold'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-dark-800/60'
                }`}
              >
                <Icon className={`w-3.5 h-3.5 ${isActive ? 'text-blue-400' : 'text-slate-400'}`} />
                <span>{item.label}</span>
              </Link>
            );
          })}
        </div>
      </div>
    </header>
  );
};
