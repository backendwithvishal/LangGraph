from pydantic import BaseModel
from typing import Optional, List, Dict, Any

class QuizQuestion(BaseModel):
    id: str
    category: str
    type: str  # mcq, predict_output, bug_hunter, code_fill, routing
    difficulty: str
    question: str
    code_snippet: Optional[str] = None
    options: Optional[List[str]] = None
    correct_answer: Any
    explanation: str
    hint: str
    topic_id: str

class QuizSubmission(BaseModel):
    question_id: str
    selected_answer: Any

class QuizResult(BaseModel):
    is_correct: bool
    correct_answer: Any
    explanation: str
    feedback: str

class ProjectStep(BaseModel):
    step_number: int
    title: str
    instruction: str
    hints: List[str]
    code_template: str
    solution_code: str

class Project(BaseModel):
    id: str
    title: str
    difficulty: str
    estimated_hours: float
    description: str
    learning_outcomes: List[str]
    architecture_diagram: str
    requirements: List[str]
    steps: List[ProjectStep]
    starter_code: str
    solution_code: str
    test_cases_code: str
    sample_request: Dict[str, Any]
    expected_response: Dict[str, Any]
    bonus_extensions: List[str]
