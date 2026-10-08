from fastapi import APIRouter
from typing import List, Dict, Any
from backend.app.data.glossary_data import get_glossary, get_comparison

router = APIRouter(prefix="/api/reference", tags=["Reference"])

@router.get("/glossary")
def list_glossary():
    return get_glossary()

@router.get("/framework-comparison")
def list_comparison():
    return get_comparison()
