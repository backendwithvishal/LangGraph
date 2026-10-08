import React, { useState } from 'react';
import { Terminal, Play, RotateCcw, Copy, Check, Sparkles, BookOpen, Layers } from 'lucide-react';
import { CodeEditor } from '../components/editor/CodeEditor';
import { TerminalOutput } from '../components/editor/TerminalOutput';
import { api } from '../services/api';
import { Badge } from '../components/ui/Badge';

const CODE_PRESETS = [
  {
    id: "stategraph-basic",
    title: "1. StateGraph & TypedDict",
    category: "Foundations",
    code: `from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GreetingState(TypedDict):
    name: str
    greeting: str
    counter: int

def greet_node(state: GreetingState) -> dict:
    return {
        "greeting": f"Hello, {state['name']}! Welcome to GraphLab.",
        "counter": state.get("counter", 0) + 1
    }

builder = StateGraph(GreetingState)
builder.add_node("greeter", greet_node)
builder.add_edge(START, "greeter")
builder.add_edge("greeter", END)

app = builder.compile()
result = app.invoke({"name": "Vishal", "greeting": "", "counter": 0})
print("Result State:", result)
`
  },
  {
    id: "annotated-reducers",
    title: "2. Reducers & State Accumulation",
    category: "State Management",
    code: `from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class LogState(TypedDict):
    # Lists with operator.add append instead of overwriting
    logs: Annotated[list[str], operator.add]

def step_one(state: LogState) -> dict:
    return {"logs": ["Step 1: Security check completed"]}

def step_two(state: LogState) -> dict:
    return {"logs": ["Step 2: Database migration completed"]}

builder = StateGraph(LogState)
builder.add_node("s1", step_one)
builder.add_node("s2", step_two)
builder.add_edge(START, "s1")
builder.add_edge("s1", "s2")
builder.add_edge("s2", END)

app = builder.compile()
out = app.invoke({"logs": ["Initialization starting..."]})
print("Accumulated Logs:")
for log in out["logs"]:
    print(" -", log)
`
  },
  {
    id: "conditional-routing",
    title: "3. Conditional Routing & Dynamic goto",
    category: "Routing",
    code: `from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class TriageState(TypedDict):
    query: str
    route: str

def classifier_node(state: TriageState) -> dict:
    q = state["query"].lower()
    route = "billing" if "price" in q or "invoice" in q else "tech"
    return {"route": route}

def route_decision(state: TriageState) -> Literal["billing_node", "tech_node"]:
    return "billing_node" if state["route"] == "billing" else "tech_node"

def handle_billing(state: TriageState) -> dict:
    return {"route": "Handled by Billing Department"}

def handle_tech(state: TriageState) -> dict:
    return {"route": "Handled by Engineering Support"}

builder = StateGraph(TriageState)
builder.add_node("classify", classifier_node)
builder.add_node("billing_node", handle_billing)
builder.add_node("tech_node", handle_tech)

builder.add_edge(START, "classify")
builder.add_conditional_edges("classify", route_decision, {
    "billing_node": "billing_node",
    "tech_node": "tech_node"
})
builder.add_edge("billing_node", END)
builder.add_edge("tech_node", END)

app = builder.compile()
print("Test 1:", app.invoke({"query": "Need help with invoice #400", "route": ""}))
print("Test 2:", app.invoke({"query": "Server returned status 500", "route": ""}))
`
  },
  {
    id: "checkpointer-memory",
    title: "4. MemorySaver & Session Threads",
    category: "Persistence",
    code: `from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ChatState(TypedDict):
    history: Annotated[list[str], operator.add]

def bot_node(state: ChatState) -> dict:
    return {"history": [f"Turn {len(state['history'])} processed."]}

builder = StateGraph(ChatState)
builder.add_node("bot", bot_node)
builder.add_edge(START, "bot")
builder.add_edge("bot", END)

# Attach MemorySaver checkpointer
app = builder.compile(checkpointer=MemorySaver())

cfg = {"configurable": {"thread_id": "session-101"}}

print("Turn 1 Invocation:")
r1 = app.invoke({"history": ["User: Hello!"]}, config=cfg)
print("State:", r1)

print("\\nTurn 2 Invocation (State automatically loaded from checkpoint!):")
r2 = app.invoke({"history": ["User: What is LangGraph?"]}, config=cfg)
print("State:", r2)
`
  }
];

export const CodePlayground = () => {
  const [selectedPresetId, setSelectedPresetId] = useState(CODE_PRESETS[0].id);
  const [code, setCode] = useState(CODE_PRESETS[0].code);
  const [isRunning, setIsRunning] = useState(false);
  const [runnerOutput, setRunnerOutput] = useState({
    stdout: '',
    stderr: '',
    error: null,
    executionTimeMs: null
  });

  const handleSelectPreset = (id) => {
    const preset = CODE_PRESETS.find(p => p.id === id);
    if (preset) {
      setSelectedPresetId(id);
      setCode(preset.code);
      setRunnerOutput({ stdout: '', stderr: '', error: null, executionTimeMs: null });
    }
  };

  const handleRun = async (codeToRun) => {
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

  return (
    <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6 animate-in fade-in duration-200">
      
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 border-b border-dark-800 pb-6">
        <div>
          <div className="flex items-center gap-2 mb-1">
            <Terminal className="w-5 h-5 text-emerald-400" />
            <h1 className="text-2xl font-extrabold text-white tracking-tight">
              Python LangGraph Code Lab
            </h1>
          </div>
          <p className="text-xs text-slate-400">
            Write, modify, and execute genuine LangGraph Python code in a safe execution environment.
          </p>
        </div>

        {/* Preset Selector */}
        <div className="flex items-center gap-2">
          <span className="text-xs text-slate-400 font-semibold hidden sm:inline">Topic Preset:</span>
          <select
            value={selectedPresetId}
            onChange={(e) => handleSelectPreset(e.target.value)}
            className="bg-dark-800 border border-dark-700 text-slate-200 text-xs font-semibold rounded-lg px-3 py-1.5 focus:outline-none focus:ring-1 focus:ring-blue-500 cursor-pointer"
          >
            {CODE_PRESETS.map(p => (
              <option key={p.id} value={p.id}>
                {p.title}
              </option>
            ))}
          </select>
        </div>
      </div>

      {/* Code Editor & Output Console Grid */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 min-h-[520px]">
        <div className="h-full">
          <CodeEditor
            initialCode={code}
            onChange={setCode}
            onRun={handleRun}
            isRunning={isRunning}
            title="main.py"
          />
        </div>

        <div className="h-full">
          <TerminalOutput
            stdout={runnerOutput.stdout}
            stderr={runnerOutput.stderr}
            error={runnerOutput.error}
            executionTimeMs={runnerOutput.executionTimeMs}
            isLoading={isRunning}
          />
        </div>
      </div>
    </div>
  );
};
