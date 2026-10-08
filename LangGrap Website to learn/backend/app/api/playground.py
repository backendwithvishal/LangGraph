import json
import asyncio
from fastapi import APIRouter, HTTPException, Request
from sse_starlette.sse import EventSourceResponse
from typing import List, Dict, Any, Optional
from backend.app.schemas.execution import RunRequest, RunResponse, CodeRunRequest, CodeRunResponse
from backend.app.data.playground_examples import get_playground_examples, get_playground_example
from backend.app.engine.langgraph_runner import LangGraphRunner
from backend.app.engine.runner import CodeRunner

router = APIRouter(prefix="/api/playground", tags=["Playground"])

@router.get("/examples")
def list_examples():
    return get_playground_examples()

@router.get("/examples/{example_id}")
def get_example_detail(example_id: str):
    ex = get_playground_example(example_id)
    if not ex:
        raise HTTPException(status_code=404, detail=f"Example '{example_id}' not found")
    return ex

@router.post("/run", response_model=RunResponse)
def run_playground_example(req: RunRequest):
    if not req.example_id:
        raise HTTPException(status_code=400, detail="example_id is required")
    
    result = LangGraphRunner.run_example(req.example_id, req.initial_state)
    return RunResponse(
        success=result["success"],
        execution_type=result["execution_type"],
        steps=result["steps"],
        final_state=result["final_state"],
        logs=result["logs"],
        error=result.get("error"),
        execution_time_ms=result["execution_time_ms"]
    )

@router.post("/stream")
async def stream_playground_example(request: Request, req: RunRequest):
    """
    Streams genuine LangGraph step events over Server-Sent Events (SSE).
    """
    example_id = req.example_id or "sequential-pipeline"
    
    async def event_generator():
        try:
            # Yield started event
            yield {
                "event": "start",
                "data": json.dumps({"example_id": example_id, "status": "running"})
            }
            
            # Execute and stream steps with realistic pacing for visual learning
            run_result = LangGraphRunner.run_example(example_id, req.initial_state)
            
            for step in run_result["steps"]:
                if await request.is_disconnected():
                    break
                
                yield {
                    "event": "step",
                    "data": json.dumps(step)
                }
                await asyncio.sleep(0.4)  # Visual pause for step inspection
                
            yield {
                "event": "complete",
                "data": json.dumps({
                    "success": run_result["success"],
                    "final_state": run_result["final_state"],
                    "logs": run_result["logs"],
                    "execution_time_ms": run_result["execution_time_ms"]
                })
            }
        except Exception as e:
            yield {
                "event": "error",
                "data": json.dumps({"error": str(e)})
            }

    return EventSourceResponse(event_generator())

@router.post("/code/run", response_model=CodeRunResponse)
def run_custom_code(req: CodeRunRequest):
    if not req.code or not req.code.strip():
        raise HTTPException(status_code=400, detail="Code cannot be empty")
    
    res = CodeRunner.run_code(req.code, timeout_seconds=req.timeout or 10)
    return CodeRunResponse(
        success=res["success"],
        stdout=res["stdout"],
        stderr=res["stderr"],
        result=res.get("result"),
        error=res.get("error"),
        execution_time_ms=res["execution_time_ms"]
    )
