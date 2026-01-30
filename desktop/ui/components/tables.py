"""
Tables Component Module - Data table widgets matching React web UI.

This module provides data table components that match the web application's
table styling exactly.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import List, Dict, Any, Optional, Callable

from PyQt5.QtWidgets import (
    QWidget, QTableWidget, QTableWidgetItem, QVBoxLayout,
    QHBoxLayout, QLabel, QHeaderView, QFrame, QAbstractItemView,
    QSizePolicy
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor

from ui.theme import COLORS, FONT_SIZES, FONT_WEIGHTS, BORDER_RADIUS, SPACING
from ui.components.constants import LAYOUT


class DataTable(QWidget):
    """
    Data table widget matching web UI DataTable component.
    
    Displays tabular data with styled headers and hover effects.
    
    Args:
        columns: List of column definitions with 'key', 'label', 'width', 'format'.
        data: List of dictionaries containing row data.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        columns: Optional[List[Dict[str, Any]]] = None,
        data: Optional[List[Dict[str, Any]]] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.columns = columns or []
        self.table_data = data or []
        
        self._setup_ui()
        
        if data:
            self.set_data(data)
    
    def _setup_ui(self) -> None:
        """Setup the table UI."""
        self.setStyleSheet("background: transparent;")
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Table container with border
        container = QFrame()
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: {BORDER_RADIUS['xl']}px;
            }}
        """)
        
        container_layout = QVBoxLayout(container)
        container_layout.setContentsMargins(0, 0, 0, 0)
        container_layout.setSpacing(0)
        
        # Table widget
        self.table = QTableWidget()
        self.table.setColumnCount(len(self.columns))
        self.table.setHorizontalHeaderLabels([col.get('label', '') for col in self.columns])
        
        # Hide vertical header
        self.table.verticalHeader().setVisible(False)
        
        # Selection behavior
        self.table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        
        # Alternating row colors disabled (web doesn't have it)
        self.table.setAlternatingRowColors(False)
        
        # Style the table
        self.table.setStyleSheet(f"""
            QTableWidget {{
                background: {COLORS['bg_card']};
                border: none;
                gridline-color: {COLORS['border_light']};
                font-size: {FONT_SIZES['md']}px;
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item {{
                padding: {LAYOUT['table_cell_padding']}px {LAYOUT['table_cell_padding_h']}px;
                border-bottom: 1px solid {COLORS['border_light']};
            }}
            QTableWidget::item:selected {{
                background: {COLORS['primary_bg']};
                color: {COLORS['text_primary']};
            }}
            QTableWidget::item:hover {{
                background: {COLORS['bg_secondary']};
            }}
            QHeaderView::section {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                font-weight: {FONT_WEIGHTS['semibold']};
                font-size: {FONT_SIZES['sm']}px;
                text-transform: uppercase;
                letter-spacing: 0.05em;
                padding: {LAYOUT['table_cell_padding']}px {LAYOUT['table_cell_padding_h']}px;
                border: none;
                border-bottom: 2px solid {COLORS['border']};
            }}
            QScrollBar:vertical {{
                background: {COLORS['bg_secondary']};
                width: 8px;
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical {{
                background: {COLORS['gray_300']};
                border-radius: 4px;
            }}
            QScrollBar::handle:vertical:hover {{
                background: {COLORS['gray_400']};
            }}
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{
                height: 0px;
            }}
        """)
        
        # Set column widths based on definitions
        header = self.table.horizontalHeader()
        header.setStretchLastSection(True)
        
        for i, col in enumerate(self.columns):
            width = col.get('width', 0)
            if isinstance(width, float) and width <= 1:
                # Percentage width - use stretch
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            elif isinstance(width, int) and width > 0:
                header.setSectionResizeMode(i, QHeaderView.Interactive)
                self.table.setColumnWidth(i, width)
            else:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
        
        # Default to stretch all if no widths specified
        if not any(col.get('width') for col in self.columns):
            header.setSectionResizeMode(QHeaderView.Stretch)
        
        container_layout.addWidget(self.table)
        layout.addWidget(container)
        
        # Empty state
        self.empty_label = QLabel("No data available")
        self.empty_label.setAlignment(Qt.AlignCenter)
        self.empty_label.setStyleSheet(f"""
            color: {COLORS['text_muted']};
            font-size: {FONT_SIZES['md']}px;
            padding: 48px;
            background: transparent;
        """)
        self.empty_label.setVisible(False)
        layout.addWidget(self.empty_label)
    
    def set_data(self, data: List[Dict[str, Any]]) -> None:
        """Set the table data."""
        self.table_data = data
        self.table.setRowCount(len(data))
        
        if not data:
            self.table.setVisible(False)
            self.empty_label.setVisible(True)
            return
        
        self.table.setVisible(True)
        self.empty_label.setVisible(False)
        
        for row_idx, row_data in enumerate(data):
            for col_idx, col in enumerate(self.columns):
                key = col.get('key', '')
                value = row_data.get(key, '')
                
                # Format value if formatter specified
                formatter = col.get('format')
                if formatter == 'number' and value is not None:
                    try:
                        value = f"{float(value):.2f}"
                    except (ValueError, TypeError):
                        pass
                elif callable(col.get('render')):
                    value = col['render'](value)
                
                item = QTableWidgetItem(str(value) if value is not None else '-')
                item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
                
                self.table.setItem(row_idx, col_idx, item)
        
        # Adjust row heights
        self.table.resizeRowsToContents()
    
    def set_columns(self, columns: List[Dict[str, Any]]) -> None:
        """Set the table columns."""
        self.columns = columns
        self.table.setColumnCount(len(columns))
        self.table.setHorizontalHeaderLabels([col.get('label', '') for col in columns])
        
        # Update column widths
        header = self.table.horizontalHeader()
        for i, col in enumerate(columns):
            width = col.get('width', 0)
            if isinstance(width, float) and width <= 1:
                header.setSectionResizeMode(i, QHeaderView.Stretch)
            elif isinstance(width, int) and width > 0:
                self.table.setColumnWidth(i, width)
    
    def clear(self) -> None:
        """Clear all table data."""
        self.table.setRowCount(0)
        self.table_data = []
        self.table.setVisible(False)
        self.empty_label.setVisible(True)
    
    def set_empty_message(self, message: str) -> None:
        """Set the empty state message."""
        self.empty_label.setText(message)
    
    def get_selected_row(self) -> Optional[Dict[str, Any]]:
        """Get the currently selected row data."""
        selected = self.table.selectedItems()
        if selected:
            row_idx = selected[0].row()
            if 0 <= row_idx < len(self.table_data):
                return self.table_data[row_idx]
        return None


class RangesTable(QWidget):
    """
    Ranges table matching Analysis page parameter ranges display.
    
    Displays parameter ranges in a grid format.
    
    Args:
        data: Dictionary with parameter ranges.
        averages: Dictionary with parameter averages.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        averages: Optional[Dict[str, Any]] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.ranges_data = data or {}
        self.averages_data = averages or {}
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the ranges table UI."""
        self.setStyleSheet("background: transparent;")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Container
        container = QFrame()
        container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
        """)
        
        self.container_layout = QVBoxLayout(container)
        self.container_layout.setContentsMargins(0, 0, 0, 0)
        self.container_layout.setSpacing(0)
        
        layout.addWidget(container)
    
    def set_data(
        self,
        ranges: Dict[str, Dict[str, float]],
        averages: Dict[str, float]
    ) -> None:
        """Set the ranges data."""
        self.ranges_data = ranges
        self.averages_data = averages
        
        # Clear existing rows
        while self.container_layout.count():
            item = self.container_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Header row
        header = self._create_row(
            ["Parameter", "Min", "Max", "Average"],
            is_header=True
        )
        self.container_layout.addWidget(header)
        
        # Data rows
        parameters = ['flowrate', 'pressure', 'temperature']
        for param in parameters:
            param_range = ranges.get(param, {})
            avg = averages.get(param, 0)
            
            row = self._create_row([
                param.capitalize(),
                f"{param_range.get('min', 0):.2f}",
                f"{param_range.get('max', 0):.2f}",
                f"{avg:.2f}",
            ])
            self.container_layout.addWidget(row)
    
    def _create_row(self, values: List[str], is_header: bool = False) -> QWidget:
        """Create a table row."""
        row = QWidget()
        row.setStyleSheet(f"""
            QWidget {{
                background: {'#f8fafc' if is_header else 'transparent'};
                border-bottom: 1px solid {COLORS['gray_100']};
            }}
            QWidget:hover {{
                background: {COLORS['gray_50'] if not is_header else '#f8fafc'};
            }}
        """)
        
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(SPACING['md'], SPACING['sm'], SPACING['md'], SPACING['sm'])
        row_layout.setSpacing(0)
        
        for i, value in enumerate(values):
            label = QLabel(value)
            label.setStyleSheet(f"""
                color: {COLORS['gray_600'] if is_header else COLORS['text_primary']};
                font-size: {FONT_SIZES['xs'] if is_header else FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium'] if is_header else FONT_WEIGHTS['normal']};
                {'text-transform: uppercase; letter-spacing: 0.5px;' if is_header else ''}
                background: transparent;
            """)
            row_layout.addWidget(label, 1)
        
        return row
