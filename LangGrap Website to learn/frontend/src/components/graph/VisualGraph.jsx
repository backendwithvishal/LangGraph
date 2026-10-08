import React, { useState, useEffect, useMemo, useCallback } from 'react';
import {
  ReactFlow,
  MiniMap,
  Controls,
  Background,
  useNodesState,
  useEdgesState,
  MarkerType
} from '@xyflow/react';
import '@xyflow/react/dist/style.css';
import { CustomNode } from './CustomNode';
import { Play, RotateCcw, FastForward, CheckCircle2, ShieldCheck, Sparkles, Terminal } from 'lucide-react';
import { Badge } from '../ui/Badge';

const nodeTypes = {
  custom: CustomNode,
  start: CustomNode,
  end: CustomNode,
  node: CustomNode,
  conditional: CustomNode,
  tools: CustomNode
};

export const VisualGraph = ({
  graphData = null,
  activeNodeId = null,
  completedNodeIds = [],
  onStepNext = null,
  onRunAll = null,
  onReset = null,
  isRunning = false,
  isCompleted = false,
  executionType = 'real_langgraph'
}) => {
  // Compute initial node layout
  const layoutNodes = useMemo(() => {
    if (!graphData?.nodes) return [];
    
    // Auto-layout vertically or in a structured grid
    const total = graphData.nodes.length;
    return graphData.nodes.map((n, i) => {
      let x = 250;
      let y = i * 140 + 40;

      // Position conditional branches side-by-side if multiple
      if (n.type === 'conditional' || n.type === 'tools') {
        x = 250 + (i % 2 === 0 ? 120 : -120);
      }

      return {
        id: n.id,
        type: 'custom',
        position: { x, y },
        data: {
          ...n,
          isExecuting: activeNodeId === n.id,
          isCompleted: completedNodeIds.includes(n.id),
          hasError: false
        }
      };
    });
  }, [graphData, activeNodeId, completedNodeIds]);

  // Compute edges
  const layoutEdges = useMemo(() => {
    if (!graphData?.edges) return [];
    return graphData.edges.map(e => ({
      id: e.id,
      source: e.source,
      target: e.target,
      label: e.label || '',
      animated: activeNodeId === e.source || activeNodeId === e.target,
      style: {
        stroke: activeNodeId === e.source ? '#3b82f6' : '#475569',
        strokeWidth: 2
      },
      markerEnd: {
        type: MarkerType.ArrowClosed,
        color: activeNodeId === e.source ? '#3b82f6' : '#64748b'
      }
    }));
  }, [graphData, activeNodeId]);

  const [nodes, setNodes, onNodesChange] = useNodesState(layoutNodes);
  const [edges, setEdges, onEdgesChange] = useEdgesState(layoutEdges);

  useEffect(() => {
    setNodes(layoutNodes);
  }, [layoutNodes, setNodes]);

  useEffect(() => {
    setEdges(layoutEdges);
  }, [layoutEdges, setEdges]);

  return (
    <div className="relative w-full h-full flex flex-col bg-dark-900 overflow-hidden">
      
      {/* Visual Graph Control Toolbar */}
      <div className="flex items-center justify-between p-3 border-b border-dark-800 bg-dark-850/90 backdrop-blur-md z-10">
        <div className="flex items-center gap-3">
          <button
            onClick={onRunAll}
            disabled={isRunning}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold text-xs transition-all shadow-md shadow-blue-500/20 disabled:opacity-50"
          >
            <Play className="w-3.5 h-3.5 fill-white" />
            <span>{isRunning ? 'Executing...' : 'Run Full Graph'}</span>
          </button>

          <button
            onClick={onStepNext}
            disabled={isRunning || isCompleted}
            className="flex items-center gap-1.5 px-3.5 py-1.5 rounded-lg bg-dark-750 hover:bg-dark-700 text-slate-200 font-semibold text-xs border border-dark-600 transition-all disabled:opacity-50"
          >
            <FastForward className="w-3.5 h-3.5 text-cyan-400" />
            <span>Step Forward</span>
          </button>

          <button
            onClick={onReset}
            disabled={isRunning}
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg bg-dark-800 hover:bg-dark-700 text-slate-400 hover:text-slate-200 text-xs border border-dark-700 transition-all"
          >
            <RotateCcw className="w-3.5 h-3.5" />
            <span>Reset</span>
          </button>
        </div>

        {/* Execution Guarantee Badge */}
        <div className="flex items-center gap-2">
          <Badge variant={executionType === 'real_langgraph' ? 'real' : 'default'} size="sm">
            <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-400" />
            {executionType === 'real_langgraph' ? 'Real LangGraph Backend Engine' : 'Client Simulation'}
          </Badge>
        </div>
      </div>

      {/* React Flow Canvas */}
      <div className="flex-1 w-full h-full min-h-[400px]">
        <ReactFlow
          nodes={nodes}
          edges={edges}
          onNodesChange={onNodesChange}
          onEdgesChange={onEdgesChange}
          nodeTypes={nodeTypes}
          fitView
          fitViewOptions={{ padding: 0.3 }}
          attributionPosition="bottom-right"
        >
          <Background color="#1e293b" gap={20} size={1.5} />
          <Controls className="!bg-dark-800 !border-dark-700 !text-slate-300" />
          <MiniMap
            className="!bg-dark-850 !border-dark-700 rounded-lg overflow-hidden"
            nodeColor={(n) => {
              if (n.data?.type === 'start') return '#10b981';
              if (n.data?.type === 'end') return '#f43f5e';
              return '#3b82f6';
            }}
          />
        </ReactFlow>
      </div>
    </div>
  );
};
