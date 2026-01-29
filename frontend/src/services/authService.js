import api from './api';
import { STORAGE_KEYS } from '../utils/constants';

/**
 * Authentication service for handling user auth operations
 */
const authService = {
  /**
   * Login user
   */
  async login(username, password) {
    const response = await api.post('/auth/login/', { username, password });
    
    if (response.data.success) {
      const { user, tokens } = response.data;
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    }
    
    return response.data;
  },

  /**
   * Register new user
   */
  async register(userData) {
    const response = await api.post('/auth/register/', userData);
    
    if (response.data.success) {
      const { user, tokens } = response.data;
      localStorage.setItem(STORAGE_KEYS.ACCESS_TOKEN, tokens.access);
      localStorage.setItem(STORAGE_KEYS.REFRESH_TOKEN, tokens.refresh);
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(user));
    }
    
    return response.data;
  },

  /**
   * Logout user
   */
  async logout() {
    try {
      const refreshToken = localStorage.getItem(STORAGE_KEYS.REFRESH_TOKEN);
      if (refreshToken) {
        await api.post('/auth/logout/', { refresh: refreshToken });
      }
    } catch (error) {
      console.error('Logout error:', error);
    } finally {
      localStorage.removeItem(STORAGE_KEYS.ACCESS_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.REFRESH_TOKEN);
      localStorage.removeItem(STORAGE_KEYS.USER);
    }
  },

  /**
   * Get current user profile
   */
  async getProfile() {
    const response = await api.get('/auth/profile/');
    return response.data;
  },

  /**
   * Update user profile
   */
  async updateProfile(userData) {
    const response = await api.patch('/auth/profile/', userData);
    
    if (response.data.success) {
      localStorage.setItem(STORAGE_KEYS.USER, JSON.stringify(response.data.user));
    }
    
    return response.data;
  },

  /**
   * Change password
   */
  async changePassword(oldPassword, newPassword, newPasswordConfirm) {
    const response = await api.post('/auth/password/change/', {
      old_password: oldPassword,
      new_password: newPassword,
      new_password_confirm: newPasswordConfirm,
    });
    return response.data;
  },

  /**
   * Get stored user from localStorage
   */
  getStoredUser() {
    const userStr = localStorage.getItem(STORAGE_KEYS.USER);
    return userStr ? JSON.parse(userStr) : null;
  },

  /**
   * Check if user is authenticated
   */
  isAuthenticated() {
    return !!localStorage.getItem(STORAGE_KEYS.ACCESS_TOKEN);
  },
};

export default authService;
