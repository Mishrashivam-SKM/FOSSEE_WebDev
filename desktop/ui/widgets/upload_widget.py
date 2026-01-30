"""
Upload Widget Module - CSV File Upload Page.

This module provides the upload page widget for submitting CSV files
containing chemical equipment data. Uses the new modular component system
for pixel-perfect web UI matching.

Features:
    - File browser with dropzone styling
    - Optional custom dataset naming
    - Progress indication during upload
    - Success/error status feedback
    - Form reset after successful upload

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

import os
from typing import Any, Dict, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QPushButton, QFileDialog, QProgressBar, QFrame, QSizePolicy
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
from ui.components.forms import FormGroup, FileDropzone, InfoBox
from ui.components.constants import GRID_GAPS

if TYPE_CHECKING:
    from services import APIClient


class UploadWidget(QWidget):
    """
    Upload page widget for CSV file submission.
    
    Provides a user-friendly interface for uploading CSV files with:
    - File selection via browse dialog
    - Optional custom dataset naming
    - Upload progress indication
    - Status message feedback
    
    Matches web Upload page styling exactly.
    
    Signals:
        upload_success: Emitted with dataset info after successful upload.
    
    Args:
        api_client: APIClient instance for backend communication.
        parent: Optional parent widget.
    """
    
    upload_success = pyqtSignal(dict)
    
    def __init__(self, api_client: "APIClient", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.file_path: Optional[str] = None
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the upload page UI layout matching web exactly."""
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        main_layout.setAlignment(Qt.AlignTop)
        
        # =================================================================
        # PAGE HEADER - matches web .page-header
        # =================================================================
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 28)  # margin-bottom: 28px
        header_layout.setSpacing(4)
        
        # Title - 22px, bold
        title = QLabel("Upload Data")
        title.setFont(QFont("", 22, QFont.Bold))
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']}; 
            background: transparent;
            letter-spacing: -0.01em;
        """)
        header_layout.addWidget(title)
        
        # Subtitle - 13px
        subtitle = QLabel("Upload a CSV file containing chemical equipment data")
        subtitle.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 13px; 
            background: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        main_layout.addWidget(header)
        
        # =================================================================
        # UPLOAD CONTAINER - matches web .upload-container (max-width: 700px)
        # =================================================================
        container = QFrame()
        container.setMaximumWidth(700)
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
        """)
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(32, 32, 32, 32)  # padding: 32px
        container_layout.setSpacing(GRID_GAPS['form'])  # 24px
        
        # =================================================================
        # SECTION: Select CSV File
        # =================================================================
        file_section_label = self._create_section_label("Select CSV File")
        container_layout.addWidget(file_section_label)
        
        # File selection row with dropzone styling
        file_row = QHBoxLayout()
        file_row.setSpacing(12)
        
        self.file_label = QLineEdit()
        self.file_label.setPlaceholderText("No file selected - click Browse to choose a CSV file")
        self.file_label.setReadOnly(True)
        self.file_label.setMinimumHeight(48)
        self.file_label.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_card']};
                border: 2px dashed {COLORS['gray_300']};
                border-radius: 6px;
                padding: 12px 16px;
                color: {COLORS['text_muted']};
                font-size: 14px;
            }}
        """)
        file_row.addWidget(self.file_label, 1)
        
        self.browse_btn = QPushButton("Browse")
        if HAS_QTAWESOME:
            self.browse_btn.setIcon(qta.icon('fa5s.folder-open', color=COLORS['text_primary']))
        self.browse_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.browse_btn.clicked.connect(self.browse_file)
        self.browse_btn.setMinimumHeight(48)
        self.browse_btn.setMinimumWidth(120)
        self.browse_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: 6px;
                padding: 12px 20px;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                background: {COLORS['gray_200']};
                border-color: {COLORS['gray_300']};
            }}
        """)
        file_row.addWidget(self.browse_btn)
        
        container_layout.addLayout(file_row)
        
        # =================================================================
        # SECTION: Dataset Name (Optional)
        # =================================================================
        name_section_label = self._create_section_label("Dataset Name (Optional)")
        container_layout.addWidget(name_section_label)
        
        self.name_input = QLineEdit()
        self.name_input.setPlaceholderText("Enter a custom name for this dataset")
        self.name_input.setMinimumHeight(48)
        self.name_input.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_card']};
                border: 2px solid {COLORS['border']};
                border-radius: 6px;
                padding: 12px 16px;
                color: {COLORS['text_primary']};
                font-size: 14px;
            }}
            QLineEdit:focus {{
                border: 2px solid {COLORS['primary']};
            }}
            QLineEdit::placeholder {{
                color: {COLORS['text_muted']};
            }}
        """)
        container_layout.addWidget(self.name_input)
        
        # Hint text
        hint = QLabel("Leave blank to use the original filename")
        hint.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 13px; 
            padding-left: 4px; 
            background: transparent;
        """)
        container_layout.addWidget(hint)
        
        # =================================================================
        # INFO BOX: Expected CSV Format
        # =================================================================
        info_box = InfoBox(
            title="Expected CSV Format",
            description="Your CSV file should contain the following columns:",
            items=[
                ("Equipment Name", "Unique identifier for each equipment"),
                ("Type", "Equipment type (e.g., Pump, Compressor, Valve)"),
                ("Flowrate", "Flow rate measurement (numeric)"),
                ("Pressure", "Pressure measurement (numeric)"),
                ("Temperature", "Temperature measurement (numeric)"),
            ]
        )
        container_layout.addWidget(info_box)
        
        # =================================================================
        # PROGRESS BAR (hidden by default)
        # =================================================================
        self.progress = QProgressBar()
        self.progress.setVisible(False)
        self.progress.setMinimumHeight(8)
        self.progress.setMaximumHeight(8)
        self.progress.setTextVisible(False)
        self.progress.setStyleSheet(f"""
            QProgressBar {{
                background: {COLORS['bg_secondary']};
                border: none;
                border-radius: 4px;
            }}
            QProgressBar::chunk {{
                background: {COLORS['primary']};
                border-radius: 4px;
            }}
        """)
        container_layout.addWidget(self.progress)
        
        # =================================================================
        # STATUS MESSAGE
        # =================================================================
        self.status_msg = QLabel("")
        self.status_msg.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 13px; 
            background: transparent;
        """)
        self.status_msg.setVisible(False)
        container_layout.addWidget(self.status_msg)
        
        # =================================================================
        # UPLOAD BUTTON - matches web .upload-btn
        # =================================================================
        self.upload_btn = QPushButton("Upload & Analyze")
        self.upload_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.upload_btn.clicked.connect(self.do_upload)
        self.upload_btn.setMinimumHeight(52)
        self.upload_btn.setStyleSheet(f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: white;
                border: none;
                border-radius: 6px;
                padding: 14px 28px;
                font-size: 15px;
                font-weight: 600;
            }}
            QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                background: {COLORS['gray_400']};
            }}
        """)
        container_layout.addWidget(self.upload_btn)
        
        main_layout.addWidget(container)
        main_layout.addStretch()
    
    def _create_section_label(self, text: str) -> QLabel:
        """Create a styled section label with left border accent."""
        label = QLabel(text)
        label.setStyleSheet(f"""
            font-size: 15px;
            font-weight: 600;
            color: {COLORS['text_primary']};
            padding-left: 12px;
            border-left: 3px solid {COLORS['primary']};
            background: transparent;
        """)
        return label
    
    def browse_file(self) -> None:
        """Open file browser dialog for CSV selection."""
        file_path, _ = QFileDialog.getOpenFileName(
            self, "Select CSV File", "", "CSV Files (*.csv);;All Files (*)"
        )
        
        if file_path:
            self.file_path = file_path
            self.file_label.setText(os.path.basename(file_path))
            self.file_label.setStyleSheet(f"""
                QLineEdit {{
                    background: rgba(16, 185, 129, 0.08);
                    border: 1px solid rgba(16, 185, 129, 0.3);
                    border-radius: 6px;
                    padding: 12px 16px;
                    color: {COLORS['text_primary']};
                    font-size: 14px;
                    font-weight: 500;
                }}
            """)
            
            # Auto-fill name if empty
            if not self.name_input.text().strip():
                base_name = os.path.splitext(os.path.basename(file_path))[0]
                self.name_input.setText(base_name.replace('_', ' ').title())
            
            self._show_status("File selected - ready to upload", "success")
    
    def do_upload(self) -> None:
        """Execute the file upload to the backend."""
        if not self.file_path:
            self._show_status("❌ Please select a CSV file first", "error")
            return
        
        name = self.name_input.text().strip()
        if not name:
            name = os.path.splitext(os.path.basename(self.file_path))[0]
        
        self.upload_btn.setEnabled(False)
        self.upload_btn.setText("⏳ Uploading...")
        self.progress.setVisible(True)
        self.progress.setValue(30)
        self._show_status("Uploading file to server...", "info")
        
        try:
            result = self.api_client.upload_file(self.file_path, name)
            self.progress.setValue(100)
            
            # Check if upload was successful
            if result.get('success', True) and 'dataset' in result:
                dataset = result.get('dataset', {})
                row_count = dataset.get('row_count', 0)
                
                self._show_status(
                    f"✓ Successfully uploaded '{name}' with {row_count} records!",
                    "success"
                )
                
                # Reset form
                self._reset_form()
                
                # Emit success signal
                self.upload_success.emit(dataset)
            elif result.get('success') is False:
                error_msg = result.get('error', result.get('errors', 'Upload failed'))
                if isinstance(error_msg, dict):
                    error_msg = str(error_msg)
                self._show_status(f"❌ {error_msg}", "error")
            else:
                # Success response without explicit success field
                dataset = result.get('dataset', result)
                row_count = dataset.get('row_count', 0) if isinstance(dataset, dict) else 0
                
                self._show_status(
                    f"✓ Successfully uploaded '{name}' with {row_count} records!",
                    "success"
                )
                self._reset_form()
                self.upload_success.emit(dataset if isinstance(dataset, dict) else result)
        except Exception as e:
            self._show_status(f"❌ Upload failed: {str(e)}", "error")
        finally:
            self.upload_btn.setEnabled(True)
            self.upload_btn.setText("Upload & Analyze")
            self.progress.setVisible(False)
            self.progress.setValue(0)
    
    def _show_status(self, message: str, status_type: str = "info") -> None:
        """Display a status message with appropriate styling."""
        colors = {
            "success": COLORS['secondary'],
            "error": COLORS['danger'],
            "info": COLORS['primary'],
        }
        color = colors.get(status_type, COLORS['text_secondary'])
        font_weight = "600" if status_type != "info" else "400"
        
        self.status_msg.setText(message)
        self.status_msg.setStyleSheet(f"""
            color: {color}; 
            font-size: 13px; 
            font-weight: {font_weight};
            background: transparent;
        """)
        self.status_msg.setVisible(True)
    
    def _reset_form(self) -> None:
        """Reset the form to initial state."""
        self.file_path = None
        self.file_label.clear()
        self.file_label.setStyleSheet(f"""
            QLineEdit {{
                background: {COLORS['bg_card']};
                border: 2px dashed {COLORS['gray_300']};
                border-radius: 6px;
                padding: 12px 16px;
                color: {COLORS['text_muted']};
                font-size: 14px;
            }}
        """)
        self.name_input.clear()
    
    def clear(self) -> None:
        """Reset the form to its initial state."""
        self._reset_form()
        self.status_msg.setVisible(False)
        self.progress.setVisible(False)
