"""
Forms Component Module - Form widgets matching React web UI.

This module provides form components that match the web application's
form styling exactly.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Optional, Callable

from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QFileDialog
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor, QDragEnterEvent, QDropEvent

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS, FONT_SIZES, FONT_WEIGHTS, BORDER_RADIUS, SPACING


class FormGroup(QWidget):
    """
    Form group container with label and input.
    
    Matches web UI .form-group styling.
    
    Args:
        label: Form field label.
        placeholder: Input placeholder text.
        input_type: Input type ('text', 'password', 'email').
        icon: Optional QtAwesome icon name.
        parent: Optional parent widget.
    """
    
    value_changed = pyqtSignal(str)
    
    def __init__(
        self,
        label: str,
        placeholder: str = "",
        input_type: str = "text",
        icon: Optional[str] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.label_text = label
        self.placeholder = placeholder
        self.input_type = input_type
        self.icon_name = icon
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the form group UI."""
        self.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(6)  # margin-bottom: 6px for label
        
        # Label - 13px, font-weight 500
        label = QLabel(self.label_text)
        label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            font-weight: {FONT_WEIGHTS['medium']};
            background: transparent;
        """)
        layout.addWidget(label)
        
        # Input container (for icon support)
        input_container = QWidget()
        input_container.setStyleSheet("background: transparent;")
        input_layout = QHBoxLayout(input_container)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(0)
        
        # Create frame for input with icon
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
        if self.icon_name and HAS_QTAWESOME:
            icon_label = QLabel()
            icon_widget = qta.IconWidget(self.icon_name, color=COLORS['text_muted'])
            icon_widget.setIconSize(16)
            
            # Create a container for icon to center it
            icon_container = QWidget()
            icon_container.setFixedWidth(20)
            icon_container.setStyleSheet("background: transparent;")
            icon_container_layout = QHBoxLayout(icon_container)
            icon_container_layout.setContentsMargins(0, 0, 0, 0)
            icon_container_layout.addWidget(icon_widget)
            
            frame_layout.addWidget(icon_container)
        
        # Input field
        self.input = QLineEdit()
        self.input.setPlaceholderText(self.placeholder)
        
        if self.input_type == 'password':
            self.input.setEchoMode(QLineEdit.Password)
        
        self.input.setStyleSheet(f"""
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
        self.input.textChanged.connect(self.value_changed.emit)
        
        frame_layout.addWidget(self.input, 1)
        
        input_layout.addWidget(input_frame)
        layout.addWidget(input_container)
    
    def get_value(self) -> str:
        """Get the input value."""
        return self.input.text()
    
    def set_value(self, value: str) -> None:
        """Set the input value."""
        self.input.setText(value)
    
    def clear(self) -> None:
        """Clear the input."""
        self.input.clear()
    
    def set_disabled(self, disabled: bool) -> None:
        """Set disabled state."""
        self.input.setDisabled(disabled)


