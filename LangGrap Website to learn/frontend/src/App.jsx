import React, { useState } from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider } from './context/ThemeContext';
import { ProgressProvider } from './context/ProgressContext';
import { Navbar } from './components/layout/Navbar';
import { Footer } from './components/layout/Footer';
import { GlobalSearch } from './components/common/GlobalSearch';

// Pages
import { Dashboard } from './pages/Dashboard';
import { LearningPath } from './pages/LearningPath';
import { LessonDetail } from './pages/LessonDetail';
import { GraphPlayground } from './pages/GraphPlayground';
import { CodePlayground } from './pages/CodePlayground';
import { PracticeCenter } from './pages/PracticeCenter';
import { ProjectsCenter } from './pages/ProjectsCenter';
import { ProjectDetail } from './pages/ProjectDetail';
import { ProgressRevision } from './pages/ProgressRevision';
import { ReferenceLibrary } from './pages/ReferenceLibrary';
import { NotFound } from './pages/NotFound';

export const App = () => {
  const [isSearchOpen, setIsSearchOpen] = useState(false);

  return (
    <ThemeProvider>
      <ProgressProvider>
        <Router>
          <div className="flex flex-col min-h-screen bg-dark-900 text-slate-100 selection:bg-blue-500/30 selection:text-blue-300">
            <Navbar onOpenSearch={() => setIsSearchOpen(true)} />
            
            <main className="flex-1 w-full">
              <Routes>
                <Route path="/" element={<Dashboard />} />
                <Route path="/path" element={<LearningPath />} />
                <Route path="/lessons/:lessonId" element={<LessonDetail />} />
                <Route path="/playground" element={<GraphPlayground />} />
                <Route path="/code" element={<CodePlayground />} />
                <Route path="/practice" element={<PracticeCenter />} />
                <Route path="/projects" element={<ProjectsCenter />} />
                <Route path="/projects/:projectId" element={<ProjectDetail />} />
                <Route path="/progress" element={<ProgressRevision />} />
                <Route path="/reference" element={<ReferenceLibrary />} />
                <Route path="*" element={<NotFound />} />
              </Routes>
            </main>

            <Footer />

            <GlobalSearch
              isOpen={isSearchOpen}
              onClose={() => setIsSearchOpen(false)}
            />
          </div>
        </Router>
      </ProgressProvider>
    </ThemeProvider>
  );
};
export default App;
