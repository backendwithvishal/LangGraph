import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { FolderGit2, CheckCircle2, Circle, Clock, ArrowRight, Sparkles, Layers } from 'lucide-react';
import { api } from '../services/api';
import { useProgress } from '../context/ProgressContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const ProjectsCenter = () => {
  const { progress } = useProgress();
  const [projects, setProjects] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getProjects()
      .then(data => {
        setProjects(data || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="border-b border-dark-800 pb-6 space-y-2">
        <div className="flex items-center gap-2">
          <FolderGit2 className="w-5 h-5 text-emerald-400" />
          <h1 className="text-2xl font-extrabold text-white tracking-tight">
            Guided Real-World Projects
          </h1>
        </div>
        <p className="text-xs text-slate-400 max-w-2xl">
          Build 9 practical, production-oriented LangGraph systems—from conditional ticket triaging to multi-agent supervisors and streaming capstones.
        </p>
      </div>

      {/* Projects Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {projects.map((proj, idx) => {
          const isDone = Boolean(progress.completedProjects?.[proj.id]);

          return (
            <Card
              key={proj.id}
              hover
              className="flex flex-col justify-between space-y-4 border-dark-750"
            >
              <div className="space-y-3">
                <div className="flex items-center justify-between">
                  <Badge variant={proj.difficulty}>{proj.difficulty}</Badge>
                  <div className="flex items-center gap-1.5 text-[11px] text-slate-400">
                    <Clock className="w-3.5 h-3.5" />
                    <span>{proj.estimated_hours} hrs</span>
                  </div>
                </div>

                <h2 className="font-bold text-slate-100 text-sm leading-snug">
                  {proj.title}
                </h2>

                <p className="text-xs text-slate-400 line-clamp-3 leading-relaxed">
                  {proj.description}
                </p>

                {/* Outcomes */}
                <div className="space-y-1 pt-1">
                  <div className="text-[10px] uppercase font-bold text-slate-400 tracking-wider">
                    Key Outcomes:
                  </div>
                  <ul className="space-y-0.5 text-[11px] text-slate-300">
                    {proj.learning_outcomes?.slice(0, 2).map((outcome, i) => (
                      <li key={i} className="flex items-start gap-1.5">
                        <span className="text-emerald-400">•</span>
                        <span className="line-clamp-1">{outcome}</span>
                      </li>
                    ))}
                  </ul>
                </div>
              </div>

              <div className="pt-3 border-t border-dark-800 flex items-center justify-between">
                <div className="flex items-center gap-1 text-xs">
                  {isDone ? (
                    <span className="text-emerald-400 flex items-center gap-1 font-semibold">
                      <CheckCircle2 className="w-3.5 h-3.5" /> Completed
                    </span>
                  ) : (
                    <span className="text-slate-400">Not Started</span>
                  )}
                </div>

                <Link
                  to={`/projects/${proj.id}`}
                  className="px-3 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white text-xs font-semibold flex items-center gap-1 transition-colors"
                >
                  <span>Build Project</span>
                  <ArrowRight className="w-3.5 h-3.5" />
                </Link>
              </div>
            </Card>
          );
        })}
      </div>
    </div>
  );
};
