from typing import Dict, Any, List, Optional

PLAYGROUND_EXAMPLES: List[Dict[str, Any]] = [
    {
        "id": "sequential-pipeline",
        "title": "1. Linear Transformation Pipeline",
        "category": "Foundations",
        "difficulty": "Beginner",
        "description": "A clean 3-node sequential pipeline demonstrating StateGraph initialization, TypedDict state passing, and deterministic node updates.",
        "initial_state": {
            "raw_text": "  LangGraph enables complex cyclical AI workflows!  ",
            "clean_text": "",
            "word_count": 0,
            "sentiment": "NEUTRAL"
        },
        "python_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class TextPipeline(TypedDict):
    raw_text: str
    clean_text: str
    word_count: int
    sentiment: str

def sanitize_node(state: TextPipeline) -> dict:
    cleaned = state["raw_text"].strip().lower()
    return {"clean_text": cleaned}

def analyze_stats_node(state: TextPipeline) -> dict:
    words = len(state["clean_text"].split())
    return {"word_count": words}

def score_sentiment_node(state: TextPipeline) -> dict:
    text = state["clean_text"]
    sentiment = "POSITIVE" if "enables" in text or "great" in text else "NEUTRAL"
    return {"sentiment": sentiment}

builder = StateGraph(TextPipeline)
builder.add_node("sanitize", sanitize_node)
builder.add_node("analyze_stats", analyze_stats_node)
builder.add_node("score_sentiment", score_sentiment_node)

builder.add_edge(START, "sanitize")
builder.add_edge("sanitize", "analyze_stats")
builder.add_edge("analyze_stats", "score_sentiment")
builder.add_edge("score_sentiment", END)

app = builder.compile()
print(app.invoke({"raw_text": "  LangGraph enables complex cyclical AI workflows!  "}))""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "Graph Entry Point"},
                {"id": "sanitize", "label": "Sanitize Text", "type": "node", "description": "Trims whitespace and normalizes case"},
                {"id": "analyze_stats", "label": "Analyze Stats", "type": "node", "description": "Counts words in cleaned text"},
                {"id": "score_sentiment", "label": "Score Sentiment", "type": "node", "description": "Evaluates sentiment score"},
                {"id": "END", "label": "END", "type": "end", "description": "Graph Completion"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "sanitize", "label": "inbound"},
                {"id": "e1", "source": "sanitize", "target": "analyze_stats", "label": "next"},
                {"id": "e2", "source": "analyze_stats", "target": "score_sentiment", "label": "next"},
                {"id": "e3", "source": "score_sentiment", "target": "END", "label": "finish"}
            ]
        },
        "is_real_execution": True
    },
    {
        "id": "conditional-branching",
        "title": "2. Dynamic Intent Routing & Branching",
        "category": "Routing",
        "difficulty": "Intermediate",
        "description": "Classify user intent dynamically and route to dedicated Billing, Technical Support, or General FAQ handler nodes.",
        "initial_state": {
            "ticket_text": "Our payment was declined and our subscription expired.",
            "intent": "",
            "assigned_team": "",
            "priority": "NORMAL"
        },
        "python_code": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class SupportState(TypedDict):
    ticket_text: str
    intent: str
    assigned_team: str
    priority: str

def classify_intent(state: SupportState) -> dict:
    text = state["ticket_text"].lower()
    if "payment" in text or "invoice" in text or "card" in text:
        intent = "billing"
    elif "bug" in text or "error" in text or "down" in text:
        intent = "tech"
    else:
        intent = "general"
    priority = "HIGH" if "urgent" in text or "down" in text else "NORMAL"
    return {"intent": intent, "priority": priority}

def route_ticket(state: SupportState) -> Literal["billing_team", "tech_team", "faq_bot"]:
    if state["intent"] == "billing":
        return "billing_team"
    elif state["intent"] == "tech":
        return "tech_team"
    return "faq_bot"

def billing_handler(state: SupportState) -> dict:
    return {"assigned_team": "Billing & Revenue Operations"}

def tech_handler(state: SupportState) -> dict:
    return {"assigned_team": "Tier 2 Engineering Support"}

def faq_handler(state: SupportState) -> dict:
    return {"assigned_team": "Automated FAQ Knowledge Base"}

builder = StateGraph(SupportState)
builder.add_node("classifier", classify_intent)
builder.add_node("billing_team", billing_handler)
builder.add_node("tech_team", tech_handler)
builder.add_node("faq_bot", faq_handler)

builder.add_edge(START, "classifier")
builder.add_conditional_edges("classifier", route_ticket, {
    "billing_team": "billing_team",
    "tech_team": "tech_team",
    "faq_bot": "faq_bot"
})
builder.add_edge("billing_team", END)
builder.add_edge("tech_team", END)
builder.add_edge("faq_bot", END)

app = builder.compile()
print(app.invoke({"ticket_text": "Our payment was declined and our subscription expired."}))""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "Incoming Support Ticket"},
                {"id": "classifier", "label": "Intent Classifier", "type": "node", "description": "Detects intent keyword rules"},
                {"id": "billing_team", "label": "Billing Team", "type": "node", "description": "Handles payment issues"},
                {"id": "tech_team", "label": "Tech Support", "type": "node", "description": "Handles technical bugs"},
                {"id": "faq_bot", "label": "FAQ Bot", "type": "node", "description": "Handles general queries"},
                {"id": "END", "label": "END", "type": "end", "description": "Resolution Complete"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "classifier"},
                {"id": "e1", "source": "classifier", "target": "billing_team", "conditional": True, "label": "billing"},
                {"id": "e2", "source": "classifier", "target": "tech_team", "conditional": True, "label": "tech"},
                {"id": "e3", "source": "classifier", "target": "faq_bot", "conditional": True, "label": "general"},
                {"id": "e4", "source": "billing_team", "target": "END"},
                {"id": "e5", "source": "tech_team", "target": "END"},
                {"id": "e6", "source": "faq_bot", "target": "END"}
            ]
        },
        "is_real_execution": True
    },
    {
        "id": "cyclical-agent-refine",
        "title": "3. Iterative Refinement Loop",
        "category": "Loops & Cycles",
        "difficulty": "Intermediate",
        "description": "Cyclical loop with automated quality evaluation, backward edge revision, and recursion limit boundaries.",
        "initial_state": {
            "topic": "LangGraph Pregel Super-Steps",
            "draft": "",
            "quality_score": 0,
            "revision_count": 0
        },
        "python_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class RefineState(TypedDict):
    topic: str
    draft: str
    quality_score: int
    revision_count: int

def drafter_node(state: RefineState) -> dict:
    count = state.get("revision_count", 0) + 1
    new_score = state.get("quality_score", 30) + 25
    return {
        "draft": f"Draft v{count} covering {state['topic']}",
        "quality_score": new_score,
        "revision_count": count
    }

def quality_evaluator(state: RefineState) -> dict:
    return {"quality_score": state["quality_score"]}

def should_continue_refining(state: RefineState) -> str:
    if state["quality_score"] >= 80 or state["revision_count"] >= 3:
        return "publish"
    return "refine_again"

builder = StateGraph(RefineState)
builder.add_node("drafter", drafter_node)
builder.add_node("evaluator", quality_evaluator)

builder.add_edge(START, "drafter")
builder.add_edge("drafter", "evaluator")
builder.add_conditional_edges("evaluator", should_continue_refining, {
    "refine_again": "drafter",
    "publish": END
})

app = builder.compile()
print(app.invoke({"topic": "LangGraph Pregel Super-Steps"}))""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "Initiate Drafting"},
                {"id": "drafter", "label": "Drafter / Editor", "type": "node", "description": "Generates or revises draft"},
                {"id": "evaluator", "label": "Quality Evaluator", "type": "node", "description": "Inspects score >= 80"},
                {"id": "END", "label": "END", "type": "end", "description": "Publish Approved Draft"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "drafter"},
                {"id": "e1", "source": "drafter", "target": "evaluator"},
                {"id": "e2", "source": "evaluator", "target": "drafter", "conditional": True, "label": "score < 80"},
                {"id": "e3", "source": "evaluator", "target": "END", "conditional": True, "label": "score >= 80"}
            ]
        },
        "is_real_execution": True
    },
    {
        "id": "parallel-fanout",
        "title": "4. Parallel Fan-Out / Fan-In & Reducers",
        "category": "State & Concurrency",
        "difficulty": "Intermediate",
        "description": "Execute multiple nodes concurrently in the same super-step, merging lists atomically using Annotated[list, operator.add].",
        "initial_state": {
            "company_name": "Antigravity AI",
            "insights": []
        },
        "python_code": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class IntelState(TypedDict):
    company_name: str
    insights: Annotated[list[str], operator.add]

def fetch_financials(state: IntelState) -> dict:
    return {"insights": [f"Financials for {state['company_name']}: $120M ARR, profitable"]}

def fetch_news(state: IntelState) -> dict:
    return {"insights": [f"News for {state['company_name']}: Launched state-of-the-art developer platform"]}

def fetch_patents(state: IntelState) -> dict:
    return {"insights": [f"Patents for {state['company_name']}: 14 distributed graph AI patents granted"]}

def synthesize_report(state: IntelState) -> dict:
    total = len(state["insights"])
    return {"insights": [f"=== SYNTHESIS: {total} data streams consolidated successfully ==="]}

builder = StateGraph(IntelState)
builder.add_node("financials", fetch_financials)
builder.add_node("news", fetch_news)
builder.add_node("patents", fetch_patents)
builder.add_node("synthesizer", synthesize_report)

# Fan-out: 3 parallel workers
builder.add_edge(START, "financials")
builder.add_edge(START, "news")
builder.add_edge(START, "patents")

# Fan-in to synthesizer
builder.add_edge("financials", "synthesizer")
builder.add_edge("news", "synthesizer")
builder.add_edge("patents", "synthesizer")
builder.add_edge("synthesizer", END)

app = builder.compile()
res = app.invoke({"company_name": "Antigravity AI", "insights": []})
print(res)""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "Trigger Research"},
                {"id": "financials", "label": "Financial Analyzer", "type": "node", "description": "Runs concurrently in Super-step 1"},
                {"id": "news", "label": "News Scanner", "type": "node", "description": "Runs concurrently in Super-step 1"},
                {"id": "patents", "label": "Patent Search", "type": "node", "description": "Runs concurrently in Super-step 1"},
                {"id": "synthesizer", "label": "Report Synthesizer", "type": "node", "description": "Runs in Super-step 2 after all 3 merge"},
                {"id": "END", "label": "END", "type": "end", "description": "Consolidated Report"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "financials"},
                {"id": "e1", "source": "START", "target": "news"},
                {"id": "e2", "source": "START", "target": "patents"},
                {"id": "e3", "source": "financials", "target": "synthesizer"},
                {"id": "e4", "source": "news", "target": "synthesizer"},
                {"id": "e5", "source": "patents", "target": "synthesizer"},
                {"id": "e6", "source": "synthesizer", "target": "END"}
            ]
        },
        "is_real_execution": True
    },
    {
        "id": "human-in-the-loop-approval",
        "title": "5. Human-in-the-Loop Dynamic Interrupts",
        "category": "Human-in-the-Loop",
        "difficulty": "Advanced",
        "description": "Pause execution dynamically on sensitive thresholds using interrupt(), saving checkpoint for human review, and resuming with Command(resume=...).",
        "initial_state": {
            "recipient": "supplier_corp",
            "transfer_amount": 7500.0,
            "status": "INITIATED"
        },
        "python_code": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class WireTransferState(TypedDict):
    recipient: str
    transfer_amount: float
    status: str

def initiate_transfer(state: WireTransferState) -> dict:
    return {"status": "VALIDATED"}

def human_approval_gate(state: WireTransferState) -> Command:
    amt = state["transfer_amount"]
    if amt >= 5000:
        # Trigger dynamic interrupt
        approved = interrupt({
            "prompt": f"Authorize wire transfer of ${amt:,.2f} to {state['recipient']}?",
            "requires_mfa": True
        })
        if not approved:
            return Command(update={"status": "TRANSFER_REJECTED"}, goto=END)
            
    return Command(update={"status": f"COMPLETED: ${amt:,.2f} transferred to {state['recipient']}"}, goto=END)

builder = StateGraph(WireTransferState)
builder.add_node("initiate", initiate_transfer)
builder.add_node("approval_gate", human_approval_gate)

builder.add_edge(START, "initiate")
builder.add_edge("initiate", "approval_gate")

app = builder.compile(checkpointer=MemorySaver())
cfg = {"configurable": {"thread_id": "wire-tx-554"}}

# First invoke triggers interrupt
app.invoke({"recipient": "supplier_corp", "transfer_amount": 7500.0, "status": ""}, config=cfg)
print("Graph paused at interrupt!")

# Resume with approval
res = app.invoke(Command(resume=True), config=cfg)
print("Resumed final state:", res)""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "Incoming Wire Request"},
                {"id": "initiate", "label": "Initiate & Validate", "type": "node", "description": "Validates account details"},
                {"id": "approval_gate", "label": "Human Approval Gate", "type": "node", "description": "Pauses at interrupt() for amounts >= $5,000"},
                {"id": "END", "label": "END", "type": "end", "description": "Transaction Finalized"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "initiate"},
                {"id": "e1", "source": "initiate", "target": "approval_gate"},
                {"id": "e2", "source": "approval_gate", "target": "END", "label": "resume"}
            ]
        },
        "is_real_execution": True
    },
    {
        "id": "react-tool-loop",
        "title": "6. ReAct Agent Tool Execution Cycle",
        "category": "Agents",
        "difficulty": "Intermediate",
        "description": "Complete ReAct loop featuring ToolNode, tools_condition, and structured tool returns.",
        "initial_state": {
            "messages": [
                {"role": "user", "content": "What is the tax on $5,000 in California (rate 7.25%)?"}
            ]
        },
        "python_code": """from langchain_core.messages import HumanMessage, AIMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def calculate_sales_tax(amount: float, tax_rate_pct: float) -> str:
    \"\"\"Calculates sales tax and total price.\"\"\"
    tax = round(amount * (tax_rate_pct / 100), 2)
    total = round(amount + tax, 2)
    return f"Tax: ${tax:,.2f} | Total: ${total:,.2f}"

tools = [calculate_sales_tax]
tool_node = ToolNode(tools)

def agent_reasoning(state: MessagesState) -> dict:
    msgs = state["messages"]
    if isinstance(msgs[-1], ToolMessage):
        return {"messages": [AIMessage(content=f"Final Answer: {msgs[-1].content}")]}
        
    return {"messages": [AIMessage(
        content="Calculating tax using sales tax tool...",
        tool_calls=[{"name": "calculate_sales_tax", "args": {"amount": 5000, "tax_rate_pct": 7.25}, "id": "call_tax_1", "type": "tool_call"}]
    )]}

builder = StateGraph(MessagesState)
builder.add_node("agent", agent_reasoning)
builder.add_node("tools", tool_node)

builder.add_edge(START, "agent")
builder.add_conditional_edges("agent", tools_condition)
builder.add_edge("tools", "agent")

app = builder.compile()
res = app.invoke({"messages": [HumanMessage(content="Calculate CA tax on $5000")]})
print(res)""",
        "graph": {
            "nodes": [
                {"id": "START", "label": "START", "type": "start", "description": "User Question"},
                {"id": "agent", "label": "Agent Reasoner", "type": "node", "description": "Generates thought & tool calls"},
                {"id": "tools", "label": "ToolNode (Tools)", "type": "node", "description": "Executes calculate_sales_tax"},
                {"id": "END", "label": "END", "type": "end", "description": "Final Formatted Reply"}
            ],
            "edges": [
                {"id": "e0", "source": "START", "target": "agent"},
                {"id": "e1", "source": "agent", "target": "tools", "conditional": True, "label": "has tool_calls"},
                {"id": "e2", "source": "tools", "target": "agent", "label": "return ToolMessage"},
                {"id": "e3", "source": "agent", "target": "END", "conditional": True, "label": "no tool_calls"}
            ]
        },
        "is_real_execution": True
    }
]

def get_playground_examples() -> List[Dict[str, Any]]:
    return PLAYGROUND_EXAMPLES

def get_playground_example(example_id: str) -> Optional[Dict[str, Any]]:
    for ex in PLAYGROUND_EXAMPLES:
        if ex["id"] == example_id:
            return ex
    return None
