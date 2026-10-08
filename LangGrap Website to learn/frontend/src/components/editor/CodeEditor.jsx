import React, { useState, useEffect } from 'react';
import Prism from 'prismjs';
import 'prismjs/components/prism-python';
import { Copy, Check, RotateCcw, Play, Terminal } from 'lucide-react';

export const CodeEditor = ({
  initialCode = '',
  onChange = null,
  onRun = null,
  isRunning = false,
  readOnly = false,
  title = "Python LangGraph Script"
}) => {
  const [code, setCode] = useState(initialCode);
  const [copied, setCopied] = useState(false);

  useEffect(() => {
    setCode(initialCode);
  }, [initialCode]);

  useEffect(() => {
    Prism.highlightAll();
  }, [code]);

  const handleCopy = () => {
    navigator.clipboard.writeText(code);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleReset = () => {
    setCode(initialCode);
    if (onChange) onChange(initialCode);
  };

  const handleChange = (e) => {
    const val = e.target.value;
    setCode(val);
    if (onChange) onChange(val);
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-dark-700 bg-dark-950 overflow-hidden shadow-2xl">
      
      {/* Editor Header */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-dark-900 border-b border-dark-800">
        <div className="flex items-center gap-2">
          <div className="flex gap-1.5">
            <div className="w-2.5 h-2.5 rounded-full bg-rose-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-amber-500/80" />
            <div className="w-2.5 h-2.5 rounded-full bg-emerald-500/80" />
          </div>
          <span className="text-xs font-mono text-slate-300 font-semibold ml-2">
            {title}
          </span>
        </div>

        <div className="flex items-center gap-2">
          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-2.5 py-1 rounded bg-dark-800 hover:bg-dark-750 text-slate-400 hover:text-slate-200 text-xs transition-colors border border-dark-700"
            title="Copy Python Code"
          >
            {copied ? <Check className="w-3.5 h-3.5 text-emerald-400" /> : <Copy className="w-3.5 h-3.5" />}
            <span>{copied ? 'Copied!' : 'Copy'}</span>
          </button>

          {!readOnly && (
            <button
              onClick={handleReset}
              className="flex items-center gap-1 px-2.5 py-1 rounded bg-dark-800 hover:bg-dark-750 text-slate-400 hover:text-slate-200 text-xs transition-colors border border-dark-700"
              title="Reset Code"
            >
              <RotateCcw className="w-3.5 h-3.5" />
              <span>Reset</span>
            </button>
          )}

          {onRun && (
            <button
              onClick={() => onRun(code)}
              disabled={isRunning}
              className="flex items-center gap-1 px-3 py-1 rounded-lg bg-emerald-600 hover:bg-emerald-500 text-white text-xs font-semibold shadow-md shadow-emerald-600/20 transition-all disabled:opacity-50"
            >
              <Play className="w-3.5 h-3.5 fill-white" />
              <span>{isRunning ? 'Running...' : 'Run Python'}</span>
            </button>
          )}
        </div>
      </div>

      {/* Code Area */}
      <div className="relative flex-1 min-h-[250px] overflow-auto bg-[#070b14]">
        {readOnly ? (
          <pre className="!m-0 !p-4 !bg-transparent text-xs font-mono leading-relaxed">
            <code className="language-python">{code}</code>
          </pre>
        ) : (
          <textarea
            value={code}
            onChange={handleChange}
            spellCheck={false}
            className="w-full h-full p-4 bg-transparent text-slate-100 font-mono text-xs leading-relaxed resize-none focus:outline-none focus:ring-1 focus:ring-blue-500/50"
            style={{ tabSize: 4 }}
          />
        )}
      </div>
    </div>
  );
};
