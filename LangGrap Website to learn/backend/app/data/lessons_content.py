# Complete detailed lesson contents for all 14 modules
from typing import Dict, Any

LESSONS_CONTENT: Dict[str, Dict[str, Any]] = {
    "m1-l1": {
        "id": "m1-l1",
        "module_id": "module-1",
        "module_title": "Module 1: Foundations & Architecture",
        "title": "What is LangGraph & Why Does It Exist?",
        "difficulty": "Beginner",
        "estimated_minutes": 10,
        "prerequisites": ["Python basics (functions, dicts, type hints)"],
        "objectives": [
            "Understand the fundamental limitation of linear LLM chains (DAGs)",
            "Learn what makes a system 'agentic' (cycles, memory, decision branches)",
            "Understand how LangGraph models computation as nodes and edges over shared state"
        ],
        "simple_explanation": "LangGraph is a library for building stateful, multi-actor applications with LLMs. While traditional pipelines execute in a straight line (step 1 -> step 2 -> step 3), real problem solving requires loops: taking an action, checking the result, deciding to try again or take a different path, and maintaining a memory of everything that happened.",
        "why_it_matters": "Simple chains break when an LLM produces an error or needs tool iterations. With LangGraph, you gain fine-grained control over loops, human approvals, error recovery, and persistence without writing messy custom while-loops.",
        "real_world_analogy": "Imagine a chef preparing a complex recipe. A linear chain is like blindly following 5 steps without tasting the food. LangGraph is like a chef who tastes the soup (evaluates state), decides if more salt is needed (conditional edge), stirs again (cycle/loop), and only serves the dish when it meets the standard (END node).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  START([START]) --> Plan[Plan Recipe]\n  Plan --> Cook[Cook & Season]\n  Cook --> Taste{Taste Test}\n  Taste -- Needs Adjustment --> Cook\n  Taste -- Delicious --> Serve[Serve Dish]\n  Serve --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Define the state schema
class ChefState(TypedDict):
    soup_quality: int
    tastes_taken: int
    verdict: str

# 2. Define node functions
def cook_and_season(state: ChefState) -> dict:
    current_quality = state.get("soup_quality", 50)
    return {"soup_quality": current_quality + 20, "tastes_taken": state.get("tastes_taken", 0) + 1}

def decide_next_step(state: ChefState) -> str:
    if state["soup_quality"] >= 90 or state["tastes_taken"] >= 3:
        return "serve"
    return "adjust_seasoning"

def serve_dish(state: ChefState) -> dict:
    return {"verdict": f"Served premium soup with quality score {state['soup_quality']}/100!"}

# 3. Construct the StateGraph
builder = StateGraph(ChefState)
builder.add_node("cook", cook_and_season)
builder.add_node("serve", serve_dish)

builder.add_edge(START, "cook")
builder.add_conditional_edges("cook", decide_next_step, {
    "adjust_seasoning": "cook",
    "serve": "serve"
})
builder.add_edge("serve", END)

# 4. Compile and invoke
app = builder.compile()
result = app.invoke({"soup_quality": 40, "tastes_taken": 0, "verdict": ""})
print(result)""",
        "line_by_line": [
            {"line": "class ChefState(TypedDict):", "explanation": "Defines the shape and types of the shared data dictionary that flows across all graph nodes."},
            {"line": "def cook_and_season(state: ChefState) -> dict:", "explanation": "A node function receives current state and returns a dictionary with state updates."},
            {"line": "builder = StateGraph(ChefState)", "explanation": "Initializes the graph builder parameterized with our state structure."},
            {"line": "builder.add_conditional_edges('cook', decide_next_step, ...)", "explanation": "Routes execution dynamically based on the string returned by decide_next_step."},
            {"line": "app = builder.compile()", "explanation": "Validates graph topology and builds the runnable Pregel engine."}
        ],
        "sample_input": {"soup_quality": 40, "tastes_taken": 0, "verdict": ""},
        "sample_output": {
            "soup_quality": 100,
            "tastes_taken": 3,
            "verdict": "Served premium soup with quality score 100/100!"
        },
        "common_mistakes": [
            {"mistake": "Mutating state directly in-place: state['soup_quality'] += 20 without returning a dictionary.", "fix": "Always return a dictionary containing the updated keys: return {'soup_quality': state['soup_quality'] + 20}."},
            {"mistake": "Creating an infinite loop by forgetting a loop boundary / termination condition.", "fix": "Always include a max iteration count or boundary check in conditional routing functions."}
        ],
        "hands_on_task": {
            "title": "Add a secret ingredient node",
            "instruction": "Create a new node 'add_secret_spice' that increases soup_quality by 35 immediately if tastes_taken == 2.",
            "starter_code": "def add_secret_spice(state: ChefState) -> dict:\n    # Return state update here\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What primary capability does LangGraph add over traditional linear LCEL chains?",
                "options": [
                    "It makes LLM tokens stream faster in the browser",
                    "It enables cyclical graph execution, persistent state, and human-in-the-loop controls",
                    "It replaces Python with a custom scripting language",
                    "It only works with OpenAI models"
                ],
                "correct_index": 1,
                "explanation": "LangGraph is designed specifically for cyclical graphs (loops), state management across steps, checkpointing, and dynamic human-in-the-loop interactions."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "prev_lesson_id": None,
        "next_lesson_id": "m1-l2"
    },
    "m1-l2": {
        "id": "m1-l2",
        "module_id": "module-1",
        "module_title": "Module 1: Foundations & Architecture",
        "title": "LangGraph vs LangChain & Other Frameworks",
        "difficulty": "Beginner",
        "estimated_minutes": 12,
        "prerequisites": ["m1-l1"],
        "objectives": [
            "Differentiate LCEL (DAGs) from LangGraph (cyclic state machines)",
            "Compare LangGraph with CrewAI and AutoGen",
            "Identify when a graph architecture is warranted vs when plain Python suffices"
        ],
        "simple_explanation": "LangChain's LCEL was built for Directed Acyclic Graphs (DAGs)—one-way data pipelines. LangGraph was created to support loops, branching, persistence, and multi-agent coordination with full inspectability.",
        "why_it_matters": "Knowing when NOT to use LangGraph is just as important as knowing how to use it. For a simple prompt + LLM + parser chain, standard LCEL or plain Python is faster and lighter. For multi-turn reasoning, tool loops, or human approvals, LangGraph is the right tool.",
        "real_world_analogy": "LCEL is like a factory assembly line: item goes in, gets stamped, painted, and boxed in one direction. LangGraph is like an interactive design workshop: team members review blueprints, test prototypes, iterate based on feedback, and pause for client sign-off.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TB\n  subgraph LCEL[LCEL: Linear Pipeline]\n    P1[Prompt] --> M1[Model] --> O1[Parser]\n  end\n  subgraph LG[LangGraph: Cyclical Multi-Actor]\n    Start[User Input] --> Plan[Planner Node]\n    Plan --> Action[Tool Execution]\n    Action --> Eval{Evaluation}\n    Eval -- Retry --> Plan\n    Eval -- Approved --> End[Response]\n  end"
        },
        "code_example": """# Comparing standard Python logic vs LangGraph state machine
# In plain Python, managing loops with checkpointing and human interrupts requires hundreds of lines of boilerplate.
# In LangGraph, state and transitions are first-class citizens:

from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class TriageState(TypedDict):
    ticket_text: str
    urgency: str
    department: str

def analyze_ticket(state: TriageState) -> dict:
    text = state["ticket_text"].lower()
    urgency = "HIGH" if "urgent" in text or "down" in text else "NORMAL"
    return {"urgency": urgency}

def route_department(state: TriageState) -> str:
    if "billing" in state["ticket_text"].lower():
        return "billing_team"
    return "tech_support"

def billing_handler(state: TriageState) -> dict:
    return {"department": "Billing & Invoicing"}

def tech_handler(state: TriageState) -> dict:
    return {"department": "Engineering Support"}

builder = StateGraph(TriageState)
builder.add_node("analyze", analyze_ticket)
builder.add_node("billing_team", billing_handler)
builder.add_node("tech_support", tech_handler)

builder.add_edge(START, "analyze")
builder.add_conditional_edges("analyze", route_department)
builder.add_edge("billing_team", END)
builder.add_edge("tech_support", END)

app = builder.compile()
print(app.invoke({"ticket_text": "Our payment failed and server is urgent", "urgency": "", "department": ""}))""",
        "line_by_line": [
            {"line": "builder.add_conditional_edges('analyze', route_department)", "explanation": "Routes to the exact node name returned by route_department string return value."},
            {"line": "builder.add_edge('billing_team', END)", "explanation": "Directs terminal execution to the special END marker."}
        ],
        "sample_input": {"ticket_text": "Payment failed for invoice #442", "urgency": "", "department": ""},
        "sample_output": {"ticket_text": "Payment failed for invoice #442", "urgency": "NORMAL", "department": "Billing & Invoicing"},
        "common_mistakes": [
            {"mistake": "Using LangGraph for a simple 1-step prompt formatting call.", "fix": "Use standard function calls or LCEL for trivial 1-step transformations without state or cycles."}
        ],
        "hands_on_task": {
            "title": "Add an Escalation Node",
            "instruction": "Route to an 'escalations_team' node if urgency is 'HIGH' regardless of department.",
            "starter_code": "def route_department(state: TriageState) -> str:\n    # Add high-urgency branch check\n    pass"
        },
        "quick_quiz": [
            {
                "question": "When should you prefer LangGraph over a basic linear LLM chain?",
                "options": [
                    "Whenever you only need a single LLM call with a static prompt template",
                    "When your workflow requires multi-step loops, state persistence, conditional branching, or human approval",
                    "Only when you want to avoid writing Python code",
                    "When you do not want to use any LLM models"
                ],
                "correct_index": 1,
                "explanation": "LangGraph shines when applications require cyclical execution, memory across super-steps, branch decisioning, and human-in-the-loop workflows."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "prev_lesson_id": "m1-l1",
        "next_lesson_id": "m1-l3"
    },
    "m1-l3": {
        "id": "m1-l3",
        "module_id": "module-1",
        "module_title": "Module 1: Foundations & Architecture",
        "title": "Core Mental Model & Pregel Orchestration",
        "difficulty": "Beginner",
        "estimated_minutes": 15,
        "prerequisites": ["m1-l1"],
        "objectives": [
            "Understand the Pregel actor-oriented computation model",
            "Understand what a 'super-step' is",
            "Learn how state channels synchronize parallel node executions"
        ],
        "simple_explanation": "LangGraph is powered by Pregel, a distributed graph computing architecture. Computation happens in discrete rounds called 'super-steps'. In each super-step, active nodes read state, execute their logic concurrently, and send updates to state channels. At the end of the super-step, all updates are merged atomically before the next round begins.",
        "why_it_matters": "Understanding super-steps prevents race conditions when multiple nodes execute in parallel and clarifies exactly when state changes become visible to downstream nodes.",
        "real_world_analogy": "Think of a board game round: All players look at the board (read state), plan and submit their moves simultaneously during their turn (nodes execute), and the referee updates all scores and pieces before the next turn starts (super-step synchronization barrier).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "sequenceDiagram\n  autonumber\n  participant State as State Channels\n  participant N1 as Node A\n  participant N2 as Node B\n  Note over State,N2: Super-Step 1 Begins\n  State->>N1: Read current state snapshot\n  State->>N2: Read current state snapshot\n  N1->>N1: Execute logic\n  N2->>N2: Execute logic\n  N1-->>State: Write partial update A\n  N2-->>State: Write partial update B\n  Note over State: Reducers merge updates atomically\n  Note over State,N2: Super-Step 1 Ends -> Super-Step 2 Begins"
        },
        "code_example": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

# State with parallel list reducer
class ResearchState(TypedDict):
    query: str
    findings: Annotated[list[str], operator.add]

def search_academic_papers(state: ResearchState) -> dict:
    return {"findings": [f"Academic result for: {state['query']}"]}

def search_industry_blogs(state: ResearchState) -> dict:
    return {"findings": [f"Industry blog post for: {state['query']}"]}

def synthesize(state: ResearchState) -> dict:
    total = len(state["findings"])
    return {"findings": [f"Synthesized {total} sources successfully."]}

builder = StateGraph(ResearchState)
builder.add_node("academic", search_academic_papers)
builder.add_node("industry", search_industry_blogs)
builder.add_node("synthesizer", synthesize)

# Both academic and industry run in parallel during Super-Step 1
builder.add_edge(START, "academic")
builder.add_edge(START, "industry")

# Both fan-in to synthesizer for Super-Step 2
builder.add_edge("academic", "synthesizer")
builder.add_edge("industry", "synthesizer")
builder.add_edge("synthesizer", END)

app = builder.compile()
output = app.invoke({"query": "LangGraph Pregel Engine", "findings": []})
for finding in output["findings"]:
    print("-", finding)""",
        "line_by_line": [
            {"line": "findings: Annotated[list[str], operator.add]", "explanation": "Annotated reducer ensures parallel writes from academic and industry nodes append to the list rather than overwriting each other."},
            {"line": "builder.add_edge(START, 'academic')", "explanation": "Schedules academic node for execution in Super-step 1."},
            {"line": "builder.add_edge(START, 'industry')", "explanation": "Schedules industry node in the same Super-step 1 concurrently."}
        ],
        "sample_input": {"query": "LangGraph Pregel Engine", "findings": []},
        "sample_output": {
            "query": "LangGraph Pregel Engine",
            "findings": [
                "Academic result for: LangGraph Pregel Engine",
                "Industry blog post for: LangGraph Pregel Engine",
                "Synthesized 2 sources successfully."
            ]
        },
        "common_mistakes": [
            {"mistake": "Expecting a node to see state changes made by another node in the exact same super-step.", "fix": "Remember that nodes within the same super-step only see the state snapshot from the START of that super-step. Use sequential edges if Node B depends on Node A's output."}
        ],
        "hands_on_task": {
            "title": "Add a news search node",
            "instruction": "Add a third parallel node 'search_news' connected to START and flowing into 'synthesizer'.",
            "starter_code": "def search_news(state: ResearchState) -> dict:\n    # Return news findings list\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What happens during a Pregel super-step synchronization barrier?",
                "options": [
                    "The Python virtual machine restarts",
                    "All pending node writes are applied atomically using configured reducers before next super-step nodes run",
                    "An LLM evaluates if the code is syntactically valid",
                    "All previous memory is wiped clean"
                ],
                "correct_index": 1,
                "explanation": "At the end of each super-step, LangGraph applies all node returns to state channels through reducers, producing a new state snapshot for the next super-step."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "prev_lesson_id": "m1-l2",
        "next_lesson_id": "m2-l1"
    },
    "m2-l1": {
        "id": "m2-l1",
        "module_id": "module-2",
        "module_title": "Module 2: Graph Fundamentals",
        "title": "StateGraph, TypedDict State & START/END",
        "difficulty": "Beginner",
        "estimated_minutes": 15,
        "prerequisites": ["m1-l1"],
        "objectives": [
            "Construct a StateGraph with explicit state typing",
            "Understand the special START and END virtual nodes",
            "Compile and invoke a working baseline graph"
        ],
        "simple_explanation": "A StateGraph is the core class in LangGraph. You define a Python TypedDict that represents your shared state. You then register nodes (functions) and edges (transitions) between START, your nodes, and END.",
        "why_it_matters": "START and END define the entry and exit boundaries of your graph. Explicit typing ensures your node functions have clear contracts and prevents undefined key errors.",
        "real_world_analogy": "Think of START as the reception desk where a customer enters and gets an intake form (initial state), the nodes as different specialist offices, and END as the checkout exit.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  START([START]) --> StepA[Step A: Clean Input]\n  StepA --> StepB[Step B: Enrich Data]\n  StepB --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Define state structure
class WorkflowState(TypedDict):
    raw_input: str
    cleaned_input: str
    word_count: int

def clean_text_node(state: WorkflowState) -> dict:
    cleaned = state["raw_input"].strip().lower()
    return {"cleaned_input": cleaned}

def count_words_node(state: WorkflowState) -> dict:
    words = len(state["cleaned_input"].split())
    return {"word_count": words}

# Instantiate StateGraph with TypedDict
builder = StateGraph(WorkflowState)

# Register nodes
builder.add_node("clean_text", clean_text_node)
builder.add_node("count_words", count_words_node)

# Connect edges from START to clean_text -> count_words -> END
builder.add_edge(START, "clean_text")
builder.add_edge("clean_text", "count_words")
builder.add_edge("count_words", END)

# Compile into executable Runnable
graph = builder.compile()

# Invoke
initial_state = {"raw_input": "  Master LangGraph 0.2 with GraphLab!  ", "cleaned_input": "", "word_count": 0}
final_state = graph.invoke(initial_state)
print("Result:", final_state)""",
        "line_by_line": [
            {"line": "from langgraph.graph import StateGraph, START, END", "explanation": "Imports the primary graph builder and virtual entry/exit node identifiers."},
            {"line": "builder = StateGraph(WorkflowState)", "explanation": "Initializes the StateGraph specifying WorkflowState as the schema."},
            {"line": "builder.add_edge(START, 'clean_text')", "explanation": "Directs incoming graph inputs directly to the clean_text node."},
            {"line": "graph = builder.compile()", "explanation": "Validates connectivity (e.g. no disconnected components) and returns a runnable Pregel instance."}
        ],
        "sample_input": {"raw_input": "  Hello World  ", "cleaned_input": "", "word_count": 0},
        "sample_output": {"raw_input": "  Hello World  ", "cleaned_input": "hello world", "word_count": 2},
        "common_mistakes": [
            {"mistake": "Using strings 'START' and 'END' instead of importing START and END objects.", "fix": "Always import and use `from langgraph.graph import START, END`."}
        ],
        "hands_on_task": {
            "title": "Add an uppercase formatter node",
            "instruction": "Add a node 'format_caps' between clean_text and count_words that capitalizes every word.",
            "starter_code": "def format_caps(state: WorkflowState) -> dict:\n    # Update cleaned_input with .title()\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What is the purpose of graph.compile()?",
                "options": [
                    "It compiles Python into C++ for speed",
                    "It validates the node connections and returns an executable Runnable instance",
                    "It sends your state graph to cloud servers",
                    "It converts your graph into an HTML diagram only"
                ],
                "correct_index": 1,
                "explanation": "compile() performs static validation on your nodes and edges, ensuring proper channel routing, and produces a runnable LangGraph instance."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m1-l3",
        "next_lesson_id": "m2-l2"
    },
    "m2-l2": {
        "id": "m2-l2",
        "module_id": "module-2",
        "module_title": "Module 2: Graph Fundamentals",
        "title": "Node Functions & State Transitions",
        "difficulty": "Beginner",
        "estimated_minutes": 15,
        "prerequisites": ["m2-l1"],
        "objectives": [
            "Write robust node functions conforming to the LangGraph node contract",
            "Understand partial dictionary returns vs full state replacement",
            "Handle runtime configurations (RunnableConfig) in nodes"
        ],
        "simple_explanation": "In LangGraph, a node is simply any Python function (sync or async) that takes the current state as its first argument and returns a dictionary. You only need to return the specific keys you wish to update or add.",
        "why_it_matters": "Because nodes only return partial dicts, multiple nodes can touch different parts of state without trampling on each other's data.",
        "real_world_analogy": "Imagine a shared patient chart at a clinic. The triage nurse updates temperature and blood pressure, the doctor adds a diagnosis, and the pharmacist adds prescription notes. Nobody needs to rewrite the whole chart—just their section.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  InState[State Snapshot: {a: 1, b: 'hi'}] --> NodeFn[Node Function]\n  NodeFn -- Returns {b: 'hello'} --> Reducer[Channel Merge]\n  Reducer --> OutState[New State: {a: 1, b: 'hello'}]"
        },
        "code_example": """from typing import TypedDict
from langchain_core.runnables import RunnableConfig
from langgraph.graph import StateGraph, START, END

class PatientState(TypedDict):
    patient_id: str
    symptoms: list[str]
    temperature_f: float
    status: str

def triage_node(state: PatientState, config: RunnableConfig) -> dict:
    # Nodes can optionally receive config to access tags, metadata, or run_id
    tags = config.get("tags", [])
    print(f"Executing triage with tags: {tags}")
    
    temp = state["temperature_f"]
    status = "CRITICAL" if temp > 103.0 else "STABLE"
    # Return only the modified status key
    return {"status": status}

builder = StateGraph(PatientState)
builder.add_node("triage", triage_node)
builder.add_edge(START, "triage")
builder.add_edge("triage", END)

app = builder.compile()
res = app.invoke(
    {"patient_id": "PX-901", "symptoms": ["fever", "cough"], "temperature_f": 104.2, "status": "UNKNOWN"},
    config={"tags": ["emergency-room"]}
)
print("Final State:", res)""",
        "line_by_line": [
            {"line": "def triage_node(state: PatientState, config: RunnableConfig) -> dict:", "explanation": "LangGraph automatically injects the optional RunnableConfig if declared in the parameter list."},
            {"line": "return {'status': status}", "explanation": "Returns only the 'status' key update. 'patient_id', 'symptoms', and 'temperature_f' remain intact in state."}
        ],
        "sample_input": {"patient_id": "PX-901", "symptoms": ["fever"], "temperature_f": 104.2, "status": "UNKNOWN"},
        "sample_output": {"patient_id": "PX-901", "symptoms": ["fever"], "temperature_f": 104.2, "status": "CRITICAL"},
        "common_mistakes": [
            {"mistake": "Returning a non-dict value from a node (e.g., return 'DONE' or return 42).", "fix": "Nodes in StateGraph must always return a dictionary (or Command object)."}
        ],
        "hands_on_task": {
            "title": "Add symptoms logger",
            "instruction": "Create a node that appends 'evaluated_by_triage' to the symptoms list.",
            "starter_code": "def log_symptom(state: PatientState) -> dict:\n    # Update symptoms list\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What must a standard StateGraph node function return?",
                "options": [
                    "A boolean True/False indicating success",
                    "A dictionary with state updates or a Command object",
                    "The entire state TypedDict with all original keys",
                    "An instance of StateGraph"
                ],
                "correct_index": 1,
                "explanation": "Nodes return a dictionary of partial updates (or a Command object) containing only the keys that were modified or added."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m2-l1",
        "next_lesson_id": "m2-l3"
    },
    "m2-l3": {
        "id": "m2-l3",
        "module_id": "module-2",
        "module_title": "Module 2: Graph Fundamentals",
        "title": "Graph Invocations: invoke(), ainvoke() & stream()",
        "difficulty": "Beginner",
        "estimated_minutes": 18,
        "prerequisites": ["m2-l2"],
        "objectives": [
            "Use synchronous invoke() vs async ainvoke()",
            "Inspect step-by-step state emissions with stream()",
            "Understand different stream return formats"
        ],
        "simple_explanation": "Compiled LangGraph apps are standard LangChain Runnables. You can execute them in one shot with `invoke()`, run them non-blocking with `ainvoke()`, or iterate over incremental node updates with `stream()`.",
        "why_it_matters": "Streaming is crucial for user interfaces. Instead of waiting 10 seconds for the entire graph to finish, `stream()` lets you update visual progress bars and UI nodes in real time as each super-step completes.",
        "real_world_analogy": "Like package delivery tracking: `invoke()` is only knowing when the box arrives at your door. `stream()` is real-time GPS tracking showing every depot the package passes through.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "sequenceDiagram\n  participant Client\n  participant Graph\n  Client->>Graph: app.stream(input_state)\n  Graph-->>Client: Chunk 1: {'node_a': {'count': 1}}\n  Graph-->>Client: Chunk 2: {'node_b': {'count': 2}}\n  Graph-->>Client: Chunk 3: {'node_c': {'final': 'done'}}"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class CounterState(TypedDict):
    count: int
    history: list[str]

def step_one(state: CounterState) -> dict:
    return {"count": state["count"] + 1, "history": state["history"] + ["step_one"]}

def step_two(state: CounterState) -> dict:
    return {"count": state["count"] * 2, "history": state["history"] + ["step_two"]}

builder = StateGraph(CounterState)
builder.add_node("step_one", step_one)
builder.add_node("step_two", step_two)

builder.add_edge(START, "step_one")
builder.add_edge("step_one", "step_two")
builder.add_edge("step_two", END)

app = builder.compile()

# 1. Full invoke
print("--- INVOKE RESULT ---")
res = app.invoke({"count": 5, "history": []})
print(res)

# 2. Step-by-step streaming
print("\\n--- STREAMING CHUNKS ---")
for chunk in app.stream({"count": 10, "history": []}):
    print("Emitted step:", chunk)""",
        "line_by_line": [
            {"line": "for chunk in app.stream(...):", "explanation": "Yields a dictionary where keys are executing node names and values are their state updates for each super-step."},
            {"line": "app.invoke(...)", "explanation": "Runs all super-steps to completion and returns the final merged state dictionary."}
        ],
        "sample_input": {"count": 10, "history": []},
        "sample_output": {
            "step_one": {"count": 11, "history": ["step_one"]},
            "step_two": {"count": 22, "history": ["step_one", "step_two"]}
        },
        "common_mistakes": [
            {"mistake": "Trying to run async code inside sync invoke() without an async event loop.", "fix": "Use `await app.ainvoke(...)` or `async for event in app.astream(...)` in async environments like FastAPI."}
        ],
        "hands_on_task": {
            "title": "Stream values mode",
            "instruction": "Test `app.stream(..., stream_mode='values')` to see complete state values instead of node updates.",
            "starter_code": "for value_snapshot in app.stream({'count': 1, 'history': []}, stream_mode='values'):\n    print(value_snapshot)"
        },
        "quick_quiz": [
            {
                "question": "By default, what does app.stream(input) yield at each iteration?",
                "options": [
                    "A string containing the raw Python code",
                    "A dict mapping the node name that just executed to its returned update",
                    "Only the final state when the graph finishes",
                    "A websocket connection object"
                ],
                "correct_index": 1,
                "explanation": "Default stream_mode='updates' yields {node_name: {updated_keys}} for each completed node execution."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/streaming",
        "prev_lesson_id": "m2-l2",
        "next_lesson_id": "m3-l1"
    }
}
