"""
Main Window Module - Application Shell with Sidebar Navigation.

This module provides the main application window with a fixed sidebar
for navigation between pages. Matches the web Layout component exactly.

Features:
    - Fixed 220px sidebar with dark theme
    - CEV branding header
    - Navigation links with active state
    - User info and logout in footer
    - Content area for page widgets

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QHBoxLayout, QVBoxLayout,
    QLabel, QPushButton, QFrame, QStackedWidget, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS

if TYPE_CHECKING:
    from services.api_client import APIClient
    from services.auth_manager import AuthManager


class NavLink(QPushButton):
    """
    Navigation link button matching web .nav-link styling.
    
    Provides hover and active states with icon support.
    """
    
    def __init__(
        self,
        text: str,
        icon_name: str,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(text, parent)
        self.icon_name = icon_name
        self._active = False
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the nav link styling."""
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(44)
        
        if HAS_QTAWESOME:
            icon = qta.icon(self.icon_name, color='rgba(255,255,255,0.7)')
            self.setIcon(icon)
        
        self._apply_style()
    
    def _apply_style(self) -> None:
        """Apply appropriate style based on active state."""
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
            """)
            if HAS_QTAWESOME:
                icon = qta.icon(self.icon_name, color='white')
                self.setIcon(icon)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: rgba(255, 255, 255, 0.7);
                    border: none;
                    border-radius: 8px;
                    padding: 12px 20px;
                    font-size: 14px;
                    font-weight: 500;
                    text-align: left;
                }}
                QPushButton:hover {{
                    background: rgba(255, 255, 255, 0.05);
                    color: white;
                }}
            """)
            if HAS_QTAWESOME:
                icon = qta.icon(self.icon_name, color='rgba(255,255,255,0.7)')
                self.setIcon(icon)
    
    def set_active(self, active: bool) -> None:
        """Set the active state of the nav link."""
        self._active = active
        self._apply_style()


