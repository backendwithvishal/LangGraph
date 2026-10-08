import React, { createContext, useContext, useState, useEffect } from 'react';
import { getStoredProgress, saveStoredProgress } from '../utils/storage';

const ProgressContext = createContext();

export const ProgressProvider = ({ children }) => {
  const [progress, setProgress] = useState(getStoredProgress);

  useEffect(() => {
    saveStoredProgress(progress);
  }, [progress]);

  const markLessonComplete = (lessonId, completed = true) => {
    setProgress(prev => ({
      ...prev,
      completedLessons: {
        ...prev.completedLessons,
        [lessonId]: completed ? new Date().toISOString() : false
      }
    }));
  };

  const recordQuizScore = (quizId, isCorrect, topicId) => {
    setProgress(prev => {
      const existing = prev.quizScores[quizId] || { attempts: 0, correct: 0, topicId };
      return {
        ...prev,
        quizScores: {
          ...prev.quizScores,
          [quizId]: {
            attempts: existing.attempts + 1,
            correct: isCorrect ? existing.correct + 1 : existing.correct,
            lastResult: isCorrect,
            topicId: topicId || existing.topicId,
            lastAttemptAt: new Date().toISOString()
          }
        }
      };
    });
  };

  const toggleBookmark = (lessonId) => {
    setProgress(prev => {
      const bookmarks = prev.bookmarks || [];
      const exists = bookmarks.includes(lessonId);
      return {
        ...prev,
        bookmarks: exists ? bookmarks.filter(id => id !== lessonId) : [...bookmarks, lessonId]
      };
    });
  };

  const saveNote = (lessonId, noteText) => {
    setProgress(prev => ({
      ...prev,
      notes: {
        ...prev.notes,
        [lessonId]: noteText
      }
    }));
  };

  const toggleFastTrack = () => {
    setProgress(prev => ({
      ...prev,
      fastTrackMode: !prev.fastTrackMode
    }));
  };

  const setLastVisited = (lessonId) => {
    setProgress(prev => ({
      ...prev,
      lastVisitedLessonId: lessonId
    }));
  };

  const markProjectComplete = (projectId) => {
    setProgress(prev => ({
      ...prev,
      completedProjects: {
        ...prev.completedProjects,
        [projectId]: new Date().toISOString()
      }
    }));
  };

  const exportProgressJSON = () => {
    return JSON.stringify(progress, null, 2);
  };

  const importProgressJSON = (jsonString) => {
    try {
      const parsed = JSON.parse(jsonString);
      setProgress(parsed);
      return true;
    } catch (e) {
      console.error('Import failed:', e);
      return false;
    }
  };

  const resetAllProgress = () => {
    const empty = {
      completedLessons: {},
      quizScores: {},
      bookmarks: [],
      notes: {},
      fastTrackMode: false,
      lastVisitedLessonId: 'm1-l1',
      completedProjects: {}
    };
    setProgress(empty);
  };

  const completedCount = Object.values(progress.completedLessons || {}).filter(Boolean).length;
  const isLessonCompleted = (id) => Boolean(progress.completedLessons?.[id]);
  const isBookmarked = (id) => (progress.bookmarks || []).includes(id);
  const getNote = (id) => progress.notes?.[id] || '';

  return (
    <ProgressContext.Provider
      value={{
        progress,
        completedCount,
        isLessonCompleted,
        isBookmarked,
        getNote,
        markLessonComplete,
        recordQuizScore,
        toggleBookmark,
        saveNote,
        toggleFastTrack,
        setLastVisited,
        markProjectComplete,
        exportProgressJSON,
        importProgressJSON,
        resetAllProgress
      }}
    >
      {children}
    </ProgressContext.Provider>
  );
};

export const useProgress = () => useContext(ProgressContext);
