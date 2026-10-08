import React, { memo } from 'react';
import { Handle, Position } from '@xyflow/react';
import {
  Play,
  Square,
  Shuffle,
  Wrench,
  UserCheck,
  Cpu,
  Layers,
  CheckCircle2,
  AlertCircle
} from 'lucide-react';

const nodeIcons = {
  start: Play,
  end: Square,
  node: Cpu,
  conditional: Shuffle,
  tools: Wrench,
  human: UserCheck,
  subgraph: Layers
};

export const CustomNode = memo(({ data, selected }) => {
  const nodeType = data.type || 'node';
  const Icon = nodeIcons[nodeType] || Cpu;
  const isExecuting = data.isExecuting;
  const isCompleted = data.isCompleted;
  const hasError = data.hasError;

  const nodeColorSchemes = {
    start: 'border-emerald-500/50 bg-emerald-950/40 text-emerald-300',
    end: 'border-rose-500/50 bg-rose-950/40 text-rose-300',
    node: 'border-blue-500/40 bg-dark-800/90 text-slate-100',
    conditional: 'border-amber-500/50 bg-amber-950/40 text-amber-300',
    tools: 'border-cyan-500/50 bg-cyan-950/40 text-cyan-300',
    human: 'border-violet-500/50 bg-violet-950/40 text-violet-300',
    subgraph: 'border-indigo-500/50 bg-indigo-950/40 text-indigo-300'
  };

  const currentTheme = nodeColorSchemes[nodeType] || nodeColorSchemes.node;

  return (
    <div
      className={`min-w-[180px] max-w-[240px] rounded-xl border-2 p-3 shadow-xl backdrop-blur-md transition-all duration-300 ${currentTheme} ${
        isExecuting ? 'node-running-glow scale-105 border-emerald-400' : ''
      } ${selected ? 'ring-2 ring-blue-400 ring-offset-2 ring-offset-dark-900' : ''}`}
    >
      {/* Target connection point */}
      {nodeType !== 'start' && (
        <Handle
          type="target"
          position={Position.Top}
          className="!w-3 !h-3 !bg-blue-500 !border-2 !border-dark-900 rounded-full"
        />
      )}

      {/* Node Header */}
      <div className="flex items-center justify-between gap-2 mb-1.5">
        <div className="flex items-center gap-1.5">
          <div className="p-1 rounded bg-dark-900/60">
            <Icon className="w-3.5 h-3.5" />
          </div>
          <span className="text-[10px] font-bold uppercase tracking-wider opacity-80 font-mono">
            {nodeType}
          </span>
        </div>

        {/* Execution status indicators */}
        <div>
          {isExecuting && (
            <span className="flex h-2 w-2 relative">
              <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-emerald-400 opacity-75"></span>
              <span className="relative inline-flex rounded-full h-2 w-2 bg-emerald-500"></span>
            </span>
          )}
          {isCompleted && !isExecuting && (
            <CheckCircle2 className="w-3.5 h-3.5 text-emerald-400" />
          )}
          {hasError && (
            <AlertCircle className="w-3.5 h-3.5 text-rose-400" />
          )}
        </div>
      </div>

      {/* Node Label */}
      <div className="text-xs font-bold text-slate-100 truncate mb-1">
        {data.label || 'Node'}
      </div>

      {/* Node Description */}
      {data.description && (
        <div className="text-[11px] text-slate-400 line-clamp-2 leading-relaxed">
          {data.description}
        </div>
      )}

      {/* Source connection point */}
      {nodeType !== 'end' && (
        <Handle
          type="source"
          position={Position.Bottom}
          className="!w-3 !h-3 !bg-cyan-500 !border-2 !border-dark-900 rounded-full"
        />
      )}
    </div>
  );
});
