from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

class GraphNode(BaseModel):
    id: str
    label: str
    description: Optional[str] = None
    type: str = "custom"  # start, end, node, conditional
    data: Optional[Dict[str, Any]] = None

class GraphEdge(BaseModel):
    id: str
    source: str
    target: str
    label: Optional[str] = None
    conditional: bool = False

class GraphDefinition(BaseModel):
    nodes: List[GraphNode]
    edges: List[GraphEdge]

class PlaygroundExample(BaseModel):
    id: str
    title: str
    category: str
    difficulty: str
    description: str
    initial_state: Dict[str, Any]
    python_code: str
    graph: GraphDefinition
    is_real_execution: bool = True
    parameters_schema: Optional[Dict[str, Any]] = None

class ExecutionStep(BaseModel):
    step_number: int
    node_name: str
    state_before: Dict[str, Any]
    state_after: Dict[str, Any]
    updates: Dict[str, Any]
    edge_taken: Optional[str] = None
    log_message: str

class RunRequest(BaseModel):
    example_id: Optional[str] = None
    custom_code: Optional[str] = None
    initial_state: Optional[Dict[str, Any]] = None
    parameters: Optional[Dict[str, Any]] = None

class RunResponse(BaseModel):
    success: bool
    execution_type: str  # "real_langgraph" or "simulation"
    steps: List[ExecutionStep]
    final_state: Dict[str, Any]
    logs: List[str]
    error: Optional[str] = None
    execution_time_ms: float

class CodeRunRequest(BaseModel):
    code: str
    input_data: Optional[Dict[str, Any]] = None
    timeout: Optional[int] = 10

class CodeRunResponse(BaseModel):
    success: bool
    stdout: str
    stderr: str
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    execution_time_ms: float
