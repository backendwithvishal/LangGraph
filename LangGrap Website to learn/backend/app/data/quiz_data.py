# Practice and Quiz Center Questions
from typing import List, Dict, Any, Optional

QUIZ_QUESTIONS: List[Dict[str, Any]] = [
    {
        "id": "q1",
        "category": "Foundations",
        "type": "mcq",
        "difficulty": "Beginner",
        "topic_id": "module-1",
        "question": "Why is LangGraph built as a cyclical graph engine rather than a linear DAG (Directed Acyclic Graph)?",
        "code_snippet": None,
        "options": [
            "Because Python does not support linear pipelines",
            "Because real-world agentic reasoning requires iterative loops, self-correction, and state persistence",
            "To prevent the use of chat models",
            "To automatically convert Python into JavaScript"
        ],
        "correct_answer": 1,
        "hint": "Think about what happens when an agent makes a mistake and needs to retry or execute another tool.",
        "explanation": "Linear DAGs cannot cycle backwards. Agentic workflows require loops for trial-and-error, tool iterations, reflection, and human reviews—which cyclical graphs enable natively."
    },
    {
        "id": "q2",
        "category": "State Management",
        "type": "predict_output",
        "difficulty": "Intermediate",
        "topic_id": "module-3",
        "question": "What will `result['tags']` contain after the following graph finishes execution?",
        "code_snippet": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class MyState(TypedDict):
    tags: Annotated[list[str], operator.add]

def node_a(state: MyState) -> dict:
    return {"tags": ["AI"]}

def node_b(state: MyState) -> dict:
    return {"tags": ["Graph", "Agent"]}

builder = StateGraph(MyState)
builder.add_node("a", node_a)
builder.add_node("b", node_b)
builder.add_edge(START, "a")
builder.add_edge("a", "b")
builder.add_edge("b", END)

app = builder.compile()
result = app.invoke({"tags": ["Init"]})""",
        "options": [
            "['Graph', 'Agent']",
            "['Init', 'AI', 'Graph', 'Agent']",
            "['AI', 'Graph', 'Agent']",
            "An InvalidUpdateError is raised"
        ],
        "correct_answer": 1,
        "hint": "Look closely at `Annotated[list[str], operator.add]` and the initial state `{'tags': ['Init']}`.",
        "explanation": "Because `tags` has the `operator.add` reducer, each node appends its list to the existing state: ['Init'] + ['AI'] + ['Graph', 'Agent'] = ['Init', 'AI', 'Graph', 'Agent']."
    },
    {
        "id": "q3",
        "category": "Debugging",
        "type": "bug_hunter",
        "difficulty": "Intermediate",
        "topic_id": "module-2",
        "question": "Identify the bug in the following node definition that causes state updates to fail:",
        "code_snippet": """class AppState(TypedDict):
    score: int
    feedback: str

def calculate_score_node(state: AppState) -> dict:
    # BUG HERE:
    state["score"] += 10
    state["feedback"] = "Good job"
    return None""",
        "options": [
            "Node functions cannot use type hints",
            "The function mutates `state` in-place and returns `None` instead of returning a dictionary of updates",
            "The function name contains underscores",
            "AppState must inherit from Pydantic BaseModel only"
        ],
        "correct_answer": 1,
        "hint": "In LangGraph, node functions must return a dictionary (or Command) containing only the keys they want to update.",
        "explanation": "LangGraph relies on immutable state updates. Nodes should not mutate the incoming state dict directly; they must return a new dictionary: `return {'score': state['score'] + 10, 'feedback': 'Good job'}`."
    },
    {
        "id": "q4",
        "category": "Routing",
        "type": "routing",
        "difficulty": "Intermediate",
        "topic_id": "module-4",
        "question": "Which edge setup correctly implements dynamic conditional routing from 'evaluator' to either 'retry' or END?",
        "code_snippet": """def check_verdict(state: State) -> str:
    return "retry" if state["score"] < 70 else "done" """,
        "options": [
            "builder.add_edge('evaluator', check_verdict)",
            "builder.add_conditional_edges('evaluator', check_verdict, {'retry': 'retry', 'done': END})",
            "builder.add_conditional_edges(START, 'evaluator', 'retry')",
            "builder.add_edge('evaluator', END)"
        ],
        "correct_answer": 1,
        "hint": "`add_conditional_edges` takes (source_node, routing_function, path_mapping_dict).",
        "explanation": "`add_conditional_edges('evaluator', check_verdict, {'retry': 'retry', 'done': END})` connects the output of check_verdict to target nodes."
    },
    {
        "id": "q5",
        "category": "Human-in-the-Loop",
        "type": "mcq",
        "difficulty": "Advanced",
        "topic_id": "module-8",
        "question": "When a node invokes `interrupt({'prompt': 'Approve transaction?'})`, what happens to the graph?",
        "code_snippet": None,
        "options": [
            "The process exits with code 1 and destroys all memory",
            "Execution is suspended, a checkpoint is saved, the payload is returned to caller, and execution waits for `Command(resume=...)`",
            "It sleeps for 60 seconds and automatically approves",
            "It deletes the current thread_id"
        ],
        "correct_answer": 1,
        "hint": "Dynamic interrupts provide safe, durable pausing that can be resumed at any future time.",
        "explanation": "interrupt() saves a snapshot to the checkpointer and returns the interrupt payload. The client can resume later by passing Command(resume=value) with the same thread_id."
    },
    {
        "id": "q6",
        "category": "Streaming",
        "type": "predict_output",
        "difficulty": "Advanced",
        "topic_id": "module-9",
        "question": "What is the key difference between `stream_mode='values'` and `stream_mode='updates'`?",
        "code_snippet": None,
        "options": [
            "'values' emits the full state dictionary at each super-step; 'updates' emits only the dictionary returned by the executed node(s)",
            "'values' only streams integers, while 'updates' only streams strings",
            "'updates' does not support async execution",
            "There is no difference"
        ],
        "correct_answer": 0,
        "hint": "Think about what data is yielded after each super-step in each mode.",
        "explanation": "stream_mode='values' emits the entire merged state snapshot at each step, while stream_mode='updates' yields {node_name: {only_modified_keys}}."
    },
    {
        "id": "q7",
        "category": "Persistence",
        "type": "mcq",
        "difficulty": "Advanced",
        "topic_id": "module-7",
        "question": "What is the primary difference between a Checkpointer (e.g. MemorySaver, SqliteSaver) and a Store (e.g. InMemoryStore)?",
        "code_snippet": None,
        "options": [
            "A Checkpointer manages thread-scoped short-term execution snapshots; a Store manages cross-thread long-term memory with hierarchical namespaces",
            "Checkpointers are only for Linux; Stores are for Windows",
            "Stores are deprecated in LangGraph 0.2",
            "Checkpointers only store strings"
        ],
        "correct_answer": 0,
        "hint": "Think about thread_id vs cross-thread user profile data.",
        "explanation": "Checkpointers manage step-by-step state for a specific thread_id session, while BaseStore provides cross-thread key-value storage for long-term user memories and facts."
    },
    {
        "id": "q8",
        "category": "Functional API",
        "type": "bug_hunter",
        "difficulty": "Advanced",
        "topic_id": "module-11",
        "question": "In the LangGraph Functional API, what is missing when calling the `@task` function below?",
        "code_snippet": """@task
def query_vector_db(query: str) -> list[str]:
    return ["Doc A", "Doc B"]

@entrypoint()
def search_pipeline(q: str) -> str:
    # Potential issue here:
    docs = query_vector_db(q)
    return f"Found {len(docs)} documents" """,
        "options": [
            "Nothing, this is 100% correct",
            "Tasks return futures in entrypoints, so `query_vector_db(q).result()` must be called to await the return value",
            "query_vector_db must be written in C++",
            "search_pipeline cannot accept string arguments"
        ],
        "correct_answer": 1,
        "hint": "Remember that @task returns a Future object representing the asynchronous/checkpointed task.",
        "explanation": "In functional workflows, invoking a @task decorated function returns a task Future. To retrieve the result, call `.result()`."
    }
]

def get_all_quizzes() -> List[Dict[str, Any]]:
    return QUIZ_QUESTIONS

def get_quiz_by_id(qid: str) -> Optional[Dict[str, Any]]:
    for q in QUIZ_QUESTIONS:
        if q["id"] == qid:
            return q
    return None
