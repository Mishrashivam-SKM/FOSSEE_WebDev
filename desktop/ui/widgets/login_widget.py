"""
Login Widget - Authentication login page matching React Login.jsx.

This module provides the login page that matches the web application's
authentication UI exactly.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Optional

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFrame, QSizePolicy, QSpacerItem, QCheckBox
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS, FONT_SIZES, FONT_WEIGHTS, BORDER_RADIUS, SPACING
from ui.components.forms import FormGroup
from ui.components.buttons import ActionButton


class LoginWidget(QWidget):
    """
    Login page widget matching web UI auth-page styling.
    
    Centered card on dark background with logo, form inputs with icons,
    and submit button.
    
    Signals:
        login_success: Emitted with user data on successful login.
        register_requested: Emitted when user clicks register link.
    
    Args:
        api_client: APIClient instance for authentication.
        auth_manager: AuthManager instance for token storage.
        parent: Optional parent widget.
    """
    
    login_success = pyqtSignal()
    register_requested = pyqtSignal()
    
    def __init__(self, api_client, auth_manager, parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        
        self.api_client = api_client
        self.auth_manager = auth_manager
        self.loading = False
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the login page UI matching web auth-page."""
        # Dark background matching web .auth-page
        self.setStyleSheet(f"background: {COLORS['bg_sidebar']};")
        
        # Center the form
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(24, 24, 24, 24)
        main_layout.setAlignment(Qt.AlignCenter)
        
        # Auth container - max-width: 400px, padding: 40px 36px
        container = QFrame()
        container.setFixedWidth(400)
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border-radius: {BORDER_RADIUS['xl']}px;
            }}
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(36, 40, 36, 40)
        container_layout.setSpacing(0)
        
        # =================================================================
        # HEADER - logo, title, subtitle
        # =================================================================
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 28)
        header_layout.setSpacing(0)
        header_layout.setAlignment(Qt.AlignCenter)
        
        # Logo - CEV
        logo = QLabel("CEV")
        logo.setAlignment(Qt.AlignCenter)
        logo.setStyleSheet(f"""
            color: {COLORS['primary']};
            font-size: 24px;
            font-weight: {FONT_WEIGHTS['bold']};
            background: transparent;
            margin-bottom: 12px;
        """)
        header_layout.addWidget(logo)
        
        # Title
        title = QLabel("Chemical Equipment Visualizer")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 20px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            margin-bottom: 6px;
        """)
        header_layout.addWidget(title)
        
        # Subtitle
        subtitle = QLabel("Sign in to your account")
        subtitle.setAlignment(Qt.AlignCenter)
        subtitle.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        container_layout.addWidget(header)
        
        # =================================================================
        # FORM
        # =================================================================
        form = QWidget()
        form.setStyleSheet("background: transparent;")
        form_layout = QVBoxLayout(form)
        form_layout.setContentsMargins(0, 0, 0, 0)
        form_layout.setSpacing(16)
        
        # Username field
        username_group = self._create_input_group(
            "Username",
            "Enter your username",
            "fa5s.user",
            "text"
        )
        self.username_input = username_group.findChild(QLineEdit)
        form_layout.addWidget(username_group)
        
        # Password field
        password_group = self._create_input_group(
            "Password",
            "Enter your password",
            "fa5s.lock",
            "password"
        )
        self.password_input = password_group.findChild(QLineEdit)
        form_layout.addWidget(password_group)
        
        # Remember Me checkbox
        remember_row = QWidget()
        remember_row.setStyleSheet("background: transparent;")
        remember_layout = QHBoxLayout(remember_row)
        remember_layout.setContentsMargins(0, 4, 0, 8)
        
        self.remember_checkbox = QCheckBox("Remember me")
        self.remember_checkbox.setChecked(True)  # Default to checked
        self.remember_checkbox.setCursor(QCursor(Qt.PointingHandCursor))
        self.remember_checkbox.setStyleSheet(f"""
            QCheckBox {{
                color: {COLORS['text_secondary']};
                font-size: {FONT_SIZES['sm']}px;
                spacing: 8px;
                background: transparent;
            }}
            QCheckBox::indicator {{
                width: 18px;
                height: 18px;
                border-radius: 4px;
                border: 1px solid {COLORS['border']};
                background: {COLORS['bg_secondary']};
            }}
            QCheckBox::indicator:checked {{
                background: {COLORS['primary']};
                border-color: {COLORS['primary']};
            }}
            QCheckBox::indicator:hover {{
                border-color: {COLORS['primary']};
            }}
        """)
        remember_layout.addWidget(self.remember_checkbox)
        remember_layout.addStretch()
        form_layout.addWidget(remember_row)
        
        # Submit button
        self.submit_btn = QPushButton()
        self.submit_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self._set_button_content("Sign In", "fa5s.sign-in-alt")
        self.submit_btn.setMinimumHeight(48)
        self.submit_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                opacity: 0.6;
                background: {COLORS['gray_400']};
            }}
        """)
        self.submit_btn.clicked.connect(self._handle_submit)
        form_layout.addWidget(self.submit_btn)
        
        container_layout.addWidget(form)
        
        # =================================================================
        # FOOTER - register link
        # =================================================================
        footer = QWidget()
        footer.setStyleSheet("background: transparent;")
        footer_layout = QHBoxLayout(footer)
        footer_layout.setContentsMargins(0, 20, 0, 0)
        footer_layout.setAlignment(Qt.AlignCenter)
        
        footer_text = QLabel("Don't have an account?")
        footer_text.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
        """)
        footer_layout.addWidget(footer_text)
        
        register_link = QPushButton("Sign up")
        register_link.setCursor(QCursor(Qt.PointingHandCursor))
        register_link.setStyleSheet(f"""
            QPushButton {{
                color: {COLORS['primary']};
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
                background: transparent;
                border: none;
                padding: 0 4px;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        register_link.clicked.connect(self.register_requested.emit)
        footer_layout.addWidget(register_link)
        
        container_layout.addWidget(footer)
        
        # Error message (hidden by default)
        self.error_label = QLabel()
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setWordWrap(True)
        self.error_label.setVisible(False)
        self.error_label.setStyleSheet(f"""
            color: {COLORS['danger']};
            font-size: {FONT_SIZES['sm']}px;
            background: rgba(220, 38, 38, 0.1);
            padding: 10px;
            border-radius: {BORDER_RADIUS['md']}px;
            margin-top: 12px;
        """)
        container_layout.addWidget(self.error_label)
        
        main_layout.addWidget(container)
    
    def _create_input_group(
        self,
        label: str,
        placeholder: str,
        icon: str,
        input_type: str
    ) -> QWidget:
        """Create an input group with label, icon, and input field."""
        group = QWidget()
        group.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(group)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)
        
        # Label
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            font-weight: {FONT_WEIGHTS['medium']};
            background: transparent;
        """)
        layout.addWidget(label_widget)
        
        # Input container with icon
        input_frame = QFrame()
        input_frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_secondary']};
                border: 1px solid {COLORS['border']};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
            QFrame:focus-within {{
                border-color: {COLORS['primary']};
            }}
        """)
        
        frame_layout = QHBoxLayout(input_frame)
        frame_layout.setContentsMargins(14, 0, 14, 0)
        frame_layout.setSpacing(10)
        
        # Icon
        if HAS_QTAWESOME:
            icon_widget = qta.IconWidget(icon, color=COLORS['text_muted'])
            icon_widget.setIconSize(16)
            icon_widget.setFixedWidth(20)
            frame_layout.addWidget(icon_widget)
        else:
            icon_label = QLabel("👤" if "user" in icon else "🔒")
            icon_label.setStyleSheet(f"color: {COLORS['text_muted']}; font-size: 14px;")
            frame_layout.addWidget(icon_label)
        
        # Input
        input_widget = QLineEdit()
        input_widget.setPlaceholderText(placeholder)
        if input_type == 'password':
            input_widget.setEchoMode(QLineEdit.Password)
        input_widget.setStyleSheet(f"""
            QLineEdit {{
                background: transparent;
                border: none;
                padding: 14px 0;
                font-size: 15px;
                color: {COLORS['text_primary']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_muted']};
            }}
        """)
        # Enter key submits form
        input_widget.returnPressed.connect(self._handle_submit)
        frame_layout.addWidget(input_widget, 1)
        
        layout.addWidget(input_frame)
        
        return group
    
    def _set_button_content(self, text: str, icon: Optional[str] = None) -> None:
        """Set button text and icon."""
        if HAS_QTAWESOME and icon:
            self.submit_btn.setIcon(qta.icon(icon, color='white'))
        self.submit_btn.setText(f"  {text}")
    
    def _handle_submit(self) -> None:
        """Handle form submission."""
        if self.loading:
            return
        
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        remember_me = self.remember_checkbox.isChecked()
        
        # Validation
        if not username or not password:
            self._show_error("Please fill in all fields")
            return
        
        self._set_loading(True)
        self.error_label.setVisible(False)
        
        try:
            response = self.api_client.login(username, password)
            
            if response.get('success'):
                # If not remember me, clear tokens after this session ends
                if not remember_me:
                    self.auth_manager.set_session_only(True)
                else:
                    self.auth_manager.set_session_only(False)
                self.login_success.emit()
            else:
                self._show_error(response.get('error', 'Login failed'))
                
        except Exception as e:
            self._show_error(str(e))
        finally:
            self._set_loading(False)
    
    def _set_loading(self, loading: bool) -> None:
        """Set loading state."""
        self.loading = loading
        self.submit_btn.setDisabled(loading)
        self.username_input.setDisabled(loading)
        self.password_input.setDisabled(loading)
        
        if loading:
            self.submit_btn.setText("  Signing in...")
        else:
            self._set_button_content("Sign In", "fa5s.sign-in-alt")
    
    def _show_error(self, message: str) -> None:
        """Show error message."""
        self.error_label.setText(message)
        self.error_label.setVisible(True)
    
    def clear_form(self) -> None:
        """Clear the form inputs."""
        self.username_input.clear()
        self.password_input.clear()
        self.remember_checkbox.setChecked(True)  # Reset to default
        self.error_label.setVisible(False)
