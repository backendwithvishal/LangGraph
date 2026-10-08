import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { Search, X, BookOpen, Terminal, CheckCircle2, ArrowRight } from 'lucide-react';
import { api } from '../../services/api';

export const GlobalSearch = ({ isOpen, onClose }) => {
  const navigate = useNavigate();
  const [query, setQuery] = useState('');
  const [lessons, setLessons] = useState([]);
  const [glossary, setGlossary] = useState([]);

  useEffect(() => {
    if (isOpen) {
      api.getLessons().then(data => setLessons(data || [])).catch(() => {});
      api.getGlossary().then(data => setGlossary(data || [])).catch(() => {});
    }
  }, [isOpen]);

  useEffect(() => {
    const handleKeyDown = (e) => {
      if ((e.metaKey || e.ctrlKey) && e.key === 'k') {
        e.preventDefault();
        onClose ? onClose() : null;
      }
      if (e.key === 'Escape') {
        onClose();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [onClose]);

  if (!isOpen) return null;

  const filteredLessons = lessons.filter(l =>
    l.title.toLowerCase().includes(query.toLowerCase()) ||
    l.summary?.toLowerCase().includes(query.toLowerCase()) ||
    l.topics?.some(t => t.toLowerCase().includes(query.toLowerCase()))
  ).slice(0, 5);

  const filteredGlossary = glossary.filter(g =>
    g.term.toLowerCase().includes(query.toLowerCase()) ||
    g.definition.toLowerCase().includes(query.toLowerCase())
  ).slice(0, 4);

  const handleSelectLesson = (id) => {
    onClose();
    navigate(`/lessons/${id}`);
  };

  const handleSelectGlossary = (term) => {
    onClose();
    navigate(`/reference?search=${encodeURIComponent(term)}`);
  };

  return (
    <div className="fixed inset-0 z-50 bg-black/70 backdrop-blur-sm flex items-start justify-center pt-20 px-4">
      <div className="w-full max-w-2xl bg-dark-900 border border-dark-700 rounded-xl shadow-2xl overflow-hidden animate-in fade-in zoom-in-95 duration-150">
        
        {/* Search Input Box */}
        <div className="flex items-center px-4 border-b border-dark-800 gap-3">
          <Search className="w-5 h-5 text-slate-400" />
          <input
            type="text"
            autoFocus
            placeholder="Search lessons, concepts, APIs, errors, or keywords..."
            value={query}
            onChange={(e) => setQuery(e.target.value)}
            className="w-full py-4 bg-transparent text-sm text-slate-100 placeholder-slate-500 focus:outline-none"
          />
          <button
            onClick={onClose}
            className="p-1 rounded text-slate-400 hover:text-slate-200"
          >
            <X className="w-4 h-4" />
          </button>
        </div>

        {/* Search Results Area */}
        <div className="max-h-96 overflow-y-auto p-3 space-y-4">
          
          {/* Lessons Section */}
          {filteredLessons.length > 0 && (
            <div>
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <BookOpen className="w-3.5 h-3.5 text-blue-400" />
                <span>Lessons & Modules</span>
              </div>
              <div className="space-y-1">
                {filteredLessons.map(lesson => (
                  <button
                    key={lesson.id}
                    onClick={() => handleSelectLesson(lesson.id)}
                    className="w-full text-left p-2.5 rounded-lg hover:bg-dark-800 transition-colors flex items-center justify-between group"
                  >
                    <div>
                      <div className="text-xs font-semibold text-slate-200 group-hover:text-blue-400">
                        {lesson.title}
                      </div>
                      <div className="text-[11px] text-slate-400 line-clamp-1">
                        {lesson.summary}
                      </div>
                    </div>
                    <ArrowRight className="w-4 h-4 text-slate-600 group-hover:text-blue-400 flex-shrink-0" />
                  </button>
                ))}
              </div>
            </div>
          )}

          {/* Glossary Section */}
          {filteredGlossary.length > 0 && (
            <div>
              <div className="px-2 pb-1.5 text-[11px] font-bold uppercase tracking-wider text-slate-400 flex items-center gap-1.5">
                <Terminal className="w-3.5 h-3.5 text-cyan-400" />
                <span>Glossary Terms</span>
              </div>
              <div className="space-y-1">
                {filteredGlossary.map(term => (
                  <button
                    key={term.term}
                    onClick={() => handleSelectGlossary(term.term)}
                    className="w-full text-left p-2.5 rounded-lg hover:bg-dark-800 transition-colors flex items-center justify-between group"
                  >
                    <div>
                      <div className="text-xs font-semibold text-cyan-300 font-mono">
                        {term.term}
                      </div>
                      <div className="text-[11px] text-slate-400 line-clamp-1">
                        {term.definition}
                      </div>
                    </div>
                    <span className="text-[10px] px-2 py-0.5 rounded bg-dark-700 text-slate-400">
                      {term.category}
                    </span>
                  </button>
                ))}
              </div>
            </div>
          )}

          {query && filteredLessons.length === 0 && filteredGlossary.length === 0 && (
            <div className="text-center py-8 text-slate-400 text-xs">
              No matching lessons or terms found for "{query}".
            </div>
          )}

          {!query && (
            <div className="px-2 py-4 text-xs text-slate-400 space-y-2">
              <div className="font-semibold text-slate-300 text-[11px] uppercase tracking-wider">Quick Suggestions:</div>
              <div className="flex flex-wrap gap-1.5">
                {["StateGraph", "interrupt()", "Command", "MemorySaver", "tools_condition", "Subgraphs", "Send API", "Pregel Super-Step"].map(tag => (
                  <button
                    key={tag}
                    onClick={() => setQuery(tag)}
                    className="px-2.5 py-1 rounded bg-dark-800 hover:bg-dark-700 text-slate-300 border border-dark-700 text-xs transition-colors"
                  >
                    {tag}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>

        {/* Footer */}
        <div className="px-4 py-2 bg-dark-950/80 border-t border-dark-800 flex items-center justify-between text-[11px] text-slate-400">
          <span>Press <kbd className="px-1 bg-dark-800 rounded border border-dark-700">ESC</kbd> to exit</span>
          <span>Navigation: <kbd className="px-1 bg-dark-800 rounded border border-dark-700">↵</kbd> select</span>
        </div>
      </div>
    </div>
  );
};
