// API Configuration
export const API_BASE_URL = process.env.REACT_APP_API_URL || 'http://localhost:5000';

export const API_ENDPOINTS = {
  PREDICT: `${API_BASE_URL}/predict`,
  HOME: API_BASE_URL,
};
//again committed 