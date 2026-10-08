import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.config import settings
from backend.app.api.curriculum import router as curriculum_router
from backend.app.api.playground import router as playground_router
from backend.app.api.quizzes import router as quizzes_router
from backend.app.api.projects import router as projects_router
from backend.app.api.reference import router as reference_router

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
    description="Backend API for GraphLab — Interactive LangGraph Learning Platform"
)

# Enable CORS for frontend development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all for local dev flexibility
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API Routers
app.include_router(curriculum_router)
app.include_router(playground_router)
app.include_router(quizzes_router)
app.include_router(projects_router)
app.include_router(reference_router)

@app.get("/api/health")
def health_check():
    return {
        "status": "healthy",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
        "langgraph_version": "0.2+"
    }
