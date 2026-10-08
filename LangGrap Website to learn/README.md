# GraphLab — The Complete Interactive LangGraph Learning Platform

![GraphLab Architecture](https://img.shields.io/badge/LangGraph-0.2%2B-blue?style=for-the-badge&logo=python)
![FastAPI](https://img.shields.io/badge/FastAPI-0.110%2B-009688?style=for-the-badge&logo=fastapi)
![React](https://img.shields.io/badge/React-18-61DAFB?style=for-the-badge&logo=react)
![TailwindCSS](https://img.shields.io/badge/Tailwind_CSS-3.4-38B2AC?style=for-the-badge&logo=tailwind-css)
![React Flow](https://img.shields.io/badge/@xyflow/react-12.3-FF0072?style=for-the-badge)

**GraphLab** is a complete, responsive, interactive developer educational platform built to teach **LangGraph** from absolute beginner concepts to advanced, practical, production-oriented architectures.

---

## 🌟 Key Features

1. **Structured 14-Module Curriculum**:
   - **Foundations & Architecture**: Why LangGraph exists, cyclic state machines vs linear DAGs, Pregel actor model.
   - **Graph Fundamentals**: `StateGraph`, `START` & `END`, node functions, partial dictionary returns, `invoke()` and `stream()`.
   - **State Management & Reducers**: Custom reducers with `Annotated[T, reducer]`, `MessagesState`, `add_messages`, input/output schemas.
   - **Routing, Branching & Loops**: `add_conditional_edges`, recursion limits, parallel fan-out/in, `Send`, and modern `Command(update=..., goto=...)`.
   - **Models, Messages & Tool Calling**: `@tool`, `ToolNode`, `tools_condition`, tool error recovery.
   - **Building ReAct & Custom Agents**: ReAct architecture from scratch, `create_react_agent`, guardrails.
   - **Persistence, Checkpointing & Memory**: `MemorySaver`, `SqliteSaver`, `thread_id`, state snapshots, time-travel history replay, checkpointers vs `BaseStore`.
   - **Human-in-the-Loop & Dynamic Interrupts**: `interrupt()`, `Command(resume=...)`, approval/rejection gates, state editing before resume.
   - **Streaming Architecture & SSE**: `stream_mode='values' | 'updates' | 'messages'`, FastAPI SSE endpoints with `EventSourceResponse`.
   - **Subgraphs & Multi-Agent Architecture**: Subgraphs as nodes, parent-child state isolation, supervisor pattern, handoffs.
   - **Functional API**: `@entrypoint` & `@task`, task caching, interrupts and persistence in procedural workflows.
   - **RAG & Advanced Retrieval**: Corrective RAG (CRAG), document grading, query rewriting, Self-RAG hallucination checkers.
   - **Reliability, Testing & Production**: `RetryPolicy`, timeouts, deterministic pytest mock testing, LangSmith observability.
   - **Advanced Internals & Pregel Reference**: Super-step sync barriers, state channel queues, immutable snapshot DAGs.

2. **Interactive Visual Graph Playground (`@xyflow/react`)**:
   - Step-by-step playback with animated node pulses and glowing active edges.
   - Live **State Inspector** showing active state snapshots, super-step channel deltas (diffs), and execution logs.
   - Genuine LangGraph Python backend execution.

3. **Python Code Playground**:
   - Syntax-highlighted code editor with copy, reset, and live execution.
   - Live streaming terminal output with runtime execution telemetry.

4. **Practice & Quiz Center**:
   - Predict-the-Output questions, Bug Hunter / debugging challenges, and routing puzzles.
   - Instant conceptual explanations, hints, and progress tracking.

5. **9 Guided Real-World Projects**:
   - From conditional support triage to human wire approvals, CRAG, and an autonomous enterprise support agent capstone.

6. **Local-First Progress Persistence & Revision**:
   - Honest progress tracking stored in browser localStorage.
   - Weak topics revision queue based on quiz performance.
   - Bookmarks and personal note-taking on every lesson.
   - 1-click JSON progress export and import.

7. **Search & Reference Library**:
   - Full-text search across all lessons and concepts.
   - Glossary of 20+ terms with code snippets and links to official documentation.
   - Framework comparison matrix (LangGraph vs LangChain LCEL vs CrewAI vs AutoGen).

---

## 🚀 Quickstart & Installation

### Prerequisites
- Python 3.11+ (Python 3.13 tested)
- Node.js 18+ (v22 tested) & npm

### 1. Backend Setup

```bash
# Navigate to project root
cd "d:\LangGraph\LangGrap Website to learn"

# Activate Python virtual environment (or create if not present)
# python -m venv venv
.\venv\Scripts\activate

# Install dependencies
pip install -r backend/requirements.txt

# Run backend API server with Uvicorn
uvicorn backend.app.main:app --reload --port 8000
```
Backend API will be accessible at `http://127.0.0.1:8000`. Test docs at `http://127.0.0.1:8000/docs`.

### 2. Frontend Setup

```bash
# In a second terminal:
cd "d:\LangGraph\LangGrap Website to learn\frontend"

# Install npm dependencies
npm install

# Start Vite development server
npm run dev
```
Frontend will be accessible at `http://localhost:5173`.

---

## 🧪 Automated Testing

### Backend Unit & Integration Tests (pytest)
```bash
.\venv\Scripts\pytest -v
```
All 10 API and LangGraph engine tests pass with zero errors.

### Frontend Component Tests (Vitest)
```bash
cd frontend
npx vitest run
```
All React component and navigation tests pass.

### Frontend Production Build
```bash
cd frontend
npm run build
```
Builds optimized production bundle into `dist/`.

---

## 📁 Repository Structure

```
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entrypoint with CORS & routes
│   │   ├── config.py                # Configuration settings
│   │   ├── api/
│   │   │   ├── curriculum.py        # Curriculum & lesson endpoints
│   │   │   ├── playground.py        # Run & SSE streaming endpoints
│   │   │   ├── quizzes.py           # Practice quiz & verification endpoints
│   │   │   ├── projects.py          # Guided project specifications
│   │   │   └── reference.py         # Glossary and comparison data
│   │   ├── data/
│   │   │   ├── curriculum_data.py   # 14-module metadata & fast-track ids
│   │   │   ├── all_lessons.py       # Aggregator for all module lessons
│   │   │   ├── lessons_content.py   # Modules 1-2 detailed content
│   │   │   ├── lessons_content_extended.py  # Modules 3-4 detailed content
│   │   │   ├── lessons_content_advanced.py  # Modules 5-14 detailed content
│   │   │   ├── playground_examples.py       # Visual graph example definitions
│   │   │   ├── quiz_data.py         # Practice challenges & bug hunters
│   │   │   ├── project_data.py      # 9 guided projects with starter code & tests
│   │   │   └── glossary_data.py     # Glossary & framework comparisons
│   │   ├── engine/
│   │   │   ├── langgraph_runner.py  # Real LangGraph runner & step tracer
│   │   │   └── runner.py            # Code execution sandbox
│   │   └── schemas/                 # Pydantic validation schemas
│   ├── tests/
│   │   └── test_api.py              # Pytest test suite
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   ├── layout/              # Navbar, Sidebar, Footer
│   │   │   ├── graph/               # VisualGraph, CustomNode, StateInspector
│   │   │   ├── editor/              # CodeEditor, TerminalOutput
│   │   │   ├── ui/                  # Badge, Card, ProgressBar
│   │   │   └── common/              # GlobalSearch
│   │   ├── context/
│   │   │   ├── ProgressContext.jsx  # Local storage progress tracking
│   │   │   └── ThemeContext.jsx     # Dark/Light theme manager
│   │   ├── pages/                   # Dashboard, LearningPath, LessonDetail,
│   │   │                            # GraphPlayground, CodePlayground,
│   │   │                            # PracticeCenter, ProjectsCenter,
│   │   │                            # ProgressRevision, ReferenceLibrary
│   │   └── services/api.js          # API client
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
├── .env.example
├── pytest.ini
└── README.md
```

---

## 🎯 Curriculum Coverage Checklist

| Module | Title | Lessons | Interactive Graph | Real Code |
| :--- | :--- | :---: | :---: | :---: |
| **Module 1** | Foundations & Architecture | 3 | ✅ | ✅ |
| **Module 2** | Graph Fundamentals | 3 | ✅ | ✅ |
| **Module 3** | State Management & Reducers | 3 | ✅ | ✅ |
| **Module 4** | Routing, Branching & Loops | 4 | ✅ | ✅ |
| **Module 5** | Models, Messages & Tool Calling | 3 | ✅ | ✅ |
| **Module 6** | Building ReAct & Custom Agents | 3 | ✅ | ✅ |
| **Module 7** | Persistence, Checkpointing & Memory | 3 | ✅ | ✅ |
| **Module 8** | Human-in-the-Loop & Dynamic Interrupts | 3 | ✅ | ✅ |
| **Module 9** | Streaming Architecture & SSE | 2 | ✅ | ✅ |
| **Module 10** | Subgraphs & Multi-Agent Architecture | 2 | ✅ | ✅ |
| **Module 11** | Functional API (@entrypoint & @task) | 2 | ✅ | ✅ |
| **Module 12** | RAG & Advanced Retrieval Patterns | 2 | ✅ | ✅ |
| **Module 13** | Reliability, Testing & Production | 3 | ✅ | ✅ |
| **Module 14** | Advanced Internals & Pregel Engine | 2 | ✅ | ✅ |

---

## 📜 Official LangGraph Documentation References

- [LangGraph Overview](https://docs.langchain.com/oss/python/langgraph/overview)
- [Quickstart Guide](https://docs.langchain.com/oss/python/langgraph/quickstart)
- [Graph API Reference](https://docs.langchain.com/oss/python/langgraph/graph-api)
- [Persistence & Memory](https://docs.langchain.com/oss/python/langgraph/persistence)
- [Dynamic Interrupts](https://docs.langchain.com/oss/python/langgraph/interrupts)
- [Streaming Architecture](https://docs.langchain.com/oss/python/langgraph/streaming)
- [Subgraphs Documentation](https://docs.langchain.com/oss/python/langgraph/subgraphs)
- [Testing LangGraph Workflows](https://docs.langchain.com/oss/python/langgraph/test)