class MainWindow(QMainWindow):
    """
    Main application window with sidebar navigation.
    
    Provides the application shell matching the web Layout component:
    - Fixed 220px dark sidebar
    - CEV branding header
    - Nav links: Dashboard, Upload Data, History
    - User info footer with logout
    - Content area for page widgets
    
    Signals:
        logout_requested: Emitted when user clicks logout.
    
    Args:
        api_client: APIClient instance for backend communication.
        auth_manager: AuthManager for user session handling.
        parent: Optional parent widget.
    """
    
    logout_requested = pyqtSignal()
    
    def __init__(
        self,
        api_client: "APIClient",
        auth_manager: "AuthManager",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.auth_manager = auth_manager
        self.current_page = "dashboard"
        self._setup_ui()
        self._setup_pages()
    
    def _setup_ui(self) -> None:
        """Setup the main window UI layout."""
        self.setWindowTitle("Chemical Equipment Visualizer")
        self.setMinimumSize(1200, 800)
        self.resize(1400, 900)
        
        # Central widget
        central = QWidget()
        central.setStyleSheet(f"background: {COLORS['bg_primary']};")
        self.setCentralWidget(central)
        
        main_layout = QHBoxLayout(central)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # =================================================================
        # SIDEBAR - matches web .sidebar (220px, dark)
        # =================================================================
        sidebar = QFrame()
        sidebar.setFixedWidth(220)
        sidebar.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_sidebar']};
            }}
        """)
        
        sidebar_layout = QVBoxLayout(sidebar)
        sidebar_layout.setContentsMargins(0, 0, 0, 0)
        sidebar_layout.setSpacing(0)
        
        # Sidebar header - matches web .sidebar-header
        header = QFrame()
        header.setStyleSheet(f"""
            QFrame {{
                background: rgba(0, 0, 0, 0.1);
                border-bottom: 1px solid rgba(255, 255, 255, 0.06);
            }}
        """)
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(20, 18, 20, 18)
        header_layout.setSpacing(2)
        
        # Logo - CEV
        logo_row = QHBoxLayout()
        logo_row.setSpacing(8)
        
        if HAS_QTAWESOME:
            flask_icon = qta.icon('fa5s.flask', color='white')
            flask_label = QLabel()
            flask_label.setPixmap(flask_icon.pixmap(22, 22))
            flask_label.setStyleSheet("background: transparent;")
            logo_row.addWidget(flask_label)
        
        logo_text = QLabel("CEV")
        logo_text.setStyleSheet(f"""
            color: white;
            font-size: 20px;
            font-weight: 700;
            background: transparent;
        """)
        logo_row.addWidget(logo_text)
        logo_row.addStretch()
        header_layout.addLayout(logo_row)
        
        # Subtitle
        subtitle = QLabel("EQUIPMENT VISUALIZER")
        subtitle.setStyleSheet(f"""
            color: rgba(255, 255, 255, 0.5);
            font-size: 10px;
            letter-spacing: 0.5px;
            background: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        sidebar_layout.addWidget(header)
        
        # Navigation - matches web .sidebar-nav
        nav = QWidget()
        nav.setStyleSheet("background: transparent;")
        nav_layout = QVBoxLayout(nav)
        nav_layout.setContentsMargins(12, 24, 12, 24)
        nav_layout.setSpacing(6)
        
        # Nav links
        self.nav_dashboard = NavLink("Dashboard", "fa5s.home")
        self.nav_dashboard.clicked.connect(lambda: self._navigate("dashboard"))
        nav_layout.addWidget(self.nav_dashboard)
        
        self.nav_upload = NavLink("Upload Data", "fa5s.upload")
        self.nav_upload.clicked.connect(lambda: self._navigate("upload"))
        nav_layout.addWidget(self.nav_upload)
        
        self.nav_history = NavLink("History", "fa5s.clock")
        self.nav_history.clicked.connect(lambda: self._navigate("history"))
        nav_layout.addWidget(self.nav_history)
        
        nav_layout.addStretch()
        sidebar_layout.addWidget(nav, 1)
        
        # Sidebar footer - matches web .sidebar-footer
        footer = QFrame()
        footer.setStyleSheet(f"""
            QFrame {{
                background: rgba(255, 255, 255, 0.05);
                border-radius: 8px;
                margin: 8px;
            }}
        """)
        footer_layout = QVBoxLayout(footer)
        footer_layout.setContentsMargins(16, 16, 16, 16)
        footer_layout.setSpacing(12)
        
        # User info
        user_row = QHBoxLayout()
        user_row.setSpacing(10)
        
        if HAS_QTAWESOME:
            user_icon = QLabel()
            icon = qta.icon('fa5s.user', color=COLORS['primary_light'])
            user_icon.setPixmap(icon.pixmap(18, 18))
        else:
            user_icon = QLabel("👤")
            user_icon.setStyleSheet("font-size: 18px;")
        user_row.addWidget(user_icon)
        
        self.username_label = QLabel("User")
        self.username_label.setStyleSheet(f"""
            color: white;
            font-size: 13px;
            font-weight: 500;
            background: transparent;
        """)
        user_row.addWidget(self.username_label)
        user_row.addStretch()
        
        footer_layout.addLayout(user_row)
        
        # Logout button - matches web .logout-btn
        self.logout_btn = QPushButton("  Logout")  # Added spacing for icon
        self.logout_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.logout_btn.clicked.connect(self._on_logout)
        self.logout_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: rgba(255, 255, 255, 0.7);
                border: 1px solid rgba(255, 255, 255, 0.15);
                border-radius: 6px;
                padding: 10px 16px;
                font-size: 13px;
                text-align: left;
            }}
            QPushButton:hover {{
                background: rgba(220, 38, 38, 0.2);
                color: #fca5a5;
                border-color: rgba(220, 38, 38, 0.4);
            }}
        """)
        
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.sign-out-alt', color='rgba(255,255,255,0.7)')
            self.logout_btn.setIcon(icon)
        
        # Update icon color on hover using event filter
        self.logout_btn.enterEvent = self._on_logout_hover_enter
        self.logout_btn.leaveEvent = self._on_logout_hover_leave
        
        footer_layout.addWidget(self.logout_btn)
        sidebar_layout.addWidget(footer)
        
        main_layout.addWidget(sidebar)
        
        # =================================================================
        # MAIN CONTENT - matches web .main-content
        # =================================================================
        content = QWidget()
        content.setStyleSheet(f"background: {COLORS['bg_primary']};")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(28, 28, 28, 28)  # padding: 28px
        content_layout.setSpacing(0)
        
        # Stacked widget for pages
        self.page_stack = QStackedWidget()
        self.page_stack.setStyleSheet("background: transparent;")
        content_layout.addWidget(self.page_stack)
        
        main_layout.addWidget(content, 1)
        
        # Set initial active nav
        self.nav_dashboard.set_active(True)
    
    def _setup_pages(self) -> None:
        """Setup page widgets."""
        from ui.widgets.dashboard_widget import DashboardWidget
        from ui.widgets.upload_widget import UploadWidget
        from ui.widgets.history_widget import HistoryWidget
        from ui.widgets.analysis_widget import AnalysisWidget
        
        # Dashboard page
        self.dashboard_page = DashboardWidget(self.api_client)
        self.dashboard_page.navigate_to.connect(self._on_page_navigate)
        self.page_stack.addWidget(self.dashboard_page)
        
        # Upload page
        self.upload_page = UploadWidget(self.api_client)
        self.upload_page.upload_success.connect(self._on_upload_success)
        self.page_stack.addWidget(self.upload_page)
        
        # History page
        self.history_page = HistoryWidget(self.api_client)
        self.history_page.navigate_to.connect(self._on_page_navigate)
        self.page_stack.addWidget(self.history_page)
        
        # Analysis page (hidden from nav, accessed via history)
        self.analysis_page = AnalysisWidget(self.api_client)
        self.analysis_page.navigate_to.connect(self._on_page_navigate)
        self.page_stack.addWidget(self.analysis_page)
    
    def _navigate(self, page: str) -> None:
        """
        Navigate to a specific page.
        
        Args:
            page: Page name ('dashboard', 'upload', 'history', 'analysis').
        """
        self.current_page = page
        
        # Update nav active states
        self.nav_dashboard.set_active(page == "dashboard")
        self.nav_upload.set_active(page == "upload")
        self.nav_history.set_active(page == "history")
        
        # Switch page
        page_map = {
            "dashboard": 0,
            "upload": 1,
            "history": 2,
            "analysis": 3
        }
        
        index = page_map.get(page, 0)
        self.page_stack.setCurrentIndex(index)
        
        # Refresh page data
        if page == "dashboard":
            self.dashboard_page.refresh()
        elif page == "history":
            self.history_page.refresh()
    
    def _on_page_navigate(self, target: str) -> None:
        """
        Handle navigation requests from pages.
        
        Args:
            target: Target page or "analysis:id" format.
        """
        if target.startswith("analysis:"):
            # Extract dataset ID and load analysis
            dataset_id = int(target.split(":")[1])
            self.analysis_page.load_dataset(dataset_id)
            self._navigate("analysis")
        else:
            self._navigate(target)
    
    def _on_upload_success(self, dataset: dict) -> None:
        """Handle successful upload."""
        # Navigate to dashboard to show new data
        self._navigate("dashboard")
    
    def _on_logout(self) -> None:
        """Handle logout button click."""
        self.auth_manager.logout()
        self.logout_requested.emit()
    
    def _on_logout_hover_enter(self, event) -> None:
        """Handle logout button hover enter - change icon color."""
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.sign-out-alt', color='#fca5a5')
            self.logout_btn.setIcon(icon)
    
    def _on_logout_hover_leave(self, event) -> None:
        """Handle logout button hover leave - reset icon color."""
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.sign-out-alt', color='rgba(255,255,255,0.7)')
            self.logout_btn.setIcon(icon)
    
    def set_user(self, username: str) -> None:
        """
        Set the displayed username.
        
        Args:
            username: Username to display in sidebar.
        """
        self.username_label.setText(username)
    
    def showEvent(self, event) -> None:
        """Handle show event to refresh data."""
        super().showEvent(event)
        
        # Update username
        user = self.auth_manager.get_user()
        if user:
            self.set_user(user.get('username', 'User'))
        
        # Refresh current page
        if self.current_page == "dashboard":
            self.dashboard_page.refresh()
        elif self.current_page == "history":
            self.history_page.refresh()
