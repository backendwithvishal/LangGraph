import React, { useState, useEffect } from 'react';
import { useParams, Link } from 'react-router-dom';
import {
  FolderGit2,
  CheckCircle2,
  Clock,
  Code2,
  Terminal,
  Play,
  Lightbulb,
  Check,
  RotateCcw,
  Sparkles,
  ChevronLeft,
  Eye,
  EyeOff
} from 'lucide-react';
import { api } from '../services/api';
import { useProgress } from '../context/ProgressContext';
import { CodeEditor } from '../components/editor/CodeEditor';
import { TerminalOutput } from '../components/editor/TerminalOutput';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const ProjectDetail = () => {
  const { projectId } = useParams();
  const { markProjectComplete, progress } = useProgress();
  const [project, setProject] = useState(null);
  const [showSolution, setShowSolution] = useState(false);
  const [code, setCode] = useState('');
  const [isRunning, setIsRunning] = useState(false);
  const [runnerOutput, setRunnerOutput] = useState({ stdout: '', stderr: '', error: null, executionTimeMs: null });
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (projectId) {
      api.getProject(projectId)
        .then(data => {
          setProject(data);
          setCode(data.solution_code || data.starter_code || '');
          setLoading(false);
        })
        .catch(() => setLoading(false));
    }
  }, [projectId]);

  const handleRunCode = async (codeToRun) => {
    setIsRunning(true);
    setRunnerOutput({ stdout: '', stderr: '', error: null, executionTimeMs: null });
    try {
      // Append test suite code for complete test assertion
      const fullCode = `${codeToRun}\n\n${project.test_cases_code || ''}`;
      const res = await api.runCustomCode(fullCode);
      setRunnerOutput({
        stdout: res.stdout,
        stderr: res.stderr,
        error: res.error,
        executionTimeMs: res.execution_time_ms
      });
      if (res.success && !res.error) {
        markProjectComplete(project.id);
      }
    } catch (e) {
      setRunnerOutput({
        stdout: '',
        stderr: '',
        error: e.message,
        executionTimeMs: 0
      });
    } finally {
      setIsRunning(false);
    }
  };

  const isCompleted = Boolean(progress.completedProjects?.[project?.id]);

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[50vh] text-slate-400">
        <Sparkles className="w-5 h-5 text-blue-400 animate-spin mr-2" />
        <span>Loading Project Specs...</span>
      </div>
    );
  }

  if (!project) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <h2 className="text-xl font-bold text-white">Project Not Found</h2>
        <Link to="/projects" className="px-4 py-2 bg-blue-600 text-white rounded-lg text-xs inline-block">
          Return to Projects
        </Link>
      </div>
    );
  }

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="space-y-3 border-b border-dark-800 pb-6">
        <div className="flex items-center justify-between">
          <Link
            to="/projects"
            className="text-xs text-slate-400 hover:text-slate-200 flex items-center gap-1"
          >
            <ChevronLeft className="w-3.5 h-3.5" />
            <span>Back to Projects</span>
          </Link>

          <button
            onClick={() => markProjectComplete(project.id)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              isCompleted
                ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                : 'bg-dark-800 text-slate-300 border border-dark-700 hover:text-white'
            }`}
          >
            <CheckCircle2 className="w-3.5 h-3.5" />
            <span>{isCompleted ? 'Project Completed ✓' : 'Mark as Done'}</span>
          </button>
        </div>

        <div className="flex flex-wrap items-center gap-2 pt-1">
          <Badge variant={project.difficulty}>{project.difficulty}</Badge>
          <span className="text-xs text-slate-400">•</span>
          <span className="text-xs text-slate-400 flex items-center gap-1">
            <Clock className="w-3 h-3" /> {project.estimated_hours} Hours Build
          </span>
        </div>

        <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
          {project.title}
        </h1>

        <p className="text-sm text-slate-300 max-w-3xl leading-relaxed">
          {project.description}
        </p>
      </div>

      {/* Architecture & Requirements Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        
        {/* Architecture Spec */}
        <Card className="space-y-3 border-dark-750">
          <div className="text-xs font-bold text-blue-300 uppercase tracking-wider flex items-center gap-1.5">
            <Code2 className="w-4 h-4 text-blue-400" />
            <span>Architecture Diagram</span>
          </div>
          <pre className="p-3.5 rounded-xl bg-dark-950 border border-dark-750 text-xs font-mono text-cyan-200 overflow-x-auto leading-relaxed">
            {project.architecture_diagram}
          </pre>
        </Card>

        {/* Requirements */}
        <Card className="space-y-3 border-dark-750">
          <div className="text-xs font-bold text-emerald-300 uppercase tracking-wider flex items-center gap-1.5">
            <Sparkles className="w-4 h-4 text-emerald-400" />
            <span>Functional Requirements</span>
          </div>
          <ul className="space-y-2 text-xs text-slate-300">
            {project.requirements?.map((req, i) => (
              <li key={i} className="flex items-start gap-2">
                <span className="w-4 h-4 rounded-full bg-emerald-500/10 text-emerald-400 flex items-center justify-center text-[10px] font-bold flex-shrink-0 mt-0.5">
                  {i + 1}
                </span>
                <span>{req}</span>
              </li>
            ))}
          </ul>
        </Card>
      </div>

      {/* Interactive Code Editor & Test Runner */}
      <div className="space-y-4">
        <div className="flex items-center justify-between">
          <h2 className="text-lg font-bold text-white flex items-center gap-2">
            <Terminal className="w-5 h-5 text-emerald-400" />
            <span>Project Implementation & Automated Testing</span>
          </h2>

          <button
            onClick={() => setShowSolution(!showSolution)}
            className="text-xs text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1"
          >
            {showSolution ? <EyeOff className="w-3.5 h-3.5" /> : <Eye className="w-3.5 h-3.5" />}
            <span>{showSolution ? 'Hide Solution Reference' : 'Reveal Solution Reference'}</span>
          </button>
        </div>

        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-[460px]">
          <CodeEditor
            initialCode={code}
            onChange={setCode}
            onRun={handleRunCode}
            isRunning={isRunning}
            title={`${project.id}_solution.py`}
          />
          <TerminalOutput
            stdout={runnerOutput.stdout}
            stderr={runnerOutput.stderr}
            error={runnerOutput.error}
            executionTimeMs={runnerOutput.executionTimeMs}
            isLoading={isRunning}
          />
        </div>
      </div>
    </div>
  );
};
