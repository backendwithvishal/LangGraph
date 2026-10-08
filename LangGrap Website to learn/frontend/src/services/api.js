// API client for GraphLab frontend

const API_BASE = '/api';

export const api = {
  // Curriculum
  async getCurriculum() {
    const res = await fetch(`${API_BASE}/curriculum`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async getLessons() {
    const res = await fetch(`${API_BASE}/lessons`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async getLesson(id) {
    const res = await fetch(`${API_BASE}/lessons/${id}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Playground
  async getPlaygroundExamples() {
    const res = await fetch(`${API_BASE}/playground/examples`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async getPlaygroundExample(id) {
    const res = await fetch(`${API_BASE}/playground/examples/${id}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async runPlaygroundExample(exampleId, initialState) {
    const res = await fetch(`${API_BASE}/playground/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ example_id: exampleId, initial_state: initialState })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async runCustomCode(code, inputData = null) {
    const res = await fetch(`${API_BASE}/playground/code/run`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ code, input_data: inputData })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Quizzes
  async getQuizzes() {
    const res = await fetch(`${API_BASE}/quizzes`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async verifyQuiz(quizId, selectedAnswer) {
    const res = await fetch(`${API_BASE}/quizzes/${quizId}/verify`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ question_id: quizId, selected_answer: selectedAnswer })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Projects
  async getProjects() {
    const res = await fetch(`${API_BASE}/projects`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async getProject(id) {
    const res = await fetch(`${API_BASE}/projects/${id}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Reference & Glossary
  async getGlossary() {
    const res = await fetch(`${API_BASE}/reference/glossary`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async getFrameworkComparison() {
    const res = await fetch(`${API_BASE}/reference/framework-comparison`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  }
};
