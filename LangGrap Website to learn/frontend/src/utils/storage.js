const PROGRESS_KEY = 'graphlab_learning_progress_v1';

export const getStoredProgress = () => {
  try {
    const raw = localStorage.getItem(PROGRESS_KEY);
    if (!raw) {
      return {
        completedLessons: {},
        quizScores: {},
        bookmarks: [],
        notes: {},
        fastTrackMode: false,
        lastVisitedLessonId: 'm1-l1',
        completedProjects: {}
      };
    }
    return JSON.parse(raw);
  } catch (e) {
    console.error('Failed to parse stored progress:', e);
    return {
      completedLessons: {},
      quizScores: {},
      bookmarks: [],
      notes: {},
      fastTrackMode: false,
      lastVisitedLessonId: 'm1-l1',
      completedProjects: {}
    };
  }
};

export const saveStoredProgress = (progress) => {
  try {
    localStorage.setItem(PROGRESS_KEY, JSON.stringify(progress));
  } catch (e) {
    console.error('Failed to save progress to localStorage:', e);
  }
};
