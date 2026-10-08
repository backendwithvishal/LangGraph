import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import {
  ChevronDown,
  ChevronRight,
  CheckCircle2,
  Circle,
  Bookmark,
  Zap,
  BookOpen,
  Layers,
  Search
} from 'lucide-react';
import { useProgress } from '../../context/ProgressContext';
import { Badge } from '../ui/Badge';

export const Sidebar = ({ modules = [], activeLessonId = null }) => {
  const location = useLocation();
  const { isLessonCompleted, isBookmarked, progress } = useProgress();
  const [expandedModules, setExpandedModules] = useState(() => {
    // Default expand first 3 modules or the active module
    const initial = { 'module-1': true, 'module-2': true, 'module-3': true };
    if (activeLessonId) {
      for (const m of modules) {
        if (m.lessons?.some(l => l.id === activeLessonId)) {
          initial[m.id] = true;
        }
      }
    }
    return initial;
  });

  const toggleModule = (modId) => {
    setExpandedModules(prev => ({
      ...prev,
      [modId]: !prev[modId]
    }));
  };

  const fastTrackIds = [
    "m1-l1", "m1-l3", "m2-l1", "m2-l2", "m2-l3",
    "m3-l1", "m3-l2", "m4-l1", "m4-l2", "m5-l1", "m6-l1",
    "m7-l1", "m7-l2", "m8-l1", "m8-l2", "m9-l1", "m9-l2",
    "m10-l1", "m10-l2", "m11-l1", "m11-l2",
    "m12-l1", "m13-l1", "m13-l2", "m14-l1"
  ];

  return (
    <aside className="w-80 flex-shrink-0 border-r border-dark-700/80 bg-dark-900/70 overflow-y-auto max-h-[calc(100vh-7rem)] p-4 select-none">
      
      {/* Sidebar Header */}
      <div className="flex items-center justify-between pb-3 mb-3 border-b border-dark-800">
        <div className="flex items-center gap-2">
          <BookOpen className="w-4 h-4 text-blue-400" />
          <span className="text-xs font-bold uppercase tracking-wider text-slate-300">
            Curriculum Map
          </span>
        </div>
        <span className="text-[11px] font-medium text-slate-400">
          14 Modules
        </span>
      </div>

      {/* Module Accordions */}
      <div className="space-y-2">
        {modules.map((mod, index) => {
          const isExpanded = expandedModules[mod.id];
          const completedInMod = mod.lessons.filter(l => isLessonCompleted(l.id)).length;
          const totalInMod = mod.lessons.length;
          const isModComplete = completedInMod === totalInMod && totalInMod > 0;

          return (
            <div
              key={mod.id}
              className="rounded-lg border border-dark-800 bg-dark-850/50 overflow-hidden transition-colors"
            >
              {/* Module Accordion Header */}
              <button
                onClick={() => toggleModule(mod.id)}
                className="w-full flex items-center justify-between p-2.5 text-left hover:bg-dark-800/60 transition-colors"
              >
                <div className="flex items-center gap-2 min-w-0 pr-2">
                  {isExpanded ? (
                    <ChevronDown className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                  ) : (
                    <ChevronRight className="w-3.5 h-3.5 text-slate-400 flex-shrink-0" />
                  )}
                  <span className="text-xs font-semibold text-slate-200 truncate">
                    {mod.title}
                  </span>
                </div>

                <div className="flex items-center gap-1.5 flex-shrink-0">
                  {isModComplete ? (
                    <span className="w-4 h-4 rounded-full bg-emerald-500/20 text-emerald-400 flex items-center justify-center text-[10px] font-bold">
                      ✓
                    </span>
                  ) : (
                    <span className="text-[10px] font-mono text-slate-400">
                      {completedInMod}/{totalInMod}
                    </span>
                  )}
                </div>
              </button>

              {/* Lesson Items */}
              {isExpanded && (
                <div className="border-t border-dark-800/80 bg-dark-900/40 divide-y divide-dark-800/40">
                  {mod.lessons.map(lesson => {
                    const isActive = activeLessonId === lesson.id;
                    const isDone = isLessonCompleted(lesson.id);
                    const bookmarked = isBookmarked(lesson.id);
                    const isFastTrack = fastTrackIds.includes(lesson.id);

                    // Filter in fast track mode if user enabled it
                    if (progress.fastTrackMode && !isFastTrack) {
                      return null;
                    }

                    return (
                      <Link
                        key={lesson.id}
                        to={`/lessons/${lesson.id}`}
                        className={`flex items-start gap-2.5 px-3 py-2 text-xs transition-colors group ${
                          isActive
                            ? 'bg-blue-600/15 border-l-2 border-blue-500 text-blue-300 font-medium'
                            : 'text-slate-400 hover:text-slate-200 hover:bg-dark-800/40'
                        }`}
                      >
                        <div className="mt-0.5 flex-shrink-0">
                          {isDone ? (
                            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
                          ) : (
                            <Circle className="w-3.5 h-3.5 text-slate-600 group-hover:text-slate-400" />
                          )}
                        </div>

                        <div className="min-w-0 flex-1">
                          <div className="flex items-center justify-between gap-1">
                            <span className="truncate leading-tight">{lesson.title}</span>
                            <div className="flex items-center gap-1 flex-shrink-0">
                              {isFastTrack && (
                                <span title="Included in 5-Day Bootcamp">
                                  <Zap className="w-2.5 h-2.5 text-amber-400 fill-amber-400/50" />
                                </span>
                              )}
                              {bookmarked && (
                                <Bookmark className="w-2.5 h-2.5 text-blue-400 fill-blue-400" />
                              )}
                            </div>
                          </div>
                          <div className="flex items-center gap-2 mt-1 text-[10px] text-slate-400">
                            <span>{lesson.estimated_minutes} min</span>
                            <span>•</span>
                            <span className="capitalize">{lesson.difficulty}</span>
                          </div>
                        </div>
                      </Link>
                    );
                  })}
                </div>
              )}
            </div>
          );
        })}
      </div>
    </aside>
  );
};
