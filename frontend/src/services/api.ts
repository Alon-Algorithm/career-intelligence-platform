// src/services/api.ts
import axios from 'axios';

const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Upload CV to backend
export const uploadCV = async (file: File) => {
  const formData = new FormData();
  formData.append('file', file);

  const response = await api.post('/api/upload-cv', formData, {
    headers: {
      'Content-Type': 'multipart/form-data',
    },
  });
  return response.data;
};

// Analyze skills with ML
export const analyzeSkills = async (skills: string[], experienceYears: number = 0) => {
  const response = await api.post('/api/analyze-skills', {
    skills: skills,
    experience_years: experienceYears,
  });
  return response.data;
};

// Get all available skills
export const getAvailableSkills = async () => {
  const response = await api.get('/api/skills');
  return response.data;
};

// Health check
export const healthCheck = async () => {
  try {
    const response = await api.get('/api/health');
    return response.status === 200;
  } catch {
    return false;
  }
};