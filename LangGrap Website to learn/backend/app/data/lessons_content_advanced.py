# Complete detailed lesson contents for Modules 5 through 14
from typing import Dict, Any

ADVANCED_LESSONS: Dict[str, Dict[str, Any]] = {
    "m5-l1": {
        "id": "m5-l1",
        "module_id": "module-5",
        "module_title": "Module 5: Models, Messages & Tool Calling",
        "title": "Tool Binding & ToolNode Integration",
        "difficulty": "Intermediate",
        "estimated_minutes": 18,
        "prerequisites": ["m3-l2", "m4-l1"],
        "objectives": [
            "Define tools with langchain_core.tools @tool",
            "Understand tool schemas, arguments, and tool_call_id matching",
            "Use langgraph.prebuilt.ToolNode to execute tool calls safely"
        ],
        "simple_explanation": "When an LLM decides to use an external capability (like searching a database or calculating numbers), it emits a tool call with arguments and a unique `tool_call_id`. LangGraph's `ToolNode` automatically executes the matching Python tool and packages the result into a `ToolMessage` with the exact corresponding ID.",
        "why_it_matters": "Matching `tool_call_id` is required by LLM providers (Anthropic, OpenAI, Google). If IDs don't match, the model throws a validation error. `ToolNode` handles this automatically.",
        "real_world_analogy": "Like taking a claim ticket at a coat check: the model gives you a ticket (tool_call_id: 'claim-42') asking for a coat (tool: fetch_coat), and ToolNode returns the coat with that exact claim ticket attached so the model knows which request was satisfied.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  AgentNode[Agent Node: Emits tool_calls] --> ToolNode[ToolNode: Executes tools]\n  ToolNode -- Emits ToolMessage(tool_call_id) --> AgentNode\n  AgentNode -- No tool calls --> END([END])"
        },
        "code_example": """from typing import TypedDict, Annotated
from langchain_core.tools import tool
from langchain_core.messages import AIMessage, ToolMessage, HumanMessage
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode

# 1. Define custom tools
@tool
def calculate_compound_interest(principal: float, rate: float, years: int) -> float:
    \"\"\"Calculate compound interest given principal, rate (decimal), and years.\"\"\"
    return round(principal * ((1 + rate) ** years), 2)

@tool
def get_current_stock_price(ticker: str) -> str:
    \"\"\"Get the current stock price for a given ticker symbol.\"\"\"
    mock_prices = {\"AAPL\": \"$230.50\", \"GOOG\": \"$185.20\", \"NVDA\": \"$135.80\"}
    return mock_prices.get(ticker.upper(), \"Ticker not found\")

tools = [calculate_compound_interest, get_current_stock_price]
tool_node = ToolNode(tools)

# 2. Simulate model emitting tool calls
def mock_agent_node(state: MessagesState) -> dict:
    # Model generates tool call request
    ai_call = AIMessage(
        content=\"Let me calculate the compound interest for you.\",
        tool_calls=[{
            \"name\": \"calculate_compound_interest\",
            \"args\": {\"principal\": 10000, \"rate\": 0.08, \"years\": 5},
            \"id\": \"call_abc123\",
            \"type\": \"tool_call\"
        }]
    )
    return {\"messages\": [ai_call]}

builder = StateGraph(MessagesState)
builder.add_node(\"agent\", mock_agent_node)
builder.add_node(\"tools\", tool_node)

builder.add_edge(START, \"agent\")
builder.add_edge(\"agent\", \"tools\")
builder.add_edge(\"tools\", END)

app = builder.compile()
res = app.invoke({\"messages\": [HumanMessage(content=\"Calculate $10,000 at 8% for 5 years\")]})
for msg in res[\"messages\"]:
    print(f\"[{type(msg).__name__}]: {msg.content}\")""",
        "line_by_line": [
            {"line": "from langgraph.prebuilt import ToolNode", "explanation": "Imports the prebuilt node for executing list of tools."},
            {"line": "tool_node = ToolNode(tools)", "explanation": "Initializes ToolNode with registered tools."},
            {"line": "tool_calls=[{'name': '...', 'args': {...}, 'id': '...'}]", "explanation": "The standard schema emitted by tool-calling models containing tool identifier and arguments."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "Calculate $10,000 at 8% for 5 years"}]},
        "sample_output": {
            "messages": [
                {"type": "human", "content": "Calculate $10,000 at 8% for 5 years"},
                {"type": "ai", "content": "Let me calculate the compound interest for you.", "tool_calls": [{"name": "calculate_compound_interest"}]},
                {"type": "tool", "content": "14693.28", "name": "calculate_compound_interest"}
            ]
        },
        "common_mistakes": [
            {"mistake": "Missing docstrings on @tool functions.", "fix": "Always write clear docstrings on @tool functions because LLMs read docstrings as the tool definition/schema."}
        ],
        "hands_on_task": {
            "title": "Add a currency converter tool",
            "instruction": "Create a tool `convert_currency(amount: float, from_curr: str, to_curr: str) -> float`.",
            "starter_code": "@tool\ndef convert_currency(amount: float, from_curr: str, to_curr: str) -> float:\n    \"\"\"Converts currency from one currency to another.\"\"\"\n    return round(amount * 1.08, 2)"
        },
        "quick_quiz": [
            {
                "question": "What does ToolNode automatically generate after executing a tool?",
                "options": [
                    "A raw SQL INSERT query",
                    "A ToolMessage with content set to the tool output and matching tool_call_id",
                    "A HumanMessage with prompt text",
                    "A PDF document"
                ],
                "correct_index": 1,
                "explanation": "ToolNode outputs a ToolMessage with the exact matching tool_call_id, satisfying LLM provider protocols."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m4-l4",
        "next_lesson_id": "m5-l2"
    },
    "m5-l2": {
        "id": "m5-l2",
        "module_id": "module-5",
        "module_title": "Module 5: Models, Messages & Tool Calling",
        "title": "Prebuilt tools_condition & ReAct Loop Flow",
        "difficulty": "Intermediate",
        "estimated_minutes": 15,
        "prerequisites": ["m5-l1"],
        "objectives": [
            "Use langgraph.prebuilt.tools_condition routing function",
            "Understand how tools_condition inspects state['messages'][-1].tool_calls",
            "Connect the standard ReAct cycle (Model -> Tools -> Model -> END)"
        ],
        "simple_explanation": "`tools_condition` is a prebuilt routing function that checks the latest message in state. If the message contains `tool_calls`, it routes to `'tools'`; otherwise, it routes to `END`.",
        "why_it_matters": "Instead of writing your own conditional check for `len(message.tool_calls) > 0`, `tools_condition` provides a standard, thoroughly tested routing edge.",
        "real_world_analogy": "A traffic controller: If a vehicle has an oversized cargo permit (tool calls), send it to the special inspection lane ('tools'). If not, let it drive on to the highway exit (END).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  START([START]) --> AgentNode[Agent Node]\n  AgentNode --> Router{\"tools_condition\"}\n  Router -- Has tool_calls --> ToolNode[ToolNode]\n  ToolNode --> AgentNode\n  Router -- No tool_calls --> END([END])"
        },
        "code_example": """from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def get_weather(location: str) -> str:
    \"\"\"Fetch the weather forecast for a given city.\"\"\"
    return f\"Sunny, 24°C in {location}\"

tools = [get_weather]
tool_node = ToolNode(tools)

# Simulated agent node with turn tracking
def agent_node(state: MessagesState) -> dict:
    history = state[\"messages\"]
    # If the last message was a Tool result, answer the user
    if isinstance(history[-1], ToolMessage):
        return {\"messages\": [AIMessage(content=f\"Based on the forecast: {history[-1].content}\")]}
    
    # First turn: call the weather tool
    return {\"messages\": [AIMessage(
        content=\"Checking the weather...\",
        tool_calls=[{\"name\": \"get_weather\", \"args\": {\"location\": \"San Francisco\"}, \"id\": \"call_wt_1\", \"type\": \"tool_call\"}]
    )]}

builder = StateGraph(MessagesState)
builder.add_node(\"agent\", agent_node)
builder.add_node(\"tools\", tool_node)

builder.add_edge(START, \"agent\")

# Prebuilt tools_condition routes to 'tools' or END
builder.add_conditional_edges(\"agent\", tools_condition)
builder.add_edge(\"tools\", \"agent\")  # Loop back from tools to agent

app = builder.compile()
res = app.invoke({\"messages\": [HumanMessage(content=\"What is the weather in SF?\")]})

print(\"Conversation Trace:\")
for m in res[\"messages\"]:
    print(f\"- {type(m).__name__}: {m.content}\")""",
        "line_by_line": [
            {"line": "from langgraph.prebuilt import ToolNode, tools_condition", "explanation": "Imports both the execution node and the routing condition."},
            {"line": "builder.add_conditional_edges('agent', tools_condition)", "explanation": "Automatically routes to 'tools' if tool_calls exist, else END."},
            {"line": "builder.add_edge('tools', 'agent')", "explanation": "Closes the cycle by directing tool execution results back into the agent node."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "What is the weather in SF?"}]},
        "sample_output": {
            "messages": [
                {"type": "human", "content": "What is the weather in SF?"},
                {"type": "ai", "content": "Checking the weather...", "tool_calls": [{"name": "get_weather"}]},
                {"type": "tool", "content": "Sunny, 24°C in San Francisco"},
                {"type": "ai", "content": "Based on the forecast: Sunny, 24°C in San Francisco"}
            ]
        },
        "common_mistakes": [
            {"mistake": "Naming the ToolNode something other than 'tools' when using default tools_condition.", "fix": "Ensure your node is named 'tools' or pass a custom mapping to add_conditional_edges('agent', tools_condition, {'tools': 'my_custom_tool_node', '__end__': END})."}
        ],
        "hands_on_task": {
            "title": "Inspect tool_calls in tools_condition",
            "instruction": "Test running tools_condition with an AIMessage with no tool_calls and verify it returns END.",
            "starter_code": "msg = AIMessage(content='Done')\nprint(tools_condition({'messages': [msg]}))"
        },
        "quick_quiz": [
            {
                "question": "What does tools_condition return when the last message has no tool_calls?",
                "options": [
                    "'tools'",
                    "END ('__end__')",
                    "None",
                    "'error_node'"
                ],
                "correct_index": 1,
                "explanation": "tools_condition returns '__end__' (END) when there are no tool_calls in the last message, terminating the ReAct loop."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m5-l1",
        "next_lesson_id": "m5-l3"
    },
    "m5-l3": {
        "id": "m5-l3",
        "module_id": "module-5",
        "module_title": "Module 5: Models, Messages & Tool Calling",
        "title": "Tool Error Handling & Fallbacks",
        "difficulty": "Intermediate",
        "estimated_minutes": 16,
        "prerequisites": ["m5-l1"],
        "objectives": [
            "Handle tool exceptions without crashing the entire graph execution",
            "Return informative error ToolMessages to allow the model to self-correct",
            "Configure handle_tool_errors parameter in ToolNode"
        ],
        "simple_explanation": "In production, tools can fail (network timeouts, invalid database IDs, bad parameters). By setting `ToolNode(tools, handle_tool_errors=True)`, any exception raised by a tool is caught and converted into an error message fed back to the LLM so it can fix its arguments.",
        "why_it_matters": "Without error handling, a single failed API call crashes the entire graph. With error handling, the agent can apologize, retry with adjusted arguments, or try an alternative tool.",
        "real_world_analogy": "Like a GPS navigation device: If a road is closed (tool error), the GPS doesn't shut down; it informs you 'Road closed, recalculating alternative route' (self-healing loop).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Agent[Agent calls Tool with invalid param] --> ToolNode[ToolNode executes tool]\n  ToolNode -- Exception Caught --> ErrMsg[\"ToolMessage: 'Error: invalid zip code'\"]\n  ErrMsg --> Agent\n  Agent -- Retries with corrected param --> ToolNode"
        },
        "code_example": """from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

@tool
def lookup_database(record_id: int) -> str:
    \"\"\"Fetch a record from the database by integer ID.\"\"\"
    if record_id < 0:
        raise ValueError(f\"Negative ID {record_id} is invalid. IDs must be positive integers.\")
    return f\"Record #{record_id}: Customer Account Active\"

# Custom error handler function
def custom_error_handler(e: Exception) -> str:
    return f\"Tool execution error: {type(e).__name__} - {str(e)}. Please correct your arguments and retry.\"

# ToolNode with error handling enabled
tool_node = ToolNode(tools=[lookup_database], handle_tool_errors=custom_error_handler)

def smart_agent(state: MessagesState) -> dict:
    history = state[\"messages\"]
    last_msg = history[-1]
    
    if isinstance(last_msg, ToolMessage) and \"error\" in last_msg.content.lower():
        # Agent self-corrects based on tool error feedback!
        return {\"messages\": [AIMessage(
            content=\"Correcting ID to positive integer...\",
            tool_calls=[{\"name\": \"lookup_database\", \"args\": {\"record_id\": 42}, \"id\": \"call_retry_1\", \"type\": \"tool_call\"}]
        )]}
    elif isinstance(last_msg, ToolMessage):
        return {\"messages\": [AIMessage(content=f\"Successfully retrieved: {last_msg.content}\")]}
    
    # First attempt: invalid negative ID
    return {\"messages\": [AIMessage(
        content=\"Querying record -100...\",
        tool_calls=[{\"name\": \"lookup_database\", \"args\": {\"record_id\": -100}, \"id\": \"call_bad_1\", \"type\": \"tool_call\"}]
    )]}

builder = StateGraph(MessagesState)
builder.add_node(\"agent\", smart_agent)
builder.add_node(\"tools\", tool_node)

builder.add_edge(START, \"agent\")
builder.add_conditional_edges(\"agent\", tools_condition)
builder.add_edge(\"tools\", \"agent\")

app = builder.compile()
res = app.invoke({\"messages\": [HumanMessage(content=\"Find my account record\")]})

print(\"--- EXECUTION TRACE ---\")
for m in res[\"messages\"]:
    print(f\"[{type(m).__name__}]: {m.content}\")""",
        "line_by_line": [
            {"line": "tool_node = ToolNode(tools=[lookup_database], handle_tool_errors=custom_error_handler)", "explanation": "Catches tool exceptions and translates them into graceful ToolMessages using custom_error_handler."},
            {"line": "if isinstance(last_msg, ToolMessage) and 'error' in last_msg.content.lower():", "explanation": "Allows the agent to read the error feedback and adjust its next tool call."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "Find my account record"}]},
        "sample_output": {
            "messages": [
                {"type": "human", "content": "Find my account record"},
                {"type": "ai", "content": "Querying record -100..."},
                {"type": "tool", "content": "Tool execution error: ValueError - Negative ID -100 is invalid. Please correct your arguments and retry."},
                {"type": "ai", "content": "Correcting ID to positive integer..."},
                {"type": "tool", "content": "Record #42: Customer Account Active"},
                {"type": "ai", "content": "Successfully retrieved: Record #42: Customer Account Active"}
            ]
        },
        "common_mistakes": [
            {"mistake": "Leaving handle_tool_errors=False, causing unhandled exceptions to crash the entire application.", "fix": "Set handle_tool_errors=True or provide a callable error handler."}
        ],
        "hands_on_task": {
            "title": "Add retry limit",
            "instruction": "Add a counter in state to stop retrying if tool errors exceed 3 attempts.",
            "starter_code": "if state.get('tool_retries', 0) >= 3:\n    return {'messages': [AIMessage(content='Unable to fulfill request due to tool errors.')]}"
        },
        "quick_quiz": [
            {
                "question": "What happens when `handle_tool_errors=True` is passed to ToolNode?",
                "options": [
                    "All errors are ignored and state is deleted",
                    "Exceptions are caught and returned as a ToolMessage with the error string",
                    "The graph restarts from the START node",
                    "A webhook notification is sent"
                ],
                "correct_index": 1,
                "explanation": "When handle_tool_errors=True, ToolNode converts Python exceptions into ToolMessage content so the LLM can see the error and retry."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m5-l2",
        "next_lesson_id": "m6-l1"
    },
    "m6-l1": {
        "id": "m6-l1",
        "module_id": "module-6",
        "module_title": "Module 6: Building ReAct & Custom Agents",
        "title": "Building a ReAct Agent from Scratch with StateGraph",
        "difficulty": "Intermediate",
        "estimated_minutes": 22,
        "prerequisites": ["m5-l2"],
        "objectives": [
            "Implement the canonical ReAct (Reason + Act) agent architecture from first principles",
            "Manage system prompts and model tool bindings",
            "Enforce loop safety bounds and clean termination"
        ],
        "simple_explanation": "ReAct combines reasoning (thinking in natural language) with actions (calling tools). Building it from scratch in StateGraph gives you full control over prompt engineering, state schemas, guardrails, and checkpointing.",
        "why_it_matters": "Prebuilt agents are great for quick prototypes, but enterprise applications always need custom agent graphs to insert compliance checks, custom memory reducers, and audit logs.",
        "real_world_analogy": "Like a detective solving a case: 1. Reason about current clues (Agent node), 2. Take an action like questioning a witness or testing DNA (ToolNode), 3. Integrate new evidence (add_messages), 4. Repeat until the case is solved.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  START([START]) --> Agent[Agent Node: Reason & Generate Tool Calls]\n  Agent --> Router{\"tools_condition\"}\n  Router -- Tool Calls Present --> Tools[ToolNode: Execute Tools]\n  Tools --> Agent\n  Router -- Finished --> END([END])"
        },
        "code_example": """from typing import TypedDict, Annotated
from langchain_core.messages import HumanMessage, AIMessage, SystemMessage, ToolMessage
from langchain_core.tools import tool
from langgraph.graph import StateGraph, MessagesState, START, END
from langgraph.prebuilt import ToolNode, tools_condition

# 1. Define tools
@tool
def search_kb(query: str) -> str:
    \"\"\"Searches knowledge base for product documentation.\"\"\"
    return f\"Knowledge base result: {query} requires API version 2.4+\"

tools = [search_kb]
tool_node = ToolNode(tools)

# 2. Agent Node with system message injection
SYSTEM_PROMPT = SystemMessage(content=\"You are an expert technical support engineer. Use search_kb to answer questions accurately.\")

def agent_reasoning(state: MessagesState) -> dict:
    msgs = state[\"messages\"]
    # In a live app, you would do: response = model.invoke([SYSTEM_PROMPT] + msgs)
    
    # Deterministic simulation of ReAct flow:
    if len(msgs) == 1:
        # First step: call tool
        return {\"messages\": [AIMessage(
            content=\"Let me query the knowledge base.\",
            tool_calls=[{\"name\": \"search_kb\", \"args\": {\"query\": msgs[-1].content}, \"id\": \"call_kb_1\", \"type\": \"tool_call\"}]
        )]}
    else:
        # Second step: tool returned result -> generate final response
        kb_result = msgs[-1].content
        return {\"messages\": [AIMessage(content=f\"According to our official docs: {kb_result}\")]}

# 3. Assemble Graph
builder = StateGraph(MessagesState)
builder.add_node(\"agent\", agent_reasoning)
builder.add_node(\"tools\", tool_node)

builder.add_edge(START, \"agent\")
builder.add_conditional_edges(\"agent\", tools_condition)
builder.add_edge(\"tools\", \"agent\")

react_agent = builder.compile()

output = react_agent.invoke({\"messages\": [HumanMessage(content=\"LangGraph compatibility\")]})
for m in output[\"messages\"]:
    print(f\"[{type(m).__name__}]: {m.content}\")""",
        "line_by_line": [
            {"line": "builder = StateGraph(MessagesState)", "explanation": "Initializes graph with MessagesState for append-only chat history."},
            {"line": "builder.add_conditional_edges('agent', tools_condition)", "explanation": "Evaluates tool_calls on the latest AIMessage."},
            {"line": "builder.add_edge('tools', 'agent')", "explanation": "Loops back to agent with tool output for subsequent reasoning."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "LangGraph compatibility"}]},
        "sample_output": {
            "messages": [
                {"type": "human", "content": "LangGraph compatibility"},
                {"type": "ai", "content": "Let me query the knowledge base."},
                {"type": "tool", "content": "Knowledge base result: LangGraph compatibility requires API version 2.4+"},
                {"type": "ai", "content": "According to our official docs: Knowledge base result: LangGraph compatibility requires API version 2.4+"}
            ]
        },
        "common_mistakes": [
            {"mistake": "Injecting SystemMessage into state inside the agent node on every loop iteration.", "fix": "Prepend SystemMessage only when calling the model, or add it once at graph START."}
        ],
        "hands_on_task": {
            "title": "Add a calculator tool to the ReAct agent",
            "instruction": "Add a `@tool def multiply(a: int, b: int) -> int` and register it in tools list.",
            "starter_code": "@tool\ndef multiply(a: int, b: int) -> int:\n    \"\"\"Multiplies two numbers.\"\"\"\n    return a * b"
        },
        "quick_quiz": [
            {
                "question": "What is the key difference between a custom StateGraph ReAct agent and a hardcoded while loop?",
                "options": [
                    "StateGraph provides full Pregel step persistence, inspectability, checkpointing, and time-travel debugging",
                    "There is no difference",
                    "StateGraph can only run 1 tool",
                    "While loops are more memory efficient"
                ],
                "correct_index": 0,
                "explanation": "StateGraph brings enterprise-grade checkpointing, time-travel, human interrupts, streaming, and visual debugging to agent loops."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m5-l3",
        "next_lesson_id": "m6-l2"
    },
    "m6-l2": {
        "id": "m6-l2",
        "module_id": "module-6",
        "module_title": "Module 6: Building ReAct & Custom Agents",
        "title": "Using prebuilt create_react_agent & Customizing Hooks",
        "difficulty": "Intermediate",
        "estimated_minutes": 15,
        "prerequisites": ["m6-l1"],
        "objectives": [
            "Use langgraph.prebuilt.create_react_agent for rapid agent creation",
            "Customize prompts using prompt / state_modifier parameter",
            "Integrate checkpointers and custom response schemas"
        ],
        "simple_explanation": "`langgraph.prebuilt.create_react_agent` is a high-level helper that generates a complete ReAct StateGraph with tool nodes, routing conditions, and message reducers in a single function call.",
        "why_it_matters": "When you don't need complex multi-stage graphs, `create_react_agent` saves 50 lines of boilerplate while still returning a standard compiled LangGraph Pregel runnable.",
        "real_world_analogy": "Like ordering a pre-assembled desk instead of buying timber and screws: It's fast to set up, but follows the exact same standard construction under the hood.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Params[\"create_react_agent(model, tools, prompt=...)\"] --> CompiledGraph[\"Compiled StateGraph Runnable\"]\n  CompiledGraph --> Run[\"app.invoke(messages, config)\"]"
        },
        "code_example": """from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver

@tool
def get_system_uptime() -> str:
    \"\"\"Returns server uptime statistics.\"\"\"
    return \"Server online: 99.98% uptime over 180 days.\"

tools = [get_system_uptime]

# In production with an actual model:
# from langchain_openai import ChatOpenAI
# model = ChatOpenAI(model=\"gpt-4o\")
# checkpointer = MemorySaver()
# agent = create_react_agent(model, tools, prompt=\"You are a DevOps assistant.\", checkpointer=checkpointer)

print(\"create_react_agent signature:\")
print(\"create_react_agent(model, tools, prompt=..., checkpointer=..., response_format=...)\")""",
        "line_by_line": [
            {"line": "from langgraph.prebuilt import create_react_agent", "explanation": "Imports the official prebuilt ReAct agent factory."},
            {"line": "checkpointer = MemorySaver()", "explanation": "Attaches in-memory checkpointing for multi-turn conversations."}
        ],
        "sample_input": {"messages": [{"role": "user", "content": "What is our server status?"}]},
        "sample_output": {"messages": [{"type": "ai", "content": "The server has been online with 99.98% uptime over 180 days."}]},
        "common_mistakes": [
            {"mistake": "Passing a raw string to prompt without understanding that it acts as the system message.", "fix": "Ensure prompt string or SystemMessage conveys clear system guidelines."}
        ],
        "hands_on_task": {
            "title": "Inspect create_react_agent nodes",
            "instruction": "Compile a create_react_agent and inspect `agent.get_graph().nodes`.",
            "starter_code": "# agent.get_graph().nodes"
        },
        "quick_quiz": [
            {
                "question": "What is returned by `create_react_agent()` in LangGraph 0.2+?",
                "options": [
                    "A raw string response",
                    "A fully compiled Pregel StateGraph instance supporting invoke, stream, and checkpointing",
                    "A LangChain LCEL chain only",
                    "A Python list of tools"
                ],
                "correct_index": 1,
                "explanation": "create_react_agent returns a compiled Pregel StateGraph that supports all LangGraph features including streaming and checkpointing."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m6-l1",
        "next_lesson_id": "m6-l3"
    },
    "m6-l3": {
        "id": "m6-l3",
        "module_id": "module-6",
        "module_title": "Module 6: Building ReAct & Custom Agents",
        "title": "Agent Guardrails, Safety & Bounded Execution",
        "difficulty": "Intermediate",
        "estimated_minutes": 18,
        "prerequisites": ["m6-l1"],
        "objectives": [
            "Implement deterministic safety filters before calling LLM nodes",
            "Filter output messages for PII and policy violations",
            "Enforce strict tool execution boundaries"
        ],
        "simple_explanation": "Guardrails are deterministic validation steps inserted before and after agent nodes. They inspect inputs for forbidden topics or prompt injection and sanitize outputs before they reach the user.",
        "why_it_matters": "LLMs cannot be trusted 100% to follow safety rules via prompts alone. Hardcoded guardrail nodes guarantee safety constraints at the software level.",
        "real_world_analogy": "Airport security checkpoints: Passengers go through metal detectors (input guardrails) before entering the terminal, and baggage is inspected before boarding (output guardrails).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  START([START]) --> InGuard{Input Guardrail}\n  InGuard -- Blocked --> BlockNode[Return Policy Violation]\n  InGuard -- Passed --> Agent[Agent Node]\n  Agent --> OutGuard{Output Guardrail}\n  OutGuard -- Clean --> END([END])\n  OutGuard -- PII Detected --> Redact[Redact PII] --> END"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class GuardrailState(TypedDict):
    user_input: str
    is_safe: bool
    filtered_input: str
    response: str

FORBIDDEN_KEYWORDS = [\"hack\", \"bypass\", \"drop table\", \"system prompt\"]

def input_guardrail_node(state: GuardrailState) -> dict:
    inp = state[\"user_input\"].lower()
    for kw in FORBIDDEN_KEYWORDS:
        if kw in inp:
            return {\"is_safe\": False, \"response\": f\"Security violation: query contains prohibited keyword '{kw}'.\"}
    return {\"is_safe\": True, \"filtered_input\": state[\"user_input\"]}

def route_safety(state: GuardrailState) -> str:
    return \"agent_execution\" if state[\"is_safe\"] else \"blocked\"

def agent_execution_node(state: GuardrailState) -> dict:
    return {\"response\": f\"Processed query safely: {state['filtered_input']}\"}

def blocked_response_node(state: GuardrailState) -> dict:
    return {\"response\": state[\"response\"]}

builder = StateGraph(GuardrailState)
builder.add_node(\"guardrail\", input_guardrail_node)
builder.add_node(\"agent_execution\", agent_execution_node)
builder.add_node(\"blocked\", blocked_response_node)

builder.add_edge(START, \"guardrail\")
builder.add_conditional_edges(\"guardrail\", route_safety, {\"agent_execution\": \"agent_execution\", \"blocked\": \"blocked\"})
builder.add_edge(\"agent_execution\", END)
builder.add_edge(\"blocked\", END)

app = builder.compile()
print(\"Safe input test:\", app.invoke({\"user_input\": \"Help me analyze sales trends\", \"is_safe\": False, \"filtered_input\": \"\", \"response\": \"\"}))
print(\"Malicious input test:\", app.invoke({\"user_input\": \"How to drop table users?\", \"is_safe\": False, \"filtered_input\": \"\", \"response\": \"\"}))""",
        "line_by_line": [
            {"line": "builder.add_conditional_edges('guardrail', route_safety, ...)", "explanation": "Guarantees that blocked inputs never reach LLM execution nodes."}
        ],
        "sample_input": {"user_input": "How to drop table users?", "is_safe": False, "filtered_input": "", "response": ""},
        "sample_output": {"user_input": "How to drop table users?", "is_safe": False, "response": "Security violation: query contains prohibited keyword 'drop table'."},
        "common_mistakes": [
            {"mistake": "Relying solely on LLM self-moderation prompts without code-level guardrail nodes.", "fix": "Implement deterministic Python validator nodes for critical compliance and security rules."}
        ],
        "hands_on_task": {
            "title": "Add email PII mask node",
            "instruction": "Create an output guardrail node that replaces email patterns with `[REDACTED_EMAIL]`.",
            "starter_code": "import re\ndef redact_emails(state: GuardrailState) -> dict:\n    # Regex replace email patterns\n    pass"
        },
        "quick_quiz": [
            {
                "question": "Why should critical guardrails be implemented as deterministic graph nodes rather than prompt instructions?",
                "options": [
                    "Deterministic nodes guarantee 100% enforcement without risk of model jailbreaking or prompt injection",
                    "Prompts use too much RAM",
                    "Guardrail nodes are only for visual diagrams",
                    "LLMs cannot read system prompts"
                ],
                "correct_index": 0,
                "explanation": "Deterministic code nodes cannot be bypassed by prompt injection, providing reliable security boundaries."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m6-l2",
        "next_lesson_id": "m7-l1"
    },
    "m7-l1": {
        "id": "m7-l1",
        "module_id": "module-7",
        "module_title": "Module 7: Persistence, Checkpointing & Memory",
        "title": "Checkpointers, Threads & State Snapshots",
        "difficulty": "Advanced",
        "estimated_minutes": 20,
        "prerequisites": ["m2-l2"],
        "objectives": [
            "Understand how checkpointers save state after every super-step",
            "Use thread_id in RunnableConfig to manage independent user sessions",
            "Inspect state snapshots using app.get_state(config)"
        ],
        "simple_explanation": "A checkpointer writes the full state snapshot to a persistent store (RAM, SQLite, Postgres) after every single super-step. By supplying a `thread_id` in `config={'configurable': {'thread_id': 'user_123'}}`, you can pause a conversation for 3 days and resume right where the user left off.",
        "why_it_matters": "Without checkpointing, every graph execution is stateless. Checkpointing is what enables multi-turn chat, human-in-the-loop approvals, and recovery from server crashes.",
        "real_world_analogy": "Like an auto-save feature in a video game: Every time you complete a quest step, the game saves your inventory and location under your save slot (`thread_id`). If the console turns off, you reload that slot and continue.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  SuperStep1[Super-Step 1] --> CP1[(Checkpoint 1: state_v1)]\n  CP1 --> SuperStep2[Super-Step 2]\n  SuperStep2 --> CP2[(Checkpoint 2: state_v2)]\n  CP2 --> SuperStep3[Super-Step 3]\n  SuperStep3 --> CP3[(Checkpoint 3: state_v3)]"
        },
        "code_example": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class ConversationState(TypedDict):
    history: Annotated[list[str], operator.add]
    turns_count: int

def chat_node(state: ConversationState) -> dict:
    new_turn = state.get("turns_count", 0) + 1
    return {
        "history": [f"Turn #{new_turn}: User message processed."],
        "turns_count": new_turn
    }

builder = StateGraph(ConversationState)
builder.add_node("chat", chat_node)
builder.add_edge(START, "chat")
builder.add_edge("chat", END)

# 1. Attach MemorySaver checkpointer
checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

# 2. Invoke for User Alice (thread_id: 'alice-session')
alice_config = {"configurable": {"thread_id": "alice-session"}}

print("--- ALICE TURN 1 ---")
app.invoke({"history": ["Hi! I am Alice."], "turns_count": 0}, config=alice_config)

print("--- ALICE TURN 2 ---")
# Notice we don't pass initial history again; LangGraph loads it from checkpoint!
app.invoke({"history": ["What is my name?"], "turns_count": 0}, config=alice_config)

# 3. Inspect saved snapshot
state_snapshot = app.get_state(alice_config)
print("\\nAlice Current Snapshot Values:", state_snapshot.values)
print("Alice Next Nodes to Run:", state_snapshot.next)""",
        "line_by_line": [
            {"line": "from langgraph.checkpoint.memory import MemorySaver", "explanation": "Imports in-memory checkpointer for testing and development."},
            {"line": "app = builder.compile(checkpointer=checkpointer)", "explanation": "Enables persistence across all graph executions."},
            {"line": "alice_config = {'configurable': {'thread_id': 'alice-session'}}", "explanation": "Identifies the unique thread session for state retrieval and updates."},
            {"line": "state_snapshot = app.get_state(alice_config)", "explanation": "Fetches the latest StateSnapshot including values, config, metadata, and next node pointers."}
        ],
        "sample_input": {"configurable": {"thread_id": "alice-session"}},
        "sample_output": {
            "history": ["Hi! I am Alice.", "Turn #1: User message processed.", "What is my name?", "Turn #2: User message processed."],
            "turns_count": 2
        },
        "common_mistakes": [
            {"mistake": "Invoking a graph compiled with a checkpointer without passing a thread_id in config.", "fix": "Always pass `config={'configurable': {'thread_id': '...'}}` when a checkpointer is enabled."}
        ],
        "hands_on_task": {
            "title": "Create Bob session",
            "instruction": "Invoke the graph with `thread_id: 'bob-session'` and verify Bob's state is completely isolated from Alice's.",
            "starter_code": "bob_config = {'configurable': {'thread_id': 'bob-session'}}\napp.invoke({'history': ['Hi I am Bob'], 'turns_count': 0}, config=bob_config)"
        },
        "quick_quiz": [
            {
                "question": "What is required in `config` when calling a graph compiled with a checkpointer?",
                "options": [
                    "A valid database connection string",
                    "A `thread_id` inside `config['configurable']`",
                    "An encryption key",
                    "A list of all node names"
                ],
                "correct_index": 1,
                "explanation": "LangGraph uses `config['configurable']['thread_id']` to partition and retrieve checkpoint snapshots for specific sessions."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "prev_lesson_id": "m6-l3",
        "next_lesson_id": "m7-l2"
    },
    "m7-l2": {
        "id": "m7-l2",
        "module_id": "module-7",
        "module_title": "Module 7: Persistence, Checkpointing & Memory",
        "title": "Time-Travel Debugging & History Replay",
        "difficulty": "Advanced",
        "estimated_minutes": 22,
        "prerequisites": ["m7-l1"],
        "objectives": [
            "Iterate through checkpoint history with app.get_state_history(config)",
            "Rewind execution to an earlier checkpoint_id",
            "Fork execution into a new branch using update_state()"
        ],
        "simple_explanation": "Time-travel debugging allows you to inspect past states, step backwards in time, modify what the agent knew at step 3, and re-execute from that point forward to see how outcomes change.",
        "why_it_matters": "When an agent goes off the rails on step 5 of an 8-step workflow, you don't have to restart from step 1. You can rewind to step 4, edit the state, and resume instantly.",
        "real_world_analogy": "Like Git branching: You can checkout an earlier commit (checkpoint), create a new branch, and commit new changes without deleting your previous timeline.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  CP1[Checkpoint 1] --> CP2[Checkpoint 2]\n  CP2 --> CP3[Checkpoint 3: Agent Error]\n  CP2 -. Rewind & Fork .-> CP3_Fork[Checkpoint 3B: Corrected State] --> CP4_Fork[Checkpoint 4B: Success]"
        },
        "code_example": """from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class TaskState(TypedDict):
    plan: list[str]
    step_num: int

def step_one(state: TaskState) -> dict:
    return {"plan": ["Step 1: Ingest Data"], "step_num": 1}

def step_two(state: TaskState) -> dict:
    return {"plan": state["plan"] + ["Step 2: Generate Bad Output"], "step_num": 2}

builder = StateGraph(TaskState)
builder.add_node("step_one", step_one)
builder.add_node("step_two", step_two)

builder.add_edge(START, "step_one")
builder.add_edge("step_one", "step_two")
builder.add_edge("step_two", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

cfg = {"configurable": {"thread_id": "debug-session-1"}}
app.invoke({"plan": [], "step_num": 0}, config=cfg)

# 1. Fetch full checkpoint history
print("--- CHECKPOINT HISTORY ---")
history = list(app.get_state_history(cfg))
for snapshot in history:
    print(f"Checkpoint ID: {snapshot.config['configurable']['checkpoint_id']} | Next: {snapshot.next} | State: {snapshot.values}")

# 2. Time-Travel: Rewind to step_one checkpoint
step_one_snapshot = history[1]  # The snapshot after step_one ran
print(f"\\nRewinding to checkpoint: {step_one_snapshot.config['configurable']['checkpoint_id']}")

# 3. Fork state with corrected plan
forked_config = app.update_state(
    step_one_snapshot.config,
    {"plan": ["Step 1: Ingest Data", "Step 2: Generate HIGH QUALITY Output (Corrected)"]}
)
print("Forked new checkpoint config:", forked_config)""",
        "line_by_line": [
            {"line": "history = list(app.get_state_history(cfg))", "explanation": "Returns an iterator of all past StateSnapshots in reverse chronological order."},
            {"line": "forked_config = app.update_state(step_one_snapshot.config, ...)", "explanation": "Writes a new branch off the historical checkpoint."}
        ],
        "sample_input": {"configurable": {"thread_id": "debug-session-1"}},
        "sample_output": {
            "plan": ["Step 1: Ingest Data", "Step 2: Generate HIGH QUALITY Output (Corrected)"],
            "step_num": 1
        },
        "common_mistakes": [
            {"mistake": "Assuming updating state modifies past checkpoints in-place (mutating history).", "fix": "Checkpoints in LangGraph are immutable event logs. update_state() always creates a new checkpoint referencing the parent."}
        ],
        "hands_on_task": {
            "title": "Resume execution from forked checkpoint",
            "instruction": "Call `app.invoke(None, config=forked_config)` to resume graph execution from the forked checkpoint.",
            "starter_code": "res = app.invoke(None, config=forked_config)\nprint('Resumed result:', res)"
        },
        "quick_quiz": [
            {
                "question": "Are LangGraph checkpoints mutable or immutable?",
                "options": [
                    "Mutable: modifying state overwrites the previous row in the database",
                    "Immutable: each checkpoint represents a permanent, addressable point in time",
                    "Checkpoints are deleted automatically after 5 seconds",
                    "Only SQLite checkpointers are immutable"
                ],
                "correct_index": 1,
                "explanation": "LangGraph checkpoints are immutable snapshots forming a directed tree of state revisions."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "prev_lesson_id": "m7-l1",
        "next_lesson_id": "m7-l3"
    },
    "m7-l3": {
        "id": "m7-l3",
        "module_id": "module-7",
        "module_title": "Module 7: Persistence, Checkpointing & Memory",
        "title": "Long-Term Memory: Checkpointers vs BaseStore",
        "difficulty": "Advanced",
        "estimated_minutes": 20,
        "prerequisites": ["m7-l1"],
        "objectives": [
            "Differentiate short-term thread memory (Checkpointers) from long-term cross-thread memory (BaseStore)",
            "Store user profiles, preferences, and facts using InMemoryStore with namespaces",
            "Access stores inside nodes via runtime context"
        ],
        "simple_explanation": "A checkpointer manages short-term memory scoped to a single `thread_id` (a specific chat session). A `Store` (like `InMemoryStore`) manages long-term memory across ALL threads and sessions (e.g. user preferences, corporate facts, cross-session user profile).",
        "why_it_matters": "When a user starts a new conversation tomorrow (new `thread_id`), the checkpointer starts fresh, but the `Store` remembers their name, language preference, and past topics.",
        "real_world_analogy": "A checkpointer is a notepad for today's meeting (thread memory). A Store is the customer's permanent CRM account profile that persists across hundreds of meetings (long-term memory).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TB\n  subgraph LongTerm[Long-Term Cross-Thread Store]\n    Store[(Store: namespace=('users', 'user_42'))]\n  end\n  subgraph Session1[Thread 1: Monday Chat]\n    CP1[Checkpointer: thread_id='mon_01']\n    CP1 -. Reads user profile .-> Store\n  end\n  subgraph Session2[Thread 2: Friday Chat]\n    CP2[Checkpointer: thread_id='fri_02']\n    CP2 -. Reads user profile .-> Store\n  end"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.store.memory import InMemoryStore
from langgraph.checkpoint.memory import MemorySaver

class ProfileState(TypedDict):
    user_id: str
    message: str
    reply: str

# 1. Setup Long-Term Store and Short-Term Checkpointer
store = InMemoryStore()
# Store user preference across threads
store.put(
    namespace=(\"users\", \"user_42\"),
    key=\"preferences\",
    value={\"language\": \"Spanish\", \"theme\": \"Dark\", \"skill_level\": \"Advanced\"}
)

def personalized_agent(state: ProfileState) -> dict:
    uid = state[\"user_id\"]
    # Retrieve cross-thread long-term profile
    user_pref = store.get(namespace=(\"users\", uid), key=\"preferences\")
    lang = user_pref.value.get(\"language\", \"English\") if user_pref else \"English\"
    
    greeting = \"¡Hola! ¿En qué puedo ayudarte hoy?\" if lang == \"Spanish\" else \"Hello! How can I help you?\"
    return {\"reply\": f\"[{lang} Mode] {greeting}\"}

builder = StateGraph(ProfileState)
builder.add_node(\"agent\", personalized_agent)
builder.add_edge(START, \"agent\")
builder.add_edge(\"agent\", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer, store=store)

# New Thread 1
res1 = app.invoke(
    {\"user_id\": \"user_42\", \"message\": \"Hello\", \"reply\": \"\"},
    config={\"configurable\": {\"thread_id\": \"session-thread-999\"}}
)
print(\"Response in new thread:\", res1[\"reply\"])""",
        "line_by_line": [
            {"line": "from langgraph.store.memory import InMemoryStore", "explanation": "Imports cross-thread key-value memory store."},
            {"line": "store.put(namespace=('users', 'user_42'), key='preferences', value={...})", "explanation": "Persists structured data scoped by hierarchical namespace tuples."},
            {"line": "app = builder.compile(checkpointer=checkpointer, store=store)", "explanation": "Registers both short-term checkpointing and long-term storage in the compiled graph."}
        ],
        "sample_input": {"user_id": "user_42", "message": "Hello", "reply": ""},
        "sample_output": {"reply": "[Spanish Mode] ¡Hola! ¿En qué puedo ayudarte hoy?"},
        "common_mistakes": [
            {"mistake": "Storing permanent user account details inside thread state messages instead of a Store.", "fix": "Use BaseStore for cross-session long-term data so new threads don't lose user preferences."}
        ],
        "hands_on_task": {
            "title": "Update store value inside a node",
            "instruction": "Call `store.put(('users', uid), 'last_seen', {'timestamp': '2026-10-08'})`.",
            "starter_code": "# store.put(('users', uid), 'last_seen', {'time': 'now'})"
        },
        "quick_quiz": [
            {
                "question": "What is the primary difference between a Checkpointer and a Store?",
                "options": [
                    "A Checkpointer is thread-scoped short-term state; a Store is cross-thread long-term memory",
                    "A Store only works with MySQL",
                    "Checkpointers are only used for visual debugging",
                    "There is no difference"
                ],
                "correct_index": 0,
                "explanation": "Checkpointers manage step-by-step state snapshots for a specific thread_id, whereas Stores persist hierarchical data accessible across all threads."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "prev_lesson_id": "m7-l2",
        "next_lesson_id": "m8-l1"
    },
    "m8-l1": {
        "id": "m8-l1",
        "module_id": "module-8",
        "module_title": "Module 8: Human-in-the-Loop & Dynamic Interrupts",
        "title": "Dynamic Interrupts with interrupt() Function",
        "difficulty": "Advanced",
        "estimated_minutes": 20,
        "prerequisites": ["m7-l1"],
        "objectives": [
            "Use langgraph.types.interrupt() to pause graph execution dynamically",
            "Pass information from the paused node to the human UI",
            "Resume execution with Command(resume=value)"
        ],
        "simple_explanation": "The `interrupt(query)` function pauses execution right inside a node function. It returns whatever question or data you pass to the client and saves the checkpoint. When the user responds, you invoke the graph with `Command(resume=answer)` and the node resumes from that exact line with the answer!",
        "why_it_matters": "Dynamic interrupts are vastly superior to old-school static breakpoints because they can be triggered conditionally (e.g. only interrupt if a transfer amount is over $1,000).",
        "real_world_analogy": "Like a bank teller asking for your signature before cashing a large check: The transaction pauses, you sign the slip, and the teller resumes the transaction with your confirmed signature.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "sequenceDiagram\n  autonumber\n  participant Client\n  participant Node as Transfer Node\n  Client->>Node: app.invoke({'amount': 5000})\n  Node->>Node: amount > 1000 -> calls interrupt('Confirm $5000 transfer?')\n  Node-->>Client: Graph Paused! Next: ['transfer_node'], Interrupt: 'Confirm?'\n  Note over Client: User clicks 'Approve'\n  Client->>Node: app.invoke(Command(resume=True))\n  Node->>Node: interrupt() returns True\n  Node-->>Client: Transfer Completed Successfully"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class PaymentState(TypedDict):
    recipient: str
    amount: float
    confirmed: bool
    status: str

def payment_node(state: PaymentState) -> dict:
    amt = state["amount"]
    if amt >= 1000:
        # 1. Dynamic Interrupt: Pauses execution and asks human for confirmation
        human_approval = interrupt({
            "question": f"Transferring ${amt} to {state['recipient']}. Do you approve?",
            "risk_level": "HIGH"
        })
        
        # When resumed, interrupt() returns the value passed in Command(resume=...)
        if not human_approval:
            return {"confirmed": False, "status": "REJECTED_BY_HUMAN"}
            
    return {"confirmed": True, "status": f"SUCCESS: Transferred ${amt} to {state['recipient']}"}

builder = StateGraph(PaymentState)
builder.add_node("payment", payment_node)
builder.add_edge(START, "payment")
builder.add_edge("payment", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

cfg = {"configurable": {"thread_id": "tx-8899"}}

# 1. First invocation: Execution pauses at interrupt()
print("--- RUN 1 (TRIGGER INTERRUPT) ---")
app.invoke({"recipient": "supplier_inc", "amount": 2500.0, "confirmed": False, "status": ""}, config=cfg)

snapshot = app.get_state(cfg)
print("Graph State Status: PAUSED")
print("Pending Next Nodes:", snapshot.next)
print("Interrupt Payload:", snapshot.tasks[0].interrupts[0].value)

# 2. Second invocation: Resume with Command(resume=True)
print("\\n--- RUN 2 (RESUME WITH APPROVAL) ---")
final_res = app.invoke(Command(resume=True), config=cfg)
print("Final Outcome:", final_res)""",
        "line_by_line": [
            {"line": "from langgraph.types import interrupt, Command", "explanation": "Imports interrupt and Command from langgraph.types."},
            {"line": "human_approval = interrupt({...})", "explanation": "Pauses execution and exposes the dictionary payload to the client."},
            {"line": "final_res = app.invoke(Command(resume=True), config=cfg)", "explanation": "Resumes the paused thread with the human's decision payload."}
        ],
        "sample_input": {"recipient": "supplier_inc", "amount": 2500.0, "confirmed": False, "status": ""},
        "sample_output": {"confirmed": True, "status": "SUCCESS: Transferred $2500.0 to supplier_inc"},
        "common_mistakes": [
            {"mistake": "Trying to use interrupt() without compiling the graph with a checkpointer.", "fix": "Dynamic interrupts require a checkpointer to persist the paused execution state."}
        ],
        "hands_on_task": {
            "title": "Test rejection flow",
            "instruction": "Resume with `Command(resume=False)` and verify status becomes `REJECTED_BY_HUMAN`.",
            "starter_code": "rej_res = app.invoke(Command(resume=False), config=cfg)\nprint(rej_res)"
        },
        "quick_quiz": [
            {
                "question": "How do you resume a graph that paused at an `interrupt()` call?",
                "options": [
                    "By calling `app.invoke(Command(resume=value), config=cfg)`",
                    "By resetting the computer",
                    "By re-running the graph from START with all original inputs",
                    "By calling `app.restart()`"
                ],
                "correct_index": 0,
                "explanation": "Passing `Command(resume=value)` with the same thread_id config unpauses the node, with `interrupt()` evaluating to `value`."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/interrupts",
        "prev_lesson_id": "m7-l3",
        "next_lesson_id": "m8-l2"
    },
    "m8-l2": {
        "id": "m8-l2",
        "module_id": "module-8",
        "module_title": "Module 8: Human-in-the-Loop & Dynamic Interrupts",
        "title": "Human Approval & Rejection Workflows",
        "difficulty": "Advanced",
        "estimated_minutes": 18,
        "prerequisites": ["m8-l1"],
        "objectives": [
            "Build robust multi-stage approval review gates for sensitive operations",
            "Route execution to audit or corrective branches on rejection",
            "Maintain complete audit logs of human decisions"
        ],
        "simple_explanation": "For sensitive operations (publishing content, making financial transactions, deleting database records), workflows must include an approval gate where a human reviewer inspects the planned payload and approves, edits, or rejects it.",
        "why_it_matters": "Autonomous agents without human oversight can cause severe reputational and financial damage. Approval workflows combine agent efficiency with human safety.",
        "real_world_analogy": "A pull request review on GitHub: An AI developer writes the code (node 1), but merging to the main branch is blocked until a human reviewer clicks 'Approve' (approval gate).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Draft[Draft Campaign Node] --> ReviewGate{Human Approval Gate}\n  ReviewGate -- Approved --> Publish[Publish Live Campaign]\n  ReviewGate -- Rejected --> Redraft[Redraft with Human Notes]\n  Redraft --> ReviewGate\n  Publish --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class CampaignState(TypedDict):
    campaign_title: str
    budget: float
    review_status: str
    feedback_notes: str

def draft_campaign(state: CampaignState) -> dict:
    return {
        "campaign_title": "Summer Flash Sale 50% Off",
        "budget": 50000.0,
        "review_status": "PENDING_REVIEW"
    }

def human_review_gate(state: CampaignState) -> Command:
    decision = interrupt({
        "action": "REVIEW_CAMPAIGN",
        "title": state["campaign_title"],
        "budget": state["budget"]
    })
    
    # decision expected format: {"approved": bool, "notes": str}
    if decision.get("approved"):
        return Command(
            update={"review_status": "APPROVED", "feedback_notes": decision.get("notes", "")},
            goto="publish_node"
        )
    return Command(
        update={"review_status": "REJECTED", "feedback_notes": decision.get("notes", "")},
        goto="redraft_node"
    )

def publish_node(state: CampaignState) -> dict:
    return {"review_status": f"LIVE: {state['campaign_title']} launched with ${state['budget']} budget."}

def redraft_node(state: CampaignState) -> dict:
    return {"review_status": f"NEEDS_REVISION: Reviewer feedback - {state['feedback_notes']}"}

builder = StateGraph(CampaignState)
builder.add_node("draft", draft_campaign)
builder.add_node("review_gate", human_review_gate)
builder.add_node("publish_node", publish_node)
builder.add_node("redraft_node", redraft_node)

builder.add_edge(START, "draft")
builder.add_edge("draft", "review_gate")
builder.add_edge("publish_node", END)
builder.add_edge("redraft_node", END)

app = builder.compile(checkpointer=MemorySaver())

cfg = {"configurable": {"thread_id": "campaign-2026"}}
app.invoke({"campaign_title": "", "budget": 0.0, "review_status": "", "feedback_notes": ""}, config=cfg)

# Human approves with note
final_result = app.invoke(
    Command(resume={"approved": True, "notes": "Budget verified and approved by Marketing VP."}),
    config=cfg
)
print("Result:", final_result)""",
        "line_by_line": [
            {"line": "def human_review_gate(state: CampaignState) -> Command:", "explanation": "Combines dynamic interrupt with Command routing based on the reviewer's verdict."},
            {"line": "app.invoke(Command(resume={'approved': True, ...}))", "explanation": "Passes the structured review object to unpause the gate."}
        ],
        "sample_input": {"configurable": {"thread_id": "campaign-2026"}},
        "sample_output": {"review_status": "LIVE: Summer Flash Sale 50% Off launched with $50000.0 budget.", "feedback_notes": "Budget verified and approved by Marketing VP."},
        "common_mistakes": [
            {"mistake": "Failing to handle non-boolean or empty resume values from the frontend.", "fix": "Use `.get('approved', False)` to default to safe rejection on malformed inputs."}
        ],
        "hands_on_task": {
            "title": "Test rejection routing",
            "instruction": "Resume with `approved: False, notes: 'Budget too high'` and inspect redraft_node output.",
            "starter_code": "app.invoke(Command(resume={'approved': False, 'notes': 'Budget too high'}), config=cfg)"
        },
        "quick_quiz": [
            {
                "question": "What is the recommended design pattern for human approval gates in LangGraph 0.2+?",
                "options": [
                    "Writing a loop that polls an external SQL table every 10ms",
                    "Using `interrupt()` inside the review node combined with `Command(resume=...)`",
                    "Killing the Python process and restarting it manually",
                    "Hardcoding a 5-minute sleep timer"
                ],
                "correct_index": 1,
                "explanation": "Combining interrupt() with Command(resume=...) allows safe, durable pausing and dynamic branching upon human review."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/interrupts",
        "prev_lesson_id": "m8-l1",
        "next_lesson_id": "m8-l3"
    },
    "m8-l3": {
        "id": "m8-l3",
        "module_id": "module-8",
        "module_title": "Module 8: Human-in-the-Loop & Dynamic Interrupts",
        "title": "State Editing & Manual Correction Before Resume",
        "difficulty": "Advanced",
        "estimated_minutes": 18,
        "prerequisites": ["m8-l1", "m7-l2"],
        "objectives": [
            "Use app.update_state() while a graph is interrupted",
            "Specify as_node parameter to simulate state updates from a specific node",
            "Resume execution with modified state values"
        ],
        "simple_explanation": "While a graph is paused at an interrupt, a human can do more than just say 'Yes' or 'No'. You can use `app.update_state(config, {'draft_email': 'Corrected email text'})` to edit the state directly before resuming!",
        "why_it_matters": "If an agent generates a 90% perfect email with one small error, the human can fix the typo directly rather than rejecting the whole draft and asking the LLM to rewrite it from scratch.",
        "real_world_analogy": "Like an executive assistant preparing a presentation for the CEO: The CEO reads the slides, edits slide #4 personally, and tells the assistant to send it out.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  AgentNode[Agent Drafts Email] --> Interrupt[Graph Paused at Interrupt]\n  Interrupt -. Human calls update_state(as_node='agent') .- Edited[State Modified by Human]\n  Edited --> Resume[app.invoke(Command(resume=True))]\n  Resume --> SendNode[Send Email with Human Edits] --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

class EmailState(TypedDict):
    recipient: str
    email_body: str
    status: str

def compose_draft(state: EmailState) -> dict:
    return {
        "recipient": "client@enterprise.com",
        "email_body": "Hey, your invoice is due yesterday. Pay now or else."
    }

def review_and_send(state: EmailState) -> dict:
    # Interrupt to allow human to review or edit body
    approved = interrupt({"action": "REVIEW_EMAIL", "body": state["email_body"]})
    if approved:
        return {"status": f"SENT to {state['recipient']}: {state['email_body']}"}
    return {"status": "DISCARDED"}

builder = StateGraph(EmailState)
builder.add_node("compose", compose_draft)
builder.add_node("review", review_and_send)

builder.add_edge(START, "compose")
builder.add_edge("compose", "review")
builder.add_edge("review", END)

app = builder.compile(checkpointer=MemorySaver())
cfg = {"configurable": {"thread_id": "email-thread-101"}}

# Run to interrupt
app.invoke({"recipient": "", "email_body": "", "status": ""}, config=cfg)

# Human inspects draft, sees tone is too aggressive, and edits it!
print("Original Draft:", app.get_state(cfg).values["email_body"])

app.update_state(
    cfg,
    {"email_body": "Dear Partner, Friendly reminder that invoice #402 is due this week. Thank you!"}
)

# Resume execution with edited state
res = app.invoke(Command(resume=True), config=cfg)
print("Final State Result:", res["status"])""",
        "line_by_line": [
            {"line": "app.update_state(cfg, {'email_body': '...'})", "explanation": "Applies a state modification to the paused thread checkpoint."},
            {"line": "app.invoke(Command(resume=True), config=cfg)", "explanation": "Resumes the node with the newly updated email body."}
        ],
        "sample_input": {"configurable": {"thread_id": "email-thread-101"}},
        "sample_output": {"status": "SENT to client@enterprise.com: Dear Partner, Friendly reminder that invoice #402 is due this week. Thank you!"},
        "common_mistakes": [
            {"mistake": "Forgetting that update_state creates a new checkpoint snapshot.", "fix": "Always use the returned config or the original thread_id config to resume."}
        ],
        "hands_on_task": {
            "title": "Update recipient before sending",
            "instruction": "Use `app.update_state` to change `recipient` to `'billing@enterprise.com'`.",
            "starter_code": "app.update_state(cfg, {'recipient': 'billing@enterprise.com'})"
        },
        "quick_quiz": [
            {
                "question": "When can `app.update_state()` be called on a thread?",
                "options": [
                    "Only before the graph has ever been run",
                    "At any time, including when the graph is paused at an interrupt",
                    "Only after the graph has completely finished",
                    "Never; state cannot be modified externally"
                ],
                "correct_index": 1,
                "explanation": "app.update_state() can be called while a graph is paused to inject corrections or steer execution."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/interrupts",
        "prev_lesson_id": "m8-l2",
        "next_lesson_id": "m9-l1"
    },
    "m9-l1": {
        "id": "m9-l1",
        "module_id": "module-9",
        "module_title": "Module 9: Streaming Architecture & SSE",
        "title": "LangGraph Streaming Modes (values vs updates vs messages)",
        "difficulty": "Advanced",
        "estimated_minutes": 18,
        "prerequisites": ["m2-l3"],
        "objectives": [
            "Understand stream_mode='values' (full state snapshots)",
            "Understand stream_mode='updates' (incremental node returns)",
            "Understand stream_mode='messages' (real-time LLM token streaming)",
            "Use combined streaming modes: stream_mode=['updates', 'messages']"
        ],
        "simple_explanation": "LangGraph offers 4 core streaming modes: 1. `values`: yields the entire state snapshot after each super-step. 2. `updates`: yields only what the executing node returned. 3. `messages`: streams individual token chunks from chat models. 4. `custom`: emits arbitrary developer events via StreamWriter.",
        "why_it_matters": "Choosing the right stream mode powers responsive web UIs: you can display streaming token text in chat bubbles while simultaneously highlighting active graph nodes as super-steps progress.",
        "real_world_analogy": "Watching a football match: `values` is viewing the complete scoreboard after every play; `updates` is a notification of just the points scored on that play; `messages` is real-time audio commentary word-by-word.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  GraphExecution[Graph Super-Step Running] --> StreamChoice{Stream Mode}\n  StreamChoice -- 'values' --> FullSnap[\"Yields: {a: 1, b: 2, c: 3}\"]\n  StreamChoice -- 'updates' --> IncUpdate[\"Yields: {'node_a': {b: 2}}\"]\n  StreamChoice -- 'messages' --> TokenStream[\"Yields: ('AIMessageChunk', 'Hello ')\"]"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class StreamDemoState(TypedDict):
    query: str
    counter: int

def step_a(state: StreamDemoState) -> dict:
    return {"counter": state["counter"] + 10}

def step_b(state: StreamDemoState) -> dict:
    return {"counter": state["counter"] + 20}

builder = StateGraph(StreamDemoState)
builder.add_node("step_a", step_a)
builder.add_node("step_b", step_b)
builder.add_edge(START, "step_a")
builder.add_edge("step_a", "step_b")
builder.add_edge("step_b", END)

app = builder.compile()

print("=== 1. STREAM MODE: 'updates' (Default) ===")
for chunk in app.stream({"query": "demo", "counter": 0}, stream_mode="updates"):
    print("Update Chunk:", chunk)

print("\\n=== 2. STREAM MODE: 'values' ===")
for chunk in app.stream({"query": "demo", "counter": 0}, stream_mode="values"):
    print("Full Values Snapshot:", chunk)""",
        "line_by_line": [
            {"line": "app.stream(..., stream_mode='updates')", "explanation": "Yields {node_name: partial_dict} after each node finishes."},
            {"line": "app.stream(..., stream_mode='values')", "explanation": "Yields complete state dictionary after each super-step."}
        ],
        "sample_input": {"query": "demo", "counter": 0},
        "sample_output": {
            "updates": [{"step_a": {"counter": 10}}, {"step_b": {"counter": 30}}],
            "values": [{"counter": 0}, {"counter": 10}, {"counter": 30}]
        },
        "common_mistakes": [
            {"mistake": "Using stream_mode='messages' without an LLM that supports token streaming.", "fix": "Ensure the model is invoked with streaming enabled in the node."}
        ],
        "hands_on_task": {
            "title": "Test tuple stream mode",
            "instruction": "Try `stream_mode=['updates', 'values']` and unpack the `(mode, data)` tuples.",
            "starter_code": "for mode, data in app.stream(..., stream_mode=['updates', 'values']):\n    print(f'[{mode}]: {data}')"
        },
        "quick_quiz": [
            {
                "question": "Which stream_mode yields the entire state dictionary after every super-step?",
                "options": [
                    "stream_mode='messages'",
                    "stream_mode='values'",
                    "stream_mode='tokens'",
                    "stream_mode='nodes'"
                ],
                "correct_index": 1,
                "explanation": "stream_mode='values' emits the complete state snapshot after each super-step."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/streaming",
        "prev_lesson_id": "m8-l3",
        "next_lesson_id": "m9-l2"
    },
    "m9-l2": {
        "id": "m9-l2",
        "module_id": "module-9",
        "module_title": "Module 9: Streaming Architecture & SSE",
        "title": "Production SSE Streaming with FastAPI",
        "difficulty": "Advanced",
        "estimated_minutes": 22,
        "prerequisites": ["m9-l1"],
        "objectives": [
            "Build an async Server-Sent Events (SSE) FastAPI endpoint",
            "Stream graph super-steps and token chunks via sse_starlette",
            "Handle client disconnects and cancellation safely"
        ],
        "simple_explanation": "Server-Sent Events (SSE) provide a one-way HTTP connection from server to browser. With FastAPI and `EventSourceResponse`, you can stream JSON events as nodes execute in your LangGraph graph.",
        "why_it_matters": "SSE is much simpler and more firewall-friendly than WebSockets for LLM applications because communication is primarily server-to-client streaming.",
        "real_world_analogy": "Like a ticker tape or financial news wire: The server publishes news items as they happen, and your browser displays them in real time without refreshing.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "sequenceDiagram\n  participant UI as React Frontend (EventSource)\n  participant API as FastAPI /api/stream\n  participant LG as LangGraph astream()\n  UI->>API: POST /api/stream\n  API->>LG: app.astream(input, stream_mode='updates')\n  LG-->>API: Yields Step 1: node_a\n  API-->>UI: data: {\"event\": \"node_complete\", \"node\": \"node_a\"}\n  LG-->>API: Yields Step 2: node_b\n  API-->>UI: data: {\"event\": \"node_complete\", \"node\": \"node_b\"}\n  API-->>UI: data: {\"event\": \"done\"}"
        },
        "code_example": """import json
import asyncio
from fastapi import FastAPI, Request
from sse_starlette.sse import EventSourceResponse
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

app_api = FastAPI()

class PipelineState(TypedDict):
    text: str
    status: str

async def step_one(state: PipelineState) -> dict:
    await asyncio.sleep(0.5)  # Simulate processing
    return {"status": "Step 1 Completed: Data ingested"}

async def step_two(state: PipelineState) -> dict:
    await asyncio.sleep(0.5)
    return {"status": "Step 2 Completed: Analysis generated"}

builder = StateGraph(PipelineState)
builder.add_node("step_one", step_one)
builder.add_node("step_two", step_two)
builder.add_edge(START, "step_one")
builder.add_edge("step_one", "step_two")
builder.add_edge("step_two", END)

graph_app = builder.compile()

@app_api.get("/api/stream-graph")
async def stream_graph_endpoint(request: Request):
    async def event_generator():
        initial = {"text": "Process this data", "status": "STARTING"}
        try:
            async for step_chunk in graph_app.astream(initial, stream_mode="updates"):
                # Check for client disconnect
                if await request.is_disconnected():
                    print("Client disconnected, stopping stream.")
                    break
                    
                node_name = list(step_chunk.keys())[0]
                payload = {
                    "node": node_name,
                    "update": step_chunk[node_name]
                }
                yield {"event": "node_update", "data": json.dumps(payload)}
                
            yield {"event": "end", "data": json.dumps({"status": "SUCCESS"})}
        except Exception as e:
            yield {"event": "error", "data": json.dumps({"error": str(e)})}

    return EventSourceResponse(event_generator())""",
        "line_by_line": [
            {"line": "from sse_starlette.sse import EventSourceResponse", "explanation": "FastAPI SSE response wrapper for async generators."},
            {"line": "async for step_chunk in graph_app.astream(..., stream_mode='updates'):", "explanation": "Iterates asynchronously over super-step updates without blocking FastAPI event loop."},
            {"line": "if await request.is_disconnected(): break", "explanation": "Prevents wasted server computations if user closes the tab."}
        ],
        "sample_input": "GET /api/stream-graph",
        "sample_output": {
            "event 1": "node_update: {'node': 'step_one', 'update': {'status': 'Step 1 Completed: Data ingested'}}",
            "event 2": "node_update: {'node': 'step_two', 'update': {'status': 'Step 2 Completed: Analysis generated'}}",
            "event 3": "end: {'status': 'SUCCESS'}"
        },
        "common_mistakes": [
            {"mistake": "Using sync app.stream inside an async FastAPI route, blocking the worker thread.", "fix": "Always use `async for chunk in app.astream(...)` in async endpoint handlers."}
        ],
        "hands_on_task": {
            "title": "Add step progress percentage",
            "instruction": "Emit a `progress` integer (50%, 100%) in the SSE payload.",
            "starter_code": "payload['progress'] = 50 if node_name == 'step_one' else 100"
        },
        "quick_quiz": [
            {
                "question": "Why is checking `await request.is_disconnected()` important in SSE endpoints?",
                "options": [
                    "To prevent memory leaks and cancel graph execution if the user closes their browser",
                    "To reboot the web server",
                    "To increase CSS rendering speed",
                    "It is mandatory by the HTTP 1.1 spec"
                ],
                "correct_index": 0,
                "explanation": "Checking is_disconnected() allows the server to stop long-running graph workflows immediately when the user navigates away."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/streaming",
        "prev_lesson_id": "m9-l1",
        "next_lesson_id": "m10-l1"
    },
    "m10-l1": {
        "id": "m10-l1",
        "module_id": "module-10",
        "module_title": "Module 10: Subgraphs & Multi-Agent Architecture",
        "title": "Subgraphs as Nodes & State Isolation",
        "difficulty": "Advanced",
        "estimated_minutes": 20,
        "prerequisites": ["m4-l3"],
        "objectives": [
            "Compile independent subgraphs and embed them as nodes in parent graphs",
            "Understand shared state keys vs isolated child state schemas",
            "Transform parent state into child state and map child outputs back"
        ],
        "simple_explanation": "A subgraph is simply a compiled StateGraph added as a node to another StateGraph (`parent_builder.add_node('subgraph_node', child_graph)`). Subgraphs can share the same state schema or maintain their own isolated schema.",
        "why_it_matters": "Large enterprise systems with 50+ nodes become unmaintainable as a single flat graph. Subgraphs allow you to modularize domains (e.g. an Auth Subgraph, a Payment Subgraph, a Research Subgraph) with independent teams and tests.",
        "real_world_analogy": "Like a corporation: The Executive Board (Parent Graph) delegates a project to the Legal Department (Subgraph). Legal runs its internal 5-step contract review graph, and returns only the final approved contract to the Board.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TB\n  subgraph Parent[Parent Graph]\n    P_Start([START]) --> Planner[Planner Node]\n    Planner --> SubNode[Child Subgraph Node]\n    subgraph Child[Child Subgraph]\n      C_Start([START]) --> C1[Search Node] --> C2[Analyze Node] --> C_End([END])\n    end\n    SubNode --> Reporter[Reporter Node] --> P_End([END])\n  end"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# 1. Child Subgraph (Research Domain)
class ChildState(TypedDict):
    topic: str
    research_summary: str

def child_step_1(state: ChildState) -> dict:
    return {"research_summary": f"Raw data collected for {state['topic']}."}

def child_step_2(state: ChildState) -> dict:
    return {"research_summary": state["research_summary"] + " Verified with 3 sources."}

child_builder = StateGraph(ChildState)
child_builder.add_node("c1", child_step_1)
child_builder.add_node("c2", child_step_2)
child_builder.add_edge(START, "c1")
child_builder.add_edge("c1", "c2")
child_builder.add_edge("c2", END)
child_subgraph = child_builder.compile()

# 2. Parent Graph
class ParentState(TypedDict):
    topic: str
    research_summary: str
    final_report: str

def format_report_node(state: ParentState) -> dict:
    return {"final_report": f"=== EXECUTIVE REPORT ===\\n{state['research_summary']}"}

parent_builder = StateGraph(ParentState)
# Adding child_subgraph directly as a node!
parent_builder.add_node("research_dept", child_subgraph)
parent_builder.add_node("format_report", format_report_node)

parent_builder.add_edge(START, "research_dept")
parent_builder.add_edge("research_dept", "format_report")
parent_builder.add_edge("format_report", END)

parent_app = parent_builder.compile()

res = parent_app.invoke({"topic": "Quantum Encryption", "research_summary": "", "final_report": ""})
print(res["final_report"])""",
        "line_by_line": [
            {"line": "child_subgraph = child_builder.compile()", "explanation": "Compiles the independent child graph."},
            {"line": "parent_builder.add_node('research_dept', child_subgraph)", "explanation": "Registers the compiled subgraph runnable directly as a node in the parent graph."}
        ],
        "sample_input": {"topic": "Quantum Encryption", "research_summary": "", "final_report": ""},
        "sample_output": {
            "final_report": "=== EXECUTIVE REPORT ===\nRaw data collected for Quantum Encryption. Verified with 3 sources."
        },
        "common_mistakes": [
            {"mistake": "Adding the child builder (`child_builder`) instead of the compiled graph (`child_builder.compile()`).", "fix": "Always pass the compiled subgraph runnable to add_node."}
        ],
        "hands_on_task": {
            "title": "Add a validation node to child subgraph",
            "instruction": "Add a node `c3` in child subgraph that verifies facts before END.",
            "starter_code": "child_builder.add_node('c3', lambda s: {'research_summary': s['research_summary'] + ' [VERIFIED]'})"
        },
        "quick_quiz": [
            {
                "question": "Can a compiled StateGraph be added as a node inside another StateGraph?",
                "options": [
                    "No, LangGraph only supports flat graphs",
                    "Yes, compiled subgraphs can be registered directly with `parent_builder.add_node(name, child_graph)`",
                    "Only if both graphs use SQLite checkpointers",
                    "Only in Python 3.14"
                ],
                "correct_index": 1,
                "explanation": "Any compiled LangGraph Runnable can be added as a first-class node in another graph."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/subgraphs",
        "prev_lesson_id": "m9-l2",
        "next_lesson_id": "m10-l2"
    },
    "m10-l2": {
        "id": "m10-l2",
        "module_id": "module-10",
        "module_title": "Module 10: Subgraphs & Multi-Agent Architecture",
        "title": "Supervisor & Multi-Agent Collaboration Patterns",
        "difficulty": "Advanced",
        "estimated_minutes": 24,
        "prerequisites": ["m10-l1", "m6-l1"],
        "objectives": [
            "Build a Multi-Agent Supervisor pattern",
            "Delegate tasks to specialized worker agents (Researcher, Coder, Reviewer)",
            "Coordinate agent handoffs and prevent infinite ping-pong loops"
        ],
        "simple_explanation": "In the Supervisor pattern, a central Supervisor agent acts as a manager. It assesses the user request, delegates subtasks to specialist worker agents, collects their findings, and decides whether to consult another specialist or return the final answer.",
        "why_it_matters": "Single agents struggle with broad tasks requiring varied skills. Dividing responsibilities among dedicated specialist agents with scoped prompts produces far higher quality and reliability.",
        "real_world_analogy": "A general contractor building a house: The contractor (Supervisor) hires an electrician (Worker 1) and a plumber (Worker 2). The contractor reviews their work and gives the keys to the homeowner when everything is inspected.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  START([START]) --> Supervisor[Supervisor Agent]\n  Supervisor --> Router{Delegate To?}\n  Router -- 'researcher' --> ResearchAgent[Research Agent]\n  Router -- 'coder' --> CodeAgent[Coder Agent]\n  Router -- 'FINISH' --> END([END])\n  ResearchAgent --> Supervisor\n  CodeAgent --> Supervisor"
        },
        "code_example": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class MultiAgentState(TypedDict):
    task: str
    research_notes: str
    code_solution: str
    next_actor: str
    iterations: int

# Supervisor node decides which agent should act next
def supervisor_node(state: MultiAgentState) -> dict:
    iters = state.get("iterations", 0) + 1
    
    # Simple deterministic supervisor rules
    if not state.get("research_notes"):
        return {"next_actor": "researcher", "iterations": iters}
    elif not state.get("code_solution"):
        return {"next_actor": "coder", "iterations": iters}
    else:
        return {"next_actor": "FINISH", "iterations": iters}

def researcher_node(state: MultiAgentState) -> dict:
    return {"research_notes": f"Researched requirements for: {state['task']} (API endpoint needed)"}

def coder_node(state: MultiAgentState) -> dict:
    return {"code_solution": "def handler(req): return {'status': 'ok'}"}

def route_supervisor(state: MultiAgentState) -> Literal["researcher", "coder", "__end__"]:
    if state["next_actor"] == "researcher":
        return "researcher"
    elif state["next_actor"] == "coder":
        return "coder"
    return "__end__"

builder = StateGraph(MultiAgentState)
builder.add_node("supervisor", supervisor_node)
builder.add_node("researcher", researcher_node)
builder.add_node("coder", coder_node)

builder.add_edge(START, "supervisor")
builder.add_conditional_edges("supervisor", route_supervisor, {
    "researcher": "researcher",
    "coder": "coder",
    "__end__": END
})
builder.add_edge("researcher", "supervisor")  # Handoff back to supervisor
builder.add_edge("coder", "supervisor")       # Handoff back to supervisor

app = builder.compile()
res = app.invoke({"task": "Build health check API", "research_notes": "", "code_solution": "", "next_actor": "", "iterations": 0})
print("Final Multi-Agent Result:")
print("Research:", res["research_notes"])
print("Code:", res["code_solution"])
print("Total Super-Steps:", res["iterations"])""",
        "line_by_line": [
            {"line": "def route_supervisor(state: MultiAgentState) -> ...:", "explanation": "Supervisor routes control to specialist worker nodes or terminates at END."},
            {"line": "builder.add_edge('researcher', 'supervisor')", "explanation": "Ensures worker returns control back to supervisor for evaluation."}
        ],
        "sample_input": {"task": "Build health check API", "research_notes": "", "code_solution": "", "next_actor": "", "iterations": 0},
        "sample_output": {
            "research_notes": "Researched requirements for: Build health check API (API endpoint needed)",
            "code_solution": "def handler(req): return {'status': 'ok'}",
            "iterations": 3
        },
        "common_mistakes": [
            {"mistake": "Allowing workers to call each other directly without a clear supervisor or explicit handoff protocol, causing infinite loops.", "fix": "Route all transitions through the central supervisor or use structured handoff objects."}
        ],
        "hands_on_task": {
            "title": "Add a QA Tester Agent",
            "instruction": "Add a 'qa_tester' node that verifies the code before FINISH.",
            "starter_code": "def qa_tester(state: MultiAgentState) -> dict:\n    return {'qa_verdict': 'PASSED'}"
        },
        "quick_quiz": [
            {
                "question": "In the Supervisor Multi-Agent pattern, what is the role of the supervisor node?",
                "options": [
                    "It executes all Python tools itself",
                    "It analyzes state and orchestrates delegation to specialist worker nodes",
                    "It only handles database backups",
                    "It replaces the checkpointer"
                ],
                "correct_index": 1,
                "explanation": "The supervisor assesses the current state and delegates to specialized worker nodes until the goal is satisfied."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/subgraphs",
        "prev_lesson_id": "m10-l1",
        "next_lesson_id": "m11-l1"
    },
    "m11-l1": {
        "id": "m11-l1",
        "module_id": "module-11",
        "module_title": "Module 11: Functional API (@entrypoint & @task)",
        "title": "The Functional API: @entrypoint & @task",
        "difficulty": "Advanced",
        "estimated_minutes": 18,
        "prerequisites": ["m2-l1"],
        "objectives": [
            "Understand the Functional API as an alternative to StateGraph",
            "Use @entrypoint to define workflow boundaries",
            "Use @task to declare independently checkpointed subtasks",
            "Know when to choose Functional API vs StateGraph"
        ],
        "simple_explanation": "In addition to the graph-based `StateGraph`, LangGraph provides the Functional API. With `@entrypoint` and `@task`, you write standard Python code (if-statements, for-loops, function calls) while still getting checkpointing, interrupts, and time travel.",
        "why_it_matters": "If your workflow looks like ordinary procedural Python logic, the Functional API feels much more natural than declaring node and edge objects explicitly.",
        "real_world_analogy": "Graph API is like building a custom circuit board (nodes & wires). Functional API is like writing a standard recipe script where special ingredients are tagged with `@task` for auto-saving.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Entry[\"@entrypoint workflow(input)\"] --> Task1[\"@task fetch_data(input)\"]\n  Task1 --> Task2[\"@task transform_data(data)\"]\n  Task2 --> ReturnVal[\"Return final result\"]"
        },
        "code_example": """from langgraph.func import entrypoint, task
from langgraph.checkpoint.memory import MemorySaver

# 1. Define modular tasks (each task is checkpointed)
@task
def step_a(val: int) -> int:
    print(f"Executing Task A on {val}")
    return val * 2

@task
def step_b(val: int) -> int:
    print(f"Executing Task B on {val}")
    return val + 100

# 2. Define the main workflow entrypoint
@entrypoint(checkpointer=MemorySaver())
def math_workflow(initial_val: int) -> int:
    # Standard Python imperative logic!
    # Tasks return Futures; .result() waits for completion
    res_a = step_a(initial_val).result()
    if res_a > 10:
        res_b = step_b(res_a).result()
        return res_b
    return res_a

# Invoke workflow
config = {"configurable": {"thread_id": "func-thread-1"}}
out = math_workflow.invoke(8, config=config)
print("Functional Workflow Output:", out)""",
        "line_by_line": [
            {"line": "from langgraph.func import entrypoint, task", "explanation": "Imports the functional workflow decorators."},
            {"line": "@task def step_a(val: int) -> int:", "explanation": "Marks function as an atomic checkpointed task."},
            {"line": "step_a(initial_val).result()", "explanation": "Executes task and resolves its future result."}
        ],
        "sample_input": 8,
        "sample_output": 116,
        "common_mistakes": [
            {"mistake": "Calling a `@task` function without `.result()` when you need its return value in synchronous entrypoints.", "fix": "Call `.result()` on the task future to retrieve the actual return value."}
        ],
        "hands_on_task": {
            "title": "Add Task C to functional workflow",
            "instruction": "Create `@task def step_c(val: int) -> str` that formats the number as currency.",
            "starter_code": "@task\ndef step_c(val: int) -> str:\n    return f'${val:,.2f}'"
        },
        "quick_quiz": [
            {
                "question": "What is the primary benefit of the Functional API (@entrypoint / @task)?",
                "options": [
                    "It allows writing procedural Python workflows with standard control flow while preserving LangGraph persistence and interrupts",
                    "It eliminates the need for Python",
                    "It only works in browser JavaScript",
                    "It disables checkpointing"
                ],
                "correct_index": 0,
                "explanation": "The Functional API provides the durability and interrupts of LangGraph without needing to explicitly construct a graph structure."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m10-l2",
        "next_lesson_id": "m11-l2"
    },
    "m11-l2": {
        "id": "m11-l2",
        "module_id": "module-11",
        "module_title": "Module 11: Functional API (@entrypoint & @task)",
        "title": "Checkpoints & Interrupts in Functional Workflows",
        "difficulty": "Advanced",
        "estimated_minutes": 18,
        "prerequisites": ["m11-l1", "m7-l1", "m8-l1"],
        "objectives": [
            "Use interrupt() inside an @entrypoint functional workflow",
            "Resume functional workflows with Command(resume=...)",
            "Understand task caching and replay in functional workflows"
        ],
        "simple_explanation": "Just like StateGraph, functional `@entrypoint` workflows support `interrupt(payload)`. When resumed, completed `@task` results are read directly from cache so previous tasks are NOT re-executed!",
        "why_it_matters": "Task caching prevents re-running expensive API calls or database operations when resuming a paused workflow.",
        "real_world_analogy": "Like building a Lego set: If you pause to ask a question, you don't dismantle the first 4 modules when you resume; you continue right from step 5.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "sequenceDiagram\n  autonumber\n  participant C as Caller\n  participant E as @entrypoint Workflow\n  participant T as @task (Cached)\n  C->>E: workflow.invoke(data)\n  E->>T: Run task 1 -> returns data\n  E->>E: calls interrupt('Confirm?')\n  E-->>C: Paused!\n  C->>E: workflow.invoke(Command(resume=True))\n  Note over E,T: Task 1 loaded from cache (NOT re-run!)\n  E-->>C: Workflow Completed"
        },
        "code_example": """from langgraph.func import entrypoint, task
from langgraph.types import interrupt, Command
from langgraph.checkpoint.memory import MemorySaver

@task
def calculate_quote(item: str) -> float:
    print(f"--> Calculating price for {item} (EXPENSIVE DB QUERY)")
    return 1250.00

@entrypoint(checkpointer=MemorySaver())
def quote_workflow(item: str) -> str:
    price = calculate_quote(item).result()
    
    # Pause for customer approval
    approved = interrupt({"item": item, "price": price})
    
    if approved:
        return f"Order confirmed for {item} at ${price}."
    return "Order cancelled by customer."

cfg = {"configurable": {"thread_id": "quote-99"}}

# First run: calculates quote and interrupts
print("--- FIRST RUN ---")
quote_workflow.invoke("Industrial 3D Printer", config=cfg)

# Second run: Resumes! Notice calculate_quote is NOT re-run!
print("\\n--- RESUMING WITH APPROVAL ---")
res = quote_workflow.invoke(Command(resume=True), config=cfg)
print("Result:", res)""",
        "line_by_line": [
            {"line": "approved = interrupt({'item': item, 'price': price})", "explanation": "Pauses the functional workflow and yields the interrupt payload."},
            {"line": "quote_workflow.invoke(Command(resume=True), config=cfg)", "explanation": "Resumes the workflow, loading completed task outputs from cache."}
        ],
        "sample_input": "Industrial 3D Printer",
        "sample_output": "Order confirmed for Industrial 3D Printer at $1250.0.",
        "common_mistakes": [
            {"mistake": "Placing non-deterministic side-effects (like generating random UUIDs) directly in the @entrypoint body without wrapping in @task.", "fix": "Always wrap side-effects and external calls in @task so their outputs are cached during resume."}
        ],
        "hands_on_task": {
            "title": "Test rejection in functional workflow",
            "instruction": "Resume with `Command(resume=False)` and verify 'Order cancelled' output.",
            "starter_code": "quote_workflow.invoke(Command(resume=False), config=cfg)"
        },
        "quick_quiz": [
            {
                "question": "What happens to completed `@task` functions when an `@entrypoint` resumes from an interrupt?",
                "options": [
                    "They are re-executed from scratch",
                    "Their results are retrieved from the checkpoint cache and NOT re-executed",
                    "They are deleted",
                    "They raise an error"
                ],
                "correct_index": 1,
                "explanation": "LangGraph caches completed task outputs in checkpoints, skipping re-execution during resume."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m11-l1",
        "next_lesson_id": "m12-l1"
    },
    "m12-l1": {
        "id": "m12-l1",
        "module_id": "module-12",
        "module_title": "Module 12: RAG & Advanced Retrieval Patterns",
        "title": "Corrective RAG (CRAG) Architecture",
        "difficulty": "Production",
        "estimated_minutes": 22,
        "prerequisites": ["m4-l2", "m5-l1"],
        "objectives": [
            "Build Corrective RAG (CRAG) graphs with document grading nodes",
            "Implement automated query rewriting when retrieval score is low",
            "Fallback gracefully to web search or domain knowledge"
        ],
        "simple_explanation": "Standard RAG blindly passes whatever documents were retrieved to the LLM. Corrective RAG (CRAG) inserts a 'Document Grader' node. If retrieved documents are irrelevant, the graph rewrites the query and searches again or falls back to web search before generating an answer.",
        "why_it_matters": "CRAG drastically reduces hallucinations by filtering out noise before the LLM generates an answer.",
        "real_world_analogy": "A researcher fact-checking sources: If the library books returned are irrelevant to the topic, the researcher rephrases the query and searches the digital archives instead of writing a paper using bad sources.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  START([START]) --> Retrieve[Retrieve Documents Node]\n  Retrieve --> Grade[Grade Documents Node]\n  Grade --> Decision{All Relevant?}\n  Decision -- Yes --> Generate[Generate Grounded Answer]\n  Decision -- No --> Rewrite[Rewrite Query Node] --> WebSearch[Fallback Search] --> Generate\n  Generate --> END([END])"
        },
        "code_example": """from typing import TypedDict, Literal
from langgraph.graph import StateGraph, START, END

class CRAGState(TypedDict):
    question: str
    documents: list[str]
    is_relevant: bool
    rewritten_query: str
    generation: str

def retrieve_node(state: CRAGState) -> dict:
    q = state["question"].lower()
    # Simulated vector store lookup
    if "langgraph" in q:
        docs = ["LangGraph is a library for building stateful multi-agent workflows with LLMs."]
    else:
        docs = ["Irrelevant document about unrelated gardening tips."]
    return {"documents": docs}

def grade_documents_node(state: CRAGState) -> dict:
    docs = state["documents"]
    q = state["question"].lower()
    # Grade document relevance
    relevant = any("langgraph" in d.lower() for d in docs)
    return {"is_relevant": relevant}

def decide_to_generate(state: CRAGState) -> Literal["generate_node", "rewrite_node"]:
    return "generate_node" if state["is_relevant"] else "rewrite_node"

def rewrite_query_node(state: CRAGState) -> dict:
    return {
        "rewritten_query": f"LangGraph framework: {state['question']}",
        "documents": ["Web search result: LangGraph provides cyclically orchestrated agent state."]
    }

def generate_answer_node(state: CRAGState) -> dict:
    doc_context = " ".join(state["documents"])
    return {"generation": f"Answer based on verified sources: {doc_context}"}

builder = StateGraph(CRAGState)
builder.add_node("retrieve", retrieve_node)
builder.add_node("grade", grade_documents_node)
builder.add_node("rewrite", rewrite_query_node)
builder.add_node("generate", generate_answer_node)

builder.add_edge(START, "retrieve")
builder.add_edge("retrieve", "grade")
builder.add_conditional_edges("grade", decide_to_generate, {
    "generate_node": "generate",
    "rewrite_node": "rewrite"
})
builder.add_edge("rewrite", "generate")
builder.add_edge("generate", END)

app = builder.compile()

print("1. Direct relevant query:")
print(app.invoke({"question": "What is LangGraph?", "documents": [], "is_relevant": False, "rewritten_query": "", "generation": ""})["generation"])

print("\\n2. Ambiguous query requiring query rewrite:")
print(app.invoke({"question": "Tell me about state machines", "documents": [], "is_relevant": False, "rewritten_query": "", "generation": ""})["generation"])""",
        "line_by_line": [
            {"line": "builder.add_conditional_edges('grade', decide_to_generate, ...)", "explanation": "Directs flow to answer generation if documents pass grading, or query rewrite if not."},
            {"line": "builder.add_edge('rewrite', 'generate')", "explanation": "Feeds corrected context into generator."}
        ],
        "sample_input": {"question": "Tell me about state machines"},
        "sample_output": {
            "generation": "Answer based on verified sources: Web search result: LangGraph provides cyclically orchestrated agent state."
        },
        "common_mistakes": [
            {"mistake": "Sending raw unranked documents directly to LLM generation without validation.", "fix": "Insert a grading node to filter or rewrite queries before final answer generation."}
        ],
        "hands_on_task": {
            "title": "Add Hallucination Grader Node",
            "instruction": "Create a node that checks if the generated answer is grounded in the documents.",
            "starter_code": "def check_hallucination(state: CRAGState) -> dict:\n    # Return groundedness score\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What is the primary role of the Document Grader node in Corrective RAG (CRAG)?",
                "options": [
                    "To evaluate whether retrieved context is truly relevant to the query before generating an answer",
                    "To format Markdown tables",
                    "To translate documents to French",
                    "To delete outdated files from disk"
                ],
                "correct_index": 0,
                "explanation": "The Document Grader filters out irrelevant retrieval results, triggering query rewriting or web search fallback when needed."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m11-l2",
        "next_lesson_id": "m12-l2"
    },
    "m12-l2": {
        "id": "m12-l2",
        "module_id": "module-12",
        "module_title": "Module 12: RAG & Advanced Retrieval Patterns",
        "title": "Self-RAG: Hallucination & Answer Quality Grading",
        "difficulty": "Production",
        "estimated_minutes": 22,
        "prerequisites": ["m12-l1"],
        "objectives": [
            "Implement self-reflection and groundedness checks on LLM answers",
            "Route back to generation if hallucinations are detected",
            "Set finite loop bounds to guarantee termination"
        ],
        "simple_explanation": "Self-RAG adds self-reflection loops. After generating an answer, a 'Hallucination Checker' node verifies if every claim is grounded in the retrieved documents. If not, it loops back to regenerate with stricter grounding.",
        "why_it_matters": "Enterprise compliance requires zero-hallucination guarantees for medical, legal, and financial queries.",
        "real_world_analogy": "An author and an editor: The author writes the chapter (Generator), the editor checks citations (Hallucination Checker). If a fact is unverified, the editor sends it back for revision.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Generate[Generate Answer Node] --> CheckHallucination{Is Grounded?}\n  CheckHallucination -- No & Retries < 2 --> Generate\n  CheckHallucination -- Yes or Max Retries --> END([END])"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class SelfRAGState(TypedDict):
    context: str
    answer: str
    grounded_score: float
    retries: int

def generate_grounded_answer(state: SelfRAGState) -> dict:
    r = state.get("retries", 0) + 1
    # Simulate first attempt hallucinating, second attempt grounded
    if r == 1:
        ans = "LangGraph was released in 1995 for Windows 95."  # Hallucination!
    else:
        ans = "LangGraph is an open-source library for building stateful agent workflows."
    return {"answer": ans, "retries": r}

def grade_groundedness(state: SelfRAGState) -> dict:
    ans = state["answer"]
    # Check if answer aligns with context
    if "1995" in ans:
        score = 0.2
    else:
        score = 0.98
    return {"grounded_score": score}

def route_hallucination(state: SelfRAGState) -> str:
    if state["grounded_score"] >= 0.8 or state["retries"] >= 2:
        return "approved"
    return "regenerate"

builder = StateGraph(SelfRAGState)
builder.add_node("generate", generate_grounded_answer)
builder.add_node("grader", grade_groundedness)

builder.add_edge(START, "generate")
builder.add_edge("generate", "grader")
builder.add_conditional_edges("grader", route_hallucination, {
    "regenerate": "generate",
    "approved": END
})

app = builder.compile()
res = app.invoke({"context": "LangGraph agent library", "answer": "", "grounded_score": 0.0, "retries": 0})
print("Final Grounded Answer:", res["answer"])
print("Final Grounded Score:", res["grounded_score"])
print("Total Generations:", res["retries"])""",
        "line_by_line": [
            {"line": "builder.add_conditional_edges('grader', route_hallucination, ...)", "explanation": "Creates self-correcting cycle between generation and grading until groundedness threshold is achieved."}
        ],
        "sample_input": {"context": "LangGraph agent library", "answer": "", "grounded_score": 0.0, "retries": 0},
        "sample_output": {
            "answer": "LangGraph is an open-source library for building stateful agent workflows.",
            "grounded_score": 0.98,
            "retries": 2
        },
        "common_mistakes": [
            {"mistake": "Creating an infinite self-reflection loop by not bounding retries count.", "fix": "Always check `or state['retries'] >= max_limit` in the routing function."}
        ],
        "hands_on_task": {
            "title": "Add context relevance score",
            "instruction": "Add a field `usefulness_score: float` to evaluate if the answer actually answers the user's prompt.",
            "starter_code": "return {'grounded_score': score, 'usefulness_score': 0.95}"
        },
        "quick_quiz": [
            {
                "question": "What is the primary objective of Self-RAG reflection loops?",
                "options": [
                    "To evaluate and self-correct hallucinations before output is shown to the user",
                    "To generate random images",
                    "To compress database tables",
                    "To encrypt user passwords"
                ],
                "correct_index": 0,
                "explanation": "Self-RAG uses evaluation nodes to grade whether LLM generations are factually grounded in retrieved source documents."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m12-l1",
        "next_lesson_id": "m13-l1"
    },
    "m13-l1": {
        "id": "m13-l1",
        "module_id": "module-13",
        "module_title": "Module 13: Reliability, Testing & Production",
        "title": "Retry Policies, Timeouts & Error Boundaries",
        "difficulty": "Production",
        "estimated_minutes": 18,
        "prerequisites": ["m2-l2"],
        "objectives": [
            "Configure langgraph.prebuilt.RetryPolicy on specific nodes",
            "Set exponential backoff, retry limits, and exception filters",
            "Implement graceful degradation fallbacks"
        ],
        "simple_explanation": "Network requests and external APIs fail unpredictably. LangGraph allows you to attach a `RetryPolicy(max_attempts=3, initial_interval=1.0, backoff_factor=2.0)` directly to individual nodes. If the node raises a transient error, LangGraph automatically retries with exponential backoff before failing.",
        "why_it_matters": "Without retry policies, a 200ms network blip fails an entire user transaction. With retry policies, transient errors heal transparently.",
        "real_world_analogy": "Redialing a busy phone number: You wait 1 second, redial; wait 2 seconds, redial; wait 4 seconds, redial. If still busy after 3 tries, you leave a voicemail (fallback).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Node[Node executes] --> Error{Transient Network Error?}\n  Error -- RetryPolicy: Attempt < 3 -- Exponential Backoff --> Node\n  Error -- Attempts Exhausted --> Fallback[Fallback Node]\n  Error -- No Error --> NextNode[Next Node]"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.types import RetryPolicy

class APICallState(TypedDict):
    endpoint: str
    data: dict
    attempts_made: int

call_count = 0

def flakey_api_node(state: APICallState) -> dict:
    global call_count
    call_count += 1
    print(f"API Call Attempt #{call_count}...")
    if call_count < 3:
        raise ConnectionResetError("Connection reset by remote peer (transient network glitch)")
    return {"data": {"user_id": 101, "name": "Alice"}, "attempts_made": call_count}

builder = StateGraph(APICallState)

# Attach RetryPolicy to flakey_api_node!
builder.add_node(
    "fetch_api",
    flakey_api_node,
    retry=RetryPolicy(
        max_attempts=4,
        initial_interval=0.1,
        backoff_factor=2.0,
        retry_on=(ConnectionResetError, TimeoutError)
    )
)

builder.add_edge(START, "fetch_api")
builder.add_edge("fetch_api", END)

app = builder.compile()
result = app.invoke({"endpoint": "https://api.internal/users", "data": {}, "attempts_made": 0})
print("Success after retries:", result)""",
        "line_by_line": [
            {"line": "from langgraph.types import RetryPolicy", "explanation": "Imports the official RetryPolicy configuration class."},
            {"line": "retry=RetryPolicy(max_attempts=4, initial_interval=0.1, backoff_factor=2.0, retry_on=...)", "explanation": "Configures automatic exponential backoff retries for specific exception types."}
        ],
        "sample_input": {"endpoint": "https://api.internal/users", "data": {}, "attempts_made": 0},
        "sample_output": {"data": {"user_id": 101, "name": "Alice"}, "attempts_made": 3},
        "common_mistakes": [
            {"mistake": "Retrying non-transient errors like `ValueError('invalid syntax')` or authentication errors.", "fix": "Specify `retry_on=(ConnectionError, TimeoutError, RateLimitError)` so code bugs fail fast."}
        ],
        "hands_on_task": {
            "title": "Configure jitter",
            "instruction": "Add `jitter=True` to RetryPolicy to prevent thundering herd problems in production.",
            "starter_code": "retry=RetryPolicy(max_attempts=3, jitter=True)"
        },
        "quick_quiz": [
            {
                "question": "What is the effect of setting `backoff_factor=2.0` in a `RetryPolicy`?",
                "options": [
                    "It doubles the wait duration between consecutive retry attempts",
                    "It doubles the CPU usage",
                    "It retries twice as many nodes",
                    "It halves the timeout"
                ],
                "correct_index": 0,
                "explanation": "backoff_factor=2.0 applies exponential backoff, doubling the delay after each failed attempt."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m12-l2",
        "next_lesson_id": "m13-l2"
    },
    "m13-l2": {
        "id": "m13-l2",
        "module_id": "module-13",
        "module_title": "Module 13: Reliability, Testing & Production",
        "title": "Unit & Integration Testing of LangGraph Workflows",
        "difficulty": "Production",
        "estimated_minutes": 20,
        "prerequisites": ["m2-l3", "m7-l1"],
        "objectives": [
            "Write deterministic unit tests for node functions and router functions with pytest",
            "Mock LLM responses for fast, zero-cost continuous integration (CI)",
            "Test interrupted execution flows and checkpoint assertions"
        ],
        "simple_explanation": "Testing AI graphs requires isolating deterministic node logic, mocking LLM tool calls, and asserting state transitions across super-steps using standard `pytest` fixtures.",
        "why_it_matters": "Real LLM calls are slow, expensive, and non-deterministic. Mock testing guarantees that routing logic, state schemas, and error boundaries work reliably before deploying to production.",
        "real_world_analogy": "Crash testing cars in a simulator before building the physical vehicle: You test the brakes, steering, and airbags under thousands of simulated scenarios in seconds.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph LR\n  Test[pytest test_graph.py] --> Mock[Mock LLM Fixture]\n  Mock --> Graph[Compiled StateGraph]\n  Graph --> Assert[Assert final_state['status'] == 'APPROVED']"
        },
        "code_example": """import pytest
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

class OrderState(TypedDict):
    item_id: str
    quantity: int
    total_price: float
    status: str

def calculate_price_node(state: OrderState) -> dict:
    unit_price = 25.0
    return {"total_price": state["quantity"] * unit_price}

def validate_inventory_node(state: OrderState) -> dict:
    if state["quantity"] > 100:
        return {"status": "BACKORDERED"}
    return {"status": "IN_STOCK"}

def build_order_graph():
    builder = StateGraph(OrderState)
    builder.add_node("calc", calculate_price_node)
    builder.add_node("inventory", validate_inventory_node)
    builder.add_edge(START, "calc")
    builder.add_edge("calc", "inventory")
    builder.add_edge("inventory", END)
    return builder.compile()

# === PYTEST TEST CASES ===
def test_order_in_stock():
    app = build_order_graph()
    res = app.invoke({"item_id": "SKU-1", "quantity": 4, "total_price": 0.0, "status": ""})
    assert res["total_price"] == 100.0
    assert res["status"] == "IN_STOCK"

def test_order_backordered():
    app = build_order_graph()
    res = app.invoke({"item_id": "SKU-2", "quantity": 150, "total_price": 0.0, "status": ""})
    assert res["total_price"] == 3750.0
    assert res["status"] == "BACKORDERED"

# Run tests
test_order_in_stock()
test_order_backordered()
print("All unit test assertions PASSED successfully!")""",
        "line_by_line": [
            {"line": "def test_order_in_stock():", "explanation": "Standard pytest function asserting graph output correctness."},
            {"line": "assert res['total_price'] == 100.0", "explanation": "Verifies state transition and computation accuracy."}
        ],
        "sample_input": {"item_id": "SKU-1", "quantity": 4, "total_price": 0.0, "status": ""},
        "sample_output": {"item_id": "SKU-1", "quantity": 4, "total_price": 100.0, "status": "IN_STOCK"},
        "common_mistakes": [
            {"mistake": "Running live LLM API calls in CI test suites, causing high bills and flaky tests.", "fix": "Use deterministic mock model outputs or mock node fixtures in test suites."}
        ],
        "hands_on_task": {
            "title": "Write a test for negative quantity",
            "instruction": "Write a test asserting that negative quantity raises ValueError.",
            "starter_code": "def test_negative_quantity():\n    # assert error\n    pass"
        },
        "quick_quiz": [
            {
                "question": "What is the recommended best practice for testing LangGraph workflows in CI/CD pipelines?",
                "options": [
                    "Always make live $50 API calls to OpenAI",
                    "Use pytest with deterministic mock models to test node logic, routing branches, and state schemas without external API dependencies",
                    "Never write tests for AI graphs",
                    "Test only by clicking in the browser UI"
                ],
                "correct_index": 1,
                "explanation": "Mocking external models allows fast, deterministic, free testing of graph routing logic in CI pipelines."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/test",
        "prev_lesson_id": "m13-l1",
        "next_lesson_id": "m13-l3"
    },
    "m13-l3": {
        "id": "m13-l3",
        "module_id": "module-13",
        "module_title": "Module 13: Reliability, Testing & Production",
        "title": "LangSmith Tracing, Observability & Deployment",
        "difficulty": "Production",
        "estimated_minutes": 18,
        "prerequisites": ["m13-l1"],
        "objectives": [
            "Enable zero-config LangSmith tracing with environment variables",
            "Inspect super-step execution run trees, token latencies, and state channels",
            "Tag graph invocations with user IDs and metadata for production analytics"
        ],
        "simple_explanation": "LangSmith provides complete observability for LangGraph. By setting `LANGCHAIN_TRACING_V2=true` and `LANGCHAIN_API_KEY=...`, every graph invocation, node execution, LLM call, and tool execution is automatically recorded in a visual trace tree.",
        "why_it_matters": "In production, when a user reports 'the agent answered incorrectly 2 hours ago', LangSmith lets you pull up the exact run tree, view the inputs/outputs of every node, and diagnose the root cause in seconds.",
        "real_world_analogy": "A flight data recorder (black box) for an aircraft: It records all instrument readings, control inputs, and engine states so engineers can analyze flight performance.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  Run[app.invoke(input, config=tags)] --> Tree[LangSmith Trace Tree]\n  Tree --> S1[Super-Step 1: Router Node]\n  Tree --> S2[Super-Step 2: ToolNode - 142ms, 230 tokens]\n  Tree --> S3[Super-Step 3: Response Generator - 450ms, 510 tokens]"
        },
        "code_example": """import os
from typing import TypedDict
from langgraph.graph import StateGraph, START, END

# Configure LangSmith Environment Variables:
# os.environ["LANGCHAIN_TRACING_V2"] = "true"
# os.environ["LANGCHAIN_API_KEY"] = "lsv2_pt_..."
# os.environ["LANGCHAIN_PROJECT"] = "graphlab-production"

class ObservabilityState(TypedDict):
    query: str
    answer: str

def processing_node(state: ObservabilityState) -> dict:
    return {"answer": f"Processed '{state['query']}' with full trace telemetry."}

builder = StateGraph(ObservabilityState)
builder.add_node("process", processing_node)
builder.add_edge(START, "process")
builder.add_edge("process", END)

app = builder.compile()

# Tag run with user metadata for LangSmith filtering
config = {
    "tags": ["production", "tier-enterprise"],
    "metadata": {
        "user_id": "usr_9981",
        "organization": "AcmeCorp",
        "environment": "production"
    }
}

res = app.invoke({"query": "Generate Q3 Financial Summary", "answer": ""}, config=config)
print("Result with observability tags:", res)""",
        "line_by_line": [
            {"line": "config = {'tags': ['production'], 'metadata': {'user_id': 'usr_9981'}}", "explanation": "Attaches searchable tags and metadata to the LangSmith trace run tree."}
        ],
        "sample_input": {"query": "Generate Q3 Financial Summary", "answer": ""},
        "sample_output": {"query": "Generate Q3 Financial Summary", "answer": "Processed 'Generate Q3 Financial Summary' with full trace telemetry."},
        "common_mistakes": [
            {"mistake": "Committing LangSmith API keys or secrets directly in source code.", "fix": "Always load API keys from environment variables or .env files."}
        ],
        "hands_on_task": {
            "title": "Add latency monitoring tag",
            "instruction": "Add `'monitor_sla': True` to the metadata dictionary.",
            "starter_code": "config['metadata']['monitor_sla'] = True"
        },
        "quick_quiz": [
            {
                "question": "How do you attach custom searchable metadata (like user_id) to a LangGraph execution in LangSmith?",
                "options": [
                    "By writing to a CSV file",
                    "By passing `metadata={'user_id': '...'}` inside `config` during invocation",
                    "By renaming node functions",
                    "By restarting the server"
                ],
                "correct_index": 1,
                "explanation": "LangGraph passes `config['metadata']` directly to LangSmith as indexed attributes for filtering and analytics."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
        "prev_lesson_id": "m13-l2",
        "next_lesson_id": "m14-l1"
    },
    "m14-l1": {
        "id": "m14-l1",
        "module_id": "module-14",
        "module_title": "Module 14: Advanced Internals & Reference",
        "title": "Deep Dive: The Pregel Engine & Super-Steps",
        "difficulty": "Production",
        "estimated_minutes": 20,
        "prerequisites": ["m1-l3", "m4-l3"],
        "objectives": [
            "Understand the Pregel synchronization barrier lifecycle",
            "Learn how state channels manage write queues and reducers",
            "Understand why in-place mutations violate Pregel determinism"
        ],
        "simple_explanation": "Pregel organizes execution into discrete rounds. In Round N, all triggered nodes read immutable channel snapshots, execute concurrently, and push update packets to a writer queue. At the synchronization barrier, LangGraph drains the queues, applies reducer functions, persists the new checkpoint, and activates Round N+1 nodes.",
        "why_it_matters": "Knowing the Pregel engine internals allows you to design high-throughput graphs with zero race conditions and understand exactly how parallel fan-out/fan-in behaves under high load.",
        "real_world_analogy": "Like a central stock exchange clearing house: Orders are submitted throughout the trading session (nodes write updates), and at market close, all trades are settled atomically in a single clearing batch (synchronization barrier).",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TB\n  subgraph SuperStep[Pregel Super-Step N]\n    Read[1. Read Channel Snapshots] --> Exec[2. Concurrent Node Executions]\n    Exec --> Queue[3. Write Packets to Channel Queues]\n    Queue --> Barrier[4. Synchronization Barrier: Apply Reducers]\n    Barrier --> Checkpoint[5. Persist Checkpoint Snapshot]\n  end\n  Checkpoint --> NextStep[Super-Step N+1 Begins]"
        },
        "code_example": """# Demonstrating Pregel channel synchronization mechanics
from typing import TypedDict, Annotated
import operator
from langgraph.graph import StateGraph, START, END

class PregelDemoState(TypedDict):
    # Channel with list append reducer
    messages_channel: Annotated[list[str], operator.add]
    # Channel with default overwrite
    status_channel: str

def worker_alpha(state: PregelDemoState) -> dict:
    # Sees state from start of super-step
    return {"messages_channel": ["Alpha finished"], "status_channel": "ALPHA_DONE"}

def worker_beta(state: PregelDemoState) -> dict:
    # Sees the exact same state from start of super-step
    return {"messages_channel": ["Beta finished"]}

def barrier_aggregator(state: PregelDemoState) -> dict:
    # Runs in next super-step after both alpha and beta writes are merged
    return {"status_channel": f"MERGED: {len(state['messages_channel'])} items"}

builder = StateGraph(PregelDemoState)
builder.add_node("alpha", worker_alpha)
builder.add_node("beta", worker_beta)
builder.add_node("aggregator", barrier_aggregator)

# Parallel execution in Super-step 1
builder.add_edge(START, "alpha")
builder.add_edge(START, "beta")

# Fan-in to aggregator in Super-step 2
builder.add_edge("alpha", "aggregator")
builder.add_edge("beta", "aggregator")
builder.add_edge("aggregator", END)

app = builder.compile()
res = app.invoke({"messages_channel": ["Initial"], "status_channel": "START"})
print("Channel Final State:", res)""",
        "line_by_line": [
            {"line": "builder.add_edge(START, 'alpha'); builder.add_edge(START, 'beta')", "explanation": "Both nodes execute concurrently in Super-step 1 against identical initial state snapshots."},
            {"line": "builder.add_edge('alpha', 'aggregator'); builder.add_edge('beta', 'aggregator')", "explanation": "Pregel waits for both workers to finish before executing aggregator in Super-step 2."}
        ],
        "sample_input": {"messages_channel": ["Initial"], "status_channel": "START"},
        "sample_output": {
            "messages_channel": ["Initial", "Alpha finished", "Beta finished"],
            "status_channel": "MERGED: 3 items"
        },
        "common_mistakes": [
            {"mistake": "Assuming worker_beta can read what worker_alpha wrote in the same super-step.", "fix": "Remember that nodes in the same super-step only see state from the beginning of that super-step."}
        ],
        "hands_on_task": {
            "title": "Add a third parallel worker gamma",
            "instruction": "Add `worker_gamma` and verify all 3 parallel updates merge cleanly in the reducer.",
            "starter_code": "builder.add_node('gamma', lambda s: {'messages_channel': ['Gamma finished']})"
        },
        "quick_quiz": [
            {
                "question": "What happens at the Pregel synchronization barrier at the end of a super-step?",
                "options": [
                    "All pending node writes are drained from queues and merged into state channels using configured reducers",
                    "The graph pauses for 10 seconds",
                    "All memory is wiped",
                    "An error is thrown"
                ],
                "correct_index": 0,
                "explanation": "The synchronization barrier applies all channel writes atomically and updates the checkpoint snapshot before the next super-step."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/graph-api",
        "prev_lesson_id": "m13-l3",
        "next_lesson_id": "m14-l2"
    },
    "m14-l2": {
        "id": "m14-l2",
        "module_id": "module-14",
        "module_title": "Module 14: Advanced Internals & Reference",
        "title": "Mastering Time Travel & Forking Internals",
        "difficulty": "Production",
        "estimated_minutes": 20,
        "prerequisites": ["m7-l2", "m14-l1"],
        "objectives": [
            "Understand the checkpoint parent-pointer tree data model",
            "Learn how checkpoint_id and parent_checkpoint_id enable non-destructive forking",
            "Implement programmatic rollback and state branching in production"
        ],
        "simple_explanation": "LangGraph checkpointers store checkpoints as an immutable Directed Acyclic Graph (DAG) of revisions. Each checkpoint stores a `checkpoint_id` and a `parent_checkpoint_id`. When you time-travel and call `update_state()`, LangGraph creates a new child checkpoint referencing that historical ancestor without modifying existing history.",
        "why_it_matters": "Immutable event sourcing ensures complete auditability. You can explore 'what-if' scenarios or correct customer issues without losing the historical record of what the agent originally did.",
        "real_world_analogy": "Like a multiverse timeline in science fiction: Stepping back into the past and changing a decision creates an alternate reality branch (new checkpoint fork) while leaving the original timeline intact.",
        "diagram_type": "mermaid",
        "diagram_definition": {
            "chart": "graph TD\n  CP1[\"CP 1 (id: 001, parent: null)\"] --> CP2[\"CP 2 (id: 002, parent: 001)\"]\n  CP2 --> CP3[\"CP 3 (id: 003, parent: 002) [Original Branch]\"]\n  CP2 -. Forked Branch .-> CP3_Fork[\"CP 3B (id: 004, parent: 002) [Forked Revision]\"]\n  CP3_Fork --> CP4_Fork[\"CP 4B (id: 005, parent: 004)\"]"
        },
        "code_example": """from typing import TypedDict
from langgraph.graph import StateGraph, START, END
from langgraph.checkpoint.memory import MemorySaver

class BranchingState(TypedDict):
    step_history: list[str]
    score: int

def step_one(state: BranchingState) -> dict:
    return {"step_history": ["Step 1 Executed"], "score": 10}

def step_two_branch_a(state: BranchingState) -> dict:
    return {"step_history": state["step_history"] + ["Branch A Chosen"], "score": state["score"] + 50}

builder = StateGraph(BranchingState)
builder.add_node("step_one", step_one)
builder.add_node("branch_a", step_two_branch_a)
builder.add_edge(START, "step_one")
builder.add_edge("step_one", "branch_a")
builder.add_edge("branch_a", END)

checkpointer = MemorySaver()
app = builder.compile(checkpointer=checkpointer)

cfg = {"configurable": {"thread_id": "multiverse-thread-1"}}
app.invoke({"step_history": [], "score": 0}, config=cfg)

# 1. Fetch checkpoints
history = list(app.get_state_history(cfg))
print(f"Total Checkpoint Snapshots in Tree: {len(history)}")
for s in history:
    print(f"- CP ID: {s.config['configurable']['checkpoint_id'][:8]} | Values: {s.values}")

# 2. Time travel to step_one checkpoint
step_one_cp = history[1]
print(f"\\nForking from CP: {step_one_cp.config['configurable']['checkpoint_id'][:8]}")

# 3. Write fork update
fork_cfg = app.update_state(
    step_one_cp.config,
    {"step_history": ["Step 1 Executed", "Branch B (Alternate Universe Chosen)"], "score": 100}
)

fork_res = app.get_state(fork_cfg)
print("Forked Branch State:", fork_res.values)""",
        "line_by_line": [
            {"line": "step_one_cp = history[1]", "explanation": "Selects historical checkpoint snapshot from the history tree."},
            {"line": "fork_cfg = app.update_state(step_one_cp.config, ...)", "explanation": "Creates a new branch pointing to step_one_cp as its parent checkpoint."}
        ],
        "sample_input": {"configurable": {"thread_id": "multiverse-thread-1"}},
        "sample_output": {
            "step_history": ["Step 1 Executed", "Branch B (Alternate Universe Chosen)"],
            "score": 100
        },
        "common_mistakes": [
            {"mistake": "Confusing fork branch creation with destructive state overwriting.", "fix": "LangGraph never deletes old checkpoints during update_state; it builds an immutable tree of checkpoints."}
        ],
        "hands_on_task": {
            "title": "Inspect parent checkpoint ID",
            "instruction": "Print `s.parent_checkpoint_id` for each snapshot in `app.get_state_history(cfg)`.",
            "starter_code": "for s in app.get_state_history(cfg):\n    print('Parent:', s.parent_config)"
        },
        "quick_quiz": [
            {
                "question": "How does LangGraph maintain historical checkpoints when forking state via update_state?",
                "options": [
                    "It overwrites the database row",
                    "It creates a new immutable checkpoint whose parent points to the historical checkpoint, preserving full history",
                    "It wipes out the thread",
                    "It only saves to disk once a day"
                ],
                "correct_index": 1,
                "explanation": "LangGraph uses immutable parent pointers, allowing multiple divergent branches to share common ancestors without data loss."
            }
        ],
        "docs_url": "https://docs.langchain.com/oss/python/langgraph/persistence",
        "prev_lesson_id": "m14-l1",
        "next_lesson_id": None
    }
}
