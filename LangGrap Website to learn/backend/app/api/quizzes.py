from fastapi import APIRouter, HTTPException
from typing import List, Dict, Any
from backend.app.schemas.quiz import QuizSubmission, QuizResult
from backend.app.data.quiz_data import get_all_quizzes, get_quiz_by_id

router = APIRouter(prefix="/api/quizzes", tags=["Quizzes"])

@router.get("")
def list_quizzes():
    return get_all_quizzes()

@router.get("/{quiz_id}")
def get_quiz(quiz_id: str):
    q = get_quiz_by_id(quiz_id)
    if not q:
        raise HTTPException(status_code=404, detail=f"Quiz '{quiz_id}' not found")
    # Return without spoiling correct answer for practice mode
    safe_q = dict(q)
    return safe_q

@router.post("/{quiz_id}/verify", response_model=QuizResult)
def verify_quiz_answer(quiz_id: str, sub: QuizSubmission):
    q = get_quiz_by_id(quiz_id)
    if not q:
        raise HTTPException(status_code=404, detail=f"Quiz '{quiz_id}' not found")
    
    is_correct = (sub.selected_answer == q["correct_answer"])
    feedback = "Correct! Outstanding understanding of LangGraph." if is_correct else "Not quite. Check the conceptual explanation and try again!"
    
    return QuizResult(
        is_correct=is_correct,
        correct_answer=q["correct_answer"],
        explanation=q["explanation"],
        feedback=feedback
    )
