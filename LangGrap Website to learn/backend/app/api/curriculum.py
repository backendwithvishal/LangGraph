from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.data.curriculum_data import CURRICULUM_MODULES, FAST_TRACK_LESSON_IDS
from backend.app.data.all_lessons import get_lesson, ALL_LESSONS_MAP

router = APIRouter(prefix="/api", tags=["Curriculum"])

@router.get("/curriculum")
def get_curriculum_overview():
    total_lessons = sum(len(m["lessons"]) for m in CURRICULUM_MODULES)
    total_minutes = sum(
        sum(l["estimated_minutes"] for l in m["lessons"])
        for m in CURRICULUM_MODULES
    )
    return {
        "modules": CURRICULUM_MODULES,
        "total_lessons": total_lessons,
        "total_estimated_minutes": total_minutes,
        "fast_track_lesson_ids": FAST_TRACK_LESSON_IDS
    }

@router.get("/lessons")
def list_lessons():
    all_summaries = []
    for mod in CURRICULUM_MODULES:
        for l in mod["lessons"]:
            all_summaries.append(l)
    return all_summaries

@router.get("/lessons/{lesson_id}")
def get_lesson_detail(lesson_id: str):
    detail = get_lesson(lesson_id)
    if not detail:
        # Fallback to search in module lessons
        for mod in CURRICULUM_MODULES:
            for l in mod["lessons"]:
                if l["id"] == lesson_id:
                    return {
                        "id": l["id"],
                        "module_id": mod["id"],
                        "module_title": mod["title"],
                        "title": l["title"],
                        "difficulty": l["difficulty"],
                        "estimated_minutes": l["estimated_minutes"],
                        "prerequisites": l.get("prerequisites", []),
                        "objectives": ["Master the core concepts of this lesson", "Apply real Python LangGraph code", "Pass the comprehension quiz"],
                        "simple_explanation": l["summary"],
                        "why_it_matters": "Essential knowledge for architecting production-grade LangGraph systems.",
                        "real_world_analogy": "Like building a robust control system in software engineering.",
                        "diagram_type": "mermaid",
                        "diagram_definition": {"chart": "graph LR\n  START([START]) --> Step1[Process Data] --> END([END])"},
                        "code_example": "# LangGraph example\nfrom langgraph.graph import StateGraph, START, END\n# See lesson content",
                        "line_by_line": [{"line": "from langgraph.graph import StateGraph", "explanation": "Imports StateGraph"}],
                        "sample_input": {},
                        "sample_output": {},
                        "common_mistakes": [{"mistake": "Unchecked state mutation", "fix": "Return partial dict updates"}],
                        "hands_on_task": {"title": "Practice task", "instruction": "Implement the node function", "starter_code": "def my_node(state): return {}"},
                        "quick_quiz": [{"question": "What is the primary benefit of this concept?", "options": ["Option A", "Option B", "Option C", "Option D"], "correct_index": 0, "explanation": "Core principle of LangGraph."}],
                        "docs_url": "https://docs.langchain.com/oss/python/langgraph/overview",
                        "prev_lesson_id": None,
                        "next_lesson_id": None
                    }
        raise HTTPException(status_code=404, detail=f"Lesson '{lesson_id}' not found")
    return detail