class FileDropzone(QFrame):
    """
    File dropzone matching web UI dropzone styling.
    
    Supports drag-and-drop and click-to-browse for file selection.
    
    Signals:
        file_selected: Emitted with file path when a file is selected.
        file_cleared: Emitted when file selection is cleared.
    
    Args:
        accept: File type filter (e.g., "CSV Files (*.csv)").
        parent: Optional parent widget.
    """
    
    file_selected = pyqtSignal(str)
    file_cleared = pyqtSignal()
    
    def __init__(
        self,
        accept: str = "CSV Files (*.csv)",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.accept = accept
        self.selected_file: Optional[str] = None
        self.is_dragging = False
        
        self.setAcceptDrops(True)
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the dropzone UI."""
        self._update_style()
        
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self.setMinimumHeight(150)
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(40, 40, 40, 40)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        self.icon_label = QLabel()
        self.icon_label.setAlignment(Qt.AlignCenter)
        if HAS_QTAWESOME:
            icon_widget = qta.IconWidget('fa5s.cloud-upload-alt', color=COLORS['gray_400'])
            icon_widget.setIconSize(40)
            layout.addWidget(icon_widget, alignment=Qt.AlignCenter)
        else:
            self.icon_label.setText("📤")
            self.icon_label.setStyleSheet(f"font-size: 40px; color: {COLORS['gray_400']};")
            layout.addWidget(self.icon_label)
        
        # Text
        text_label = QLabel("Drag and drop your CSV file here, or click to browse")
        text_label.setAlignment(Qt.AlignCenter)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
        """)
        layout.addWidget(text_label)
        
        # Hint
        hint_label = QLabel("Supports: .csv files")
        hint_label.setAlignment(Qt.AlignCenter)
        hint_label.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: {FONT_SIZES['xs']}px;
            background: transparent;
        """)
        layout.addWidget(hint_label)
        
        # Selected file display (hidden by default)
        self.file_display = QFrame()
        self.file_display.setVisible(False)
        self.file_display.setStyleSheet(f"""
            QFrame {{
                background: rgba(5, 150, 105, 0.08);
                border: 1px solid rgba(5, 150, 105, 0.2);
                border-radius: {BORDER_RADIUS['md']}px;
            }}
        """)
        
        file_layout = QHBoxLayout(self.file_display)
        file_layout.setContentsMargins(16, 12, 16, 12)
        file_layout.setSpacing(12)
        
        if HAS_QTAWESOME:
            file_icon = qta.IconWidget('fa5s.file-csv', color=COLORS['secondary'])
            file_icon.setIconSize(24)
            file_layout.addWidget(file_icon)
        
        self.file_name_label = QLabel()
        self.file_name_label.setStyleSheet(f"""
            color: {COLORS['secondary']};
            font-size: {FONT_SIZES['sm']}px;
            font-weight: {FONT_WEIGHTS['medium']};
            background: transparent;
        """)
        file_layout.addWidget(self.file_name_label, 1)
        
        # Clear button
        clear_btn = QPushButton("✕")
        clear_btn.setFixedSize(24, 24)
        clear_btn.setCursor(QCursor(Qt.PointingHandCursor))
        clear_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_muted']};
                border: none;
                border-radius: 12px;
                font-size: 14px;
            }}
            QPushButton:hover {{
                background: rgba(0, 0, 0, 0.1);
                color: {COLORS['danger']};
            }}
        """)
        clear_btn.clicked.connect(self._clear_file)
        file_layout.addWidget(clear_btn)
        
        layout.addWidget(self.file_display)
    
    def _update_style(self) -> None:
        """Update frame style based on state."""
        if self.is_dragging:
            border_color = COLORS['primary']
            bg_color = COLORS['primary_bg']
        else:
            border_color = COLORS['gray_300']
            bg_color = COLORS['gray_50']
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border: 2px dashed {border_color};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
        """)
    
    def mousePressEvent(self, event) -> None:
        """Handle click to browse."""
        if event.button() == Qt.LeftButton:
            self._browse_file()
    
    def dragEnterEvent(self, event: QDragEnterEvent) -> None:
        """Handle drag enter."""
        if event.mimeData().hasUrls():
            urls = event.mimeData().urls()
            if urls and urls[0].toLocalFile().lower().endswith('.csv'):
                event.acceptProposedAction()
                self.is_dragging = True
                self._update_style()
    
    def dragLeaveEvent(self, event) -> None:
        """Handle drag leave."""
        self.is_dragging = False
        self._update_style()
    
    def dropEvent(self, event: QDropEvent) -> None:
        """Handle file drop."""
        self.is_dragging = False
        self._update_style()
        
        urls = event.mimeData().urls()
        if urls:
            file_path = urls[0].toLocalFile()
            if file_path.lower().endswith('.csv'):
                self._set_file(file_path)
    
    def _browse_file(self) -> None:
        """Open file dialog to browse for file."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select CSV File",
            "",
            self.accept
        )
        if file_path:
            self._set_file(file_path)
    
    def _set_file(self, file_path: str) -> None:
        """Set the selected file."""
        import os
        self.selected_file = file_path
        self.file_name_label.setText(os.path.basename(file_path))
        self.file_display.setVisible(True)
        self.file_selected.emit(file_path)
    
    def _clear_file(self) -> None:
        """Clear the selected file."""
        self.selected_file = None
        self.file_display.setVisible(False)
        self.file_cleared.emit()
    
    def get_file(self) -> Optional[str]:
        """Get the selected file path."""
        return self.selected_file


