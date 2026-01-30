#!/usr/bin/env python3
"""
Chemical Equipment Visualizer - Desktop Application Entry Point.

This is the main entry point for the PyQt5 desktop application.
It initializes the application, checks authentication state,
and shows either the login page or main window.

Usage:
    python main.py

Requirements:
    - PyQt5 >= 5.15
    - requests
    - matplotlib
    - qtawesome (optional, for icons)

Author: FOSSEE Team
Version: 2.0.0
"""

import sys
import os

# Add the desktop directory to path for imports
DESKTOP_DIR = os.path.dirname(os.path.abspath(__file__))
if DESKTOP_DIR not in sys.path:
    sys.path.insert(0, DESKTOP_DIR)

from PyQt5.QtWidgets import QApplication, QStackedWidget
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QFontDatabase

from services.api_client import APIClient
from services.auth_manager import AuthManager
from ui.theme import COLORS
from ui.widgets.login_widget import LoginWidget
from ui.widgets.register_widget import RegisterWidget
from ui.main_window import MainWindow


class Application:
    """
    Main application controller.
    
    Manages the application lifecycle:
    - Initializes services (API client, auth manager)
    - Shows login/register or main window based on auth state
    - Handles authentication flow
    """
    
    def __init__(self) -> None:
        """Initialize the application."""
        # Create Qt application
        self.app = QApplication(sys.argv)
        self.app.setApplicationName("Chemical Equipment Visualizer")
        self.app.setOrganizationName("FOSSEE")
        self.app.setOrganizationDomain("fossee.in")
        
        # Prevent app from quitting when windows are hidden (for logout flow)
        self.app.setQuitOnLastWindowClosed(False)
        
        # Set application-wide font
        self._setup_fonts()
        
        # Initialize services
        self.auth_manager = AuthManager()
        self.api_client = APIClient(self.auth_manager)
        
        # Create stacked widget for auth flow
        # Match web auth page - full window with centered form
        self.auth_stack = QStackedWidget()
        self.auth_stack.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.auth_stack.setMinimumSize(500, 650)
        self.auth_stack.resize(500, 700)
        self.auth_stack.setStyleSheet(f"background: {COLORS['bg_sidebar']};")
        
        # Handle close event on auth stack to quit app
        def on_auth_close(event):
            self.app.quit()
        self.auth_stack.closeEvent = on_auth_close
        
        # Create auth pages
        self.login_page = LoginWidget(self.api_client, self.auth_manager)
        self.login_page.login_success.connect(self._on_login_success)
        self.login_page.register_requested.connect(self._show_register)
        self.auth_stack.addWidget(self.login_page)
        
        self.register_page = RegisterWidget(self.api_client, self.auth_manager)
        self.register_page.register_success.connect(self._on_register_success)
        self.register_page.login_requested.connect(self._show_login)
        self.auth_stack.addWidget(self.register_page)
        
        # Main window (created on login)
        self.main_window: MainWindow = None
    
    def _setup_fonts(self) -> None:
        """Setup application fonts."""
        # Use system font - fallback to available fonts
        font = QFont()
        # Try common system fonts in order of preference
        for family in ['SF Pro Display', 'Segoe UI', 'Roboto', 'Helvetica Neue', 'Arial']:
            font.setFamily(family)
            if font.exactMatch() or font.family() == family:
                break
        font.setPointSize(13)
        self.app.setFont(font)
    
    def run(self) -> int:
        """
        Run the application.
        
        Returns:
            Exit code from Qt event loop.
        """
        # Check if already authenticated
        if self.auth_manager.is_authenticated():
            self._show_main_window()
        else:
            self._show_login()
        
        return self.app.exec_()
    
    def _show_login(self) -> None:
        """Show the login page."""
        self.auth_stack.setCurrentIndex(0)
        self.auth_stack.setWindowTitle("Chemical Equipment Visualizer - Login")
        
        if self.main_window:
            self.main_window.hide()
        
        self.auth_stack.show()
        self.auth_stack.raise_()
        self.auth_stack.activateWindow()
    
    def _show_register(self) -> None:
        """Show the registration page."""
        self.auth_stack.setCurrentIndex(1)
        self.auth_stack.setWindowTitle("Chemical Equipment Visualizer - Register")
    
    def _on_login_success(self) -> None:
        """Handle successful login."""
        self.auth_stack.hide()
        self._show_main_window()
    
    def _on_register_success(self) -> None:
        """Handle successful registration."""
        # After registration, show login
        self._show_login()
    
    def _show_main_window(self) -> None:
        """Show the main application window."""
        if not self.main_window:
            self.main_window = MainWindow(self.api_client, self.auth_manager)
            self.main_window.logout_requested.connect(self._on_logout)
        
        # Update user info
        user = self.auth_manager.get_user()
        if user:
            self.main_window.set_user(user.get('username', 'User'))
        
        self.main_window.show()
        self.main_window.raise_()
        self.main_window.activateWindow()
    
    def _on_logout(self) -> None:
        """Handle logout - return to login page like app startup."""
        # Clear auth state first
        self.auth_manager.logout()
        
        # Reset login form
        self.login_page.clear_form()
        
        # Ensure auth_stack is ready and visible BEFORE hiding main window
        self.auth_stack.setCurrentIndex(0)
        self.auth_stack.setWindowTitle("Chemical Equipment Visualizer - Login")
        self.auth_stack.show()
        self.auth_stack.raise_()
        self.auth_stack.activateWindow()
        
        # Now hide and schedule main window for deletion
        if self.main_window:
            self.main_window.hide()
            self.main_window.deleteLater()
            self.main_window = None


def main() -> int:
    """
    Application entry point.
    
    Returns:
        Exit code.
    """
    # Enable high DPI scaling
    QApplication.setAttribute(Qt.AA_EnableHighDpiScaling, True)
    QApplication.setAttribute(Qt.AA_UseHighDpiPixmaps, True)
    
    # Create and run application
    app = Application()
    return app.run()


if __name__ == "__main__":
    sys.exit(main())
