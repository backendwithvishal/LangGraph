import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  BookOpen,
  CheckCircle2,
  Circle,
  Clock,
  Zap,
  ArrowRight,
  Filter,
  Layers,
  ChevronRight,
  Sparkles
} from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';

export const LearningPath = () => {
  const navigate = useNavigate();
  const { isLessonCompleted, progress, toggleFastTrack } = useProgress();
  const [curriculum, setCurriculum] = useState(null);
  const [selectedDifficulty, setSelectedDifficulty] = useState('all');
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCurriculum()
      .then(data => {
        setCurriculum(data);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const difficulties = ['all', 'Beginner', 'Intermediate', 'Advanced', 'Production'];

  const fastTrackIds = curriculum?.fast_track_lesson_ids || [];

  const filteredModules = curriculum?.modules?.filter(mod => {
    if (selectedDifficulty !== 'all' && mod.difficulty.toLowerCase() !== selectedDifficulty.toLowerCase()) {
      return false;
    }
    return true;
  }) || [];

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-dark-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <BookOpen className="w-5 h-5 text-blue-400" />
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Curriculum & Learning Path
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            Master all 14 official LangGraph 0.2+ architectural modules in logical prerequisite order.
          </p>
        </div>

        {/* Filter Controls */}
        <div className="flex flex-wrap items-center gap-2">
          {difficulties.map(diff => (
            <button
              key={diff}
              onClick={() => setSelectedDifficulty(diff)}
              className={`px-3 py-1.5 rounded-lg text-xs font-semibold capitalize transition-colors ${
                selectedDifficulty === diff
                  ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                  : 'bg-dark-800 text-slate-400 hover:text-slate-200 border border-dark-700'
              }`}
            >
              {diff}
            </button>
          ))}

          <button
            onClick={toggleFastTrack}
            className={`flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-semibold border transition-all ${
              progress.fastTrackMode
                ? 'bg-amber-500/20 text-amber-300 border-amber-500/50'
                : 'bg-dark-800 text-slate-400 border-dark-700 hover:text-slate-200'
            }`}
          >
            <Zap className={`w-3.5 h-3.5 ${progress.fastTrackMode ? 'text-amber-400 fill-amber-400' : ''}`} />
            <span>Fast-Track Bootcamp</span>
          </button>
        </div>
      </div>

      {/* Modules List */}
      <div className="space-y-6">
        {filteredModules.map((mod, idx) => {
          const completedInMod = mod.lessons.filter(l => isLessonCompleted(l.id)).length;
          const totalInMod = mod.lessons.length;
          const modPercent = Math.round((completedInMod / totalInMod) * 100);

          return (
            <div
              key={mod.id}
              className="rounded-2xl border border-dark-750 bg-dark-850/70 overflow-hidden shadow-lg transition-all"
            >
              {/* Module Header Bar */}
              <div className="p-5 border-b border-dark-800 bg-dark-900/60 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
                <div className="space-y-1">
                  <div className="flex items-center gap-2.5">
                    <span className="w-6 h-6 rounded-lg bg-blue-500/10 text-blue-400 font-bold font-mono text-xs flex items-center justify-center border border-blue-500/20">
                      {mod.order}
                    </span>
                    <h2 className="text-base font-bold text-white tracking-tight">
                      {mod.title}
                    </h2>
                    <Badge variant={mod.difficulty} size="xs">
                      {mod.difficulty}
                    </Badge>
                  </div>
                  <p className="text-xs text-slate-400 max-w-2xl leading-relaxed">
                    {mod.description}
                  </p>
                </div>

                <div className="flex items-center gap-4 sm:flex-shrink-0">
                  <div className="w-32">
                    <ProgressBar progress={modPercent} size="sm" showLabel />
                  </div>
                  <span className="text-xs font-mono text-slate-400">
                    {completedInMod}/{totalInMod} Done
                  </span>
                </div>
              </div>

              {/* Lessons Grid in Module */}
              <div className="p-4 grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3 bg-dark-900/30">
                {mod.lessons.map(lesson => {
                  const isDone = isLessonCompleted(lesson.id);
                  const isFast = fastTrackIds.includes(lesson.id);

                  if (progress.fastTrackMode && !isFast) {
                    return null;
                  }

                  return (
                    <Link
                      key={lesson.id}
                      to={`/lessons/${lesson.id}`}
                      className="group p-4 rounded-xl border border-dark-750/80 bg-dark-800/60 hover:bg-dark-750 hover:border-blue-500/40 transition-all flex flex-col justify-between space-y-3"
                    >
                      <div className="space-y-2">
                        <div className="flex items-center justify-between gap-2">
                          <div className="flex items-center gap-2">
                            {isDone ? (
                              <CheckCircle2 className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                            ) : (
                              <Circle className="w-4 h-4 text-slate-600 group-hover:text-slate-400 flex-shrink-0" />
                            )}
                            <span className="text-xs font-bold text-slate-200 group-hover:text-blue-300 leading-tight">
                              {lesson.title}
                            </span>
                          </div>
                          {isFast && (
                            <span title="Included in 5-Day Bootcamp">
                              <Zap className="w-3 h-3 text-amber-400 fill-amber-400/40 flex-shrink-0" />
                            </span>
                          )}
                        </div>

                        <p className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
                          {lesson.summary}
                        </p>
                      </div>

                      <div className="pt-2 border-t border-dark-700/60 flex items-center justify-between text-[11px] text-slate-400">
                        <div className="flex items-center gap-1">
                          <Clock className="w-3 h-3" />
                          <span>{lesson.estimated_minutes} min</span>
                        </div>
                        <span className="text-blue-400 font-semibold group-hover:translate-x-0.5 transition-transform flex items-center gap-0.5">
                          Start <ChevronRight className="w-3 h-3" />
                        </span>
                      </div>
                    </Link>
                  );
                })}
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
};
