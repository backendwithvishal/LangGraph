from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any, Union

class LessonSummary(BaseModel):
    id: str
    module_id: str
    title: str
    difficulty: str  # Beginner, Intermediate, Advanced, Production
    estimated_minutes: int
    summary: str
    prerequisites: List[str] = []
    topics: List[str] = []

class LessonDetail(BaseModel):
    id: str
    module_id: str
    module_title: str
    title: str
    difficulty: str
    estimated_minutes: int
    prerequisites: List[str] = []
    objectives: List[str] = []
    simple_explanation: str
    why_it_matters: str
    real_world_analogy: str
    diagram_type: Optional[str] = None
    diagram_definition: Optional[Dict[str, Any]] = None
    code_example: str
    line_by_line: List[Dict[str, str]] = []
    sample_input: Dict[str, Any] = {}
    sample_output: Dict[str, Any] = {}
    common_mistakes: List[Dict[str, str]] = []
    hands_on_task: Dict[str, Any] = {}
    quick_quiz: List[Dict[str, Any]] = []
    docs_url: str
    prev_lesson_id: Optional[str] = None
    next_lesson_id: Optional[str] = None

class Module(BaseModel):
    id: str
    title: str
    description: str
    difficulty: str
    order: int
    icon: str
    lessons: List[LessonSummary] = []

class CurriculumOverview(BaseModel):
    modules: List[Module]
    total_lessons: int
    total_estimated_minutes: int
    fast_track_lesson_ids: List[str]
