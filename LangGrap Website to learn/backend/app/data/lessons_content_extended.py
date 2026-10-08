# Complete detailed lesson contents for Modules 3 through 14
from typing import Dict, Any

EXTENDED_LESSONS: Dict[str, Dict[str, Any]] = {
    "m3-l1": {
        "id": "m3-l1",
        "module_id": "module-3",
        "module_title": "Module 3: State Management & Reducers",
        "title": "Custom Reducers with Annotated[T, reducer]",
        "difficulty": "Intermediate",
        "estimated_minutes": 15,
        "prerequisites": ["m2-l1"],
        "objectives": [
            "Understand default channel overwrite semantics vs reducer functions",
            "Use typing.Annotated with operator.add for list accumulation",
            "Write custom state reducers for complex dictionaries and merge policies"
        ],
        "simple_explanation": "By default, when a node returns a key, it completely overwrites the previous value in state. If you want a list to accumulate items from multiple nodes or super-steps instead of replacing it, you wrap the type in Annotated[list[T], operator.add] or a custom reducer function.",
        "why_it_matters": "Without reducers, parallel nodes will overwrite each other's data, causing race conditions and lost outputs. Reducers define exactly how concurrent or sequential updates get merged.",
        "real_world_analogy": "A whiteboard vs a ledger. Default state is a whiteboard: whoever writes on it erases what was there before. An Annotated reducer is an append-only ledger: every participant adds their entries at the bottom.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  OldState[\"State: ['Item 1']\"] --> NodeUpdate[\"Node returns: ['Item 2']\"]\n  NodeUpdate --> Reducer{\"operator.add\"}\n  Reducer --> NewState[\"State: ['Item 1', 'Item 2']\"]"
        },
        "code_example": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

# Custom reducer function for deduplicating tags
def merge_unique_tags(left: list[str], right: list[str]) -> list[str]:
    # left: current state value, right: update returned by node
    return list(set((left or []) + (right or [])))

class DocumentState(TypedDict):
    title: str  # Default overwrite behavior
    logs: Annotated[list[str], operator.add]  # Append reducer
    tags: Annotated[list[str], merge_unique_tags]  # Custom deduplication reducer

def tag_security(state: DocumentState) -> dict:
    return {
        "logs": ["Security review completed."],
        "tags": ["security", "confidential"]
    }

def tag_compliance(state: DocumentState) -> dict:
    return {
        "logs": ["Compliance review completed."],
        "tags": ["compliance", "security"]  # Notice duplicate 'security'
    }

builder = StateGraph(DocumentState)
builder.add_node("sec", tag_security)
builder.add_node("comp", tag_compliance)

builder.add_edge(START, "sec")
builder.add_edge("sec", "comp")
builder.add_edge("comp", END)

app = builder.compile()
res = app.invoke({"title": "Q3 Report", "logs": ["Intake done."], "tags": ["internal"]})
print("Logs:", res["logs"])
print("Unique Tags:", res["tags"])""",
        "line_by_line": [
            {"line": "def merge_unique_tags(left: list[str], right: list[str]) -> list[str]:", "explanation": "A reducer function takes (current_value, new_update) and returns the combined state value."},
            {"line": "logs: Annotated[list[str], operator.add]", "explanation": "Tells LangGraph to concatenate lists using operator.add rather than overwriting."}
        ],
        "sample_input": {"title": "Q3 Report", "logs": ["Intake done."], "tags": ["internal"]},
        "sample_output": {
            "title": "Q3 Report",
            "logs": ["Intake done.", "Security review completed.", "Compliance review completed."],
            "tags": ["internal", "security", "confidential", "compliance"]
        },
        "common_mistakes": [
            {"mistake": "Writing a reducer that does not handle None as the left argument when state is uninitialized.", "fix": "Always do `(left or []) + (right or [])` or check `if not left:` to handle initial empty states."}
        ],
        "hands_on_task": {
            "title": "Create a max-score reducer",
            "instruction": "Write a reducer function `keep_highest_score(left: int, right: int) -> int` that stores the maximum score.",
            "starter_code": "def keep_highest_score(left: int, right: int) -> int:\n    return max(left or 0, right or 0)"
        },
        "quick_quiz": [
            {
                "question": "What happens if two parallel nodes write to a field typed as `name: str` without an Annotated reducer?",
                "options": [
                    "LangGraph automatically concatenates the strings",
                    "An InvalidUpdateError is raised because parallel writes to an unreduced channel conflict",
                    "The graph pauses for human approval",
                    "The second string is silently ignored"
                ],
                "correct_index": 1,
                "explanation": "If multiple nodes write to the same unreduced channel in the same super-step, LangGraph raises an error because it cannot deterministically choose which value wins."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m2-l3",
        "next_lesson_id": "m3-l2"
    },
    "m3-l2": {
        "id": "m3-l2",
        "module_id": "module-3",
        "module_title": "Module 3: State Management & Reducers",
        "title": "MessagesState & add_messages Reducer",
        "difficulty": "Intermediate",
        "estimated_minutes": 18,
        "prerequisites": ["m3-l1"],
        "objectives": [
            "Use prebuilt MessagesState for chat conversational workflows",
            "Understand add_messages reducer with ID matching and message updates",
            "Construct HumanMessage, AIMessage, and ToolMessage objects"
        ],
        "simple_explanation": "Conversational agents deal with message streams. LangGraph provides `MessagesState`, which has a preconfigured `messages: Annotated[list[AnyMessage], add_messages]` field. `add_messages` automatically appends new messages or updates existing messages if their `id` matches.",
        "why_it_matters": "Updating an existing message by ID allows models to edit previous responses, clear temporary thoughts, or attach tool outputs without recreating the whole conversation array.",
        "real_world_analogy": "Like an online chat group where members can send new replies (appends) or edit a typo in their previous message if they reference its ID.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Msg1[\"HumanMessage(id='1', 'Hi')\"] --> AddMsg{\"add_messages\"}\n  Msg2[\"AIMessage(id='2', 'Thinking...')\"] --> AddMsg\n  MsgUpdate[\"AIMessage(id='2', 'Hello! How can I help?')\"] --> AddMsg\n  AddMsg --> FinalState[\"Result: [HumanMessage('Hi'), AIMessage('Hello! How can I help?')]\"]"
        },
        "code_example": """from langchain_core.messages import HumanMessage, AIMessage, BaseMessage
from langgraph.graph import StateGraph, MessagesState, START, END

# MessagesState comes with:
# class MessagesState(TypedDict):
#     messages: Annotated[list[BaseMessage], add_messages]

def bot_responder(state: MessagesState) -> dict:
    history = state["messages"]
    last_user_msg = history[-1].content
    ai_reply = AIMessage(
        id="reply-1",
        content=f"Echoing back your message: {last_user_msg}"
    )
    return {"messages": [ai_reply]}

def bot_polisher(state: MessagesState) -> dict:
    # Overwriting the previous reply by referencing the exact same ID 'reply-1'
    polished_reply = AIMessage(
        id="reply-1",
        content="Polished: Welcome! I am your AI assistant. How may I support your learning today?"
    )
    return {"messages": [polished_reply]}

builder = StateGraph(MessagesState)
builder.add_node("bot", bot_responder)
builder.add_node("polish", bot_polisher)

builder.add_edge(START, "bot")
builder.add_edge("bot", "polish")
builder.add_edge("polish", END)

app = builder.compile()
out = app.invoke({"messages": [HumanMessage(content="Hello assistant!")]})

print(f"Total messages in state: {len(out['messages'])}")
for m in out["messages"]:
    print(f"[{m.type} - ID: {m.id}]: {m.content}")""",
        "line_by_line": [
            {"line": "builder = StateGraph(MessagesState)", "explanation": "Uses the prebuilt MessagesState class which includes the add_messages reducer."},
            {"line": "polished_reply = AIMessage(id='reply-1', ...)", "explanation": "Because 'reply-1' matches the previous message's ID, add_messages replaces it in-place."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "Hello"}]},
        "sample_output": {
            "messages": [
                {"type": "human", "content": "Hello assistant!"},
                {"type": "ai", "id": "reply-1", "content": "Polished: Welcome! I am your AI assistant. How may I support your learning today?"}
            ]
        },
        "common_mistakes": [
            {"mistake": "Returning a raw string instead of a message object or message dict in messages list.", "fix": "Return `AIMessage(content='...')` or `[{'role': 'assistant', 'content': '...'}]`."}
        ],
        "hands_on_task": {
            "title": "Add a RemoveMessage test",
            "instruction": "Import `from langchain_core.messages import RemoveMessage` and remove a message by ID.",
            "starter_code": "from langchain_core.messages import RemoveMessage\n# return {'messages': [RemoveMessage(id='msg-id-to-delete')]}"
        },
        "quick_quiz": [
            {
                "question": "How does add_messages handle a new message that shares the same `id` as an existing message in state?",
                "options": [
                    "It creates a duplicate message with suffix _2",
                    "It replaces the existing message in-place at the exact same position in the list",
                    "It throws a DuplicateKeyError",
                    "It deletes both messages"
                ],
                "correct_index": 1,
                "explanation": "add_messages updates the existing message with matching ID in-place, enabling in-flight updates and revisions."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m3-l1",
        "next_lesson_id": "m3-l3"
    },
    "m3-l3": {
        "id": "m3-l3",
        "module_id": "module-3",
        "module_title": "Module 3: State Management & Reducers",
        "title": "Separate Input, Internal, & Output State Schemas",
        "difficulty": "Intermediate",
        "estimated_minutes": 15,
        "prerequisites": ["m3-l1"],
        "objectives": [
            "Define distinct InputState and OutputState schemas for public graph interfaces",
            "Hide private internal scratchpads and API tokens from external callers",
            "Construct StateGraph(state_schema=..., input=..., output=...)"
        ],
        "simple_explanation": "In production, callers should only provide required inputs (e.g. `query`) and receive clean outputs (e.g. `answer`), without exposing private internal variables like `scratchpad`, `tool_retries`, or `raw_tokens`.",
        "why_it_matters": "Separating schemas guarantees clean API contracts, enforces validation on incoming requests, and avoids leaking sensitive intermediate data.",
        "real_world_analogy": "Like a restaurant kitchen: customers see the Menu (Input schema) and receive the Plated Meal (Output schema). They don't see the prep pans, timers, or meat thermometers used internally (Internal State).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Input[InputSchema: {user_query}] --> Start([START])\n  Start --> Node[Node: Computes with InternalState: {scratchpad, tokens, answer}]\n  Node --> End([END])\n  End --> Output[OutputSchema: {final_answer}]"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Public Input Schema
class PublicInput(TypedDict):
    question: str

# 2. Public Output Schema
class PublicOutput(TypedDict):
    answer: str
    confidence: float

# 3. Full Internal Graph State
class PrivateGraphState(TypedDict):
    question: str
    intermediate_notes: list[str]
    raw_api_tokens: int
    answer: str
    confidence: float

def reasoning_node(state: PrivateGraphState) -> dict:
    return {
        "intermediate_notes": ["Analyzed syntax", "Checked database knowledge"],
        "raw_api_tokens": 142,
        "answer": f"LangGraph is modular and powerful for {state['question']}.",
        "confidence": 0.98
    }

# Configure StateGraph with distinct input and output schemas
builder = StateGraph(
    state_schema=PrivateGraphState,
    input=PublicInput,
    output=PublicOutput
)

builder.add_node("reason", reasoning_node)
builder.add_edge(START, "reason")
builder.add_edge("reason", END)

app = builder.compile()

# Invoke with just PublicInput
res = app.invoke({"question": "agent orchestration"})
print("Filtered Output Schema:", res)
# Notice: 'intermediate_notes' and 'raw_api_tokens' are NOT returned to caller!""",
        "line_by_line": [
            {"line": "builder = StateGraph(state_schema=PrivateGraphState, input=PublicInput, output=PublicOutput)", "explanation": "Specifies internal state as well as input/output boundary contracts."},
            {"line": "res = app.invoke({'question': 'agent orchestration'})", "explanation": "Returns only keys defined in PublicOutput ('answer' and 'confidence')."}
        ],
        "sample_input": {"question": "agent orchestration"},
        "sample_output": {"answer": "LangGraph is modular and powerful for agent orchestration.", "confidence": 0.98},
        "common_mistakes": [
            {"mistake": "Adding fields to PublicOutput that are not present in the internal state_schema.", "fix": "Ensure all keys in PublicInput and PublicOutput exist in the internal state_schema."}
        ],
        "hands_on_task": {
            "title": "Add latency metric to output",
            "instruction": "Add `latency_ms: float` to both PublicOutput and PrivateGraphState.",
            "starter_code": "class PublicOutput(TypedDict):\n    answer: str\n    confidence: float\n    latency_ms: float"
        },
        "quick_quiz": [
            {
                "question": "What is the primary benefit of passing `output=PublicOutput` to StateGraph?",
                "options": [
                    "It speeds up execution by 50%",
                    "It filters the final returned dictionary so external consumers only receive defined public keys",
                    "It automatically serializes data to a SQL database",
                    "It encrypts all internal variables"
                ],
                "correct_index": 1,
                "explanation": "Setting the output schema ensures only the designated public fields are returned to the caller upon completion."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m3-l2",
        "next_lesson_id": "m4-l1"
    },
    "m4-l1": {
        "id": "m4-l1",
        "module_id": "module-4",
        "module_title": "Module 4: Routing, Branching & Loops",
        "title": "Conditional Edges & Routing Functions",
        "difficulty": "Intermediate",
        "estimated_minutes": 16,
        "prerequisites": ["m2-l2"],
        "objectives": [
            "Understand add_conditional_edges signature and behavior",
            "Write deterministic and LLM-driven routing functions",
            "Use path mapping dictionaries for clear node aliasing"
        ],
        "simple_explanation": "Normal edges (`add_edge('A', 'B')`) are static: execution always goes from A to B. Conditional edges (`add_conditional_edges('A', router_fn, mapping)`) dynamically determine the next node by evaluating the return value of `router_fn(state)`.",
        "why_it_matters": "Dynamic branching is what enables classification, intent detection, error recovery branches, and tool selection.",
        "real_world_analogy": "A train switch track: As the train (state) reaches the junction, the track switch (routing function) checks the train's destination tag and directs it to Track 1, Track 2, or the Depot.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Classifier[Intent Classifier Node] --> Branch{Check Intent}\n  Branch -- 'billing' --> Billing[Billing Flow]\n  Branch -- 'technical' --> Tech[Tech Support Flow]\n  Branch -- 'general' --> FAQ[FAQ Responder]"
        },
        "code_example": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class SupportState(TypedDict):
    query: str
    intent: str
    response: str

def classify_intent_node(state: SupportState) -> dict:
    q = state["query"].lower()
    if "refund" in q or "price" in q:
        intent = "billing"
    elif "bug" in q or "crash" in q:
        intent = "tech"
    else:
        intent = "general"
    return {"intent": intent}

# Routing function
def route_by_intent(state: SupportState) -> Literal["billing_node", "tech_node", "general_node"]:
    if state["intent"] == "billing":
        return "billing_node"
    elif state["intent"] == "tech":
        return "tech_node"
    return "general_node"

def handle_billing(state: SupportState) -> dict:
    return {"response": "Directing to Billing Portal for refunds."}

def handle_tech(state: SupportState) -> dict:
    return {"response": "Opening engineering diagnostic ticket."}

def handle_general(state: SupportState) -> dict:
    return {"response": "Here is our general knowledge base link."}

builder = StateGraph(SupportState)
builder.add_node("classify", classify_intent_node)
builder.add_node("billing_node", handle_billing)
builder.add_node("tech_node", handle_tech)
builder.add_node("general_node", handle_general)

builder.add_edge(START, "classify")

# Conditional Edge from classify to targets
builder.add_conditional_edges(
    "classify",
    route_by_intent,
    {
        "billing_node": "billing_node",
        "tech_node": "tech_node",
        "general_node": "general_node"
    }
)

builder.add_edge("billing_node", END)
builder.add_edge("tech_node", END)
builder.add_edge("general_node", END)

app = builder.compile()
print(app.invoke({"query": "My app crashed with error 500", "intent": "", "response": ""}))""",
        "line_by_line": [
            {"line": "def route_by_intent(state: SupportState) -> Literal[...]:", "explanation": "The routing function receives current state and returns a string key corresponding to the next destination."},
            {"line": "builder.add_conditional_edges('classify', route_by_intent, mapping)", "explanation": "Registers the conditional edge from source node 'classify'."}
        ],
        "sample_input": {"query": "My app crashed with error 500", "intent": "", "response": ""},
        "sample_output": {"query": "My app crashed with error 500", "intent": "tech", "response": "Opening engineering diagnostic ticket."},
        "common_mistakes": [
            {"mistake": "Returning a destination node name from route_by_intent that is not registered in the graph.", "fix": "Ensure all returned destination keys correspond to registered nodes or END."}
        ],
        "hands_on_task": {
            "title": "Add an Urgent routing path",
            "instruction": "If the query contains 'urgent', route directly to an 'escalations' node.",
            "starter_code": "def route_by_intent(state: SupportState) -> str:\n    if 'urgent' in state['query'].lower(): return 'escalations'\n    ..."
        },
        "quick_quiz": [
            {
                "question": "What is the 3rd argument in add_conditional_edges(source, path_func, path_map)?",
                "options": [
                    "A list of database table names",
                    "An optional mapping dictionary {path_func_return_value: target_node_name}",
                    "A secret API key",
                    "The number of retry attempts"
                ],
                "correct_index": 1,
                "explanation": "The path_map dictionary maps values returned by the path function to concrete target node names in the graph."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m3-l3",
        "next_lesson_id": "m4-l2"
    },
    "m4-l2": {
        "id": "m4-l2",
        "module_id": "module-4",
        "module_title": "Module 4: Routing, Branching & Loops",
        "title": "Cyclical Loops, Termination & Recursion Limits",
        "difficulty": "Intermediate",
        "estimated_minutes": 18,
        "prerequisites": ["m4-l1"],
        "objectives": [
            "Build robust cyclic loops for iterative refinement",
            "Define explicit termination criteria",
            "Configure recursion_limit in RunnableConfig to prevent infinite loops"
        ],
        "simple_explanation": "In LangGraph, edges can point backwards to previously executed nodes, forming loops. To prevent infinite loops when LLMs get stuck, LangGraph enforces a default `recursion_limit` (default: 25 steps). You can adjust this limit in your invocation config.",
        "why_it_matters": "Iterative self-correction (code generation -> test execution -> fix code -> retry) requires loops. Without termination safeguards, runaways can burn hundreds of dollars in API credits.",
        "real_world_analogy": "Like a quality inspector on an assembly line: If an item fails inspection, it goes back to the rework station. But if it fails 3 times in a row, it's flagged as unfixable and sent to scrap (safe termination).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  START([START]) --> Generate[Generate Draft]\n  Generate --> Evaluate{Quality >= 80%?}\n  Evaluate -- No & Iteration < 3 --> Revise[Revise Draft]\n  Revise --> Evaluate\n  Evaluate -- Yes or Max Retries --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.errors import GraphRecursionError

class RefineState(TypedDict):
    draft: str
    iteration: int
    score: int

def generate_draft(state: RefineState) -> dict:
    return {"draft": "Initial draft v1", "iteration": 1, "score": 40}

def critique_and_refine(state: RefineState) -> dict:
    i = state["iteration"] + 1
    new_score = state["score"] + 25
    return {"draft": f"Refined draft v{i}", "iteration": i, "score": new_score}

def should_continue(state: RefineState) -> str:
    # Explicit loop termination condition
    if state["score"] >= 85:
        return "approved"
    if state["iteration"] >= 4:
        return "max_iterations_reached"
    return "refine"

builder = StateGraph(RefineState)
builder.add_node("generate", generate_draft)
builder.add_node("refine", critique_and_refine)

builder.add_edge(START, "generate")
builder.add_conditional_edges(
    "generate",
    should_continue,
    {"refine": "refine", "approved": END, "max_iterations_reached": END}
)
builder.add_conditional_edges(
    "refine",
    should_continue,
    {"refine": "refine", "approved": END, "max_iterations_reached": END}
)

app = builder.compile()

# Invoke with recursion limit safeguard
config = {"recursion_limit": 10}
result = app.invoke({"draft": "", "iteration": 0, "score": 0}, config=config)
print("Final State:", result)""",
        "line_by_line": [
            {"line": "config = {'recursion_limit': 10}", "explanation": "Sets the maximum number of super-steps the graph is allowed to execute before raising GraphRecursionError."},
            {"line": "if state['iteration'] >= 4: return 'max_iterations_reached'", "explanation": "Guarantees loop termination even if the score never reaches 85."}
        ],
        "sample_input": {"draft": "", "iteration": 0, "score": 0},
        "sample_output": {"draft": "Refined draft v3", "iteration": 3, "score": 90},
        "common_mistakes": [
            {"mistake": "Setting recursion_limit too low (e.g. 3) for a graph that naturally takes 5 super-steps.", "fix": "Calculate the expected maximum steps and set recursion_limit with adequate buffer."}
        ],
        "hands_on_task": {
            "title": "Trigger GraphRecursionError",
            "instruction": "Set `config = {'recursion_limit': 2}` and catch `GraphRecursionError`.",
            "starter_code": "try:\n    app.invoke(..., config={'recursion_limit': 2})\nexcept GraphRecursionError:\n    print('Recursion limit exceeded!')"
        },
        "quick_quiz": [
            {
                "question": "What happens if a LangGraph cycle exceeds the configured `recursion_limit`?",
                "options": [
                    "The computer crashes",
                    "LangGraph raises a GraphRecursionError to protect against infinite loops",
                    "The graph silently returns None",
                    "The state is reset to empty"
                ],
                "correct_index": 1,
                "explanation": "LangGraph terminates execution immediately and raises GraphRecursionError when the super-step count reaches recursion_limit."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m4-l1",
        "next_lesson_id": "m4-l3"
    },
    "m4-l3": {
        "id": "m4-l3",
        "module_id": "module-4",
        "module_title": "Module 4: Routing, Branching & Loops",
        "title": "Parallel Execution, Fan-Out / Fan-In & Send API",
        "difficulty": "Intermediate",
        "estimated_minutes": 20,
        "prerequisites": ["m4-l1", "m3-l1"],
        "objectives": [
            "Create static parallel fan-out / fan-in graphs",
            "Use the dynamic Send() API for map-reduce over unknown list lengths",
            "Aggregate parallel outputs using Annotated reducers"
        ],
        "simple_explanation": "When you have independent tasks (e.g. searching 5 websites or processing 10 chapters), running them sequentially is slow. LangGraph supports static parallel branching and dynamic map-reduce with `Send(node_name, node_input_state)`.",
        "why_it_matters": "`Send()` lets your graph fan out dynamically based on runtime data (e.g. generating 3 sub-queries or 20 summary chunks) and fan back in cleanly to a single aggregator node.",
        "real_world_analogy": "A manager (router) assigns 3 distinct research topics to 3 analysts (parallel worker nodes). When all 3 finish their reports, the editor (aggregator node) compiles them into the final publication.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Start([START]) --> Planner[Generate Topics Node]\n  Planner -- Send() --> W1[Worker: Topic 1]\n  Planner -- Send() --> W2[Worker: Topic 2]\n  Planner -- Send() --> W3[Worker: Topic 3]\n  W1 --> Aggregator[Aggregator Node]\n  W2 --> Aggregator\n  W3 --> Aggregator\n  Aggregator --> End([END])"
        },
        "code_example": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.types import Send

# 1. Overall Graph State
class MapReduceState(TypedDict):
    subjects: list[str]
    summaries: Annotated[list[str], operator.add]

# 2. Worker node state schema
class WorkerState(TypedDict):
    subject: str

def generate_topics(state: MapReduceState) -> dict:
    return {"subjects": ["Quantum Computing", "Neuromorphic Chips", "Photonics"]}

# Conditional router that returns dynamic Send() objects
def fan_out_topics(state: MapReduceState) -> list[Send]:
    return [Send("research_worker", {"subject": s}) for s in state["subjects"]]

def research_worker(state: WorkerState) -> dict:
    # Executes in parallel for each item
    return {"summaries": [f"Deep dive research completed for {state['subject']}"]}

def aggregate_report(state: MapReduceState) -> dict:
    total = len(state["summaries"])
    return {"summaries": [f"=== EXECUTIVE SUMMARY: {total} TOPICS COMPILED ==="]}

builder = StateGraph(MapReduceState)
builder.add_node("generate_topics", generate_topics)
builder.add_node("research_worker", research_worker)
builder.add_node("aggregate_report", aggregate_report)

builder.add_edge(START, "generate_topics")
builder.add_conditional_edges("generate_topics", fan_out_topics, ["research_worker"])
builder.add_edge("research_worker", "aggregate_report")
builder.add_edge("aggregate_report", END)

app = builder.compile()
out = app.invoke({"subjects": [], "summaries": []})
for item in out["summaries"]:
    print(item)""",
        "line_by_line": [
            {"line": "from langgraph.types import Send", "explanation": "Imports the modern Send primitive for dynamic parallel routing."},
            {"line": "return [Send('research_worker', {'subject': s}) for s in state['subjects']]", "explanation": "Dispatches multiple instances of research_worker in parallel, each with custom worker state."},
            {"line": "builder.add_edge('research_worker', 'aggregate_report')", "explanation": "Automatically fans in all parallel worker executions before aggregate_report runs."}
        ],
        "sample_input": {"subjects": [], "summaries": []},
        "sample_output": {
            "summaries": [
                "Deep dive research completed for Quantum Computing",
                "Deep dive research completed for Neuromorphic Chips",
                "Deep dive research completed for Photonics",
                "=== EXECUTIVE SUMMARY: 3 TOPICS COMPILED ==="
            ]
        },
        "common_mistakes": [
            {"mistake": "Failing to define an Annotated reducer on the output aggregation list in parent state.", "fix": "Always use `Annotated[list, operator.add]` for fields receiving parallel worker updates."}
        ],
        "hands_on_task": {
            "title": "Add a 4th subject dynamically",
            "instruction": "Add 'DNA Data Storage' to the subjects list and observe 4 parallel executions.",
            "starter_code": "return {'subjects': ['Quantum Computing', 'Neuromorphic Chips', 'Photonics', 'DNA Storage']}"
        },
        "quick_quiz": [
            {
                "question": "What is the primary purpose of the `Send` API in LangGraph?",
                "options": [
                    "To send emails to human reviewers",
                    "To dynamically spawn parallel node executions (map-reduce) with custom payloads",
                    "To send HTTP POST requests to an external API",
                    "To terminate the graph prematurely"
                ],
                "correct_index": 1,
                "explanation": "Send allows conditional edges to dynamically map over lists of varying lengths and trigger concurrent worker nodes in the same super-step."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m4-l2",
        "next_lesson_id": "m4-l4"
    },
    "m4-l4": {
        "id": "m4-l4",
        "module_id": "module-4",
        "module_title": "Module 4: Routing, Branching & Loops",
        "title": "Command API: Combined State Updates & Routing",
        "difficulty": "Intermediate",
        "estimated_minutes": 15,
        "prerequisites": ["m4-l1"],
        "objectives": [
            "Use Command(update=..., goto=...) in modern LangGraph 0.2+",
            "Perform state updates and control flow routing in a single node return",
            "Replace complex conditional edge setups with clean Command returns"
        ],
        "simple_explanation": "Traditionally in LangGraph, a node updates state, and a separate conditional edge decides where to go next. The `Command` API combines both: a node can return `Command(update={'status': 'ok'}, goto='next_node')` to update state and command the graph's next move simultaneously.",
        "why_it_matters": "Command reduces boilerplate, eliminates the need for separate routing functions for simple branches, and makes multi-agent handoffs much cleaner.",
        "real_world_analogy": "Like a project lead who hands you a completed document (update) while explicitly telling you: 'Take this directly to legal for review' (goto).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  NodeA[Node A: Evaluates Data] -- \"Command(update={...}, goto='NodeC')\" --> NodeC[Node C]\n  NodeA -. Direct bypass .- NodeB[Node B]"
        },
        "code_example": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END
from langgraph.types import Command

class OrderState(TypedDict):
    order_id: str
    amount: float
    status: str

def check_fraud_node(state: OrderState) -> Command[Literal["flag_fraud", "process_payment"]]:
    amt = state["amount"]
    if amt > 10000:
        # High risk -> Update status and route to flag_fraud
        return Command(
            update={"status": "FLAGGED_FOR_REVIEW"},
            goto="flag_fraud"
        )
    # Low risk -> Update status and route to process_payment
    return Command(
        update={"status": "APPROVED_AUTOMATICALLY"},
        goto="process_payment"
    )

def flag_fraud(state: OrderState) -> dict:
    return {"status": "HOLD: Escalated to Fraud Prevention Team"}

def process_payment(state: OrderState) -> dict:
    return {"status": f"SUCCESS: Charged ${state['amount']}"}

builder = StateGraph(OrderState)
builder.add_node("check_fraud", check_fraud_node)
builder.add_node("flag_fraud", flag_fraud)
builder.add_node("process_payment", process_payment)

builder.add_edge(START, "check_fraud")
builder.add_edge("flag_fraud", END)
builder.add_edge("process_payment", END)

app = builder.compile()
print("High value order:", app.invoke({"order_id": "ORD-1", "amount": 15000.0, "status": ""}))
print("Normal order:", app.invoke({"order_id": "ORD-2", "amount": 49.99, "status": ""}))""",
        "line_by_line": [
            {"line": "from langgraph.types import Command", "explanation": "Imports Command from langgraph.types."},
            {"line": "return Command(update={'status': 'APPROVED_AUTOMATICALLY'}, goto='process_payment')", "explanation": "Returns both the dictionary state update and the target node destination in one atomic object."}
        ],
        "sample_input": {"order_id": "ORD-1", "amount": 15000.0, "status": ""},
        "sample_output": {"order_id": "ORD-1", "amount": 15000.0, "status": "HOLD: Escalated to Fraud Prevention Team"},
        "common_mistakes": [
            {"mistake": "Adding a normal add_edge from a node that returns Command with a goto destination.", "fix": "Do not create conflicting static edges from nodes that use Command(goto=...)."}
        ],
        "hands_on_task": {
            "title": "Use goto=END directly",
            "instruction": "Modify check_fraud_node to return `goto=END` directly if amount == 0.",
            "starter_code": "if state['amount'] == 0: return Command(update={'status': 'FREE_ORDER'}, goto=END)"
        },
        "quick_quiz": [
            {
                "question": "What two things does a `Command` object specify in a node return?",
                "options": [
                    "A SQL query and a database password",
                    "A state update dictionary and the next destination node (goto)",
                    "A Python package and a virtual environment path",
                    "A port number and a host address"
                ],
                "correct_index": 1,
                "explanation": "Command(update=..., goto=...) allows a node to atomically emit state updates and dynamically dictate the next node destination."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m4-l3",
        "next_lesson_id": "m5-l1"
    }
}
