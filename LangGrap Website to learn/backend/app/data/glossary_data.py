# Glossary, Terminology & Framework Comparison Reference Data
from typing import List, Dict, Any

GLOSSARY_TERMS: List[Dict[str, Any]] = [
    {
        "term": "StateGraph",
        "category": "Core Concept",
        "definition": "The primary graph class in LangGraph that holds nodes and edges, parameterized by a state schema (TypedDict, Pydantic, or Dataclass).",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.graph import StateGraph\nbuilder = StateGraph(MyStateSchema)"
    },
    {
        "term": "Super-Step",
        "category": "Architecture & Pregel",
        "definition": "A discrete execution round in the Pregel computation model. In each super-step, active nodes read current state, execute concurrently, and emit channel writes. At the barrier, all updates merge atomically.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "code_snippet": "# Super-steps happen automatically during app.invoke() or app.stream()"
    },
    {
        "term": "Reducer",
        "category": "State Management",
        "definition": "A function that specifies how channel updates from nodes get merged with existing state (e.g. operator.add for appending to lists, or custom conflict-resolution functions).",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from typing import Annotated\nimport operator\nmessages: Annotated[list[str], operator.add]"
    },
    {
        "term": "MessagesState",
        "category": "State Management",
        "definition": "A prebuilt TypedDict schema provided by LangGraph containing a 'messages' list with the 'add_messages' reducer attached.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.graph import MessagesState\nbuilder = StateGraph(MessagesState)"
    },
    {
        "term": "add_messages",
        "category": "State Management",
        "definition": "A smart reducer function for message lists that appends new messages or updates existing messages in-place if their 'id' matches.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.graph.message import add_messages"
    },
    {
        "term": "START & END",
        "category": "Graph API",
        "definition": "Virtual node constants representing the graph entry point (START) and terminal exit point (END).",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.graph import START, END\nbuilder.add_edge(START, 'first_node')\nbuilder.add_edge('last_node', END)"
    },
    {
        "term": "add_conditional_edges",
        "category": "Routing",
        "definition": "Method to define dynamic branching based on the return value of a routing/decision function.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "builder.add_conditional_edges('source_node', router_fn, {'branch_a': 'node_a', 'branch_b': 'node_b'})"
    },
    {
        "term": "Command",
        "category": "Routing & Execution",
        "definition": "An object returned by a node that combines state updates (update={...}) and dynamic routing (goto=...) in a single return.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.types import Command\nreturn Command(update={'status': 'ok'}, goto='next_step')"
    },
    {
        "term": "Send",
        "category": "Concurrency & Map-Reduce",
        "definition": "A primitive used in conditional edges to dynamically fan-out and dispatch parallel node executions with custom payloads.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.types import Send\nreturn [Send('worker_node', {'item': x}) for x in items]"
    },
    {
        "term": "interrupt()",
        "category": "Human-in-the-Loop",
        "definition": "A function called inside a node that pauses execution, returns a query payload to the client, and saves state to the checkpointer until resumed.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/interrupts",
        "code_snippet": "from langgraph.types import interrupt\napproved = interrupt({'action': 'confirm_delete'})"
    },
    {
        "term": "Checkpointer (MemorySaver / SqliteSaver / PostgresSaver)",
        "category": "Persistence",
        "definition": "A persistence engine that saves state snapshots after every super-step, enabling session resumption by thread_id.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "code_snippet": "from langgraph.checkpoint.memory import MemorySaver\napp = builder.compile(checkpointer=MemorySaver())"
    },
    {
        "term": "thread_id",
        "category": "Persistence",
        "definition": "A unique identifier passed inside config={'configurable': {'thread_id': '...'}} that partitions checkpoint snapshots per user session.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "code_snippet": "config = {'configurable': {'thread_id': 'user_session_42'}}"
    },
    {
        "term": "BaseStore / InMemoryStore",
        "category": "Memory",
        "definition": "A cross-thread key-value storage engine with hierarchical namespaces for long-term user memories and facts across conversations.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "code_snippet": "from langgraph.store.memory import InMemoryStore\nstore = InMemoryStore()\nstore.put(('users', '123'), 'profile', {'name': 'Alice'})"
    },
    {
        "term": "ToolNode",
        "category": "Agents & Tools",
        "definition": "A prebuilt node that receives tool_calls from an AIMessage, invokes the corresponding Python tools, and returns ToolMessages with matching IDs.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.prebuilt import ToolNode\ntool_node = ToolNode(tools=[my_tool])"
    },
    {
        "term": "tools_condition",
        "category": "Agents & Tools",
        "definition": "A prebuilt routing function that checks if the latest message has tool_calls; routes to 'tools' if present, or END if finished.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.prebuilt import tools_condition\nbuilder.add_conditional_edges('agent', tools_condition)"
    },
    {
        "term": "stream_mode",
        "category": "Streaming",
        "definition": "Execution mode specifying what data to yield during app.stream() ('values', 'updates', 'messages', or 'custom').",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/streaming",
        "code_snippet": "for chunk in app.stream(input_data, stream_mode='updates'):\n    print(chunk)"
    },
    {
        "term": "Time Travel",
        "category": "Debugging & Replay",
        "definition": "The ability to inspect historical checkpoint snapshots with get_state_history(), fork past states, and replay from any historical super-step.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "code_snippet": "history = list(app.get_state_history(config))\napp.update_state(history[2].config, {'score': 90})"
    },
    {
        "term": "Functional API (@entrypoint & @task)",
        "category": "Functional API",
        "definition": "An alternative decorator-driven programming model for writing procedural workflows with automatic checkpointing and task caching.",
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "code_snippet": "from langgraph.func import entrypoint, task\n@task\ndef my_task(x): return x * 2\n@entrypoint()\ndef my_flow(x): return my_task(x).result()"
    }
]

FRAMEWORK_COMPARISON = [
    {
        "framework": "LangGraph",
        "paradigm": "Stateful Cyclical Graph & Pregel Engine",
        "best_for": "Complex agentic reasoning, tool loops, human approval gates, production persistence, time travel",
        "strengths": "Fine-grained control, robust persistence, streaming, subgraphs, active ecosystem, official LangChain integration",
        "weaknesses": "Higher initial learning curve than simple 1-file chains"
    },
    {
        "framework": "LangChain LCEL",
        "paradigm": "Linear Directed Acyclic Graphs (DAGs)",
        "best_for": "Simple 1-pass prompt -> model -> parser transformations, basic RAG lookups",
        "strengths": "Concise syntax for linear pipelines, lightweight",
        "weaknesses": "Does not support cycles, branching loops, or checkpoint persistence"
    },
    {
        "framework": "CrewAI",
        "paradigm": "Role-Playing Agent Crews",
        "best_for": "Collaborative research and multi-agent content generation crews",
        "strengths": "Fast high-level abstraction for persona-based collaboration",
        "weaknesses": "Less low-level execution control, harder to customize state persistence channels"
    },
    {
        "framework": "AutoGen (Microsoft)",
        "paradigm": "Conversational Multi-Agent Group Chat",
        "best_for": "Multi-agent debate, code execution in docker containers",
        "strengths": "Strong multi-party dialogue dynamics",
        "weaknesses": "Complex event model, heavier setup"
    }
]

def get_glossary() -> List[Dict[str, Any]]:
    return GLOSSARY_TERMS

def get_comparison() -> List[Dict[str, Any]]:
    return FRAMEWORK_COMPARISON
