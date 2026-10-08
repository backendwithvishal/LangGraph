import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import {
  Play,
  CheckCircle2,
  BookOpen,
  GitBranch,
  Terminal,
  Zap,
  Clock,
  ArrowRight,
  Shield,
  Layers,
  Sparkles,
  HelpCircle,
  FolderGit2
} from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import { api } from '../services/api';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';

export const Dashboard = () => {
  const navigate = useNavigate();
  const { progress, completedCount, isLessonCompleted } = useProgress();
  const [curriculum, setCurriculum] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getCurriculum()
      .then(data => {
        setCurriculum(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Failed to load curriculum:', err);
        setLoading(false);
      });
  }, []);

  const totalLessons = curriculum?.total_lessons || 32;
  const totalMinutes = curriculum?.total_estimated_minutes || 540;
  const percent = Math.min(100, Math.round((completedCount / totalLessons) * 100));

  // Find next recommended lesson
  let nextLesson = null;
  let nextModule = null;

  if (curriculum?.modules) {
    for (const mod of curriculum.modules) {
      for (const les of mod.lessons) {
        if (!isLessonCompleted(les.id)) {
          nextLesson = les;
          nextModule = mod;
          break;
        }
      }
      if (nextLesson) break;
    }
  }

  // Calculate remaining minutes
  const completedMinutes = (completedCount * (totalMinutes / totalLessons));
  const remainingMinutes = Math.max(0, Math.round(totalMinutes - completedMinutes));

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Hero Banner with Continue Learning Action */}
      <div className="relative rounded-2xl border border-blue-500/20 bg-gradient-to-r from-blue-950/40 via-dark-850 to-dark-900 p-6 sm:p-8 overflow-hidden shadow-2xl">
        <div className="absolute top-0 right-0 -mr-16 -mt-16 w-80 h-80 bg-blue-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute bottom-0 right-1/4 -mb-16 w-60 h-60 bg-cyan-500/10 rounded-full blur-2xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="flex flex-wrap items-center gap-2">
            <Badge variant="beginner" size="sm">
              <Sparkles className="w-3 h-3 mr-1" />
              Accelerated LangGraph 0.2+ Curriculum
            </Badge>
            {progress.fastTrackMode && (
              <Badge variant="production" size="sm">
                <Zap className="w-3 h-3 mr-1" />
                5-Day Intensive Bootcamp Active
              </Badge>
            )}
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
            Master Stateful Multi-Agent AI with <span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 via-cyan-400 to-emerald-400">LangGraph</span>
          </h1>

          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            Learn cyclical graphs, state reducers, persistence checkpointing, dynamic human-in-the-loop interrupts, and real-time streaming with live visual execution.
          </p>

          <div className="pt-2 flex flex-wrap items-center gap-4">
            {nextLesson ? (
              <Link
                to={`/lessons/${nextLesson.id}`}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-gradient-to-r from-blue-600 to-cyan-500 hover:from-blue-500 hover:to-cyan-400 text-white font-bold text-sm shadow-lg shadow-blue-500/25 transition-all transform hover:-translate-y-0.5"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>Continue: {nextLesson.title}</span>
              </Link>
            ) : (
              <Link
                to="/lessons/m1-l1"
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white font-bold text-sm shadow-lg transition-all"
              >
                <Play className="w-4 h-4 fill-white" />
                <span>Start Lesson 1</span>
              </Link>
            )}

            <Link
              to="/playground"
              className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-dark-800 hover:bg-dark-750 text-slate-200 font-semibold text-sm border border-dark-700 hover:border-dark-600 transition-all"
            >
              <GitBranch className="w-4 h-4 text-cyan-400" />
              <span>Launch Graph Playground</span>
            </Link>
          </div>
        </div>
      </div>

      {/* Metrics Row */}
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
        
        {/* Metric 1 */}
        <Card className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-blue-500/10 border border-blue-500/20 flex items-center justify-center text-blue-400 flex-shrink-0">
            <CheckCircle2 className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">
              {completedCount} <span className="text-xs font-normal text-slate-400">/ {totalLessons}</span>
            </div>
            <div className="text-xs text-slate-400 font-medium">Lessons Mastered</div>
          </div>
        </Card>

        {/* Metric 2 */}
        <Card className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-cyan-500/10 border border-cyan-500/20 flex items-center justify-center text-cyan-400 flex-shrink-0">
            <Layers className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">{percent}%</div>
            <div className="text-xs text-slate-400 font-medium">Curriculum Progress</div>
          </div>
        </Card>

        {/* Metric 3 */}
        <Card className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-amber-500/10 border border-amber-500/20 flex items-center justify-center text-amber-400 flex-shrink-0">
            <Clock className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">{remainingMinutes} <span className="text-xs font-normal text-slate-400">min</span></div>
            <div className="text-xs text-slate-400 font-medium">Estimated Study Left</div>
          </div>
        </Card>

        {/* Metric 4 */}
        <Card className="flex items-center gap-4">
          <div className="w-12 h-12 rounded-xl bg-emerald-500/10 border border-emerald-500/20 flex items-center justify-center text-emerald-400 flex-shrink-0">
            <FolderGit2 className="w-6 h-6" />
          </div>
          <div>
            <div className="text-2xl font-extrabold text-white">9 <span className="text-xs font-normal text-slate-400">Projects</span></div>
            <div className="text-xs text-slate-400 font-medium">Hands-On Builds</div>
          </div>
        </Card>
      </div>

      {/* Main Sections Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Left 2 Cols: 5-Day Intensive Track & Featured Modules */}
        <div className="lg:col-span-2 space-y-6">
          
          <div className="flex items-center justify-between">
            <div>
              <h2 className="text-lg font-bold text-slate-100 flex items-center gap-2">
                <BookOpen className="w-5 h-5 text-blue-400" />
                <span>Structured Learning Tracks</span>
              </h2>
              <p className="text-xs text-slate-400 mt-0.5">
                From basic StateGraph to enterprise-grade subgraphs and deployment
              </p>
            </div>
            <Link to="/path" className="text-xs font-semibold text-blue-400 hover:text-blue-300 flex items-center gap-1">
              View All 14 Modules <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </div>

          {/* Module Cards Grid */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            {curriculum?.modules?.slice(0, 4).map(mod => {
              const completedInMod = mod.lessons.filter(l => isLessonCompleted(l.id)).length;
              const modPercent = Math.round((completedInMod / mod.lessons.length) * 100);

              return (
                <Card
                  key={mod.id}
                  hover
                  onClick={() => navigate(`/lessons/${mod.lessons[0]?.id}`)}
                  className="space-y-3"
                >
                  <div className="flex items-center justify-between">
                    <Badge variant={mod.difficulty}>{mod.difficulty}</Badge>
                    <span className="text-[11px] font-mono text-slate-400">
                      {completedInMod}/{mod.lessons.length} Done
                    </span>
                  </div>

                  <div>
                    <h3 className="font-bold text-slate-100 text-sm">{mod.title}</h3>
                    <p className="text-xs text-slate-400 line-clamp-2 mt-1 leading-relaxed">
                      {mod.description}
                    </p>
                  </div>

                  <ProgressBar progress={modPercent} size="sm" color="blue" />
                </Card>
              );
            })}
          </div>

          {/* 5-Day Accelerated Schedule Callout */}
          <div className="p-5 rounded-xl border border-dark-750 bg-dark-850/60 space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-bold text-xs uppercase tracking-wider text-slate-300 flex items-center gap-1.5">
                <Zap className="w-4 h-4 text-amber-400" />
                <span>5-Day Recommended Accelerated Schedule</span>
              </span>
              <Badge variant="production" size="xs">Intensive Plan</Badge>
            </div>

            <div className="grid grid-cols-1 sm:grid-cols-5 gap-2 text-xs">
              <div className="p-2.5 rounded-lg bg-dark-900/80 border border-dark-800 space-y-1">
                <div className="font-bold text-slate-200">Day 1</div>
                <div className="text-[11px] text-slate-400 leading-tight">Foundations, StateGraph, TypedDict, START/END</div>
              </div>
              <div className="p-2.5 rounded-lg bg-dark-900/80 border border-dark-800 space-y-1">
                <div className="font-bold text-slate-200">Day 2</div>
                <div className="text-[11px] text-slate-400 leading-tight">Reducers, Routing, Tools, ReAct Agents</div>
              </div>
              <div className="p-2.5 rounded-lg bg-dark-900/80 border border-dark-800 space-y-1">
                <div className="font-bold text-slate-200">Day 3</div>
                <div className="text-[11px] text-slate-400 leading-tight">Checkpointers, Memory, Interrupts, Streaming</div>
              </div>
              <div className="p-2.5 rounded-lg bg-dark-900/80 border border-dark-800 space-y-1">
                <div className="font-bold text-slate-200">Day 4</div>
                <div className="text-[11px] text-slate-400 leading-tight">Subgraphs, Multi-Agent Supervisor, Functional API</div>
              </div>
              <div className="p-2.5 rounded-lg bg-dark-900/80 border border-dark-800 space-y-1">
                <div className="font-bold text-slate-200">Day 5</div>
                <div className="text-[11px] text-slate-400 leading-tight">CRAG, Testing, Observability & Capstone</div>
              </div>
            </div>
          </div>
        </div>

        {/* Right Col: Quick Access Hub & Weak Topics */}
        <div className="space-y-6">
          
          {/* Quick Playground Launcher */}
          <Card className="space-y-4 border-cyan-500/20 bg-gradient-to-b from-cyan-950/20 to-dark-850">
            <div className="flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-cyan-400" />
              <h3 className="font-bold text-slate-100 text-sm">Interactive Playground</h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              Step through real LangGraph graphs with live node glows and state channel diff inspection.
            </p>
            <div className="space-y-2">
              <Link
                to="/playground?example=sequential-pipeline"
                className="block p-2.5 rounded-lg bg-dark-800/80 hover:bg-dark-750 text-xs text-slate-200 font-medium transition-colors border border-dark-700/60"
              >
                1. Linear Transformation Pipeline
              </Link>
              <Link
                to="/playground?example=conditional-branching"
                className="block p-2.5 rounded-lg bg-dark-800/80 hover:bg-dark-750 text-xs text-slate-200 font-medium transition-colors border border-dark-700/60"
              >
                2. Dynamic Intent Routing
              </Link>
              <Link
                to="/playground?example=human-in-the-loop-approval"
                className="block p-2.5 rounded-lg bg-dark-800/80 hover:bg-dark-750 text-xs text-slate-200 font-medium transition-colors border border-dark-700/60"
              >
                3. Human-in-the-Loop Wire Approval
              </Link>
            </div>
            <Link
              to="/playground"
              className="w-full py-2 rounded-lg bg-cyan-600/20 hover:bg-cyan-600/30 text-cyan-300 text-xs font-semibold flex items-center justify-center gap-1.5 border border-cyan-500/30 transition-colors"
            >
              <span>Open Full Playground</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </Card>

          {/* Quick Quizzes Card */}
          <Card className="space-y-3">
            <div className="flex items-center justify-between">
              <span className="font-bold text-slate-200 text-xs uppercase tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <span>Practice & Quiz Center</span>
              </span>
              <Badge variant="beginner" size="xs">Self-Check</Badge>
            </div>
            <p className="text-xs text-slate-400 leading-relaxed">
              Test your knowledge with Predict-the-Output exercises, Bug Hunter challenges, and routing puzzles.
            </p>
            <Link
              to="/practice"
              className="w-full py-2 rounded-lg bg-dark-800 hover:bg-dark-750 text-slate-200 text-xs font-semibold flex items-center justify-center gap-1.5 border border-dark-700 transition-colors"
            >
              <span>Start Practice Challenge</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </Link>
          </Card>
        </div>
      </div>
    </div>
  );
};
