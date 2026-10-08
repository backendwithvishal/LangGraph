import { render, screen } from '@testing-library/react';
import { describe, it, expect, vi } from 'vitest';
import App from '../App';

// Mock fetch for tests
global.fetch = vi.fn((url) => {
  if (url.includes('/api/curriculum')) {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve({
        modules: [
          {
            id: "module-1",
            title: "Module 1: Foundations",
            description: "Foundations of LangGraph",
            difficulty: "Beginner",
            order: 1,
            lessons: [{ id: "m1-l1", title: "What is LangGraph", estimated_minutes: 10, difficulty: "Beginner" }]
          }
        ],
        total_lessons: 32,
        total_estimated_minutes: 540,
        fast_track_lesson_ids: ["m1-l1"]
      })
    });
  }
  if (url.includes('/api/playground/examples')) {
    return Promise.resolve({
      ok: true,
      json: () => Promise.resolve([
        {
          id: "sequential-pipeline",
          title: "Linear Pipeline",
          category: "Foundations",
          difficulty: "Beginner",
          graph: { nodes: [], edges: [] }
        }
      ])
    });
  }
  return Promise.resolve({
    ok: true,
    json: () => Promise.resolve([])
  });
});

describe('GraphLab App Smoke Tests', () => {
  it('renders the brand title in Navbar', () => {
    render(<App />);
    const brandElements = screen.getAllByText(/Graph/i);
    expect(brandElements.length).toBeGreaterThan(0);
  });

  it('renders navigation links', () => {
    render(<App />);
    expect(screen.getByText(/Dashboard/i)).toBeInTheDocument();
    expect(screen.getByText(/Learning Path/i)).toBeInTheDocument();
    expect(screen.getByText(/Visual Graph/i)).toBeInTheDocument();
    expect(screen.getByText(/Python Lab/i)).toBeInTheDocument();
    expect(screen.getByText(/Quiz & Practice/i)).toBeInTheDocument();
  });
});
