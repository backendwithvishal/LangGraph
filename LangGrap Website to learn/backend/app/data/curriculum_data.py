# Comprehensive 14-Module Curriculum for GraphLab
# Based on current LangGraph 0.2+ documentation

CURRICULUM_MODULES = [
    {
        "id": "module-1",
        "title": "Module 1: Foundations & Architecture",
        "description": "Understand what LangGraph is, how it differs from LangChain chains, deterministic workflows vs agentic loops, and when to use graphs.",
        "difficulty": "Beginner",
        "order": 1,
        "icon": "Compass",
        "lessons": [
            {
                "id": "m1-l1",
                "module_id": "module-1",
                "title": "What is LangGraph & Why Does It Exist?",
                "difficulty": "Beginner",
                "estimated_minutes": 10,
                "summary": "Understand the limitations of linear LLM chains and why cyclical, stateful graph orchestration is necessary for robust agent systems.",
                "prerequisites": ["Python basics (functions, dicts, type hints)"],
                "topics": ["Agents vs Chains", "Cyclical graphs", "State machine concept", "Deterministic vs Autonomous"]
            },
            {
                "id": "m1-l2",
                "module_id": "module-1",
                "title": "LangGraph vs LangChain & Other Frameworks",
                "difficulty": "Beginner",
                "estimated_minutes": 12,
                "summary": "Compare LCEL, LangGraph, CrewAI, and AutoGen. Learn when a graph is ideal vs when simple Python code is enough.",
                "prerequisites": ["m1-l1"],
                "topics": ["LCEL vs Graphs", "Multi-Agent architectures", "When to use LangGraph", "Over-engineering warning"]
            },
            {
                "id": "m1-l3",
                "module_id": "module-1",
                "title": "Core Mental Model & Pregel Orchestration",
                "difficulty": "Beginner",
                "estimated_minutes": 15,
                "summary": "Learn the Pregel super-step paradigm: state channels, node executions, and atomic reducer merges.",
                "prerequisites": ["m1-l1"],
                "topics": ["Pregel concept", "Super-steps", "State channels", "Atomic updates"]
            }
        ]
    },
    {
        "id": "module-2",
        "title": "Module 2: Graph Fundamentals",
        "description": "Master StateGraph, START and END nodes, node functions, edge compilation, input/output schemas, and invocation modes.",
        "difficulty": "Beginner",
        "order": 2,
        "icon": "GitBranch",
        "lessons": [
            {
                "id": "m2-l1",
                "module_id": "module-2",
                "title": "StateGraph, TypedDict State & START/END",
                "difficulty": "Beginner",
                "estimated_minutes": 15,
                "summary": "Build your first StateGraph using TypedDict, adding nodes, and connecting START to END.",
                "prerequisites": ["m1-l1"],
                "topics": ["StateGraph", "TypedDict", "START", "END", "graph.compile()"]
            },
            {
                "id": "m2-l2",
                "module_id": "module-2",
                "title": "Node Functions & State Transitions",
                "difficulty": "Beginner",
                "estimated_minutes": 15,
                "summary": "How nodes receive state, process data, and return partial dictionary updates to mutate graph state.",
                "prerequisites": ["m2-l1"],
                "topics": ["Node signature", "Partial state returns", "Deterministic nodes", "Graph compilation"]
            },
            {
                "id": "m2-l3",
                "module_id": "module-2",
                "title": "Graph Invocations: invoke(), ainvoke() & stream()",
                "difficulty": "Beginner",
                "estimated_minutes": 18,
                "summary": "Executing compiled graphs synchronously, asynchronously, and streaming state snapshots.",
                "prerequisites": ["m2-l2"],
                "topics": ["invoke()", "ainvoke()", "stream()", "Event streams", "Async support"]
            }
        ]
    },
    {
        "id": "module-3",
        "title": "Module 3: State Management & Reducers",
        "description": "Deep dive into state schema types (TypedDict, Pydantic, Dataclasses), Annotated fields, reducer functions, and MessagesState.",
        "difficulty": "Intermediate",
        "order": 3,
        "icon": "Database",
        "lessons": [
            {
                "id": "m3-l1",
                "module_id": "module-3",
                "title": "Custom Reducers with Annotated[T, reducer]",
                "difficulty": "Intermediate",
                "estimated_minutes": 15,
                "summary": "Learn how values are updated: default overwrite vs list accumulation with operator.add and custom reducer logic.",
                "prerequisites": ["m2-l1"],
                "topics": ["Annotated", "operator.add", "Custom reducer functions", "State accumulation"]
            },
            {
                "id": "m3-l2",
                "module_id": "module-3",
                "title": "MessagesState & add_messages Reducer",
                "difficulty": "Intermediate",
                "estimated_minutes": 18,
                "summary": "Handling chat histories with MessagesState, ID-based message deduplication, and update-by-ID semantics.",
                "prerequisites": ["m3-l1"],
                "topics": ["MessagesState", "add_messages", "HumanMessage", "AIMessage", "Message IDs"]
            },
            {
                "id": "m3-l3",
                "module_id": "module-3",
                "title": "Separate Input, Internal, & Output State Schemas",
                "difficulty": "Intermediate",
                "estimated_minutes": 15,
                "summary": "Refining graph interfaces with custom input and output schemas while preserving rich internal state.",
                "prerequisites": ["m3-l1"],
                "topics": ["Input Schema", "Output Schema", "Internal State", "Information Hiding"]
            }
        ]
    },
    {
        "id": "module-4",
        "title": "Module 4: Routing, Branching & Loops",
        "description": "Implement conditional edges, dynamic routing functions, loops, recursion limits, fan-out/fan-in parallel nodes, and Command.",
        "difficulty": "Intermediate",
        "order": 4,
        "icon": "Shuffle",
        "lessons": [
            {
                "id": "m4-l1",
                "module_id": "module-4",
                "title": "Conditional Edges & Routing Functions",
                "difficulty": "Intermediate",
                "estimated_minutes": 16,
                "summary": "Dynamic branching using add_conditional_edges, path functions, and routing dictionaries.",
                "prerequisites": ["m2-l2"],
                "topics": ["add_conditional_edges", "Router functions", "Path mapping", "Fallback paths"]
            },
            {
                "id": "m4-l2",
                "module_id": "module-4",
                "title": "Cyclical Loops, Termination & Recursion Limits",
                "difficulty": "Intermediate",
                "estimated_minutes": 18,
                "summary": "Building iterative evaluation loops, preventing infinite cycles, and configuring recursion_limit.",
                "prerequisites": ["m4-l1"],
                "topics": ["Graph cycles", "Termination conditions", "recursion_limit", "RecursionError handling"]
            },
            {
                "id": "m4-l3",
                "module_id": "module-4",
                "title": "Parallel Execution, Fan-Out / Fan-In & Send API",
                "difficulty": "Intermediate",
                "estimated_minutes": 20,
                "summary": "Execute multiple nodes concurrently in the same super-step, and map-reduce dynamic workloads using Send.",
                "prerequisites": ["m4-l1", "m3-l1"],
                "topics": ["Parallel nodes", "Fan-out / Fan-in", "Send API", "Map-Reduce in graphs"]
            },
            {
                "id": "m4-l4",
                "module_id": "module-4",
                "title": "Command API: Combined State Updates & Routing",
                "difficulty": "Intermediate",
                "estimated_minutes": 15,
                "summary": "Use the modern Command(update=..., goto=...) to update state and determine navigation in a single return.",
                "prerequisites": ["m4-l1"],
                "topics": ["Command object", "Dynamic goto", "Inline state updates", "Multi-destination routing"]
            }
        ]
    },
    {
        "id": "module-5",
        "title": "Module 5: Models, Messages & Tool Calling",
        "description": "Connect chat models, bind tools with schemas, use ToolNode and tools_condition, handle tool validation errors and retries.",
        "difficulty": "Intermediate",
        "order": 5,
        "icon": "Wrench",
        "lessons": [
            {
                "id": "m5-l1",
                "module_id": "module-5",
                "title": "Tool Binding & ToolNode Integration",
                "difficulty": "Intermediate",
                "estimated_minutes": 18,
                "summary": "Define typed tools with @tool, bind them to LLMs, and execute them reliably with prebuilt ToolNode.",
                "prerequisites": ["m3-l2", "m4-l1"],
                "topics": ["@tool decorator", "llm.bind_tools()", "ToolNode", "ToolMessage", "tool_call_id"]
            },
            {
                "id": "m5-l2",
                "module_id": "module-5",
                "title": "Prebuilt tools_condition & ReAct Loop Flow",
                "difficulty": "Intermediate",
                "estimated_minutes": 15,
                "summary": "Automate tool routing with tools_condition and construct standard reasoning-action cycles.",
                "prerequisites": ["m5-l1"],
                "topics": ["tools_condition", "ReAct pattern", "tool_calls inspection", "End conditions"]
            },
            {
                "id": "m5-l3",
                "module_id": "module-5",
                "title": "Tool Error Handling & Fallbacks",
                "difficulty": "Intermediate",
                "estimated_minutes": 16,
                "summary": "Catch tool exceptions gracefully, feed error messages back to the model, and implement retry policies.",
                "prerequisites": ["m5-l1"],
                "topics": ["Tool exceptions", "Self-healing tools", "Fallback nodes", "Validation errors"]
            }
        ]
    },
    {
        "id": "module-6",
        "title": "Module 6: Building ReAct & Custom Agents",
        "description": "Construct ReAct agents from scratch with StateGraph, prebuilt create_react_agent, guardrails, and bounded execution.",
        "difficulty": "Intermediate",
        "order": 6,
        "icon": "Bot",
        "lessons": [
            {
                "id": "m6-l1",
                "module_id": "module-6",
                "title": "Building a ReAct Agent from Scratch with StateGraph",
                "difficulty": "Intermediate",
                "estimated_minutes": 22,
                "summary": "Full implementation of a ReAct agent: agent node -> conditional edge -> ToolNode -> agent node loop.",
                "prerequisites": ["m5-l2"],
                "topics": ["ReAct loop", "System prompts", "Tool invocation cycle", "Stop criteria"]
            },
            {
                "id": "m6-l2",
                "module_id": "module-6",
                "title": "Using prebuilt create_react_agent & Customizing Hooks",
                "difficulty": "Intermediate",
                "estimated_minutes": 15,
                "summary": "When and how to use langgraph.prebuilt.create_react_agent with prompt modifiers, state schemas, and checkpointers.",
                "prerequisites": ["m6-l1"],
                "topics": ["create_react_agent", "state_modifier", "Checkpointer integration", "Custom response formats"]
            },
            {
                "id": "m6-l3",
                "module_id": "module-6",
                "title": "Agent Guardrails, Safety & Bounded Execution",
                "difficulty": "Intermediate",
                "estimated_minutes": 18,
                "summary": "Implement deterministic safety filters, maximum loop bounds, tool allowlists, and output validators.",
                "prerequisites": ["m6-l1"],
                "topics": ["Input guardrails", "Output guardrails", "Execution limits", "Safety nodes"]
            }
        ]
    },
    {
        "id": "module-7",
        "title": "Module 7: Persistence, Checkpointing & Memory",
        "description": "Thread management, MemorySaver, SQLite/Postgres checkpointers, time travel, checkpoint replay, and cross-thread Long-Term Stores.",
        "difficulty": "Advanced",
        "order": 7,
        "icon": "HardDrive",
        "lessons": [
            {
                "id": "m7-l1",
                "module_id": "module-7",
                "title": "Checkpointers, Threads & State Snapshots",
                "difficulty": "Advanced",
                "estimated_minutes": 20,
                "summary": "How checkpointers persist super-step snapshots, thread_id configuration, and state recovery.",
                "prerequisites": ["m2-l2"],
                "topics": ["MemorySaver", "thread_id", "RunnableConfig", "get_state()", "StateSnapshot"]
            },
            {
                "id": "m7-l2",
                "module_id": "module-7",
                "title": "Time-Travel Debugging & History Replay",
                "difficulty": "Advanced",
                "estimated_minutes": 22,
                "summary": "Inspect historical checkpoints with get_state_history(), fork past states, and replay from any point in time.",
                "prerequisites": ["m7-l1"],
                "topics": ["get_state_history()", "checkpoint_id", "update_state()", "State forking", "Time-travel"]
            },
            {
                "id": "m7-l3",
                "module_id": "module-7",
                "title": "Long-Term Memory: Checkpointers vs BaseStore",
                "difficulty": "Advanced",
                "estimated_minutes": 20,
                "summary": "Understand the difference between thread-scoped short-term checkpoints and cross-thread long-term memory with BaseStore.",
                "prerequisites": ["m7-l1"],
                "topics": ["InMemoryStore", "BaseStore", "Namespaces", "Cross-thread memory", "User profiles"]
            }
        ]
    },
    {
        "id": "module-8",
        "title": "Module 8: Human-in-the-Loop & Dynamic Interrupts",
        "description": "Implement interrupt(), Command(resume=...), approval/rejection workflows, state editing before resumption, and review dashboards.",
        "difficulty": "Advanced",
        "order": 8,
        "icon": "UserCheck",
        "lessons": [
            {
                "id": "m8-l1",
                "module_id": "module-8",
                "title": "Dynamic Interrupts with interrupt() Function",
                "difficulty": "Advanced",
                "estimated_minutes": 20,
                "summary": "Pause execution inside any node with interrupt(query), prompt the user, and resume with Command(resume=value).",
                "prerequisites": ["m7-l1"],
                "topics": ["interrupt()", "Command(resume=...)", "Pending interruptions", "Safe suspension"]
            },
            {
                "id": "m8-l2",
                "module_id": "module-8",
                "title": "Human Approval & Rejection Workflows",
                "difficulty": "Advanced",
                "estimated_minutes": 18,
                "summary": "Build real-world approval gates for critical actions like payments, database mutations, or email sending.",
                "prerequisites": ["m8-l1"],
                "topics": ["Approval pattern", "Action confirmation", "Rejection routing", "Thread preservation"]
            },
            {
                "id": "m8-l3",
                "module_id": "module-8",
                "title": "State Editing & Manual Correction Before Resume",
                "difficulty": "Advanced",
                "estimated_minutes": 18,
                "summary": "Modify graph state directly using update_state(as_node=...) while interrupted, steering agent decisions.",
                "prerequisites": ["m8-l1", "m7-l2"],
                "topics": ["update_state()", "as_node parameter", "Steering agent execution", "Audit logging"]
            }
        ]
    },
    {
        "id": "module-9",
        "title": "Module 9: Streaming Architecture & SSE",
        "description": "Streaming modes (values, updates, messages, custom), async generators, FastAPI SSE streaming, and client disconnect handling.",
        "difficulty": "Advanced",
        "order": 9,
        "icon": "Radio",
        "lessons": [
            {
                "id": "m9-l1",
                "module_id": "module-9",
                "title": "LangGraph Streaming Modes (values vs updates vs messages)",
                "difficulty": "Advanced",
                "estimated_minutes": 18,
                "summary": "Deep dive into stream_mode='values', 'updates', 'messages', 'custom', and combined mode tuples.",
                "prerequisites": ["m2-l3"],
                "topics": ["stream_mode='values'", "stream_mode='updates'", "stream_mode='messages'", "LLM token chunks"]
            },
            {
                "id": "m9-l2",
                "module_id": "module-9",
                "title": "Production SSE Streaming with FastAPI",
                "difficulty": "Advanced",
                "estimated_minutes": 22,
                "summary": "Build a robust Server-Sent Events (SSE) FastAPI endpoint that streams graph updates and LLM tokens to the frontend.",
                "prerequisites": ["m9-l1"],
                "topics": ["FastAPI SSE", "EventSource", "Async generators", "Client disconnects", "JSON serialization"]
            }
        ]
    },
    {
        "id": "module-10",
        "title": "Module 10: Subgraphs & Multi-Agent Architecture",
        "description": "Compile hierarchical graphs, parent-child state transformations, supervisor routing, agent handoffs, and isolation.",
        "difficulty": "Advanced",
        "order": 10,
        "icon": "Layers",
        "lessons": [
            {
                "id": "m10-l1",
                "module_id": "module-10",
                "title": "Subgraphs as Nodes & State Isolation",
                "difficulty": "Advanced",
                "estimated_minutes": 20,
                "summary": "Embed compiled subgraphs as nodes inside parent graphs. Learn shared vs isolated state transformations.",
                "prerequisites": ["m4-l3"],
                "topics": ["Subgraph as node", "Parent vs Child state", "State mapping", "Encapsulation"]
            },
            {
                "id": "m10-l2",
                "module_id": "module-10",
                "title": "Supervisor & Multi-Agent Collaboration Patterns",
                "difficulty": "Advanced",
                "estimated_minutes": 24,
                "summary": "Build supervisor agents that delegate tasks to specialist subgraphs (researcher, coder, reviewer) with handoffs.",
                "prerequisites": ["m10-l1", "m6-l1"],
                "topics": ["Supervisor pattern", "Agent handoffs", "Structured worker schemas", "Aggregation"]
            }
        ]
    },
    {
        "id": "module-11",
        "title": "Module 11: Functional API (@entrypoint & @task)",
        "description": "Explore the Functional API alternative to StateGraph: @entrypoint, @task, persistence, interrupts, and when to choose each API.",
        "difficulty": "Advanced",
        "order": 11,
        "icon": "Code2",
        "lessons": [
            {
                "id": "m11-l1",
                "module_id": "module-11",
                "title": "The Functional API: @entrypoint & @task",
                "difficulty": "Advanced",
                "estimated_minutes": 18,
                "summary": "Write intuitive Pythonic workflows using decorators without declaring graph objects explicitly.",
                "prerequisites": ["m2-l1"],
                "topics": ["@entrypoint", "@task", "Task futures", "Functional vs Graph API comparison"]
            },
            {
                "id": "m11-l2",
                "module_id": "module-11",
                "title": "Checkpoints & Interrupts in Functional Workflows",
                "difficulty": "Advanced",
                "estimated_minutes": 18,
                "summary": "Enable durable persistence and human-in-the-loop interrupts within @entrypoint workflows.",
                "prerequisites": ["m11-l1", "m7-l1", "m8-l1"],
                "topics": ["Functional checkpointers", "interrupt in entrypoint", "Resume arguments", "Task caching"]
            }
        ]
    },
    {
        "id": "module-12",
        "title": "Module 12: RAG & Advanced Retrieval Patterns",
        "description": "Build Adaptive & Corrective RAG (CRAG) graphs with retrieval grading nodes, query rewrite loops, and hallucination checkers.",
        "difficulty": "Production",
        "order": 12,
        "icon": "Search",
        "lessons": [
            {
                "id": "m12-l1",
                "module_id": "module-12",
                "title": "Corrective RAG (CRAG) Architecture",
                "difficulty": "Production",
                "estimated_minutes": 22,
                "summary": "Construct a CRAG graph: Retrieve -> Grade documents -> Fallback to web search or query transform if irrelevant.",
                "prerequisites": ["m4-l2", "m5-l1"],
                "topics": ["CRAG", "Document grader", "Query rewrite", "Web fallback", "Hallucination check"]
            },
            {
                "id": "m12-l2",
                "module_id": "module-12",
                "title": "Self-RAG: Hallucination & Answer Quality Grading",
                "difficulty": "Production",
                "estimated_minutes": 22,
                "summary": "Implement self-reflection nodes that evaluate if the generated answer is grounded in retrieved context.",
                "prerequisites": ["m12-l1"],
                "topics": ["Self-RAG", "Groundedness check", "Answer relevance", "Loop termination"]
            }
        ]
    },
    {
        "id": "module-13",
        "title": "Module 13: Reliability, Testing & Production",
        "description": "Retry policies, timeouts, mock testing with pytest, LangSmith observability, auth, rate limiting, and durable deployment.",
        "difficulty": "Production",
        "order": 13,
        "icon": "ShieldCheck",
        "lessons": [
            {
                "id": "m13-l1",
                "module_id": "module-13",
                "title": "Retry Policies, Timeouts & Error Boundaries",
                "difficulty": "Production",
                "estimated_minutes": 18,
                "summary": "Configure RetryPolicy on nodes, set execution timeouts, and gracefully isolate external service failures.",
                "prerequisites": ["m2-l2"],
                "topics": ["RetryPolicy", "backoff_factor", "retry_on", "Node timeouts", "Graceful degradation"]
            },
            {
                "id": "m13-l2",
                "module_id": "module-13",
                "title": "Unit & Integration Testing of LangGraph Workflows",
                "difficulty": "Production",
                "estimated_minutes": 20,
                "summary": "Test graphs with deterministic mock models, test edge routing branches, and verify checkpoint persistence.",
                "prerequisites": ["m2-l3", "m7-l1"],
                "topics": ["pytest with LangGraph", "Mock models", "Snapshot assertions", "Testing interrupts"]
            },
            {
                "id": "m13-l3",
                "module_id": "module-13",
                "title": "LangSmith Tracing, Observability & Deployment",
                "difficulty": "Production",
                "estimated_minutes": 18,
                "summary": "Trace graph executions in LangSmith, capture run trees, monitor token usage, and deploy LangGraph API.",
                "prerequisites": ["m13-l1"],
                "topics": ["LangSmith setup", "Run trees", "Metadata tagging", "Cost monitoring", "Production checklist"]
            }
        ]
    },
    {
        "id": "module-14",
        "title": "Module 14: Advanced Internals & Reference",
        "description": "Pregel execution model, super-step sync barriers, channel buffers, immutable snapshots, and architectural glossary.",
        "difficulty": "Production",
        "order": 14,
        "icon": "Cpu",
        "lessons": [
            {
                "id": "m14-l1",
                "module_id": "module-14",
                "title": "Deep Dive: The Pregel Engine & Super-Steps",
                "difficulty": "Production",
                "estimated_minutes": 20,
                "summary": "Understand how LangGraph orchestrates concurrent nodes in discrete super-steps, barrier syncs, and state channels.",
                "prerequisites": ["m1-l3", "m4-l3"],
                "topics": ["Super-step lifecycle", "Channel mechanics", "Writer queues", "Determinism guarantees"]
            },
            {
                "id": "m14-l2",
                "module_id": "module-14",
                "title": "Mastering Time Travel & Forking Internals",
                "difficulty": "Production",
                "estimated_minutes": 20,
                "summary": "How checkpoint parent pointers and writes tables enable non-destructive branching and state forks.",
                "prerequisites": ["m7-l2", "m14-l1"],
                "topics": ["Parent checkpoint pointers", "Forking mechanics", "Immutable event sourcing", "State branching"]
            }
        ]
    }
]

# Fast-track 5-Day Intensive Bootcamp Lesson IDs
FAST_TRACK_LESSON_IDS = [
    "m1-l1", "m1-l3", "m2-l1", "m2-l2", "m2-l3",  # Day 1: Foundations & StateGraph
    "m3-l1", "m3-l2", "m4-l1", "m4-l2", "m5-l1", "m6-l1",  # Day 2: Reducers, Routing, Tools & Agents
    "m7-l1", "m7-l2", "m8-l1", "m8-l2", "m9-l1", "m9-l2",  # Day 3: Persistence, Interrupts & Streaming
    "m10-l1", "m10-l2", "m11-l1", "m11-l2",        # Day 4: Subgraphs, Supervisor & Functional API
    "m12-l1", "m13-l1", "m13-l2", "m14-l1"         # Day 5: RAG, Testing & Production Internals
]
