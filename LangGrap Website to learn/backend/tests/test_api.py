import pytest
from fastapi.testclient import TestClient
from backend.app.main import app

client = TestClient(app)

def test_health_check():
    response = client.get("/api/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "GraphLab" in data["app"]

def test_curriculum_overview():
    response = client.get("/api/curriculum")
    assert response.status_code == 200
    data = response.json()
    assert len(data["modules"]) == 14
    assert data["total_lessons"] >= 30
    assert len(data["fast_track_lesson_ids"]) > 0

def test_lesson_detail():
    response = client.get("/api/lessons/m1-l1")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "m1-l1"
    assert "LangGraph" in data["title"]
    assert "code_example" in data
    assert len(data["objectives"]) > 0

def test_playground_examples_list():
    response = client.get("/api/playground/examples")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 5
    assert any(ex["id"] == "sequential-pipeline" for ex in data)

def test_playground_run_sequential():
    response = client.post("/api/playground/run", json={"example_id": "sequential-pipeline"})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["execution_type"] == "real_langgraph"
    assert len(data["steps"]) >= 3
    assert data["final_state"]["word_count"] > 0

def test_playground_run_conditional():
    response = client.post("/api/playground/run", json={
        "example_id": "conditional-branching",
        "initial_state": {"ticket_text": "Need urgent refund for double payment", "intent": "", "assigned_team": "", "priority": ""}
    })
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert data["final_state"]["intent"] == "billing"
    assert data["final_state"]["priority"] == "URGENT"

def test_code_execution_endpoint():
    code = """from langgraph.graph import StateGraph, START, END
print("Hello from LangGraph test runner!")
"""
    response = client.post("/api/playground/code/run", json={"code": code})
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "Hello from LangGraph" in data["stdout"]

def test_quizzes_and_verification():
    response = client.get("/api/quizzes")
    assert response.status_code == 200
    quizzes = response.json()
    assert len(quizzes) >= 5
    
    # Test verification
    q1 = quizzes[0]
    verify_resp = client.post(f"/api/quizzes/{q1['id']}/verify", json={"question_id": q1["id"], "selected_answer": q1["correct_answer"]})
    assert verify_resp.status_code == 200
    assert verify_resp.json()["is_correct"] is True

def test_projects_endpoints():
    response = client.get("/api/projects")
    assert response.status_code == 200
    projects = response.json()
    assert len(projects) == 9
    
    p1 = client.get(f"/api/projects/{projects[0]['id']}")
    assert p1.status_code == 200
    assert "steps" in p1.json()

def test_reference_glossary():
    response = client.get("/api/reference/glossary")
    assert response.status_code == 200
    assert len(response.json()) >= 15
