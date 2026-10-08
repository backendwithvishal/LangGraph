import React, { useState, useEffect } from 'react';
import {
  CheckCircle2,
  HelpCircle,
  Bug,
  Shuffle,
  Terminal,
  Lightbulb,
  Check,
  X,
  RotateCcw,
  Sparkles,
  ArrowRight
} from 'lucide-react';
import { api } from '../services/api';
import { useProgress } from '../context/ProgressContext';
import { Card } from '../components/ui/Card';
import { Badge } from '../components/ui/Badge';

export const PracticeCenter = () => {
  const { recordQuizScore, progress } = useProgress();
  const [quizzes, setQuizzes] = useState([]);
  const [selectedCategory, setSelectedCategory] = useState('all');
  const [answers, setAnswers] = useState({});
  const [results, setResults] = useState({});
  const [revealedHints, setRevealedHints] = useState({});
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    api.getQuizzes()
      .then(data => {
        setQuizzes(data || []);
        setLoading(false);
      })
      .catch(() => setLoading(false));
  }, []);

  const categories = ['all', 'Foundations', 'State Management', 'Debugging', 'Routing', 'Human-in-the-Loop', 'Streaming', 'Persistence', 'Functional API'];

  const filteredQuizzes = quizzes.filter(q => {
    if (selectedCategory !== 'all' && q.category.toLowerCase() !== selectedCategory.toLowerCase()) {
      return false;
    }
    return true;
  });

  const handleSelectOption = async (quizId, optionIndex, topicId) => {
    setAnswers(prev => ({ ...prev, [quizId]: optionIndex }));
    try {
      const res = await api.verifyQuiz(quizId, optionIndex);
      setResults(prev => ({ ...prev, [quizId]: res }));
      recordQuizScore(quizId, res.is_correct, topicId);
    } catch (e) {
      console.error('Verification error:', e);
    }
  };

  const toggleHint = (qid) => {
    setRevealedHints(prev => ({ ...prev, [qid]: !prev[qid] }));
  };

  const scoreValues = Object.values(progress.quizScores || {});
  const correctCount = scoreValues.filter(s => s.lastResult).length;
  const totalAttempted = scoreValues.length;

  return (
    <div className="max-w-5xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-dark-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <CheckCircle2 className="w-5 h-5 text-emerald-400" />
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Practice & Quiz Center
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            Reinforce your understanding through predict-the-output questions, bug-hunting challenges, and routing puzzles.
          </p>
        </div>

        {/* Score Counter */}
        <div className="flex items-center gap-3 px-4 py-2 rounded-xl bg-dark-850 border border-dark-750">
          <div className="text-right">
            <div className="text-xs font-semibold text-slate-300">Total Score</div>
            <div className="text-sm font-extrabold text-emerald-400 font-mono">
              {correctCount} / {quizzes.length} Correct
            </div>
          </div>
        </div>
      </div>

      {/* Category Pills */}
      <div className="flex flex-wrap items-center gap-2 overflow-x-auto pb-2">
        {categories.map(cat => (
          <button
            key={cat}
            onClick={() => setSelectedCategory(cat)}
            className={`px-3 py-1.5 rounded-lg text-xs font-semibold transition-colors capitalize ${
              selectedCategory === cat
                ? 'bg-blue-600 text-white shadow-md shadow-blue-500/20'
                : 'bg-dark-800 text-slate-400 hover:text-slate-200 border border-dark-700'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Quiz Question Cards */}
      <div className="space-y-6">
        {filteredQuizzes.map((q, idx) => {
          const selected = answers[q.id];
          const result = results[q.id];
          const isHintRevealed = revealedHints[q.id];

          return (
            <Card key={q.id} className="space-y-4 border-dark-750">
              
              {/* Question Header */}
              <div className="flex items-center justify-between">
                <div className="flex items-center gap-2">
                  <Badge variant={q.difficulty} size="xs">{q.difficulty}</Badge>
                  <span className="text-xs text-slate-400 font-medium">Category: {q.category}</span>
                </div>
                <span className="text-xs font-mono text-slate-500">#{q.id}</span>
              </div>

              {/* Question Prompt */}
              <div className="text-sm font-bold text-slate-100 leading-relaxed">
                {q.question}
              </div>

              {/* Code Snippet if applicable */}
              {q.code_snippet && (
                <pre className="p-3.5 rounded-xl bg-dark-950 border border-dark-750 text-xs font-mono text-cyan-200 overflow-x-auto leading-relaxed">
                  {q.code_snippet}
                </pre>
              )}

              {/* Options */}
              <div className="space-y-2">
                {q.options?.map((opt, optIdx) => {
                  const isThisSelected = selected === optIdx;
                  let optClasses = "bg-dark-800/80 hover:bg-dark-750 text-slate-200 border-dark-700";

                  if (result) {
                    if (optIdx === result.correct_answer) {
                      optClasses = "bg-emerald-950/40 text-emerald-300 border-emerald-500/60 font-semibold";
                    } else if (isThisSelected && !result.is_correct) {
                      optClasses = "bg-rose-950/40 text-rose-300 border-rose-500/60";
                    }
                  }

                  return (
                    <button
                      key={optIdx}
                      onClick={() => handleSelectOption(q.id, optIdx, q.topic_id)}
                      className={`w-full text-left p-3 rounded-xl border text-xs transition-all flex items-center justify-between gap-3 ${optClasses}`}
                    >
                      <span>{opt}</span>
                      {result && optIdx === result.correct_answer && (
                        <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                      )}
                      {result && isThisSelected && !result.is_correct && (
                        <X className="w-4 h-4 text-rose-400 flex-shrink-0" />
                      )}
                    </button>
                  );
                })}
              </div>

              {/* Hint and Explanation Section */}
              <div className="flex flex-wrap items-center justify-between gap-2 pt-2 border-t border-dark-800/80">
                {q.hint && (
                  <button
                    onClick={() => toggleHint(q.id)}
                    className="text-xs text-amber-400 hover:text-amber-300 flex items-center gap-1 font-semibold"
                  >
                    <Lightbulb className="w-3.5 h-3.5" />
                    <span>{isHintRevealed ? 'Hide Hint' : 'Need a Hint?'}</span>
                  </button>
                )}

                {result && (
                  <span className={`text-xs font-bold ${result.is_correct ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {result.feedback}
                  </span>
                )}
              </div>

              {/* Revealed Hint */}
              {isHintRevealed && (
                <div className="p-3 rounded-xl bg-amber-950/20 border border-amber-500/30 text-xs text-amber-200/90 flex items-start gap-2">
                  <Lightbulb className="w-4 h-4 text-amber-400 flex-shrink-0 mt-0.5" />
                  <div>
                    <span className="font-bold block mb-0.5">Hint:</span>
                    <span>{q.hint}</span>
                  </div>
                </div>
              )}

              {/* Conceptual Explanation */}
              {result && (
                <div className="p-3.5 rounded-xl bg-dark-900 border border-dark-700 text-xs text-slate-300 space-y-1">
                  <span className="font-bold text-slate-200 block">Conceptual Explanation:</span>
                  <p className="leading-relaxed">{result.explanation}</p>
                </div>
              )}
            </Card>
          );
        })}
      </div>
    </div>
  );
};
