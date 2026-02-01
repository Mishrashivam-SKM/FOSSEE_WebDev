"""
Analysis Widget Module - Dataset Analysis Page.

This module provides the analysis page widget for viewing detailed
analytics of a specific dataset. Includes overview, charts, and data table.

Features:
    - Tab navigation (Overview, Charts, Data Table)
    - Summary statistics cards
    - Type distribution breakdown
    - Parameter ranges table
    - Pie and bar charts
    - Equipment data table with sorting
    - PDF download to user-chosen location

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QScrollArea, QPushButton, QFileDialog, QMessageBox,
    QGridLayout, QStackedWidget, QSizePolicy, QTableWidget,
    QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS, CHART_COLORS
from ui.components.charts import PieChartWidget, BarChartWidget
from ui.components.tables import DataTable

if TYPE_CHECKING:
    from services.api_client import APIClient


class TabButton(QPushButton):
    """Individual tab button matching web .tab styling."""
    
    def __init__(self, text: str, parent: Optional[QWidget] = None) -> None:
        super().__init__(text, parent)
        self._active = False
        self._apply_style()
        self.setCursor(QCursor(Qt.PointingHandCursor))
    
    def _apply_style(self) -> None:
        """Apply appropriate styling based on active state."""
        if self._active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['primary']};
                    color: white;
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLORS['text_secondary']};
                    border: none;
                    border-radius: 8px;
                    padding: 10px 20px;
                    font-size: 14px;
                    font-weight: 500;
                }}
                QPushButton:hover {{
                    background: {COLORS['bg_secondary']};
                    color: {COLORS['text_primary']};
                }}
            """)
    
    def set_active(self, active: bool) -> None:
        """Set the active state of the tab."""
        self._active = active
        self._apply_style()


