// API Base URL
export const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api';

// Local Storage Keys
export const STORAGE_KEYS = {
  ACCESS_TOKEN: 'access_token',
  REFRESH_TOKEN: 'refresh_token',
  USER: 'user',
};

// Equipment Types
export const EQUIPMENT_TYPES = [
  'Pump',
  'Compressor',
  'Valve',
  'HeatExchanger',
  'Reactor',
  'Condenser',
  'Other',
];

// Chart Colors
export const CHART_COLORS = {
  primary: 'rgba(59, 130, 246, 0.8)',
  secondary: 'rgba(16, 185, 129, 0.8)',
  warning: 'rgba(245, 158, 11, 0.8)',
  danger: 'rgba(239, 68, 68, 0.8)',
  purple: 'rgba(139, 92, 246, 0.8)',
  pink: 'rgba(236, 72, 153, 0.8)',
};

export const CHART_COLORS_ARRAY = [
  'rgba(59, 130, 246, 0.8)',
  'rgba(16, 185, 129, 0.8)',
  'rgba(245, 158, 11, 0.8)',
  'rgba(239, 68, 68, 0.8)',
  'rgba(139, 92, 246, 0.8)',
  'rgba(236, 72, 153, 0.8)',
  'rgba(20, 184, 166, 0.8)',
  'rgba(251, 146, 60, 0.8)',
];

// Routes
export const ROUTES = {
  HOME: '/',
  LOGIN: '/login',
  REGISTER: '/register',
  UPLOAD: '/upload',
  HISTORY: '/history',
  ANALYSIS: '/analysis',
};
