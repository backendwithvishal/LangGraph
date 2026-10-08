import React, { useState, useEffect } from 'react';
import { useSearchParams } from 'react-router-dom';
import {
  GitBranch,
  Play,
  RotateCcw,
  FastForward,
  Code2,
  Layers,
  Sparkles,
  ShieldCheck,
  ChevronDown
} from 'lucide-react';
import { api } from '../services/api';
import { VisualGraph } from '../components/graph/VisualGraph';
import { StateInspector } from '../components/graph/StateInspector';
import { CodeEditor } from '../components/editor/CodeEditor';
import { Badge } from '../components/ui/Badge';

export const GraphPlayground = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const [examples, setExamples] = useState([]);
  const [selectedExampleId, setSelectedExampleId] = useState(
    searchParams.get('example') || 'sequential-pipeline'
  );
  const [activeExample, setActiveExample] = useState(null);
  const [viewMode, setViewMode] = useState('graph'); // 'graph' | 'code'

  // Execution state
  const [isRunning, setIsRunning] = useState(false);
  const [isCompleted, setIsCompleted] = useState(false);
  const [activeNodeId, setActiveNodeId] = useState(null);
  const [completedNodeIds, setCompletedNodeIds] = useState([]);
  const [steps, setSteps] = useState([]);
  const [currentStepIndex, setCurrentStepIndex] = useState(-1);
  const [finalState, setFinalState] = useState(null);
  const [logs, setLogs] = useState([]);
  const [executionType, setExecutionType] = useState('real_langgraph');

  // Load playground examples
  useEffect(() => {
    api.getPlaygroundExamples()
      .then(data => {
        setExamples(data || []);
        const found = (data || []).find(e => e.id === selectedExampleId) || data?.[0];
        if (found) {
          setActiveExample(found);
          resetState(found);
        }
      })
      .catch(err => console.error('Failed to load examples:', err));
  }, []);

  useEffect(() => {
    if (selectedExampleId && examples.length > 0) {
      const found = examples.find(e => e.id === selectedExampleId);
      if (found) {
        setActiveExample(found);
        resetState(found);
      }
    }
  }, [selectedExampleId, examples]);

  const resetState = (exampleObj) => {
    setIsRunning(false);
    setIsCompleted(false);
    setActiveNodeId(null);
    setCompletedNodeIds([]);
    setSteps([]);
    setCurrentStepIndex(-1);
    setFinalState(exampleObj?.initial_state || {});
    setLogs([]);
  };

  const handleSelectExample = (id) => {
    setSelectedExampleId(id);
    setSearchParams({ example: id });
  };

  // Run all steps sequentially with live delays
  const handleRunAll = async () => {
    if (!activeExample) return;
    setIsRunning(true);
    setIsCompleted(false);
    setActiveNodeId(null);
    setCompletedNodeIds([]);
    setSteps([]);
    setCurrentStepIndex(-1);

    try {
      const result = await api.runPlaygroundExample(activeExample.id, activeExample.initial_state);
      setExecutionType(result.execution_type);
      setSteps(result.steps);
      setFinalState(result.final_state);
      setLogs(result.logs);

      // Play through steps with animated delays
      for (let i = 0; i < result.steps.length; i++) {
        const step = result.steps[i];
        setActiveNodeId(step.node_name);
        setCurrentStepIndex(i);
        await new Promise(r => setTimeout(r, 650));
        setCompletedNodeIds(prev => [...prev, step.node_name]);
      }

      setActiveNodeId(null);
      setIsCompleted(true);
    } catch (e) {
      console.error('Run failed:', e);
      setLogs(prev => [...prev, `Execution error: ${e.message}`]);
    } finally {
      setIsRunning(false);
    }
  };

  // Step forward one node at a time
  const handleStepNext = async () => {
    if (!activeExample) return;

    // If steps not yet fetched, fetch full trace first
    let currentSteps = steps;
    if (currentSteps.length === 0) {
      const result = await api.runPlaygroundExample(activeExample.id, activeExample.initial_state);
      currentSteps = result.steps;
      setSteps(currentSteps);
      setFinalState(result.final_state);
      setLogs(result.logs);
      setExecutionType(result.execution_type);
    }

    const nextIdx = currentStepIndex + 1;
    if (nextIdx < currentSteps.length) {
      const step = currentSteps[nextIdx];
      setActiveNodeId(step.node_name);
      setCompletedNodeIds(prev => Array.from(new Set([...prev, step.node_name])));
      setCurrentStepIndex(nextIdx);

      if (nextIdx === currentSteps.length - 1) {
        setIsCompleted(true);
      }
    }
  };

  return (
    <div className="flex flex-col h-[calc(100vh-4rem)] bg-dark-900 overflow-hidden">
      
      {/* Playground Header Bar */}
      <div className="flex flex-wrap items-center justify-between px-6 py-3 border-b border-dark-800 bg-dark-850 gap-4 select-none z-20">
        
        {/* Left: Example Selector */}
        <div className="flex items-center gap-3">
          <div className="flex items-center gap-2">
            <GitBranch className="w-5 h-5 text-blue-400" />
            <span className="font-bold text-slate-100 text-sm hidden sm:inline">
              Interactive Playground:
            </span>
          </div>

          <div className="relative">
            <select
              value={selectedExampleId}
              onChange={(e) => handleSelectExample(e.target.value)}
              className="bg-dark-900 border border-dark-700 text-slate-200 text-xs font-semibold rounded-lg px-3 py-1.5 pr-8 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer"
            >
              {examples.map(ex => (
                <option key={ex.id} value={ex.id}>
                  {ex.title} ({ex.difficulty})
                </option>
              ))}
            </select>
          </div>
        </div>

        {/* Center: Graph View vs Code View Switcher */}
        <div className="flex items-center bg-dark-900 p-1 rounded-lg border border-dark-700">
          <button
            onClick={() => setViewMode('graph')}
            className={`px-3 py-1 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              viewMode === 'graph'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <GitBranch className="w-3.5 h-3.5" />
            <span>Interactive Graph</span>
          </button>
          <button
            onClick={() => setViewMode('code')}
            className={`px-3 py-1 rounded-md text-xs font-semibold flex items-center gap-1.5 transition-colors ${
              viewMode === 'code'
                ? 'bg-blue-600 text-white shadow-sm'
                : 'text-slate-400 hover:text-slate-200'
            }`}
          >
            <Code2 className="w-3.5 h-3.5" />
            <span>Python Source</span>
          </button>
        </div>

        {/* Right: Badge */}
        <Badge variant="real" size="sm">
          <ShieldCheck className="w-3.5 h-3.5 mr-1 text-emerald-400" />
          Genuine LangGraph 0.2+ Engine
        </Badge>
      </div>

      {/* Main Split Layout: Left Graph / Code | Right State Inspector */}
      <div className="flex-1 grid grid-cols-1 lg:grid-cols-3 overflow-hidden">
        
        {/* Left 2 Columns: Visual Canvas or Code View */}
        <div className="lg:col-span-2 h-full flex flex-col border-r border-dark-800 relative">
          {viewMode === 'graph' ? (
            <VisualGraph
              graphData={activeExample?.graph}
              activeNodeId={activeNodeId}
              completedNodeIds={completedNodeIds}
              onRunAll={handleRunAll}
              onStepNext={handleStepNext}
              onReset={() => resetState(activeExample)}
              isRunning={isRunning}
              isCompleted={isCompleted}
              executionType={executionType}
            />
          ) : (
            <div className="p-4 h-full">
              <CodeEditor
                initialCode={activeExample?.python_code || ''}
                readOnly
                title={`${activeExample?.id}.py`}
              />
            </div>
          )}
        </div>

        {/* Right Column: State Inspector Panel */}
        <div className="lg:col-span-1 h-full overflow-hidden">
          <StateInspector
            steps={steps}
            currentStepIndex={currentStepIndex}
            finalState={finalState}
            logs={logs}
            executionType={executionType}
          />
        </div>
      </div>
    </div>
  );
};
