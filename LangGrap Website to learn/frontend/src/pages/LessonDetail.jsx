import React, { useState, useEffect } from 'react';
import { useParams, Link, useNavigate } from 'react-router-dom';
import {
  BookOpen,
  CheckCircle2,
  Circle,
  Bookmark,
  ExternalLink,
  ChevronLeft,
  ChevronRight,
  Sparkles,
  AlertTriangle,
  Lightbulb,
  Terminal,
  Code2,
  Check,
  RotateCcw,
  HelpCircle,
  FileText
} from 'lucide-react';
import { useProgress } from '../context/ProgressContext';
import { api } from '../services/api';
import { Sidebar } from '../components/layout/Sidebar';
import { CodeEditor } from '../components/editor/CodeEditor';
import { TerminalOutput } from '../components/editor/TerminalOutput';
import { Badge } from '../components/ui/Badge';
import { Card } from '../components/ui/Card';

export const LessonDetail = () => {
  const { lessonId } = useParams();
  const navigate = useNavigate();
  const {
    isLessonCompleted,
    markLessonComplete,
    isBookmarked,
    toggleBookmark,
    getNote,
    saveNote,
    setLastVisited
  } = useProgress();

  const [lesson, setLesson] = useState(null);
  const [curriculum, setCurriculum] = useState(null);
  const [loading, setLoading] = useState(true);
  const [noteText, setNoteText] = useState('');
  const [quizAnswers, setQuizAnswers] = useState({});
  const [quizFeedback, setQuizFeedback] = useState({});
  const [activeTab, setActiveTab] = useState('lesson'); // 'lesson' | 'practice' | 'notes'

  // Code runner state
  const [isRunning, setIsRunning] = useState(false);
  const [runnerOutput, setRunnerOutput] = useState({ stdout: '', stderr: '', error: null, executionTimeMs: null });

  useEffect(() => {
    setLoading(true);
    setQuizAnswers({});
    setQuizFeedback({});
    setRunnerOutput({ stdout: '', stderr: '', error: null, executionTimeMs: null });

    if (lessonId) {
      setLastVisited(lessonId);
      setNoteText(getNote(lessonId));

      api.getLesson(lessonId)
        .then(data => {
          setLesson(data);
          setLoading(false);
        })
        .catch(err => {
          console.error('Failed to load lesson:', err);
          setLoading(false);
        });

      api.getCurriculum()
        .then(data => setCurriculum(data))
        .catch(() => {});
    }
  }, [lessonId]);

  const handleRunCode = async (codeToRun) => {
    setIsRunning(true);
    setRunnerOutput({ stdout: '', stderr: '', error: null, executionTimeMs: null });
    try {
      const res = await api.runCustomCode(codeToRun);
      setRunnerOutput({
        stdout: res.stdout,
        stderr: res.stderr,
        error: res.error,
        executionTimeMs: res.execution_time_ms
      });
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

  const handleQuizSelect = (qIdx, optIdx, correctIdx, explanation) => {
    const isCorrect = (optIdx === correctIdx);
    setQuizAnswers(prev => ({ ...prev, [qIdx]: optIdx }));
    setQuizFeedback(prev => ({
      ...prev,
      [qIdx]: {
        isCorrect,
        explanation
      }
    }));
  };

  if (loading) {
    return (
      <div className="flex items-center justify-center min-h-[60vh] text-slate-400">
        <div className="flex items-center gap-2 animate-pulse text-sm">
          <Sparkles className="w-4 h-4 text-blue-400" />
          <span>Loading LangGraph Lesson...</span>
        </div>
      </div>
    );
  }

  if (!lesson) {
    return (
      <div className="max-w-xl mx-auto py-16 text-center space-y-4">
        <h2 className="text-xl font-bold text-white">Lesson Not Found</h2>
        <p className="text-slate-400 text-xs">The requested lesson could not be loaded.</p>
        <Link to="/path" className="px-4 py-2 bg-blue-600 text-white text-xs rounded-lg inline-block">
          Return to Learning Path
        </Link>
      </div>
    );
  }

  const isCompleted = isLessonCompleted(lesson.id);
  const bookmarked = isBookmarked(lesson.id);

  return (
    <div className="flex w-full min-h-[calc(100vh-4rem)]">
      
      {/* Sidebar Navigation */}
      <div className="hidden lg:block">
        <Sidebar modules={curriculum?.modules || []} activeLessonId={lesson.id} />
      </div>

      {/* Main Lesson Content Area */}
      <div className="flex-1 max-w-5xl mx-auto px-4 sm:px-8 py-8 space-y-8 overflow-y-auto">
        
        {/* Lesson Breadcrumb & Title Bar */}
        <div className="space-y-3 border-b border-dark-800 pb-6">
          <div className="flex items-center justify-between text-xs text-slate-400">
            <div className="flex items-center gap-1.5">
              <Link to="/path" className="hover:text-blue-400">Curriculum</Link>
              <span>/</span>
              <span className="text-slate-200">{lesson.module_title || 'Module'}</span>
            </div>

            <div className="flex items-center gap-2">
              <button
                onClick={() => toggleBookmark(lesson.id)}
                className={`p-1.5 rounded-lg border text-xs flex items-center gap-1 transition-colors ${
                  bookmarked
                    ? 'bg-blue-500/20 text-blue-400 border-blue-500/40'
                    : 'bg-dark-800 text-slate-400 border-dark-700 hover:text-slate-200'
                }`}
                title="Bookmark this lesson"
              >
                <Bookmark className={`w-3.5 h-3.5 ${bookmarked ? 'fill-blue-400' : ''}`} />
                <span className="hidden sm:inline">{bookmarked ? 'Bookmarked' : 'Bookmark'}</span>
              </button>

              <button
                onClick={() => markLessonComplete(lesson.id, !isCompleted)}
                className={`px-3 py-1.5 rounded-lg text-xs font-semibold flex items-center gap-1.5 transition-all ${
                  isCompleted
                    ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/40'
                    : 'bg-blue-600 hover:bg-blue-500 text-white'
                }`}
              >
                <CheckCircle2 className="w-3.5 h-3.5" />
                <span>{isCompleted ? 'Completed ✓' : 'Mark as Complete'}</span>
              </button>
            </div>
          </div>

          <div className="flex flex-wrap items-center gap-2 pt-1">
            <Badge variant={lesson.difficulty}>{lesson.difficulty}</Badge>
            <span className="text-xs text-slate-400">•</span>
            <span className="text-xs text-slate-400">{lesson.estimated_minutes} min read</span>
          </div>

          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            {lesson.title}
          </h1>
        </div>

        {/* Section 1: Objectives & Prerequisites */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <Card className="space-y-2 border-blue-500/20 bg-blue-950/10">
            <div className="text-xs font-bold text-blue-300 uppercase tracking-wider flex items-center gap-1.5">
              <Sparkles className="w-3.5 h-3.5 text-blue-400" />
              <span>Learning Objectives</span>
            </div>
            <ul className="space-y-1 text-xs text-slate-300">
              {lesson.objectives?.map((obj, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-blue-400 font-bold">•</span>
                  <span>{obj}</span>
                </li>
              ))}
            </ul>
          </Card>

          <Card className="space-y-2 border-dark-700 bg-dark-850/60">
            <div className="text-xs font-bold text-slate-300 uppercase tracking-wider flex items-center gap-1.5">
              <BookOpen className="w-3.5 h-3.5 text-slate-400" />
              <span>Prerequisites</span>
            </div>
            <ul className="space-y-1 text-xs text-slate-400">
              {lesson.prerequisites?.map((prereq, i) => (
                <li key={i} className="flex items-start gap-2">
                  <span className="text-slate-500">•</span>
                  <span>{prereq}</span>
                </li>
              ))}
            </ul>
          </Card>
        </div>

        {/* Section 2: Simple English Explanation & Why It Matters */}
        <div className="space-y-4">
          <div className="space-y-2">
            <h2 className="text-lg font-bold text-white">Conceptual Overview</h2>
            <p className="text-sm text-slate-300 leading-relaxed">
              {lesson.simple_explanation}
            </p>
          </div>

          {lesson.why_it_matters && (
            <div className="p-4 rounded-xl border border-dark-700 bg-dark-850/80 space-y-1">
              <div className="text-xs font-bold text-emerald-400 uppercase tracking-wider flex items-center gap-1.5">
                <Lightbulb className="w-3.5 h-3.5" />
                <span>Why This Concept Matters in Production</span>
              </div>
              <p className="text-xs text-slate-300 leading-relaxed">
                {lesson.why_it_matters}
              </p>
            </div>
          )}

          {lesson.real_world_analogy && (
            <div className="p-4 rounded-xl border border-cyan-500/20 bg-cyan-950/15 space-y-1">
              <div className="text-xs font-bold text-cyan-400 uppercase tracking-wider flex items-center gap-1.5">
                <Sparkles className="w-3.5 h-3.5" />
                <span>Real-World Intuition Analogy</span>
              </div>
              <p className="text-xs text-cyan-200/90 leading-relaxed">
                {lesson.real_world_analogy}
              </p>
            </div>
          )}
        </div>

        {/* Section 3: Architecture Diagram (Mermaid Definition) */}
        {lesson.diagram_definition?.chart && (
          <div className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Code2 className="w-5 h-5 text-blue-400" />
              <span>Flow Architecture Diagram</span>
            </h2>
            <div className="p-4 rounded-xl border border-dark-700 bg-dark-950/80 font-mono text-xs text-cyan-300 overflow-x-auto">
              <div className="text-[11px] text-slate-500 uppercase tracking-wider mb-2 font-sans font-bold">
                Mermaid Topology Specification:
              </div>
              <pre className="text-slate-300">{lesson.diagram_definition.chart}</pre>
            </div>
          </div>
        )}

        {/* Section 4: Live Python Code Example with Editor & Terminal */}
        <div className="space-y-4">
          <div className="flex items-center justify-between">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <Terminal className="w-5 h-5 text-emerald-400" />
              <span>Complete Python Implementation</span>
            </h2>
            <Badge variant="real" size="xs">Deterministic & Runnable</Badge>
          </div>

          <div className="grid grid-cols-1 lg:grid-cols-2 gap-4 min-h-[380px]">
            <CodeEditor
              initialCode={lesson.code_example}
              onRun={handleRunCode}
              isRunning={isRunning}
              title={`${lesson.id}.py`}
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

        {/* Section 5: Line-by-Line Breakdown */}
        {lesson.line_by_line?.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-lg font-bold text-white">Line-by-Line Breakdown</h2>
            <div className="space-y-2">
              {lesson.line_by_line.map((item, i) => (
                <div key={i} className="p-3 rounded-lg border border-dark-800 bg-dark-850/60 space-y-1">
                  <div className="text-xs font-mono text-cyan-300 font-semibold bg-dark-900/80 px-2 py-1 rounded border border-dark-700/60 inline-block">
                    {item.line}
                  </div>
                  <div className="text-xs text-slate-300 font-sans mt-1">
                    {item.explanation}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 6: Common Pitfalls & Fixes */}
        {lesson.common_mistakes?.length > 0 && (
          <div className="space-y-3">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <AlertTriangle className="w-5 h-5 text-rose-400" />
              <span>Common Pitfalls & Fixes</span>
            </h2>
            <div className="space-y-2">
              {lesson.common_mistakes.map((pitfall, i) => (
                <div key={i} className="p-3 rounded-xl border border-rose-500/20 bg-rose-950/10 space-y-1.5">
                  <div className="text-xs font-bold text-rose-400">
                    ⚠️ Mistake: {pitfall.mistake}
                  </div>
                  <div className="text-xs text-emerald-400">
                    💡 Solution: {pitfall.fix}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Section 7: Hands-On Practice Task */}
        {lesson.hands_on_task?.instruction && (
          <div className="p-5 rounded-2xl border border-blue-500/30 bg-gradient-to-b from-blue-950/20 to-dark-850 space-y-3">
            <div className="flex items-center gap-2">
              <Code2 className="w-5 h-5 text-blue-400" />
              <h3 className="font-bold text-white text-base">
                Hands-On Task: {lesson.hands_on_task.title}
              </h3>
            </div>
            <p className="text-xs text-slate-300 leading-relaxed">
              {lesson.hands_on_task.instruction}
            </p>
            {lesson.hands_on_task.starter_code && (
              <pre className="p-3 rounded-lg bg-dark-950 border border-dark-750 text-xs font-mono text-cyan-300 overflow-x-auto">
                {lesson.hands_on_task.starter_code}
              </pre>
            )}
          </div>
        )}

        {/* Section 8: Knowledge Check Quiz */}
        {lesson.quick_quiz?.length > 0 && (
          <div className="space-y-4 pt-4 border-t border-dark-800">
            <h2 className="text-lg font-bold text-white flex items-center gap-2">
              <HelpCircle className="w-5 h-5 text-violet-400" />
              <span>Knowledge Check Quiz</span>
            </h2>

            <div className="space-y-4">
              {lesson.quick_quiz.map((q, qIdx) => {
                const selected = quizAnswers[qIdx];
                const feedback = quizFeedback[qIdx];

                return (
                  <Card key={qIdx} className="space-y-3">
                    <div className="text-xs font-bold text-slate-200">
                      Q{qIdx + 1}: {q.question}
                    </div>

                    <div className="space-y-2">
                      {q.options?.map((opt, optIdx) => {
                        const isThisSelected = selected === optIdx;
                        const isCorrectOption = optIdx === q.correct_index;

                        let optStyle = "bg-dark-800/80 hover:bg-dark-750 text-slate-300 border-dark-700";
                        if (selected !== undefined) {
                          if (isCorrectOption) {
                            optStyle = "bg-emerald-950/40 text-emerald-300 border-emerald-500/60";
                          } else if (isThisSelected && !feedback?.isCorrect) {
                            optStyle = "bg-rose-950/40 text-rose-300 border-rose-500/60";
                          }
                        }

                        return (
                          <button
                            key={optIdx}
                            onClick={() => handleQuizSelect(qIdx, optIdx, q.correct_index, q.explanation)}
                            className={`w-full text-left p-2.5 rounded-lg border text-xs transition-all flex items-center justify-between ${optStyle}`}
                          >
                            <span>{opt}</span>
                            {selected !== undefined && isCorrectOption && (
                              <Check className="w-4 h-4 text-emerald-400 flex-shrink-0" />
                            )}
                          </button>
                        );
                      })}
                    </div>

                    {feedback && (
                      <div className={`p-3 rounded-lg text-xs ${
                        feedback.isCorrect ? 'bg-emerald-950/40 text-emerald-300 border border-emerald-500/30' : 'bg-rose-950/40 text-rose-300 border border-rose-500/30'
                      }`}>
                        <div className="font-bold mb-1">
                          {feedback.isCorrect ? '✓ Correct!' : '✗ Not quite.'}
                        </div>
                        <div className="text-slate-300">{feedback.explanation}</div>
                      </div>
                    )}
                  </Card>
                );
              })}
            </div>
          </div>
        )}

        {/* Section 9: Personal Notes Editor */}
        <div className="space-y-3 pt-4 border-t border-dark-800">
          <div className="flex items-center justify-between">
            <h2 className="text-base font-bold text-white flex items-center gap-2">
              <FileText className="w-4 h-4 text-blue-400" />
              <span>Your Lesson Notes</span>
            </h2>
            <button
              onClick={() => saveNote(lesson.id, noteText)}
              className="px-3 py-1 rounded bg-dark-800 hover:bg-dark-700 text-slate-300 border border-dark-700 text-xs font-semibold transition-colors"
            >
              Save Notes
            </button>
          </div>
          <textarea
            value={noteText}
            onChange={(e) => setNoteText(e.target.value)}
            placeholder="Jot down personal insights, gotchas, or code snippets for this topic..."
            rows={3}
            className="w-full p-3 rounded-xl bg-dark-950 border border-dark-750 text-slate-200 text-xs focus:outline-none focus:ring-1 focus:ring-blue-500 resize-none font-sans"
          />
        </div>

        {/* Section 10: Official Docs & Navigation Footer */}
        <div className="pt-6 border-t border-dark-800 space-y-6">
          {lesson.docs_url && (
            <div className="flex items-center justify-between p-3 rounded-xl bg-dark-850/60 border border-dark-700 text-xs">
              <span className="text-slate-400">Official LangGraph Documentation Reference:</span>
              <a
                href={lesson.docs_url}
                target="_blank"
                rel="noreferrer"
                className="text-blue-400 hover:text-blue-300 font-semibold flex items-center gap-1"
              >
                <span>Read Official Docs</span>
                <ExternalLink className="w-3.5 h-3.5" />
              </a>
            </div>
          )}

          {/* Prev / Next Lesson Navigation */}
          <div className="flex items-center justify-between gap-4">
            {lesson.prev_lesson_id ? (
              <Link
                to={`/lessons/${lesson.prev_lesson_id}`}
                className="flex items-center gap-2 px-4 py-2.5 rounded-xl bg-dark-800 hover:bg-dark-750 text-slate-200 text-xs font-semibold border border-dark-700 transition-colors"
              >
                <ChevronLeft className="w-4 h-4" />
                <span>Previous Lesson</span>
              </Link>
            ) : <div />}

            {lesson.next_lesson_id ? (
              <Link
                to={`/lessons/${lesson.next_lesson_id}`}
                onClick={() => markLessonComplete(lesson.id, true)}
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-blue-600 hover:bg-blue-500 text-white text-xs font-bold shadow-lg shadow-blue-500/20 transition-all"
              >
                <span>Next Lesson</span>
                <ChevronRight className="w-4 h-4" />
              </Link>
            ) : (
              <Link
                to="/path"
                className="flex items-center gap-2 px-5 py-2.5 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-bold transition-all"
              >
                <span>Finish Module</span>
                <Check className="w-4 h-4" />
              </Link>
            )}
          </div>
        </div>
      </div>
    </div>
  );
};
