import React, { useState } from 'react';
import {
  Layers,
  Clock,
  ArrowRight,
  CheckCircle2,
  Terminal,
  ChevronRight,
  ChevronDown,
  Sparkles,
  Info
} from 'lucide-react';
import { Badge } from '../ui/Badge';

export const StateInspector = ({
  steps = [],
  currentStepIndex = -1,
  selectedNode = null,
  finalState = null,
  logs = [],
  executionType = 'real_langgraph'
}) => {
  const [activeTab, setActiveTab] = useState('state'); // 'state' | 'steps' | 'logs'
  const [expandedKeys, setExpandedKeys] = useState({ state: true, updates: true });

  const activeStep = steps[currentStepIndex] || steps[steps.length - 1] || null;

  const toggleKey = (k) => {
    setExpandedKeys(prev => ({ ...prev, [k]: !prev[k] }));
  };

  return (
    <div className="flex flex-col h-full bg-dark-900 border-l border-dark-700/80 text-xs select-none">
      
      {/* Header & Tabs */}
      <div className="flex items-center justify-between p-3 border-b border-dark-800 bg-dark-850">
        <div className="flex items-center gap-1.5 font-bold text-slate-200">
          <Layers className="w-4 h-4 text-blue-400" />
          <span>State Inspector</span>
        </div>

        {/* Execution Type Badge */}
        <Badge variant={executionType === 'real_langgraph' ? 'real' : 'default'} size="xs">
          {executionType === 'real_langgraph' ? '⚡ Genuine LangGraph' : 'Browser Simulation'}
        </Badge>
      </div>

      {/* Tab Selectors */}
      <div className="flex border-b border-dark-800 bg-dark-900/80 px-2 pt-1 gap-1">
        <button
          onClick={() => setActiveTab('state')}
          className={`px-3 py-1.5 font-semibold text-xs border-b-2 transition-colors ${
            activeTab === 'state'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-300'
          }`}
        >
          Active State Snapshot
        </button>
        <button
          onClick={() => setActiveTab('steps')}
          className={`px-3 py-1.5 font-semibold text-xs border-b-2 transition-colors ${
            activeTab === 'steps'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-300'
          }`}
        >
          Super-Steps ({steps.length})
        </button>
        <button
          onClick={() => setActiveTab('logs')}
          className={`px-3 py-1.5 font-semibold text-xs border-b-2 transition-colors ${
            activeTab === 'logs'
              ? 'border-blue-500 text-blue-400'
              : 'border-transparent text-slate-400 hover:text-slate-300'
          }`}
        >
          Execution Logs
        </button>
      </div>

      {/* Tab Content Body */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4 font-mono">
        
        {/* TAB 1: ACTIVE STATE */}
        {activeTab === 'state' && (
          <div className="space-y-4">
            
            {/* Active Step Indicator */}
            {activeStep ? (
              <div className="p-3 rounded-lg bg-dark-800/80 border border-dark-700">
                <div className="flex items-center justify-between text-slate-300 mb-1 font-sans">
                  <span className="font-bold">Step #{activeStep.step_number}: {activeStep.node_name}</span>
                  <span className="text-[10px] text-emerald-400 font-mono">Completed</span>
                </div>
                <div className="text-[11px] text-slate-400 font-sans">
                  {activeStep.log_message}
                </div>
              </div>
            ) : (
              <div className="p-4 rounded-lg bg-dark-800/40 border border-dark-800 text-center text-slate-400 font-sans">
                Click "Run Step-by-Step" or "Run Full Graph" to observe state transitions.
              </div>
            )}

            {/* State Updates (Diff) Section */}
            {activeStep?.updates && (
              <div className="rounded-lg border border-cyan-500/30 bg-cyan-950/20 overflow-hidden">
                <button
                  onClick={() => toggleKey('updates')}
                  className="w-full flex items-center justify-between p-2.5 bg-cyan-900/30 text-cyan-300 font-bold font-sans text-xs"
                >
                  <span className="flex items-center gap-1.5">
                    <Sparkles className="w-3.5 h-3.5" />
                    <span>Channel Updates Merged (Super-Step Delta)</span>
                  </span>
                  {expandedKeys.updates ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
                </button>
                {expandedKeys.updates && (
                  <pre className="p-3 text-[11px] text-cyan-200 overflow-x-auto">
                    {JSON.stringify(activeStep.updates, null, 2)}
                  </pre>
                )}
              </div>
            )}

            {/* Full Current State Snapshot */}
            <div className="rounded-lg border border-dark-700 bg-dark-800/80 overflow-hidden">
              <button
                onClick={() => toggleKey('state')}
                className="w-full flex items-center justify-between p-2.5 bg-dark-750 text-slate-200 font-bold font-sans text-xs"
              >
                <span className="flex items-center gap-1.5">
                  <Layers className="w-3.5 h-3.5 text-blue-400" />
                  <span>Full State Snapshot</span>
                </span>
                {expandedKeys.state ? <ChevronDown className="w-3 h-3" /> : <ChevronRight className="w-3 h-3" />}
              </button>
              {expandedKeys.state && (
                <pre className="p-3 text-[11px] text-slate-200 overflow-x-auto">
                  {JSON.stringify(activeStep ? activeStep.state_after : finalState || {}, null, 2)}
                </pre>
              )}
            </div>
          </div>
        )}

        {/* TAB 2: STEP HISTORY TIMELINE */}
        {activeTab === 'steps' && (
          <div className="space-y-2">
            {steps.map((step, idx) => (
              <div
                key={idx}
                className={`p-3 rounded-lg border transition-all ${
                  idx === currentStepIndex
                    ? 'border-blue-500 bg-blue-950/30 shadow-md shadow-blue-500/10'
                    : 'border-dark-700 bg-dark-800/60'
                }`}
              >
                <div className="flex items-center justify-between text-slate-200 font-sans mb-1">
                  <span className="font-bold">Step {step.step_number}: {step.node_name}</span>
                  <span className="text-[10px] text-slate-400 font-mono">{step.edge_taken}</span>
                </div>
                <div className="text-[11px] text-slate-400 font-sans mb-2">
                  {step.log_message}
                </div>
                <div className="text-[10px] bg-dark-900/80 p-2 rounded border border-dark-700/60 text-cyan-300">
                  <span className="text-slate-400 block mb-0.5">Node Return:</span>
                  {JSON.stringify(step.updates)}
                </div>
              </div>
            ))}
            {steps.length === 0 && (
              <div className="text-center py-8 text-slate-400 font-sans">
                No execution steps recorded yet.
              </div>
            )}
          </div>
        )}

        {/* TAB 3: EXECUTION LOGS */}
        {activeTab === 'logs' && (
          <div className="space-y-1.5 font-mono text-[11px]">
            {logs.map((log, idx) => (
              <div key={idx} className="p-1.5 rounded bg-dark-800/60 border border-dark-800 text-slate-300">
                <span className="text-slate-500 mr-2">[{idx + 1}]</span>
                <span>{log}</span>
              </div>
            ))}
            {logs.length === 0 && (
              <div className="text-center py-8 text-slate-400 font-sans">
                No logs recorded yet.
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