class AnalysisWidget(QWidget):
    """
    Analysis page widget for detailed dataset analytics.
    
    Provides three tabs:
    - Overview: Summary stats, type distribution, parameter ranges
    - Charts: Pie chart and bar chart visualizations
    - Data Table: Sortable equipment data table
    
    Matches web Analysis page styling exactly.
    
    Signals:
        navigate_to: Emitted for navigation (str: page name).
    
    Args:
        api_client: APIClient instance for backend communication.
        parent: Optional parent widget.
    """
    
    navigate_to = pyqtSignal(str)
    
    def __init__(self, api_client: "APIClient", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.current_dataset: Optional[Dict[str, Any]] = None
        self.analytics: Optional[Dict[str, Any]] = None
        self.equipment: List[Dict[str, Any]] = []
        self.dataset_id: Optional[int] = None
        self._setup_ui()
    
    def _show_styled_message(self, title: str, message: str, icon_type: str = "info") -> None:
        """Show a styled message box with proper color contrast."""
        msg_box = QMessageBox(self)
        msg_box.setWindowTitle(title)
        msg_box.setText(message)
        
        if icon_type == "warning":
            msg_box.setIcon(QMessageBox.Warning)
        elif icon_type == "error":
            msg_box.setIcon(QMessageBox.Critical)
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

    def _setup_ui(self) -> None:
        """Setup the analysis page UI layout matching web exactly."""
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")
        
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)
        
        # =================================================================
        # HEADER - matches web .analysis-header
        # =================================================================
        header = QWidget()
        header.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header)
        header_layout.setContentsMargins(0, 0, 0, 24)
        header_layout.setSpacing(8)
        
        # Back link row
        back_row = QHBoxLayout()
        
        self.back_btn = QPushButton("Back to History")
        self.back_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.back_btn.clicked.connect(lambda: self.navigate_to.emit("history"))
        self.back_btn.setStyleSheet(f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['primary']};
                border: none;
                padding: 4px 0;
                font-size: 14px;
                font-weight: 500;
            }}
            QPushButton:hover {{
                text-decoration: underline;
            }}
        """)
        
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.arrow-left', color=COLORS['primary'])
            self.back_btn.setIcon(icon)
        
        back_row.addWidget(self.back_btn)
        back_row.addStretch()
        
        # Download PDF button
        self.download_btn = QPushButton("Download PDF Report")
        self.download_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.download_btn.clicked.connect(self._download_pdf)
        self.download_btn.setStyleSheet(f"""
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
            QPushButton:disabled {{
                background: {COLORS['gray_400']};
            }}
        """)
        
        if HAS_QTAWESOME:
            icon = qta.icon('fa5s.download', color='white')
            self.download_btn.setIcon(icon)
        
        back_row.addWidget(self.download_btn)
        header_layout.addLayout(back_row)
        
        # Title
        self.title_label = QLabel("Dataset Analysis")
        self.title_label.setFont(QFont("", 22, QFont.Bold))
        self.title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            background: transparent;
            letter-spacing: -0.01em;
        """)
        header_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Loading...")
        self.subtitle_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
            background: transparent;
        """)
        header_layout.addWidget(self.subtitle_label)
        
        main_layout.addWidget(header)
        
        # =================================================================
        # TABS - matches web .tabs
        # =================================================================
        tabs_container = QFrame()
        tabs_container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        tabs_layout = QHBoxLayout(tabs_container)
        tabs_layout.setContentsMargins(4, 4, 4, 4)
        tabs_layout.setSpacing(4)
        
        self.tab_overview = TabButton("Overview")
        self.tab_overview.set_active(True)
        self.tab_overview.clicked.connect(lambda: self._switch_tab(0))
        tabs_layout.addWidget(self.tab_overview)
        
        self.tab_charts = TabButton("Charts")
        self.tab_charts.clicked.connect(lambda: self._switch_tab(1))
        tabs_layout.addWidget(self.tab_charts)
        
        self.tab_data = TabButton("Data Table")
        self.tab_data.clicked.connect(lambda: self._switch_tab(2))
        tabs_layout.addWidget(self.tab_data)
        
        tabs_layout.addStretch()
        
        main_layout.addWidget(tabs_container)
        main_layout.addSpacing(24)
        
        # =================================================================
        # TAB CONTENT - stacked widget
        # =================================================================
        self.content_stack = QStackedWidget()
        self.content_stack.setStyleSheet("background: transparent;")
        
        # Overview tab
        self.overview_widget = self._create_overview_tab()
        self.content_stack.addWidget(self.overview_widget)
        
        # Charts tab
        self.charts_widget = self._create_charts_tab()
        self.content_stack.addWidget(self.charts_widget)
        
        # Data tab
        self.data_widget = self._create_data_tab()
        self.content_stack.addWidget(self.data_widget)
        
        main_layout.addWidget(self.content_stack, 1)
    
    def _create_overview_tab(self) -> QWidget:
        """Create the Overview tab content."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QVBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Stats row - 4 cards matching web .stats-row
        stats_grid = QGridLayout()
        stats_grid.setSpacing(20)
        
        # Create stat cards
        self.stat_total = self._create_stat_card_simple(
            "Total Equipment", "0", "fa5s.chart-bar",
            COLORS['primary'], "rgba(59, 130, 246, 0.1)"
        )
        self.stat_flowrate = self._create_stat_card_simple(
            "Avg Flowrate", "-", "fa5s.tint",
            COLORS['primary'], "rgba(59, 130, 246, 0.1)"
        )
        self.stat_pressure = self._create_stat_card_simple(
            "Avg Pressure", "-", "fa5s.chart-line",
            COLORS['secondary'], "rgba(16, 185, 129, 0.1)"
        )
        self.stat_temperature = self._create_stat_card_simple(
            "Avg Temperature", "-", "fa5s.thermometer-half",
            COLORS['warning'], "rgba(245, 158, 11, 0.1)"
        )
        
        stats_grid.addWidget(self.stat_total, 0, 0)
        stats_grid.addWidget(self.stat_flowrate, 0, 1)
        stats_grid.addWidget(self.stat_pressure, 0, 2)
        stats_grid.addWidget(self.stat_temperature, 0, 3)
        
        layout.addLayout(stats_grid)
        
        # Type Distribution section - matching web .distribution-section
        dist_section = QFrame()
        dist_section.setObjectName("DistSection")
        dist_section.setStyleSheet(f"""
            QFrame#DistSection {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 16px;
                padding: 0px;
            }}
        """)
        dist_layout = QVBoxLayout(dist_section)
        dist_layout.setContentsMargins(24, 24, 24, 24)
        dist_layout.setSpacing(20)
        
        # Title with left accent bar
        dist_title_row = QHBoxLayout()
        dist_accent = QFrame()
        dist_accent.setFixedSize(3, 16)
        dist_accent.setStyleSheet(f"background: {COLORS['primary']}; border-radius: 2px;")
        dist_title_row.addWidget(dist_accent)
        dist_title_row.addSpacing(8)
        
        dist_title = QLabel("Equipment Type Distribution")
        dist_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
        """)
        dist_title_row.addWidget(dist_title)
        dist_title_row.addStretch()
        dist_layout.addLayout(dist_title_row)
        
        # Distribution grid
        self.dist_grid = QGridLayout()
        self.dist_grid.setSpacing(12)
        dist_layout.addLayout(self.dist_grid)
        
        layout.addWidget(dist_section)
        
        # Parameter Ranges section - matching web .ranges-section
        ranges_section = QFrame()
        ranges_section.setObjectName("RangesSection")
        ranges_section.setStyleSheet(f"""
            QFrame#RangesSection {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 16px;
            }}
        """)
        ranges_layout = QVBoxLayout(ranges_section)
        ranges_layout.setContentsMargins(24, 24, 24, 24)
        ranges_layout.setSpacing(20)
        
        # Title with left accent bar
        ranges_title_row = QHBoxLayout()
        ranges_accent = QFrame()
        ranges_accent.setFixedSize(3, 16)
        ranges_accent.setStyleSheet(f"background: {COLORS['secondary']}; border-radius: 2px;")
        ranges_title_row.addWidget(ranges_accent)
        ranges_title_row.addSpacing(8)
        
        ranges_title = QLabel("Parameter Ranges")
        ranges_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
        """)
        ranges_title_row.addWidget(ranges_title)
        ranges_title_row.addStretch()
        ranges_layout.addLayout(ranges_title_row)
        
        # Ranges table - styled without inner borders (rows added dynamically)
        self.ranges_table = QTableWidget(0, 4)  # Start with 0 rows, add dynamically
        self.ranges_table.setHorizontalHeaderLabels(["Parameter", "Min", "Max", "Average"])
        self.ranges_table.verticalHeader().setVisible(False)
        self.ranges_table.setEditTriggers(QTableWidget.NoEditTriggers)
        self.ranges_table.setSelectionMode(QTableWidget.NoSelection)
        self.ranges_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.ranges_table.setMinimumHeight(180)
        self.ranges_table.setMaximumHeight(300)
        self.ranges_table.setShowGrid(True)
        self.ranges_table.setStyleSheet(f"""
            QTableWidget {{
                background: transparent;
                border: 1px solid {COLORS['gray_100']};
                border-radius: 8px;
                gridline-color: {COLORS['gray_100']};
            }}
            QTableWidget::item {{
                padding: 12px 16px;
                color: {COLORS['text_primary']};
                border-bottom: 1px solid {COLORS['gray_100']};
            }}
            QTableWidget::item:hover {{
                background: {COLORS['bg_secondary']};
            }}
            QHeaderView::section {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_secondary']};
                padding: 12px 16px;
                border: none;
                border-bottom: 1px solid {COLORS['gray_100']};
                font-weight: 500;
                font-size: 12px;
                text-transform: uppercase;
                letter-spacing: 0.5px;
            }}
        """)
        
        ranges_layout.addWidget(self.ranges_table)
        layout.addWidget(ranges_section)
        
        layout.addStretch()
        scroll.setWidget(content)
        return scroll
    
    def _create_stat_card_simple(
        self,
        label: str,
        value: str,
        icon_name: str,
        color: str,
        bg_color: str
    ) -> QFrame:
        """Create a stat card for overview tab matching web .stat-card."""
        card = QFrame()
        card.setObjectName("StatCardSimple")
        card.setStyleSheet(f"""
            QFrame#StatCardSimple {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 12px;
            }}
        """)
        card.setMinimumHeight(100)
        
        layout = QHBoxLayout(card)
        layout.setContentsMargins(16, 16, 16, 16)
        layout.setSpacing(16)
        
        # Icon container
        icon_frame = QFrame()
        icon_frame.setFixedSize(52, 52)
        icon_frame.setStyleSheet(f"""
            QFrame {{
                background: {bg_color};
                border-radius: 10px;
                border: none;
            }}
        """)
        icon_layout = QVBoxLayout(icon_frame)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        if HAS_QTAWESOME:
            icon_label = QLabel()
            icon = qta.icon(icon_name, color=color)
            icon_label.setPixmap(icon.pixmap(24, 24))
            icon_label.setAlignment(Qt.AlignCenter)
            icon_label.setStyleSheet("background: transparent; border: none;")
        else:
            icon_label = QLabel("📊")
            icon_label.setStyleSheet(f"font-size: 24px; background: transparent; border: none;")
            icon_label.setAlignment(Qt.AlignCenter)
        
        icon_layout.addWidget(icon_label)
        layout.addWidget(icon_frame)
        
        # Value and label - reversed order (value on top)
        text_layout = QVBoxLayout()
        text_layout.setSpacing(4)
        
        value_label = QLabel(value)
        value_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 24px;
            font-weight: 700;
            background: transparent;
            border: none;
        """)
        text_layout.addWidget(value_label)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
            font-weight: 500;
            background: transparent;
            border: none;
        """)
        text_layout.addWidget(label_widget)
        
        layout.addLayout(text_layout)
        layout.addStretch()
        
        # Store reference for updates
        card.value_label = value_label
        
        return card
    
    def _create_charts_tab(self) -> QWidget:
        """Create the Charts tab content."""
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        layout = QHBoxLayout(content)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(24)
        
        # Pie chart card - matching web .chart-card
        pie_card = QFrame()
        pie_card.setObjectName("ChartCard")
        pie_card.setStyleSheet(f"""
            QFrame#ChartCard {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 16px;
            }}
        """)
        pie_layout = QVBoxLayout(pie_card)
        pie_layout.setContentsMargins(24, 24, 24, 24)
        pie_layout.setSpacing(20)
        
        pie_title = QLabel("Equipment Type Distribution")
        pie_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        pie_layout.addWidget(pie_title)
        
        self.pie_chart = PieChartWidget()
        self.pie_chart.setStyleSheet("background: transparent; border: none;")
        pie_layout.addWidget(self.pie_chart)
        
        layout.addWidget(pie_card, 1)
        
        # Bar chart card
        bar_card = QFrame()
        bar_card.setObjectName("ChartCard2")
        bar_card.setStyleSheet(f"""
            QFrame#ChartCard2 {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: 16px;
            }}
        """)
        bar_layout = QVBoxLayout(bar_card)
        bar_layout.setContentsMargins(24, 24, 24, 24)
        bar_layout.setSpacing(20)
        
        bar_title = QLabel("Average Parameters by Type")
        bar_title.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 18px;
            font-weight: 600;
            background: transparent;
            border: none;
        """)
        bar_layout.addWidget(bar_title)
        
        self.bar_chart = BarChartWidget()
        self.bar_chart.setStyleSheet("background: transparent; border: none;")
        bar_layout.addWidget(self.bar_chart)
        
        layout.addWidget(bar_card, 1)
        
        scroll.setWidget(content)
        return scroll
    
    def _create_data_tab(self) -> QWidget:
        """Create the Data Table tab content."""
        container = QWidget()
        container.setStyleSheet("background: transparent;")
        container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(container)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Create data table - remove fixed widths to let columns stretch
        columns = [
            {"key": "name", "label": "Equipment Name"},
            {"key": "type", "label": "Type"},
            {"key": "flowrate", "label": "Flowrate"},
            {"key": "pressure", "label": "Pressure"},
            {"key": "temperature", "label": "Temperature"}
        ]
        
        self.data_table = DataTable(columns)
        self.data_table.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        layout.addWidget(self.data_table, 1)  # stretch factor 1
        
        return container
    
    def _switch_tab(self, index: int) -> None:
        """Switch to the specified tab."""
        self.tab_overview.set_active(index == 0)
        self.tab_charts.set_active(index == 1)
        self.tab_data.set_active(index == 2)
        self.content_stack.setCurrentIndex(index)
    
    def load_dataset(self, dataset_id: int) -> None:
        """
        Load a dataset and its analytics.
        
        Args:
            dataset_id: The ID of the dataset to load.
        """
        self.dataset_id = dataset_id
        self._switch_tab(0)  # Start on overview
        
        # Load dataset info
        try:
            data = self.api_client.get_dataset(dataset_id)
            if data.get('success', True):  # Default to True for successful responses
                self.current_dataset = data.get('dataset', data)
                self._update_header()
        except Exception as e:
            print(f"Error loading dataset: {e}")
        
        # Load analytics
        try:
            data = self.api_client.get_dataset_analytics(dataset_id)
            if data.get('success', True):
                self.analytics = data
                self._update_overview()
                self._update_charts()
        except Exception as e:
            print(f"Error loading analytics: {e}")
        
        # Load equipment data
        try:
            data = self.api_client.get_dataset_equipment(dataset_id)
            # API returns list or dict with equipment
            if isinstance(data, list):
                self.equipment = data
            else:
                self.equipment = data.get('equipment', data.get('results', []))
            self._update_data_table()
        except Exception as e:
            print(f"Error loading equipment: {e}")
    
    def _update_header(self) -> None:
        """Update header with dataset info."""
        if not self.current_dataset:
            return
        
        name = self.current_dataset.get('name', 'Unknown')
        row_count = self.current_dataset.get('row_count', 0)
        uploaded_at = self.current_dataset.get('uploaded_at', '')
        
        self.title_label.setText(name)
        
        # Format date
        if uploaded_at:
            from datetime import datetime
            try:
                dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                date_str = dt.strftime("%b %d, %Y")
            except:
                date_str = uploaded_at[:10] if len(uploaded_at) >= 10 else uploaded_at
        else:
            date_str = "Unknown"
        
        self.subtitle_label.setText(f"{row_count} equipment records • Uploaded {date_str}")
    
    def _update_overview(self) -> None:
        """Update overview tab with analytics data."""
        if not self.analytics:
            return
        
        summary = self.analytics.get('summary', {})
        averages = summary.get('averages', {})
        ranges = summary.get('ranges', {})
        type_dist = summary.get('type_distribution', {})
        
        # Update stat cards - use dynamic parameter names
        total = summary.get('total_count', 0)
        self.stat_total.value_label.setText(str(total))
        
        # Update first 3 parameter stat cards dynamically
        param_cards = [self.stat_flowrate, self.stat_pressure, self.stat_temperature]
        param_keys = list(averages.keys())[:3]  # Get first 3 parameters from data
        
        for i, card in enumerate(param_cards):
            if i < len(param_keys):
                param = param_keys[i]
                value = averages.get(param, 0)
                card.value_label.setText(f"{value:.1f}" if value else "-")
            else:
                card.value_label.setText("-")
        
        # Update distribution grid
        # Clear existing items
        while self.dist_grid.count():
            item = self.dist_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Add distribution items
        total_count = sum(type_dist.values()) if type_dist else 1
        col = 0
        for i, (type_name, count) in enumerate(type_dist.items()):
            item = self._create_dist_item(type_name, count, total_count)
            self.dist_grid.addWidget(item, i // 4, i % 4)
            col += 1
        
        # Update ranges table dynamically based on parameter names from data
        self.ranges_table.setRowCount(len(averages))
        for i, param in enumerate(averages.keys()):
            avg = averages.get(param, 0)
            param_range = ranges.get(param, {})
            min_val = param_range.get('min', 0)
            max_val = param_range.get('max', 0)
            
            # Parameter name (capitalized)
            name_item = QTableWidgetItem(param.capitalize())
            name_item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
            self.ranges_table.setItem(i, 0, name_item)
            
            # Min value
            min_item = QTableWidgetItem(f"{min_val:.1f}" if min_val else "-")
            min_item.setTextAlignment(Qt.AlignCenter)
            self.ranges_table.setItem(i, 1, min_item)
            
            # Max value
            max_item = QTableWidgetItem(f"{max_val:.1f}" if max_val else "-")
            max_item.setTextAlignment(Qt.AlignCenter)
            self.ranges_table.setItem(i, 2, max_item)
            
            # Average value
            avg_item = QTableWidgetItem(f"{avg:.1f}" if avg else "-")
            avg_item.setTextAlignment(Qt.AlignCenter)
            self.ranges_table.setItem(i, 3, avg_item)
    
    def _create_dist_item(self, type_name: str, count: int, total: int) -> QFrame:
        """Create a distribution item widget."""
        frame = QFrame()
        frame.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_secondary']};
                border-radius: 8px;
                padding: 12px;
            }}
        """)
        
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(12, 12, 12, 12)
        layout.setSpacing(4)
        
        # Type name
        name_label = QLabel(type_name)
        name_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: 500;
            background: transparent;
        """)
        layout.addWidget(name_label)
        
        # Count and percentage
        pct = (count / total * 100) if total > 0 else 0
        count_label = QLabel(f"{count} ({pct:.1f}%)")
        count_label.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: 13px;
            background: transparent;
        """)
        layout.addWidget(count_label)
        
        return frame
    
    def _update_charts(self) -> None:
        """Update charts with analytics data."""
        if not self.analytics:
            return
        
        summary = self.analytics.get('summary', {})
        chart_data = self.analytics.get('chart_data', {})
        type_dist = summary.get('type_distribution', {})
        
        # Update pie chart
        if type_dist:
            labels = list(type_dist.keys())
            values = list(type_dist.values())
            self.pie_chart.update_data(labels, values)
        else:
            self.pie_chart.clear()
        
        # Bar chart - use chart_data if available (grouped by equipment type)
        bar_chart_data = chart_data.get('bar_chart', {}) if chart_data else {}
        if bar_chart_data and bar_chart_data.get('labels') and bar_chart_data.get('datasets'):
            # Use the proper grouped bar chart format from API
            self.bar_chart.update_chart(bar_chart_data)
        else:
            # Fallback to simple bar chart with overall averages
            averages = summary.get('averages', {})
            if averages:
                params = [key.capitalize() for key in averages.keys()]
                vals = [averages.get(key, 0) or 0 for key in averages.keys()]
                self.bar_chart.update_simple(params, vals)
            else:
                self.bar_chart.clear()
    
    def _update_data_table(self) -> None:
        """Update data table with equipment data."""
        self.data_table.set_data(self.equipment)
    
    def _download_pdf(self) -> None:
        """Download PDF report to user-chosen location."""
        if not self.dataset_id:
            return
        
        # Default filename
        name = self.current_dataset.get('name', 'report') if self.current_dataset else 'report'
        default_name = f"{name}_report.pdf"
        
        # Ask user where to save
        file_path, _ = QFileDialog.getSaveFileName(
            self,
            "Save PDF Report",
            default_name,
            "PDF Files (*.pdf)"
        )
        
        if not file_path:
            return
        
        self.download_btn.setEnabled(False)
        self.download_btn.setText("Downloading...")
        
        try:
            success = self.api_client.download_pdf(self.dataset_id, file_path)
            
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
            self.download_btn.setEnabled(True)
            self.download_btn.setText("Download PDF Report")
            if HAS_QTAWESOME:
                self.download_btn.setIcon(qta.icon('fa5s.download', color='white'))
