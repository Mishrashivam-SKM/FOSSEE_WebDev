"""
History Widget Module - Dataset Management Page.

This module provides the history page widget for viewing and managing
uploaded datasets. Includes view, PDF download, and delete functionality.

Features:
    - Dataset list cards with metadata
    - View analytics button (navigates to Analysis)
    - PDF report download to user-chosen location
    - Delete with confirmation dialog
    - Empty state for no datasets

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

import os
from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QMessageBox, QFileDialog, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS
from ui.components.buttons import ActionButton

if TYPE_CHECKING:
    from services.api_client import APIClient


class HoverIconButton(QPushButton):
    """
    Button that changes icon color on hover.
    
    Handles the issue where qtawesome icons have a fixed color
    and don't change with CSS :hover pseudo-class.
    """
    
    def __init__(
        self,
        text: str,
        icon_name: str,
        normal_color: str,
        hover_color: str = "white",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(text, parent)
        self.icon_name = icon_name
        self.normal_color = normal_color
        self.hover_color = hover_color
        self._update_icon(False)
    
    def _update_icon(self, hovered: bool) -> None:
        """Update icon color based on hover state."""
        if HAS_QTAWESOME and self.icon_name and not self.icon_name.startswith(('👁', '📥', '🗑')):
            color = self.hover_color if hovered else self.normal_color
            icon = qta.icon(self.icon_name, color=color)
            self.setIcon(icon)
    
    def enterEvent(self, event) -> None:
        """Handle mouse enter."""
        self._update_icon(True)
        super().enterEvent(event)
    
    def leaveEvent(self, event) -> None:
        """Handle mouse leave."""
        self._update_icon(False)
        super().leaveEvent(event)


class DatasetCard(QFrame):
    """
    Individual dataset card matching web .dataset-card styling.
    
    Shows dataset name, record count, upload date with action buttons.
    
    Signals:
        view_clicked: Emitted when View button clicked (dataset_id).
        pdf_clicked: Emitted when PDF button clicked (dataset_id).
        delete_clicked: Emitted when Delete button clicked (dataset_id, name).
    """
    
    view_clicked = pyqtSignal(int)
    pdf_clicked = pyqtSignal(int)
    delete_clicked = pyqtSignal(int, str)
    
    def __init__(
        self,
        dataset: Dict[str, Any],
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        self.dataset = dataset
        self.dataset_id = dataset.get('id')
        self.dataset_name = dataset.get('name', 'Unnamed')
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the card layout matching web .dataset-card."""
        self.setObjectName("DatasetCard")
        self.setStyleSheet(f"""
            QFrame#DatasetCard {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 12px;
            }}
            QFrame#DatasetCard:hover {{
                border-color: {COLORS['gray_200']};
                background: {COLORS['bg_card']};
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(24, 20, 24, 20)  # padding: lg xl
        layout.setSpacing(20)
        
        # =================================================================
        # LEFT SIDE: Icon + Details
        # =================================================================
        info_layout = QHBoxLayout()
        info_layout.setSpacing(20)
        
        # Dataset icon - 48x48, primary background
        icon_container = QFrame()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['primary_bg']};
                border-radius: 8px;
            }}
        """)
        icon_layout = QVBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        if HAS_QTAWESOME:
            icon_label = QLabel()
            icon = qta.icon('fa5s.database', color=COLORS['primary'])
            icon_label.setPixmap(icon.pixmap(20, 20))
            icon_label.setAlignment(Qt.AlignCenter)
        else:
            icon_label = QLabel("📊")
            icon_label.setStyleSheet(f"font-size: 20px; color: {COLORS['primary']};")
            icon_label.setAlignment(Qt.AlignCenter)
        icon_layout.addWidget(icon_label)
        info_layout.addWidget(icon_container)
        
        # Details column
        details_layout = QVBoxLayout()
        details_layout.setSpacing(4)
        
        # Dataset name - 18px font, bold
        name_label = QLabel(self.dataset_name)
        name_label.setStyleSheet(f"""
            color: {COLORS['gray_900']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
        """)
        details_layout.addWidget(name_label)
        
        # Meta info row
        meta_layout = QHBoxLayout()
        meta_layout.setSpacing(12)
        
        row_count = self.dataset.get('row_count', 0)
        records_label = QLabel(f"<b>{row_count}</b> equipment records")
        records_label.setStyleSheet(f"""
            color: {COLORS['gray_500']};
            font-size: 14px;
            background: transparent;
        """)
        meta_layout.addWidget(records_label)
        
        # Separator dot
        sep = QLabel("•")
        sep.setStyleSheet(f"color: {COLORS['gray_300']}; font-size: 8px; background: transparent;")
        meta_layout.addWidget(sep)
        
        # Upload date
        uploaded_at = self.dataset.get('uploaded_at', '')
        if uploaded_at:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                date_str = dt.strftime("%b %d, %Y at %I:%M %p")
            except:
                date_str = uploaded_at[:10] if len(uploaded_at) >= 10 else uploaded_at
        else:
            date_str = "Unknown"
        
        date_label = QLabel(f"Uploaded {date_str}")
        date_label.setStyleSheet(f"""
            color: {COLORS['gray_500']};
            font-size: 14px;
            background: transparent;
        """)
        meta_layout.addWidget(date_label)
        meta_layout.addStretch()
        
        details_layout.addLayout(meta_layout)
        info_layout.addLayout(details_layout, 1)
        
        layout.addLayout(info_layout, 1)
        
        # =================================================================
        # RIGHT SIDE: Action Buttons
        # =================================================================
        actions_layout = QHBoxLayout()
        actions_layout.setSpacing(8)
        
        # View button - primary outline
        self.view_btn = self._create_action_button(
            "View", "fa5s.eye" if HAS_QTAWESOME else "👁",
            COLORS['primary'], "rgba(30, 64, 175, 0.04)", "rgba(30, 64, 175, 0.3)"
        )
        self.view_btn.clicked.connect(lambda: self.view_clicked.emit(self.dataset_id))
        actions_layout.addWidget(self.view_btn)
        
        # PDF button - secondary outline
        self.pdf_btn = self._create_action_button(
            "PDF", "fa5s.download" if HAS_QTAWESOME else "📥",
            COLORS['secondary'], "rgba(5, 150, 105, 0.04)", "rgba(5, 150, 105, 0.3)"
        )
        self.pdf_btn.clicked.connect(lambda: self.pdf_clicked.emit(self.dataset_id))
        actions_layout.addWidget(self.pdf_btn)
        
        # Delete button - danger outline
        self.delete_btn = self._create_action_button(
            "Delete", "fa5s.trash-alt" if HAS_QTAWESOME else "🗑",
            COLORS['danger'], "rgba(239, 68, 68, 0.04)", "rgba(239, 68, 68, 0.3)"
        )
        self.delete_btn.clicked.connect(
            lambda: self.delete_clicked.emit(self.dataset_id, self.dataset_name)
        )
        actions_layout.addWidget(self.delete_btn)
        
        layout.addLayout(actions_layout)
    
    def _create_action_button(
        self,
        text: str,
        icon_name: str,
        color: str,
        bg_color: str,
        border_color: str
    ) -> QPushButton:
        """Create a styled action button matching web .action-btn."""
        btn = HoverIconButton(text, icon_name, color, "white")
        btn.setCursor(QCursor(Qt.PointingHandCursor))
        btn.setMinimumHeight(38)
        btn.setStyleSheet(f"""
            QPushButton {{
                background: {bg_color};
                color: {color};
                border: 2px solid {border_color};
                border-radius: 8px;
                padding: 8px 16px;
                font-size: 13px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {color};
                color: white;
                border-color: {color};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """)
        
        if not HAS_QTAWESOME or icon_name.startswith(('👁', '📥', '🗑')):
            # Use emoji prefix for fallback
            btn.setText(f"{icon_name} {text}" if len(icon_name) < 3 else text)
        
        return btn
    
    def set_loading(self, button_type: str, loading: bool) -> None:
        """Set loading state for a specific button."""
        btn_map = {
            'view': self.view_btn,
            'pdf': self.pdf_btn,
            'delete': self.delete_btn
        }
        btn = btn_map.get(button_type)
        if btn:
            btn.setEnabled(not loading)
            if loading:
                btn.setText("...")
            else:
                labels = {'view': 'View', 'pdf': 'PDF', 'delete': 'Delete'}
                btn.setText(labels.get(button_type, ''))