class InfoBox(QFrame):
    """
    Info box matching web UI .upload-info styling.
    
    Displays expected format information with a left border accent.
    
    Args:
        title: Info box title.
        description: Description text.
        items: List of bullet point items (can contain HTML).
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        title: str,
        description: str = "",
        items: Optional[list] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.title_text = title
        self.description = description
        self.items = items or []
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the info box UI."""
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['gray_50']};
                border: 1px solid {COLORS['gray_200']};
                border-left: 3px solid {COLORS['primary']};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        layout.setSpacing(SPACING['sm'])
        
        # Title
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet(f"""
            color: {COLORS['gray_900']};
            font-size: {FONT_SIZES['lg']}px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            padding-left: {SPACING['md']}px;
        """)
        layout.addWidget(title_label)
        
        # Description
        if self.description:
            desc_label = QLabel(self.description)
            desc_label.setWordWrap(True)
            desc_label.setStyleSheet(f"""
                color: {COLORS['gray_600']};
                font-size: {FONT_SIZES['sm']}px;
                background: transparent;
                padding-left: {SPACING['md']}px;
            """)
            layout.addWidget(desc_label)
        
        layout.addSpacing(8)
        
        # Bullet items
        for item in self.items:
            item_widget = self._create_bullet_item(item)
            layout.addWidget(item_widget)
    
    def _create_bullet_item(self, item) -> QWidget:
        """Create a bullet point item."""
        # Handle both string and tuple (label, description) format
        if isinstance(item, tuple):
            label, desc = item
            text = f"<b>{label}</b>: {desc}"
        else:
            text = str(item)
        
        widget = QWidget()
        widget.setStyleSheet("background: transparent;")
        
        item_layout = QHBoxLayout(widget)
        item_layout.setContentsMargins(SPACING['md'], 0, 0, 0)
        item_layout.setSpacing(SPACING['lg'])
        
        # Bullet
        bullet = QLabel()
        bullet.setFixedSize(6, 6)
        bullet.setStyleSheet(f"""
            background: {COLORS['secondary']};
            border-radius: 3px;
        """)
        item_layout.addWidget(bullet, alignment=Qt.AlignTop)
        
        # Text (supports HTML for bold)
        text_label = QLabel(text)
        text_label.setWordWrap(True)
        text_label.setStyleSheet(f"""
            color: {COLORS['gray_600']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
            line-height: 1.6;
        """)
        text_label.setTextFormat(Qt.RichText)
        item_layout.addWidget(text_label, 1)
        
        return widget


class NoteBox(QFrame):
    """
    Note/warning box matching web UI .history-note styling.
    
    Args:
        text: Note text content (can contain HTML).
        variant: Box variant ('info', 'warning', 'danger').
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        text: str,
        variant: str = 'warning',
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.text = text
        self.variant = variant
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the note box UI."""
        # Variant colors
        variant_styles = {
            'info': {
                'bg': COLORS['primary_bg'],
                'border': COLORS['primary'],
                'text': COLORS['primary_dark'],
            },
            'warning': {
                'bg': '#fffbeb',
                'border': COLORS['warning'],
                'text': COLORS['warning_dark'],
            },
            'danger': {
                'bg': '#fef2f2',
                'border': COLORS['danger'],
                'text': COLORS['danger'],
            },
        }
        
        style = variant_styles.get(self.variant, variant_styles['warning'])
        
        self.setStyleSheet(f"""
            QFrame {{
                background: {style['bg']};
                border: 1px solid {style['border']};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
        
        text_label = QLabel(self.text)
        text_label.setWordWrap(True)
        text_label.setTextFormat(Qt.RichText)
        text_label.setStyleSheet(f"""
            color: {style['text']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
        """)
        layout.addWidget(text_label)
