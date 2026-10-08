# Master aggregator for all lesson data
from typing import Dict, Any, Optional
from backend.app.data.lessons_content import LESSONS_CONTENT
from backend.app.data.lessons_content_extended import EXTENDED_LESSONS
from backend.app.data.lessons_content_advanced import ADVANCED_LESSONS

ALL_LESSONS_MAP: Dict[str, Dict[str, Any]] = {
    **LESSONS_CONTENT,
    **EXTENDED_LESSONS,
    **ADVANCED_LESSONS
}

def get_lesson(lesson_id: str) -> Optional[Dict[str, Any]]:
    return ALL_LESSONS_MAP.get(lesson_id)

def get_all_lesson_ids() -> list[str]:
    return list(ALL_LESSONS_MAP.keys())