class HistoryWidget(QWidget):
    """
    History page widget for dataset management.
    
    Displays all uploaded datasets as cards with actions:
    - View: Navigate to Analysis page
    - PDF: Download report to user-chosen location
    - Delete: Remove dataset with confirmation
    
    Matches web History page styling exactly.
    
    Signals:
        navigate_to: Emitted for navigation (str: page name or "analysis:id").
    
    Args:
        api_client: APIClient instance for backend communication.
        parent: Optional parent widget.
    """
    
    navigate_to = pyqtSignal(str)
    
    def __init__(self, api_client: "APIClient", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.datasets: List[Dict[str, Any]] = []
        self.dataset_cards: List[DatasetCard] = []
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the history page UI layout matching web exactly."""
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # Container with max-width: 1000px
        container = QWidget()
        container.setMaximumWidth(1000)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(24)
        
        # =================================================================
        # PAGE HEADER - matches web .page-header with flex justify-between
        # =================================================================
        header_row = QHBoxLayout()
        header_row.setContentsMargins(0, 0, 0, 4)
        
        # Left side: Title + subtitle
        header_left = QVBoxLayout()
        header_left.setSpacing(4)
        
        title = QLabel("Upload History")
        title.setFont(QFont("", 22, QFont.Bold))
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            background: transparent;
            letter-spacing: -0.01em;
        """)
        header_left.addWidget(title)
        
        subtitle = QLabel("View and manage your uploaded datasets (max 5 stored)")
        subtitle.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
            background: transparent;
        """)
        header_left.addWidget(subtitle)
        
        header_row.addLayout(header_left)
        header_row.addStretch()
        
        # Right side: Upload New button
        upload_btn = QPushButton("Upload New")
        upload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        upload_btn.clicked.connect(lambda: self.navigate_to.emit("upload"))
        upload_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
        """)
        
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.upload', color='white')
            upload_btn.setIcon(icon)
        
        header_row.addWidget(upload_btn)
        container_layout.addLayout(header_row)
        
        # =================================================================
        # SCROLLABLE CONTENT
        # =================================================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        scroll_content = QWidget()
        scroll_content.setStyleSheet("background: transparent;")
        self.list_layout = QVBoxLayout(scroll_content)
        self.list_layout.setContentsMargins(0, 0, 0, 0)
        self.list_layout.setSpacing(16)  # gap: md
        
        # Empty state placeholder (will be hidden when datasets exist)
        self.empty_state = self._create_empty_state()
        self.list_layout.addWidget(self.empty_state)
        
        self.list_layout.addStretch()
        
        scroll.setWidget(scroll_content)
        container_layout.addWidget(scroll, 1)
        
        # =================================================================
        # HISTORY NOTE - matches web .history-note
        # =================================================================
        note = QLabel(
            "<b>Note:</b> Only the last 5 uploaded datasets are stored. "
            "Older datasets are automatically removed when new ones are uploaded."
        )
        note.setWordWrap(True)
        note.setStyleSheet(f"""
            background: {COLORS['bg_secondary']};
            color: {COLORS['text_secondary']};
            padding: 16px 20px;
            border-radius: 8px;
            font-size: 13px;
        """)
        container_layout.addWidget(note)
        
        main_layout.addWidget(container)
    
    def _create_empty_state(self) -> QFrame:
        """Create empty state widget matching web .empty-state."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 12px;
            }}
        """)
        # Set minimum height to ensure proper spacing when empty
        frame.setMinimumHeight(300)
        frame.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(48, 64, 48, 64)
        layout.setSpacing(12)
        layout.setAlignment(Qt.AlignCenter)
        
        # Icon
        if HAS_QTAWESOME:
            icon_label = QLabel()
            icon = qta.icon('fa5s.database', color=COLORS['gray_300'])
            icon_label.setPixmap(icon.pixmap(48, 48))
            icon_label.setAlignment(Qt.AlignCenter)
        else:
            icon_label = QLabel("📊")
            icon_label.setStyleSheet(f"font-size: 48px; color: {COLORS['gray_300']};")
            icon_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(icon_label)
        
        # Title
        title = QLabel("No Datasets Yet")
        title.setStyleSheet(f"""
            color: {COLORS['gray_800']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
        """)
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        # Description
        desc = QLabel("You haven't uploaded any data files. Get started by uploading your first CSV.")
        desc.setStyleSheet(f"""
            color: {COLORS['gray_500']};
            font-size: 14px;
            background: transparent;
            max-width: 400px;
        """)
        desc.setAlignment(Qt.AlignCenter)
        desc.setWordWrap(True)
        layout.addWidget(desc)
        
        layout.addSpacing(16)
        
        # Upload button
        upload_btn = QPushButton("Upload Data")
        upload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        upload_btn.clicked.connect(lambda: self.navigate_to.emit("upload"))
        upload_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 8px;
                padding: 12px 24px;
                font-size: 14px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
        """)
        layout.addWidget(upload_btn, alignment=Qt.AlignCenter)
        
        return frame
    
    def refresh(self) -> None:
        """Refresh the dataset list from API."""
        self._load_datasets()
    
    def _load_datasets(self) -> None:
        """Load datasets from API."""
        try:
            data = self.api_client.get_datasets()
            if data.get('success', True):  # Default to True for successful responses
                datasets = data.get('datasets', data.get('results', []))
                self.update_datasets(datasets)
        except Exception as e:
            print(f"Error loading datasets: {e}")
    
    def update_datasets(self, datasets: List[Dict[str, Any]]) -> None:
        """
        Update the displayed datasets.
        
        Args:
            datasets: List of dataset dictionaries from API.
        """
        self.datasets = datasets
        
        # Clear existing cards
        for card in self.dataset_cards:
            card.deleteLater()
        self.dataset_cards.clear()
        
        # Show/hide empty state
        self.empty_state.setVisible(len(datasets) == 0)
        
        # Create new cards
        for dataset in datasets:
            card = DatasetCard(dataset)
            card.view_clicked.connect(self._on_view)
            card.pdf_clicked.connect(self._on_download_pdf)
            card.delete_clicked.connect(self._on_delete)
            
            # Insert before the stretch
            self.list_layout.insertWidget(len(self.dataset_cards), card)
            self.dataset_cards.append(card)
    
    def _show_styled_message(self, title: str, message: str, icon_type: str = "info") -> None:
        """Show a styled message box with proper color contrast."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if icon_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif icon_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
        elif icon_type == "question":
            msg_box.setIcon(QMessageBox.Question)
        else:
            msg_box.setIcon(QMessageBox.Information)
        
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['bg_card']};
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
                font-size: 14px;
                min-width: 250px;
                padding: 8px;
            }}
            QMessageBox QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
        """)
        msg_box.exec_()
    
    def _show_styled_confirm(self, title: str, message: str) -> bool:
        """Show a styled confirmation dialog with proper color contrast."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        msg_box.setIcon(QMessageBox.Question)
        msg_box.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg_box.setDefaultButton(QMessageBox.No)
        
        msg_box.setStyleSheet(f"""
            QMessageBox {{
                background-color: {COLORS['bg_card']};
            }}
            QMessageBox QLabel {{
                color: {COLORS['text_primary']};
                font-size: 14px;
                min-width: 280px;
                padding: 8px;
            }}
            QMessageBox QPushButton {{
                background: {COLORS['gray_200']};
                color: {COLORS['text_primary']};
                border: none;
                border-radius: 6px;
                padding: 8px 20px;
                font-size: 13px;
                font-weight: 600;
                min-width: 80px;
            }}
            QMessageBox QPushButton:hover {{
                background: {COLORS['gray_300']};
            }}
            QMessageBox QPushButton[text="Yes"], 
            QMessageBox QPushButton[text="&Yes"] {{
                background: {COLORS['danger']};
                color: white;
            }}
            QMessageBox QPushButton[text="Yes"]:hover,
            QMessageBox QPushButton[text="&Yes"]:hover {{
                background: {COLORS['danger_light']};
            }}
        """)
        return msg_box.exec_() == QMessageBox.Yes

    def _on_view(self, dataset_id: int) -> None:
        """Handle view button click."""
        self.navigate_to.emit(f"analysis:{dataset_id}")
    
    def _on_download_pdf(self, dataset_id: int) -> None:
        """Handle PDF download with file save dialog."""
        # Find the dataset name
        dataset = next((d for d in self.datasets if d['id'] == dataset_id), None)
        default_name = dataset.get('name', 'report') if dataset else 'report'
        default_name = f"{default_name}_report.pdf"
        
        # Ask user where to save
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            default_name,
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return  # User cancelled
        
        # Find the card and set loading state
        for card in self.dataset_cards:
            if card.dataset_id == dataset_id:
                card.set_loading('pdf', True)
                break
        
        try:
            success = self.api_client.download_pdf(dataset_id, file_path)
            
            if success:
                self._show_styled_message(
                    "Success",
                    f"PDF report saved to:\n{file_path}",
                    "info"
                )
            else:
                self._show_styled_message("Error", "Failed to download PDF", "error")
        except Exception as e:
            self._show_styled_message("Error", f"Failed to download PDF:\n{str(e)}", "error")
        finally:
            for card in self.dataset_cards:
                if card.dataset_id == dataset_id:
                    card.set_loading('pdf', False)
                    break
    
    def _on_delete(self, dataset_id: int, name: str) -> None:
        """Handle delete with confirmation."""
        confirmed = self._show_styled_confirm(
            "Confirm Delete",
            f'Are you sure you want to delete "{name}"?'
        )
        
        if not confirmed:
            return
        
        # Find the card and set loading state
        for card in self.dataset_cards:
            if card.dataset_id == dataset_id:
                card.set_loading('delete', True)
                break
        
        try:
            result = self.api_client.delete_dataset(dataset_id)
            
            if result.get('success', True):  # Success if 'success' not in response or True
                # Refresh the list
                self._load_datasets()
            else:
                error = result.get('error', 'Delete failed')
                self._show_styled_message("Error", f"Failed to delete dataset:\n{error}", "error")
        except Exception as e:
            self._show_styled_message("Error", f"Failed to delete dataset:\n{str(e)}", "error")
        finally:
            for card in self.dataset_cards:
                if card.dataset_id == dataset_id:
                    card.set_loading('delete', False)
                    break
