"""
Authentication Manager - Token storage and authentication state.

This module handles JWT token storage, refresh, and authentication state
management using QSettings for cross-platform persistence.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

import json
from typing import Optional, Dict, Any
from datetime import datetime

from PyQt5.QtCore import QSettings, QObject, pyqtSignal


class AuthManager(QObject):
    """
    Manages authentication state and token storage.
    
    Uses QSettings for cross-platform token persistence.
    
    Signals:
        auth_changed: Emitted when authentication state changes.
        token_expired: Emitted when access token expires.
    """
    
    auth_changed = pyqtSignal(bool)  # is_authenticated
    token_expired = pyqtSignal()
    
    # Settings keys matching web localStorage keys
    KEY_ACCESS_TOKEN = 'access_token'
    KEY_REFRESH_TOKEN = 'refresh_token'
    KEY_USER = 'user'
    KEY_SESSION_ONLY = 'session_only'
    
    def __init__(self, parent: Optional[QObject] = None) -> None:
        super().__init__(parent)
        
        self.settings = QSettings('FOSSEE', 'ChemicalEquipmentVisualizer')
        self._session_only = False  # If True, clear credentials on logout/exit
    
    def get_access_token(self) -> Optional[str]:
        """Get stored access token."""
        return self.settings.value(self.KEY_ACCESS_TOKEN, None)
    
    def get_refresh_token(self) -> Optional[str]:
        """Get stored refresh token."""
        return self.settings.value(self.KEY_REFRESH_TOKEN, None)
    
    def get_user(self) -> Optional[Dict[str, Any]]:
        """Get stored user data."""
        user_str = self.settings.value(self.KEY_USER, None)
        if user_str:
            try:
                return json.loads(user_str)
            except json.JSONDecodeError:
                return None
        return None
    
    def save_tokens(self, access_token: str, refresh_token: str) -> None:
        """Save authentication tokens."""
        self.settings.setValue(self.KEY_ACCESS_TOKEN, access_token)
        self.settings.setValue(self.KEY_REFRESH_TOKEN, refresh_token)
        self.auth_changed.emit(True)
    
    def save_user(self, user: Dict[str, Any]) -> None:
        """Save user data."""
        self.settings.setValue(self.KEY_USER, json.dumps(user))
    
    def save_auth(self, tokens: Dict[str, str], user: Dict[str, Any]) -> None:
        """Save complete authentication data."""
        self.save_tokens(tokens.get('access', ''), tokens.get('refresh', ''))
        self.save_user(user)
    
    def clear_auth(self) -> None:
        """Clear all authentication data."""
        self.settings.remove(self.KEY_ACCESS_TOKEN)
        self.settings.remove(self.KEY_REFRESH_TOKEN)
        self.settings.remove(self.KEY_USER)
        self.auth_changed.emit(False)
    
    def is_authenticated(self) -> bool:
        """Check if user is authenticated."""
        return self.get_access_token() is not None
    
    def get_username(self) -> str:
        """Get current username."""
        user = self.get_user()
        if user:
            return user.get('username', 'User')
        return 'User'
    
    def update_access_token(self, new_token: str) -> None:
        """Update access token after refresh."""
        self.settings.setValue(self.KEY_ACCESS_TOKEN, new_token)
    
    def set_session_only(self, session_only: bool) -> None:
        """Set whether to keep credentials only for this session.
        
        If True, credentials will be cleared on logout.
        If False, credentials persist across app restarts.
        """
        self._session_only = session_only
    
    def is_session_only(self) -> bool:
        """Check if credentials are session-only."""
        return self._session_only
    
    def logout(self) -> None:
        """Logout user - always clears auth for clean logout."""
        self.clear_auth()


# Global singleton instance
_auth_manager: Optional[AuthManager] = None


def get_auth_manager() -> AuthManager:
    """Get or create the global AuthManager instance."""
    global _auth_manager
    if _auth_manager is None:
        _auth_manager = AuthManager()
    return _auth_manager
