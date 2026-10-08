import React, { useState } from 'react';
import { Link } from 'react-router-dom';
import {
  CheckCircle2,
  Bookmark,
  AlertTriangle,
  Download,
  Upload,
  RotateCcw,
  Sparkles,
  BookOpen,
  ArrowRight,
  Shield,
  FileText
} from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';
import { ProgressBar } from '../components/ui/ProgressBar';

export const ProgressRevision = () => {
  const {
    progress,
    completedCount,
    exportProgressJSON,
    importProgressJSON,
    resetAllProgress
  } = useProgress();

  const [importText, setImportText] = useState('');
  const [importStatus, setImportStatus] = useState(null);
  const [showImportModal, setShowImportModal] = useState(false);

  const totalLessons = 32;
  const percent = Math.min(100, Math.round((completedCount / totalLessons) * 100));

  // Identify weak topics from quiz scores
  const quizScores = Object.entries(progress.quizScores || {});
  const weakTopics = quizScores
    .filter(([_, score]) => !score.lastResult)
    .map(([qid, score]) => ({
      qid,
      topicId: score.topicId || 'module-1',
      attempts: score.attempts
    }));

  const handleExport = () => {
    const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(exportProgressJSON());
    const downloadAnchor = document.createElement('a');
    downloadAnchor.setAttribute("href", dataStr);
    downloadAnchor.setAttribute("download", "graphlab_progress.json");
    document.body.appendChild(downloadAnchor);
    downloadAnchor.click();
    downloadAnchor.remove();
  };

  const handleImport = () => {
    const success = importProgressJSON(importText);
    setImportStatus(success ? 'Imported successfully!' : 'Invalid JSON format');
    if (success) {
      setTimeout(() => setShowImportModal(false), 1500);
    }
  };

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-dark-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle2 className="w-5 h-5 text-blue-400" />
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Learning Progress & Revision Queue
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            Track completed curriculum topics, review weak areas, and manage bookmarks.
          </p>
        </div>

        {/* Data Portability Actions */}
        <div className="flex items-center gap-2">
          <button
            onClick={handleExport}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-750 text-slate-300 hover:text-white border border-dark-700 text-xs font-semibold transition-colors"
          >
            <Download className="w-3.5 h-3.5" />
            <span>Export Progress</span>
          </button>

          <button
            onClick={() => setShowImportModal(true)}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-750 text-slate-300 hover:text-white border border-dark-700 text-xs font-semibold transition-colors"
          >
            <Upload className="w-3.5 h-3.5" />
            <span>Import</span>
          </button>
        </div>
      </div>

      {/* Progress Stats Summary */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        <Card className="space-y-3 border-blue-500/20 bg-blue-950/10">
          <div className="text-xs font-bold text-blue-300 uppercase tracking-wider">
            Overall Curriculum Mastery
          </div>
          <div className="text-3xl font-extrabold text-white">
            {percent}% <span className="text-xs font-normal text-slate-400">({completedCount}/{totalLessons})</span>
          </div>
          <ProgressBar progress={percent} color="blue" size="md" />
        </Card>

        <Card className="space-y-2 border-dark-750">
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Bookmarks Saved
          </div>
          <div className="text-3xl font-extrabold text-white">
            {progress.bookmarks?.length || 0}
          </div>
          <p className="text-xs text-slate-400">Lessons flagged for quick review</p>
        </Card>

        <Card className="space-y-2 border-dark-750">
          <div className="text-xs font-bold text-slate-300 uppercase tracking-wider">
            Projects Completed
          </div>
          <div className="text-3xl font-extrabold text-emerald-400">
            {Object.keys(progress.completedProjects || {}).length} <span className="text-xs text-slate-400 font-normal">/ 9</span>
          </div>
          <p className="text-xs text-slate-400">Practical application builds</p>
        </Card>
      </div>

      {/* Weak Topics Revision Queue */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <AlertTriangle className="w-4 h-4 text-amber-400" />
          <h2 className="text-base font-bold text-white">
            Weak Topics Revision Queue ({weakTopics.length})
          </h2>
        </div>

        {weakTopics.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            {weakTopics.map(w => (
              <Card key={w.qid} className="p-4 border-amber-500/30 bg-amber-950/10 flex items-center justify-between">
                <div>
                  <div className="text-xs font-bold text-amber-300">
                    Topic Question #{w.qid}
                  </div>
                  <div className="text-[11px] text-slate-400 mt-0.5">
                    Failed on {w.attempts} practice attempts
                  </div>
                </div>
                <Link
                  to="/practice"
                  className="px-3 py-1.5 rounded-lg bg-amber-500/20 hover:bg-amber-500/30 text-amber-300 text-xs font-semibold transition-colors"
                >
                  Retake Quiz
                </Link>
              </Card>
            ))}
          </div>
        ) : (
          <div className="p-6 rounded-xl border border-dark-800 bg-dark-850/40 text-center text-xs text-slate-400">
            ✓ No weak topics recorded yet! Take practice quizzes to identify conceptual gaps.
          </div>
        )}
      </div>

      {/* Bookmarks Section */}
      <div className="space-y-4">
        <div className="flex items-center gap-2">
          <Bookmark className="w-4 h-4 text-blue-400" />
          <h2 className="text-base font-bold text-white">
            Saved Lesson Bookmarks ({progress.bookmarks?.length || 0})
          </h2>
        </div>

        {progress.bookmarks?.length > 0 ? (
          <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
            {progress.bookmarks.map(id => (
              <Link
                key={id}
                to={`/lessons/${id}`}
                className="p-3.5 rounded-xl border border-dark-750 bg-dark-850 hover:bg-dark-800 transition-colors flex items-center justify-between group"
              >
                <div className="flex items-center gap-2">
                  <BookOpen className="w-4 h-4 text-blue-400" />
                  <span className="text-xs font-bold text-slate-200 group-hover:text-blue-300 font-mono">
                    {id}
                  </span>
                </div>
                <ArrowRight className="w-3.5 h-3.5 text-slate-500 group-hover:text-blue-400 group-hover:translate-x-0.5 transition-all" />
              </Link>
            ))}
          </div>
        ) : (
          <div className="p-6 rounded-xl border border-dark-800 bg-dark-850/40 text-center text-xs text-slate-400">
            No bookmarks saved. Click the bookmark icon in any lesson to add it here.
          </div>
        )}
      </div>

      {/* Reset Progress Section */}
      <div className="pt-6 border-t border-dark-800 flex justify-between items-center text-xs text-slate-500">
        <span>Progress is saved in browser localStorage</span>
        <button
          onClick={() => {
            if (window.confirm("Are you sure you want to reset all learning progress?")) {
              resetAllProgress();
            }
          }}
          className="text-rose-400 hover:text-rose-300 font-semibold"
        >
          Reset All Progress
        </button>
      </div>

      {/* Import Modal */}
      {showImportModal && (
        <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="w-full max-w-md bg-dark-900 border border-dark-700 rounded-xl p-5 space-y-4">
            <h3 className="text-sm font-bold text-white">Import Learning Progress JSON</h3>
            <textarea
              value={importText}
              onChange={(e) => setImportText(e.target.value)}
              placeholder="Paste exported JSON here..."
              rows={6}
              className="w-full p-3 rounded-lg bg-dark-950 border border-dark-750 text-xs text-slate-200 font-mono focus:outline-none focus:ring-1 focus:ring-blue-500"
            />
            {importStatus && (
              <div className="text-xs font-bold text-emerald-400">{importStatus}</div>
            )}
            <div className="flex justify-end gap-2">
              <button
                onClick={() => setShowImportModal(false)}
                className="px-3 py-1.5 rounded bg-dark-800 text-slate-400 text-xs"
              >
                Cancel
              </button>
              <button
                onClick={handleImport}
                className="px-3 py-1.5 rounded bg-blue-600 text-white font-semibold text-xs"
              >
                Import Data
              </button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
