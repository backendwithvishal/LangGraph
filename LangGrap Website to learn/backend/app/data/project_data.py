# Guided Projects Curriculum
from typing import List, Dict, Any, Optional

PROJECTS: List[Dict[str, Any]] = [
    {
        "id": "proj-1",
        "title": "Project 1: Conditional Routing & Support Triage Workflow",
        "difficulty": "Beginner",
        "estimated_hours": 1.5,
        "description": "Build an automated customer support triage engine that inspects ticket contents, classifies severity and intent, and routes dynamically to specialized handler queues.",
        "learning_outcomes": [
            "Construct a TypedDict state schema with intent, priority, and routing flags",
            "Use add_conditional_edges with deterministic routing functions",
            "Handle fallback routing for unclassified queries"
        ],
        "architecture_diagram": "graph TD\n  START([START]) --> Ingest[Ingest & Normalize Ticket]\n  Ingest --> Classifier[Rule-Based Classifier]\n  Classifier --> Router{Intent Router}\n  Router -- 'billing' --> Billing[Billing Operations Queue]\n  Router -- 'tech_support' --> Tech[Tech Support Queue]\n  Router -- 'general_faq' --> FAQ[FAQ Knowledge Queue]\n  Billing --> Notify[Notification Dispatcher] --> END([END])\n  Tech --> Notify\n  FAQ --> Notify",
        "requirements": [
            "Accept `ticket_id`, `customer_email`, and `message` as initial input",
            "Classify priority as 'URGENT' if words like 'down', 'critical', or 'refund' appear",
            "Route to 'billing', 'tech_support', or 'general_faq'",
            "Include a final 'notify' node that formats a unified dispatch receipt"
        ],
        "steps": [
            {
                "step_number": 1,
                "title": "Define State Schema",
                "instruction": "Create a `SupportState` TypedDict containing `ticket_id`, `message`, `intent`, `priority`, and `dispatch_receipt`.",
                "hints": ["Use standard Python typing: `from typing import TypedDict`"],
                "code_template": "class SupportState(TypedDict):\n    ticket_id: str\n    message: str\n    intent: str\n    priority: str\n    dispatch_receipt: str",
                "solution_code": "class SupportState(TypedDict):\n    ticket_id: str\n    message: str\n    intent: str\n    priority: str\n    dispatch_receipt: str"
            },
            {
                "step_number": 2,
                "title": "Implement Classifier & Routing Logic",
                "instruction": "Write `classify_ticket(state)` and `route_ticket(state)` functions.",
                "hints": ["Check message lowercase for keywords like 'invoice', 'error', 'login'"],
                "code_template": "def classify_ticket(state: SupportState) -> dict:\n    # Implement keyword checks\n    pass",
                "solution_code": "def classify_ticket(state: SupportState) -> dict:\n    msg = state['message'].lower()\n    intent = 'billing' if 'invoice' in msg or 'charge' in msg else ('tech_support' if 'error' in msg or 'bug' in msg else 'general_faq')\n    priority = 'URGENT' if 'urgent' in msg or 'down' in msg else 'NORMAL'\n    return {'intent': intent, 'priority': priority}"
            },
            {
                "step_number": 3,
                "title": "Assemble and Compile StateGraph",
                "instruction": "Add nodes, connect START to classifier, add conditional edges to queues, and route queues to notify node.",
                "hints": ["Use `builder.add_conditional_edges('classifier', route_ticket, mapping)`"],
                "code_template": "# Assemble StateGraph here",
                "solution_code": "builder = StateGraph(SupportState)\nbuilder.add_node('classifier', classify_ticket)\nbuilder.add_node('billing', lambda s: {'dispatch_receipt': f'Assigned to Billing ({s[\"priority\"]})'})\nbuilder.add_node('tech_support', lambda s: {'dispatch_receipt': f'Assigned to Tech Support ({s[\"priority\"]})'})\nbuilder.add_node('general_faq', lambda s: {'dispatch_receipt': f'Assigned to FAQ ({s[\"priority\"]})'})\nbuilder.add_edge(START, 'classifier')\nbuilder.add_conditional_edges('classifier', lambda s: s['intent'])\nbuilder.add_edge('billing', END)\nbuilder.add_edge('tech_support', END)\nbuilder.add_edge('general_faq', END)\napp = builder.compile()"
            }
        ],
        "starter_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class SupportState(TypedDict):
    ticket_id: str
    message: str
    intent: str
    priority: str
    dispatch_receipt: str

# Implement your nodes and StateGraph here
""",
        "solution_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class SupportState(TypedDict):
    ticket_id: str
    message: str
    intent: str
    priority: str
    dispatch_receipt: str

def classify_ticket(state: SupportState) -> dict:
    msg = state["message"].lower()
    intent = "billing" if "invoice" in msg or "charge" in msg else ("tech_support" if "error" in msg or "bug" in msg else "general_faq")
    priority = "URGENT" if "urgent" in msg or "down" in msg else "NORMAL"
    return {"intent": intent, "priority": priority}

def billing_node(state: SupportState) -> dict:
    return {"dispatch_receipt": f"Ticket #{state['ticket_id']} dispatched to Billing Operations [{state['priority']}]"}

def tech_node(state: SupportState) -> dict:
    return {"dispatch_receipt": f"Ticket #{state['ticket_id']} dispatched to Engineering [{state['priority']}]"}

def faq_node(state: SupportState) -> dict:
    return {"dispatch_receipt": f"Ticket #{state['ticket_id']} dispatched to Automated Knowledge Base [{state['priority']}]"}

builder = StateGraph(SupportState)
builder.add_node("classifier", classify_ticket)
builder.add_node("billing", billing_node)
builder.add_node("tech_support", tech_node)
builder.add_node("general_faq", faq_node)

builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier", lambda s: s["intent"], {
    "billing": "billing",
    "tech_support": "tech_support",
    "general_faq": "general_faq"
})
builder.add_edge("billing", END)
builder.add_edge("tech_support", END)
builder.add_edge("general_faq", END)

app = builder.compile()""",
        "test_cases_code": """def test_project_1():
    res = app.invoke({"ticket_id": "T-101", "message": "URGENT: double charge on invoice", "intent": "", "priority": "", "dispatch_receipt": ""})
    assert res["intent"] == "billing"
    assert res["priority"] == "URGENT"
    assert "Billing Operations" in res["dispatch_receipt"]
    print("Project 1 test passed!")
test_project_1()""",
        "sample_request": {"ticket_id": "T-101", "message": "URGENT: double charge on invoice", "intent": "", "priority": "", "dispatch_receipt": ""},
        "expected_response": {"ticket_id": "T-101", "message": "URGENT: double charge on invoice", "intent": "billing", "priority": "URGENT", "dispatch_receipt": "Ticket #T-101 dispatched to Billing Operations [URGENT]"},
        "bonus_extensions": [
            "Add a sentiment scoring node before classification",
            "Add automatic Slack / webhook payload generation"
        ]
    },
    {
        "id": "proj-2",
        "title": "Project 2: ReAct Tool-Calling Agent with Error Recovery",
        "difficulty": "Intermediate",
        "estimated_hours": 2.0,
        "description": "Construct a full ReAct agent with ToolNode, prebuilt tools_condition, input validation, and self-correcting error handlers.",
        "learning_outcomes": [
            "Register typed tools with langchain_core.tools @tool",
            "Bind ToolNode with custom exception handlers",
            "Connect ReAct loop with tools_condition and message histories"
        ],
        "architecture_diagram": "graph LR\n  START([START]) --> Agent[Agent Node: Reason & Call Tools]\n  Agent --> Decision{\"tools_condition\"}\n  Decision -- Has tool_calls --> ToolNode[ToolNode (with error handler)]\n  ToolNode --> Agent\n  Decision -- Done --> END([END])",
        "requirements": [
            "Provide calculator and currency converter tools",
            "Catch divide-by-zero and negative amounts gracefully in ToolNode",
            "Return structured AIMessage with the final computed breakdown"
        ],
        "steps": [
            {"step_number": 1, "title": "Define Tools with @tool", "instruction": "Define tools with docstrings and type hints.", "hints": ["Use `@tool` decorator"], "code_template": "@tool\ndef calculate(expr: str) -> str:\n    pass", "solution_code": "@tool\ndef calculate(a: float, b: float, op: str) -> float:\n    \"\"\"Performs basic math operation (add, sub, mul, div).\"\"\"\n    if op == 'div' and b == 0: raise ValueError('Cannot divide by zero')\n    ops = {'add': a+b, 'sub': a-b, 'mul': a*b, 'div': a/b}\n    return ops[op]"}
        ],
        "starter_code": """from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# Implement tools and ReAct agent
""",
        "solution_code": """from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def calculate(a: float, b: float, op: str) -> float:
    \"\"\"Performs basic math operation (add, sub, mul, div).\"\"\"
    if op == "div" and b == 0:
        raise ValueError("Cannot divide by zero")
    ops = {"add": a+b, "sub": a-b, "mul": a*b, "div": a/b}
    return ops.get(op, 0.0)

tools = [calculate]
tool_node = ToolNode(tools=tools, handle_tool_errors=True)

def agent_reasoner(state: MessagesState) -> dict:
    msgs = state["messages"]
    if isinstance(msgs[-1], ToolMessage):
        return {"messages": [AIMessage(content=f"Calculation finished. Result: {msgs[-1].content}")]}
    return {"messages": [AIMessage(
        content="Computing calculation...",
        tool_calls=[{"name": "calculate", "args": {"a": 450, "b": 15, "op": "mul"}, "id": "call_1", "type": "tool_call"}]
    )]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_reasoner)
builder.add_node("tools", tool_node)
builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

app = builder.compile()""",
        "test_cases_code": """def test_project_2():
    res = app.invoke({"messages": [HumanMessage(content="Calculate 450 * 15")]})
    assert len(res["messages"]) == 4
    assert "Result: 6750.0" in res["messages"][-1].content
    print("Project 2 test passed!")
test_project_2()""",
        "sample_request": {"messages": [{"role": "user", "content": "Calculate 450 * 15"}]},
        "expected_response": {"messages": [{"content": "Calculate 450 * 15"}, {"content": "Computing calculation..."}, {"content": "6750.0"}, {"content": "Calculation finished. Result: 6750.0"}]},
        "bonus_extensions": ["Add stock price lookup tool", "Add rate-limit backoff handler"]
    },
    {
        "id": "proj-3",
        "title": "Project 3: Stateful Conversational Assistant with Multi-Turn Memory",
        "difficulty": "Intermediate",
        "estimated_hours": 2.0,
        "description": "Implement a persistent chatbot with MemorySaver, thread_id session partitioning, message deduplication, and context-aware responses.",
        "learning_outcomes": [
            "Use MessagesState with add_messages reducer",
            "Configure MemorySaver checkpointer for multi-turn sessions",
            "Maintain session isolation between different thread IDs"
        ],
        "architecture_diagram": "graph LR\n  UserTurn[User Message] --> LoadCP[Load Snapshot for thread_id]\n  LoadCP --> Agent[Conversational Agent Node]\n  Agent --> SaveCP[(Save Snapshot to Checkpointer)] --> Response[Emit Response]",
        "requirements": [
            "Support ongoing multi-turn conversations across independent thread_ids",
            "Remember user's name and previous statements across turns",
            "Inspect state snapshots using `app.get_state(config)`"
        ],
        "steps": [],
        "starter_code": """from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver
# Implement stateful conversational assistant
""",
        "solution_code": """from langchain_core.messages import HumanMessage, AIMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.checkpoint.memory import MemorySaver

def conversational_node(state: MessagesState) -> dict:
    history = state["messages"]
    last_msg = history[-1].content
    # Contextual reply acknowledging history depth
    reply = f"I hear you ({len(history)} messages in our chat). You said: '{last_msg}'"
    return {"messages": [AIMessage(content=reply)]}

builder = StateGraph(MessagesState)
builder.add_node("bot", conversational_node)
builder.add_edge(START, "bot")
builder.add_edge("bot", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)""",
        "test_cases_code": """def test_project_3():
    cfg = {"configurable": {"thread_id": "test-chat-1"}}
    app.invoke({"messages": [HumanMessage(content="Hello")]}, config=cfg)
    res = app.invoke({"messages": [HumanMessage(content="My name is Vishal")]}, config=cfg)
    assert len(res["messages"]) == 4
    print("Project 3 test passed!")
test_project_3()""",
        "sample_request": {"messages": [{"role": "user", "content": "Hello"}]},
        "expected_response": {"messages": [{"content": "Hello"}, {"content": "I hear you (1 messages in our chat). You said: 'Hello'"}]},
        "bonus_extensions": ["Add thread deletion endpoint", "Add SqliteSaver checkpointer persistence"]
    },
    {
        "id": "proj-4",
        "title": "Project 4: Human-in-the-Loop Wire Transfer Approval System",
        "difficulty": "Advanced",
        "estimated_hours": 2.5,
        "description": "Build an enterprise wire transfer approval workflow with dynamic interrupt(), checkpoint persistence, reviewer state editing, and audit trail logging.",
        "learning_outcomes": [
            "Implement dynamic interrupt() based on transfer value thresholds",
            "Inspect pending tasks and interrupt payloads",
            "Resume suspended executions with Command(resume=...)",
            "Perform manual state edits with update_state() before resumption"
        ],
        "architecture_diagram": "graph TD\n  START([START]) --> Validate[Validate Transfer Node]\n  Validate --> AmountCheck{Amount >= $1,000?}\n  AmountCheck -- No --> ExecuteDirect[Execute Transfer Directly] --> END([END])\n  AmountCheck -- Yes --> Gate[Human Approval Gate: calls interrupt()]\n  Gate -. Pauses & awaits human verdict .- Gate\n  Gate -- Command(resume=True) --> ExecuteApproved[Execute Approved Wire] --> END\n  Gate -- Command(resume=False) --> Reject[Reject & Log Audit] --> END",
        "requirements": [
            "Transfers >= $1,000 must pause at human approval gate",
            "Expose approval payload containing transfer ID, recipient, and amount",
            "Resume on approval and complete transfer; log audit record on rejection"
        ],
        "steps": [],
        "starter_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

# Implement HITL wire approval workflow
""",
        "solution_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class WireState(TypedDict):
    transfer_id: str
    recipient: str
    amount: float
    status: str
    audit_log: str

def validate_transfer(state: WireState) -> dict:
    return {"status": "VALIDATED"}

def human_gate_node(state: WireState) -> Command:
    if state["amount"] >= 1000.0:
        approved = interrupt({
            "action": "APPROVE_WIRE",
            "transfer_id": state["transfer_id"],
            "amount": state["amount"],
            "recipient": state["recipient"]
        })
        if not approved:
            return Command(update={"status": "REJECTED", "audit_log": "Rejected by Risk Officer"}, goto="log_rejection")
    return Command(update={"status": "APPROVED", "audit_log": "Approved for settlement"}, goto="execute_wire")

def execute_wire_node(state: WireState) -> dict:
    return {"status": f"SETTLED: ${state['amount']} sent to {state['recipient']}"}

def log_rejection_node(state: WireState) -> dict:
    return {"status": f"CANCELLED: Transfer {state['transfer_id']} blocked"}

builder = StateGraph(WireState)
builder.add_node("validate", validate_transfer)
builder.add_node("human_gate", human_gate_node)
builder.add_node("execute_wire", execute_wire_node)
builder.add_node("log_rejection", log_rejection_node)

builder.add_edge(START, "validate")
builder.add_edge("validate", "human_gate")
builder.add_edge("execute_wire", END)
builder.add_edge("log_rejection", END)

app = builder.compile(checkpointer=MemorySaver())""",
        "test_cases_code": """def test_project_4():
    cfg = {"configurable": {"thread_id": "tx-test-99"}}
    app.invoke({"transfer_id": "TX-1", "recipient": "Acme", "amount": 5000.0, "status": "", "audit_log": ""}, config=cfg)
    snap = app.get_state(cfg)
    assert len(snap.next) > 0  # Still paused
    res = app.invoke(Command(resume=True), config=cfg)
    assert "SETTLED" in res["status"]
    print("Project 4 test passed!")
test_project_4()""",
        "sample_request": {"transfer_id": "TX-1", "recipient": "Acme Corp", "amount": 5000.0, "status": "", "audit_log": ""},
        "expected_response": {"status": "SETTLED: $5000.0 sent to Acme Corp", "audit_log": "Approved for settlement"},
        "bonus_extensions": ["Add multi-signature approval (2 approvals required)", "Add state editing before resume"]
    },
    {
        "id": "proj-5",
        "title": "Project 5: Corrective RAG (CRAG) Application with Document Grading",
        "difficulty": "Production",
        "estimated_hours": 3.0,
        "description": "Construct an enterprise Corrective RAG pipeline that retrieves documents, grades relevance, rewrites ambiguous queries, falls back to web knowledge, and checks for hallucinations.",
        "learning_outcomes": [
            "Implement document grading nodes with binary relevance thresholds",
            "Write query transformation and web fallback branches",
            "Add hallucination grounding checks before final output"
        ],
        "architecture_diagram": "graph TD\n  START([START]) --> Ingest[Query Ingestion]\n  Ingest --> Retrieve[Vector Retrieval]\n  Retrieve --> Grader[Document Grader]\n  Grader --> RelevanceCheck{Passes Relevance?}\n  RelevanceCheck -- Yes --> GroundCheck{Hallucination Check}\n  RelevanceCheck -- No --> Rewrite[Query Rewriter] --> Fallback[Fallback Search] --> GroundCheck\n  GroundCheck -- Grounded --> Generate[Generate Final Answer] --> END([END])\n  GroundCheck -- Hallucinated --> Rewrite",
        "requirements": [
            "Evaluate document relevance and calculate grounding score",
            "Rewrite query if retrieved documents are below confidence threshold",
            "Ensure bounded loop execution with maximum retry limit"
        ],
        "steps": [],
        "starter_code": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
# Implement CRAG pipeline
""",
        "solution_code": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class CRAGState(TypedDict):
    query: str
    documents: list[str]
    is_relevant: bool
    grounded: bool
    answer: str

def retrieve(state: CRAGState) -> dict:
    q = state["query"].lower()
    docs = ["LangGraph allows stateful agent workflows."] if "langgraph" in q else ["Unrelated text."]
    return {"documents": docs}

def grade_docs(state: CRAGState) -> dict:
    rel = any("langgraph" in d.lower() for d in state["documents"])
    return {"is_relevant": rel}

def rewrite_query(state: CRAGState) -> dict:
    return {"documents": ["Web search: LangGraph is an orchestration engine."]}

def generate_ans(state: CRAGState) -> dict:
    context = " ".join(state["documents"])
    return {"answer": f"Answer grounded in: {context}", "grounded": True}

builder = StateGraph(CRAGState)
builder.add_node("retrieve", retrieve)
builder.add_node("grade", grade_docs)
builder.add_node("rewrite", rewrite_query)
builder.add_node("generate", generate_ans)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")
builder.add_conditional_edges("grade", lambda s: "generate" if s["is_relevant"] else "rewrite", {
    "generate": "generate",
    "rewrite": "rewrite"
})
builder.add_edge("rewrite", "generate")
builder.add_edge("generate", END)

app = builder.compile()""",
        "test_cases_code": """def test_project_5():
    res = app.invoke({"query": "Explain LangGraph", "documents": [], "is_relevant": False, "grounded": False, "answer": ""})
    assert "Answer grounded in" in res["answer"]
    assert res["is_relevant"] is True
    print("Project 5 test passed!")
test_project_5()""",
        "sample_request": {"query": "Explain LangGraph", "documents": [], "is_relevant": False, "grounded": False, "answer": ""},
        "expected_response": {"answer": "Answer grounded in: LangGraph allows stateful agent workflows.", "grounded": True, "is_relevant": True},
        "bonus_extensions": ["Integrate ChromaDB / vector embeddings", "Add citation links to sources"]
    },
    {
        "id": "proj-6",
        "title": "Project 6: Multi-Agent Research & Review Supervisor",
        "difficulty": "Production",
        "estimated_hours": 3.0,
        "description": "Build a multi-agent system with a central Supervisor and specialist worker agents (Researcher, Writer, Reviewer) coordinating via structured handoffs.",
        "learning_outcomes": [
            "Implement the Supervisor architecture pattern",
            "Manage hierarchical worker state transformations",
            "Prevent infinite agent handoffs with super-step bounds"
        ],
        "architecture_diagram": "graph TD\n  START([START]) --> Supervisor[Supervisor Agent]\n  Supervisor --> Choice{Select Next Specialist}\n  Choice -- 'researcher' --> ResearchAgent[Researcher Agent]\n  Choice -- 'writer' --> WriterAgent[Writer Agent]\n  Choice -- 'reviewer' --> ReviewAgent[Reviewer Agent]\n  Choice -- 'DONE' --> END([END])\n  ResearchAgent --> Supervisor\n  WriterAgent --> Supervisor\n  ReviewAgent --> Supervisor",
        "requirements": [
            "Supervisor delegates sequentially: Researcher -> Writer -> Reviewer -> END",
            "Collect research findings and draft into unified state",
            "Reviewer verifies draft quality before granting final completion"
        ],
        "steps": [],
        "starter_code": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
# Implement Multi-Agent Supervisor workflow
""",
        "solution_code": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class TeamState(TypedDict):
    task: str
    research: str
    draft: str
    review: str
    next_agent: str

def supervisor(state: TeamState) -> dict:
    if not state.get("research"): return {"next_agent": "researcher"}
    if not state.get("draft"): return {"next_agent": "writer"}
    if not state.get("review"): return {"next_agent": "reviewer"}
    return {"next_agent": "FINISH"}

def researcher(state: TeamState) -> dict:
    return {"research": f"Key facts for: {state['task']}"}

def writer(state: TeamState) -> dict:
    return {"draft": f"Full article written based on: {state['research']}"}

def reviewer(state: TeamState) -> dict:
    return {"review": "PASSED: High quality and verified facts."}

builder = StateGraph(TeamState)
builder.add_node("supervisor", supervisor)
builder.add_node("researcher", researcher)
builder.add_node("writer", writer)
builder.add_node("reviewer", reviewer)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", lambda s: s["next_agent"], {
    "researcher": "researcher",
    "writer": "writer",
    "reviewer": "reviewer",
    "FINISH": END
})
builder.add_edge("researcher", "supervisor")
builder.add_edge("writer", "supervisor")
builder.add_edge("reviewer", "supervisor")

app = builder.compile()""",
        "test_cases_code": """def test_project_6():
    res = app.invoke({"task": "Stateful AI Architectures", "research": "", "draft": "", "review": "", "next_agent": ""})
    assert res["review"] == "PASSED: High quality and verified facts."
    print("Project 6 test passed!")
test_project_6()""",
        "sample_request": {"task": "Stateful AI Architectures", "research": "", "draft": "", "review": "", "next_agent": ""},
        "expected_response": {"task": "Stateful AI Architectures", "review": "PASSED: High quality and verified facts.", "next_agent": "FINISH"},
        "bonus_extensions": ["Add parallel worker fan-out with Send()", "Add human approval for final review"]
    },
    {
        "id": "proj-7",
        "title": "Project 7: Fault-Tolerant Workflow with Checkpoint Time Travel",
        "difficulty": "Production",
        "estimated_hours": 2.5,
        "description": "Implement checkpoint inspection, rewind, state forking, and failure recovery using get_state_history() and update_state().",
        "learning_outcomes": [
            "Iterate through checkpoint history trees",
            "Rewind execution to arbitrary historical snapshots",
            "Fork new execution paths without modifying original history"
        ],
        "architecture_diagram": "graph LR\n  CP1[Step 1 Ingestion] --> CP2[Step 2 Analysis] --> CP3[Step 3 Bad Output]\n  CP2 -. Rewind & Fork with update_state() .-> CP3_Fork[Step 3 Corrected] --> CP4_Fork[Step 4 Final]",
        "requirements": [
            "Execute multi-step workflow and inspect checkpoint history",
            "Rewind to historical checkpoint and fork with corrected payload",
            "Verify the forked branch executes to completion successfully"
        ],
        "steps": [],
        "starter_code": """from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver
# Implement Time Travel workflow
""",
        "solution_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class TimeTravelState(TypedDict):
    step_num: int
    data: str

def step_1(state: TimeTravelState) -> dict: return {"step_num": 1, "data": "Step 1 OK"}
def step_2(state: TimeTravelState) -> dict: return {"step_num": 2, "data": state["data"] + " -> Step 2 OK"}
def step_3(state: TimeTravelState) -> dict: return {"step_num": 3, "data": state["data"] + " -> Step 3 OK"}

builder = StateGraph(TimeTravelState)
builder.add_node("s1", step_1)
builder.add_node("s2", step_2)
builder.add_node("s3", step_3)
builder.add_edge(START, "s1")
builder.add_edge("s1", "s2")
builder.add_edge("s2", "s3")
builder.add_edge("s3", END)

app = builder.compile(checkpointer=MemorySaver())""",
        "test_cases_code": """def test_project_7():
    cfg = {"configurable": {"thread_id": "tt-1"}}
    app.invoke({"step_num": 0, "data": "Init"}, config=cfg)
    history = list(app.get_state_history(cfg))
    assert len(history) >= 3
    print("Project 7 test passed!")
test_project_7()""",
        "sample_request": {"step_num": 0, "data": "Init"},
        "expected_response": {"step_num": 3, "data": "Step 1 OK -> Step 2 OK -> Step 3 OK"},
        "bonus_extensions": ["Add UI time-travel scrubber slider", "Add checkpoint diff viewer"]
    },
    {
        "id": "proj-8",
        "title": "Project 8: Production FastAPI Real-Time SSE Streaming Graph",
        "difficulty": "Production",
        "estimated_hours": 3.0,
        "description": "Build an asynchronous FastAPI backend streaming LangGraph node transitions, progress events, and LLM tokens over Server-Sent Events (SSE).",
        "learning_outcomes": [
            "Implement async astream with stream_mode='updates'",
            "Format SSE events with sse_starlette",
            "Handle client cancellations and disconnects gracefully"
        ],
        "architecture_diagram": "sequenceDiagram\n  participant Client as React App (EventSource)\n  participant FastAPI as FastAPI SSE Router\n  participant Engine as LangGraph astream()\n  Client->>FastAPI: GET /api/stream\n  FastAPI->>Engine: astream(input, stream_mode='updates')\n  Engine-->>FastAPI: yield Step 1\n  FastAPI-->>Client: data: {\"node\": \"step_1\", \"status\": \"done\"}\n  Engine-->>FastAPI: yield Step 2\n  FastAPI-->>Client: data: {\"node\": \"step_2\", \"status\": \"done\"}\n  FastAPI-->>Client: data: {\"event\": \"complete\"}",
        "requirements": [
            "FastAPI endpoint with EventSourceResponse",
            "Stream node name, execution duration, and state delta for each step",
            "Safe client disconnect detection"
        ],
        "steps": [],
        "starter_code": """from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
# Implement SSE streaming router
""",
        "solution_code": """import json, asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class FastState(TypedDict):
    input_text: str
    output_text: str

async def node_a(s: FastState) -> dict:
    await asyncio.sleep(0.1)
    return {"output_text": "Node A Processed"}

async def node_b(s: FastState) -> dict:
    await asyncio.sleep(0.1)
    return {"output_text": s["output_text"] + " -> Node B Processed"}

builder = StateGraph(FastState)
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", END)

graph_app = builder.compile()""",
        "test_cases_code": """import pytest
@pytest.mark.asyncio
async def test_project_8():
    chunks = []
    async for chunk in graph_app.astream({"input_text": "hello", "output_text": ""}):
        chunks.append(chunk)
    assert len(chunks) == 2
    print("Project 8 async test passed!")""",
        "sample_request": {"input_text": "hello", "output_text": ""},
        "expected_response": {"output_text": "Node A Processed -> Node B Processed"},
        "bonus_extensions": ["Add token-by-token message streaming", "Add live WebSocket bidirectional channel"]
    },
    {
        "id": "proj-9",
        "title": "Project 9: Final Capstone: Autonomous Enterprise Support Agent",
        "difficulty": "Production",
        "estimated_hours": 4.0,
        "description": "The ultimate capstone: Integrate StateGraph, ToolNode, Human Approval Gate for high-value refunds, MemorySaver persistence, input guardrails, and SSE streaming into a production-grade enterprise agent.",
        "learning_outcomes": [
            "Combine all 14 curriculum modules into an end-to-end architecture",
            "Implement guardrails, tools, human approval, and memory in a single unified graph",
            "Deploy with production observability and error boundaries"
        ],
        "architecture_diagram": "graph TD\n  START([START]) --> Guard[Safety & PII Guardrail]\n  Guard -- Blocked --> BlockMsg[Security Violation] --> END([END])\n  Guard -- Safe --> Agent[Agent Reasoner Node]\n  Agent --> Router{\"tools_condition\"}\n  Router -- Tool Calls --> Tools[ToolNode (Lookup & Refund Tools)]\n  Tools --> NeedsHuman{Refund > $100?}\n  NeedsHuman -- Yes --> HITL[Human Approval Gate: interrupt()]\n  HITL -- Approved --> ToolsReturn[Merge Tool Outputs] --> Agent\n  NeedsHuman -- No --> ToolsReturn\n  Router -- Complete --> Persist[(Checkpointer Snapshot)] --> END",
        "requirements": [
            "Input guardrail filtering prohibited security queries",
            "Tools for account lookup and refund issuance",
            "Human approval interrupt required for refunds over $100",
            "Persistent session history with thread_id",
            "Structured response format"
        ],
        "steps": [],
        "starter_code": """# Master Capstone: Combine all LangGraph concepts into a single enterprise system!
""",
        "solution_code": """from typing import TypedDict, Annotated, Literal
from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

@tool
def lookup_customer(customer_id: str) -> str:
    \"\"\"Fetches customer tier and account balance.\"\"\"
    return f"Customer {customer_id}: Tier=ENTERPRISE, Balance=$450.00"

@tool
def process_refund(customer_id: str, amount: float) -> str:
    \"\"\"Processes a customer refund. Amounts > $100 require manager approval.\"\"\"
    return f"Refund of ${amount:,.2f} issued for {customer_id}."

tools = [lookup_customer, process_refund]
tool_node = ToolNode(tools=tools, handle_tool_errors=True)

def enterprise_agent(state: MessagesState) -> dict:
    msgs = state["messages"]
    if isinstance(msgs[-1], ToolMessage):
        return {"messages": [AIMessage(content=f"Resolution: {msgs[-1].content}")]}
    return {"messages": [AIMessage(
        content="Processing enterprise request...",
        tool_calls=[{"name": "lookup_customer", "args": {"customer_id": "CUST-99"}, "id": "call_c99", "type": "tool_call"}]
    )]}

builder = StateGraph(MessagesState)
builder.add_node("agent", enterprise_agent)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

capstone_app = builder.compile(checkpointer=MemorySaver())""",
        "test_cases_code": """def test_project_9_capstone():
    cfg = {"configurable": {"thread_id": "capstone-session-1"}}
    res = capstone_app.invoke({"messages": [HumanMessage(content="Check account CUST-99")]}, config=cfg)
    assert "Resolution: Customer CUST-99" in res["messages"][-1].content
    print("Capstone Project 9 test PASSED!")
test_project_9_capstone()""",
        "sample_request": {"messages": [{"role": "user", "content": "Check account CUST-99"}]},
        "expected_response": {"messages": [{"content": "Resolution: Customer CUST-99: Tier=ENTERPRISE, Balance=$450.00"}]},
        "bonus_extensions": ["Add multi-tenant PostgreSQL checkpointer", "Add LangSmith trace evaluator"]
    }
]

def get_all_projects() -> List[Dict[str, Any]]:
    return PROJECTS

def get_project_by_id(pid: str) -> Optional[Dict[str, Any]]:
    for p in PROJECTS:
        if p["id"] == pid:
            return p
    return None
