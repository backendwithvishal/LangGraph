import React from 'react';
import { Terminal, CheckCircle2, AlertCircle, Clock, Copy, Check } from 'lucide-react';

export const TerminalOutput = ({
  stdout = '',
  stderr = '',
  error = null,
  executionTimeMs = null,
  isLoading = false
}) => {
  const [copied, setCopied] = React.useState(false);

  const handleCopy = () => {
    const text = stdout || error || stderr || '';
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  return (
    <div className="flex flex-col h-full rounded-xl border border-dark-700 bg-dark-950 overflow-hidden shadow-2xl font-mono text-xs select-text">
      
      {/* Terminal Title Bar */}
      <div className="flex items-center justify-between px-4 py-2.5 bg-dark-900 border-b border-dark-800 select-none">
        <div className="flex items-center gap-2 text-slate-300 font-semibold">
          <Terminal className="w-4 h-4 text-emerald-400" />
          <span>Execution Output Console</span>
        </div>

        <div className="flex items-center gap-3">
          {executionTimeMs !== null && (
            <div className="flex items-center gap-1 text-[11px] text-slate-400">
              <Clock className="w-3 h-3 text-cyan-400" />
              <span>{executionTimeMs} ms</span>
            </div>
          )}

          <button
            onClick={handleCopy}
            className="flex items-center gap-1 px-2 py-0.5 rounded bg-dark-800 hover:bg-dark-750 text-slate-400 hover:text-slate-200 text-[11px] transition-colors border border-dark-700"
          >
            {copied ? <Check className="w-3 h-3 text-emerald-400" /> : <Copy className="w-3 h-3" />}
            <span>{copied ? 'Copied' : 'Copy'}</span>
          </button>
        </div>
      </div>

      {/* Terminal Content Stream */}
      <div className="flex-1 p-4 overflow-auto bg-[#070b14] space-y-2 leading-relaxed">
        {isLoading && (
          <div className="flex items-center gap-2 text-blue-400 animate-pulse">
            <span className="w-2 h-2 rounded-full bg-blue-400 animate-ping" />
            <span>Executing graph workflow in Python environment...</span>
          </div>
        )}

        {stdout && (
          <div className="text-emerald-300 whitespace-pre-wrap">
            {stdout}
          </div>
        )}

        {stderr && (
          <div className="text-amber-300/90 whitespace-pre-wrap">
            <span className="text-amber-500 font-bold block mb-1">[STDERR WARNINGS]</span>
            {stderr}
          </div>
        )}

        {error && (
          <div className="p-3 rounded-lg bg-rose-950/40 border border-rose-500/40 text-rose-300 whitespace-pre-wrap flex items-start gap-2">
            <AlertCircle className="w-4 h-4 text-rose-400 flex-shrink-0 mt-0.5" />
            <div>
              <div className="font-bold mb-1">Execution Error</div>
              <div>{error}</div>
            </div>
          </div>
        )}

        {!isLoading && !stdout && !stderr && !error && (
          <div className="text-slate-500 select-none italic">
            $ Ready. Press "Run Python" to execute LangGraph code.
          </div>
        )}
      </div>
    </div>
  );
};
