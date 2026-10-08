from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.data.project_data import get_all_projects, get_project_by_id

router = APIRouter(prefix="/api/projects", tags=["Projects"])

@router.get("")
def list_projects():
    return get_all_projects()

@router.get("/{project_id}")
def get_project_detail(project_id: str):
    p = get_project_by_id(project_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"Project '{project_id}' not found")
    return p
