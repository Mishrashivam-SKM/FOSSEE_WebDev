"""
Dashboard Widget Module - Main Analytics Dashboard.

This module provides the dashboard view that displays chemical equipment
analytics with statistics cards, charts, and data summaries. Uses the
new modular component system for pixel-perfect web UI matching.

Features:
    - Combined analytics view for all datasets
    - Individual dataset selection and analysis
    - Type distribution pie chart (400px height)
    - Parameter averages bar chart (400px height)
    - Real-time data refresh

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Any, Dict, List, Optional, TYPE_CHECKING

from PyQt5.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame,
    QComboBox, QScrollArea, QGridLayout, QSizePolicy
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

from ui.theme import COLORS, get_metrics
from ui.components.cards import StatCard, ChartCard, SummaryCard
from ui.components.buttons import ActionButton, ToggleButtonGroup
from ui.components.charts import PieChartWidget, BarChartWidget
from ui.components.constants import LAYOUT, GRID_GAPS

if TYPE_CHECKING:
    from services import APIClient


class DashboardWidget(QWidget):
    """
    Main dashboard page widget displaying analytics overview.
    
    Provides a comprehensive view of chemical equipment data with:
    - Toggle buttons for combined or individual analysis
    - Statistics cards showing key metrics (86px height, 4 columns)
    - Summary cards for Flowrate/Pressure/Temperature (3 columns)
    - Type distribution pie chart (400px height)
    - Parameter averages bar chart (400px height)
    - Quick action cards for navigation
    
    Matches web Dashboard page layout and styling exactly.
    
    Signals:
        navigate_to: Emitted when user clicks action cards (str: page name).
    
    Args:
        api_client: APIClient instance for backend communication.
        parent: Optional parent widget.
    """
    
    navigate_to = pyqtSignal(str)
    
    def __init__(self, api_client: "APIClient", parent: Optional[QWidget] = None) -> None:
        super().__init__(parent)
        self.api_client = api_client
        self.m = get_metrics()
        self.datasets: List[Dict[str, Any]] = []
        self.view_mode = 'combined'
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the dashboard UI layout matching web exactly."""
        self.setStyleSheet(f"background: {COLORS['bg_primary']};")
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # =================================================================
        # PAGE HEADER - matches web .page-header
        # =================================================================
        header_widget = QWidget()
        header_widget.setStyleSheet("background: transparent;")
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(0, 0, 0, 28)  # margin-bottom: 28px
        header_layout.setSpacing(4)
        
        # Title - 22px, bold
        title = QLabel("Dashboard")
        title.setFont(QFont("", 22, QFont.Bold))
        title.setStyleSheet(f"""
            color: {COLORS['text_primary']}; 
            background: transparent; 
            letter-spacing: -0.01em;
        """)
        header_layout.addWidget(title)
        
        # Subtitle - 13px
        subtitle = QLabel("Overview of your chemical equipment data")
        subtitle.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 13px; 
            background: transparent;
        """)
        header_layout.addWidget(subtitle)
        
        layout.addWidget(header_widget)
        
        # =================================================================
        # VIEW TOGGLE ROW - matches web .view-toggle-container
        # =================================================================
        toggle_row = QHBoxLayout()
        toggle_row.setSpacing(16)
        
        # Toggle button group
        self.toggle_group = ToggleButtonGroup([
            ("All Datasets Combined", "⊞"),
            ("Specific Dataset", "▦")
        ])
        self.toggle_group.selection_changed.connect(self._on_toggle_changed)
        toggle_row.addWidget(self.toggle_group)
        
        # Dataset selector (hidden by default)
        self.view_combo = QComboBox()
        self.view_combo.setMinimumWidth(220)
        self.view_combo.setVisible(False)
        self.view_combo.currentIndexChanged.connect(self._load_dashboard)
        self.view_combo.setStyleSheet(f"""
            QComboBox {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 8px;
                padding: 10px 16px;
                color: {COLORS['text_primary']};
                font-size: 14px;
                min-width: 220px;
            }}
            QComboBox:focus {{
                border: 1px solid {COLORS['primary']};
            }}
            QComboBox::drop-down {{
                border: none;
                width: 24px;
            }}
            QComboBox::down-arrow {{
                image: none;
                border-left: 4px solid transparent;
                border-right: 4px solid transparent;
                border-top: 5px solid {COLORS['text_muted']};
            }}
            QComboBox QAbstractItemView {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                selection-background-color: {COLORS['primary_bg']};
                selection-color: {COLORS['text_primary']};
                padding: 4px;
            }}
        """)
        toggle_row.addWidget(self.view_combo)
        toggle_row.addStretch()
        
        layout.addLayout(toggle_row)
        layout.addSpacing(24)  # margin-bottom: 24px after toggle
        
        # =================================================================
        # SCROLLABLE CONTENT
        # =================================================================
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setFrameShape(QFrame.NoFrame)
        scroll.setStyleSheet("background: transparent; border: none;")
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        
        content = QWidget()
        content.setStyleSheet("background: transparent;")
        self.content_layout = QVBoxLayout(content)
        self.content_layout.setContentsMargins(0, 0, 0, 0)
        self.content_layout.setSpacing(24)
        
        # =================================================================
        # STATS GRID - 4 columns, 20px gap, 86px card height
        # =================================================================
        stats_grid = QGridLayout()
        stats_grid.setSpacing(GRID_GAPS['stats'])  # 20px
        
        # Create stat cards using new component
        self.total_card = StatCard("Total Datasets", "0", icon="database")
        self.equip_card = StatCard("Total Equipment", "0", icon="activity")
        self.flowrate_card = StatCard("Avg Flowrate", "-", icon="trending")
        self.upload_card = StatCard("Latest Upload", "-", icon="upload")
        
        stats_grid.addWidget(self.total_card, 0, 0)
        stats_grid.addWidget(self.equip_card, 0, 1)
        stats_grid.addWidget(self.flowrate_card, 0, 2)
        stats_grid.addWidget(self.upload_card, 0, 3)
        
        self.content_layout.addLayout(stats_grid)
        
        # =================================================================
        # ANALYTICS SECTION - matches web .analytics-section
        # =================================================================
        analytics_section = QWidget()
        analytics_section.setStyleSheet("background: transparent;")
        analytics_layout = QVBoxLayout(analytics_section)
        analytics_layout.setContentsMargins(0, 8, 0, 0)
        analytics_layout.setSpacing(4)
        
        # Section title - 20px, bold
        self.analytics_title = QLabel("Combined Analytics (All Datasets)")
        self.analytics_title.setFont(QFont("", 20, QFont.Bold))
        self.analytics_title.setStyleSheet(f"""
            color: {COLORS['text_primary']}; 
            background: transparent;
        """)
        analytics_layout.addWidget(self.analytics_title)
        
        # Section subtitle - 14px
        self.analytics_subtitle = QLabel("Aggregated data from all datasets")
        self.analytics_subtitle.setStyleSheet(f"""
            color: {COLORS['text_secondary']}; 
            font-size: 14px; 
            background: transparent;
            margin-bottom: 16px;
        """)
        analytics_layout.addWidget(self.analytics_subtitle)
        analytics_layout.addSpacing(16)
        
        # Summary grid - 3 columns, 20px gap (created dynamically)
        self.summary_grid = QHBoxLayout()
        self.summary_grid.setSpacing(GRID_GAPS['summary'])  # 20px
        
        # Store summary cards by parameter name (dynamically created)
        self.summary_cards = {}
        # Default parameters - will be updated dynamically when data arrives
        for param in ['flowrate', 'pressure', 'temperature']:
            card = SummaryCard(param.capitalize())
            self.summary_cards[param] = card
            self.summary_grid.addWidget(card)
        
        analytics_layout.addLayout(self.summary_grid)
        self.content_layout.addWidget(analytics_section)
        
        # =================================================================
        # CHARTS ROW - 2 columns, 24px gap, 400px chart height
        # =================================================================
        charts_row = QHBoxLayout()
        charts_row.setSpacing(GRID_GAPS['charts'])  # 24px
        
        # Pie chart card
        self.type_chart_card = ChartCard("Equipment Type Distribution")
        self.pie_chart = PieChartWidget()
        self.type_chart_card.set_chart(self.pie_chart)
        charts_row.addWidget(self.type_chart_card)
        
        # Bar chart card
        self.params_chart_card = ChartCard("Average Parameters by Type")
        self.bar_chart = BarChartWidget()
        self.params_chart_card.set_chart(self.bar_chart)
        charts_row.addWidget(self.params_chart_card)
        
        self.content_layout.addLayout(charts_row)
        
        # =================================================================
        # QUICK ACTIONS - matches web .quick-actions
        # =================================================================
        actions_row = QHBoxLayout()
        actions_row.setSpacing(GRID_GAPS['actions'])  # 16px
        actions_row.setContentsMargins(0, 24, 0, 0)
        
        upload_action = ActionButton("Upload New Data", variant="secondary", icon="fa5s.upload")
        upload_action.clicked.connect(lambda: self.navigate_to.emit("upload"))
        actions_row.addWidget(upload_action)
        
        history_action = ActionButton("View All Datasets", variant="secondary", icon="fa5s.database")
        history_action.clicked.connect(lambda: self.navigate_to.emit("history"))
        actions_row.addWidget(history_action)
        
        # View Detailed Analytics button (for specific dataset mode) - same row
        self.view_analytics_btn = ActionButton(
            "Detailed Analysis",
            variant="secondary",
            icon="fa5s.chart-line"
        )
        self.view_analytics_btn.setVisible(False)
        self.view_analytics_btn.dataset_id = None
        self.view_analytics_btn.clicked.connect(self._on_view_analytics_clicked)
        actions_row.addWidget(self.view_analytics_btn)
        
        actions_row.addStretch()
        
        self.content_layout.addLayout(actions_row)
        self.content_layout.addStretch()
        
        scroll.setWidget(content)
        layout.addWidget(scroll)
    
    def _on_view_analytics_clicked(self) -> None:
        """Handle click on View Detailed Analytics button."""
        if hasattr(self.view_analytics_btn, 'dataset_id') and self.view_analytics_btn.dataset_id:
            # Emit navigation with dataset_id
            self.navigate_to.emit(f"analysis:{self.view_analytics_btn.dataset_id}")
    
    def _on_toggle_changed(self, index: int) -> None:
        """Handle toggle button selection change."""
        self.view_mode = 'combined' if index == 0 else 'specific'
        self.view_combo.setVisible(self.view_mode == 'specific')
        self._load_dashboard()
    
    def refresh(self) -> None:
        """Refresh dashboard data by reloading datasets."""
        self._load_datasets()
    
    def clear_data(self) -> None:
        """Clear all displayed data and reset to initial state."""
        self.datasets = []
        self.view_combo.clear()
        self.total_card.update_value("0")
        self.equip_card.update_value("0")
        self.flowrate_card.update_value("-")
        self.upload_card.update_value("-")
        self.flowrate_summary.update_values("-", "-", "-")
        self.pressure_summary.update_values("-", "-", "-")
        self.temperature_summary.update_values("-", "-", "-")
        self.pie_chart.clear()
        self.bar_chart.clear()
    
    def update_data(
        self,
        datasets: List[Dict[str, Any]],
        analytics: Optional[Dict[str, Any]]
    ) -> None:
        """
        Update dashboard with new datasets and analytics data.
        
        Args:
            datasets: List of dataset dictionaries from API.
            analytics: Dashboard analytics data or None.
        """
        self.datasets = datasets
        
        # Update combo box
        self.view_combo.blockSignals(True)
        self.view_combo.clear()
        self.view_combo.addItem("All Datasets Combined", "combined")
        for ds in datasets:
            name = ds.get('name', 'Unnamed')
            count = ds.get('row_count', 0)
            self.view_combo.addItem(f"{name} ({count} records)", ds['id'])
        self.view_combo.blockSignals(False)
        
        # Update stats
        if analytics:
            self._update_stats(analytics)
            self._update_charts(analytics)
        else:
            self.total_card.update_value(len(datasets))
            self.equip_card.update_value(0)
    
    def _load_datasets(self) -> None:
        """Load datasets from API and populate the selector."""
        try:
            data = self.api_client.get_datasets()
            # API returns {'count': X, 'results': [...]} or list directly
            if isinstance(data, list):
                self.datasets = data
            else:
                self.datasets = data.get('results', [])
            
            self.view_combo.blockSignals(True)
            self.view_combo.clear()
            for ds in self.datasets:
                name = ds.get('name', 'Unnamed')
                count = ds.get('row_count', 0)
                self.view_combo.addItem(f"{name} ({count} records)", ds['id'])
            self.view_combo.blockSignals(False)
            self._load_dashboard()
        except Exception as e:
            print(f"Error loading datasets: {e}")
    
    def _load_dashboard(self) -> None:
        """Load dashboard analytics for the selected dataset view."""
        try:
            if self.view_mode == 'combined':
                data = self.api_client.get_dashboard_analytics()
                if data.get('success', True):
                    self._update_combined_view(data)
            else:
                # Specific dataset view
                data_id = self.view_combo.currentData()
                if data_id:
                    data = self.api_client.get_dataset_analytics(data_id)
                    if data.get('success', True):
                        self._update_specific_view(data, data_id)
        except Exception as e:
            print(f"Error loading dashboard: {e}")
    
    def _update_combined_view(self, data: Dict[str, Any]) -> None:
        """Update view for combined all-datasets mode."""
        # Update stat card labels
        self.total_card.set_label("Total Datasets")
        self.upload_card.set_label("Latest Upload")
        
        # Update values
        datasets_count = data.get('datasets_count', len(self.datasets))
        total_equip = data.get('total_equipment', 0)
        
        self.total_card.update_value(str(datasets_count))
        self.equip_card.update_value(str(total_equip))
        
        summary = data.get('summary', {})
        avgs = summary.get('averages', {}) if summary else {}
        ranges = summary.get('ranges', {}) if summary else {}
        
        flowrate = avgs.get('flowrate', 0)
        self.flowrate_card.update_value(f"{flowrate:.1f}" if flowrate else "-")
        
        # Latest upload date
        if self.datasets:
            from utils.helpers import format_date
            upload_date = format_date(self.datasets[0].get('uploaded_at', ''))
            self.upload_card.update_value(upload_date, small=True)
        else:
            self.upload_card.update_value("-")
        
        # Update section title
        self.analytics_title.setText("Combined Analytics (All Datasets)")
        self.analytics_subtitle.setText(f"Aggregated data from {datasets_count} datasets")
        
        # Update summary cards
        self._update_summary_values(avgs, ranges)
        
        # Update charts
        self._update_charts(data)
        
        # Hide view analytics button
        if hasattr(self, 'view_analytics_btn'):
            self.view_analytics_btn.setVisible(False)
    
    def _update_specific_view(self, data: Dict[str, Any], dataset_id: int) -> None:
        """Update view for specific dataset mode."""
        # Find dataset info
        selected_ds = next((d for d in self.datasets if d.get('id') == dataset_id), None)
        selected_name = selected_ds.get('name', 'Dataset') if selected_ds else 'Dataset'
        
        # Update stat card labels
        self.total_card.set_label("Dataset")
        self.upload_card.set_label("Uploaded At")
        
        # Update values - show dataset name (truncated)
        self.total_card.update_value(selected_name[:15] if len(selected_name) > 15 else selected_name)
        
        summary = data.get('summary', data)
        total_count = summary.get('total_count', 0) if isinstance(summary, dict) else 0
        self.equip_card.update_value(str(total_count))
        
        avgs = summary.get('averages', {}) if isinstance(summary, dict) else {}
        ranges = summary.get('ranges', {}) if isinstance(summary, dict) else {}
        
        flowrate = avgs.get('flowrate', 0)
        self.flowrate_card.update_value(f"{flowrate:.1f}" if flowrate else "-")
        
        # Upload date
        if selected_ds:
            from utils.helpers import format_date
            upload_date = format_date(selected_ds.get('uploaded_at', ''))
            self.upload_card.update_value(upload_date, small=True)
        else:
            self.upload_card.update_value("-")
        
        # Update section title
        self.analytics_title.setText(f"Analytics: {selected_name}")
        self.analytics_subtitle.setText(f"{total_count} equipment records")
        
        # Update summary cards
        self._update_summary_values(avgs, ranges)
        
        # Update charts
        self._update_charts(data)
        
        # Show view analytics button
        if hasattr(self, 'view_analytics_btn'):
            self.view_analytics_btn.setVisible(True)
            self.view_analytics_btn.dataset_id = dataset_id
    
    def _update_stats(self, data: Dict[str, Any]) -> None:
        """Update statistics cards with data."""
        # Top stats cards
        self.total_card.update_value(
            data.get('datasets_count', len(self.datasets))
        )
        self.equip_card.update_value(
            data.get('total_equipment', data.get('total_count', 0))
        )
        
        summary = data.get('summary', data)
        avgs = summary.get('averages', {}) if isinstance(summary, dict) else {}
        ranges = summary.get('ranges', {}) if isinstance(summary, dict) else {}
        
        flowrate = avgs.get('flowrate', 0)
        self.flowrate_card.update_value(
            f"{flowrate:.1f}" if flowrate else "-"
        )
        
        if self.datasets:
            from utils.helpers import format_date
            upload_date = format_date(self.datasets[0].get('uploaded_at', ''))
            self.upload_card.update_value(upload_date, small=True)
        
        # Update analytics section title
        if self.view_mode == 'combined':
            count = data.get('datasets_count', len(self.datasets))
            self.analytics_title.setText("Combined Analytics (All Datasets)")
            self.analytics_subtitle.setText(f"Aggregated data from {count} datasets")
        else:
            selected_name = self.view_combo.currentText().split(" (")[0]
            self.analytics_title.setText(f"Analytics: {selected_name}")
            total_count = summary.get('total_count', 0) if isinstance(summary, dict) else 0
            self.analytics_subtitle.setText(f"{total_count} equipment records")
        
        # Update summary cards
        self._update_summary_values(avgs, ranges)
    
    def _update_summary_values(self, avgs: Dict, ranges: Dict) -> None:
        """Update the summary cards with values from the data."""
        # Iterate over all parameters in the averages dict
        for param, avg_val in avgs.items():
            # Get or create a card for this parameter
            if param not in self.summary_cards:
                # Create a new card for this parameter
                card = SummaryCard(param.capitalize())
                self.summary_cards[param] = card
                self.summary_grid.addWidget(card)
            
            card = self.summary_cards[param]
            range_data = ranges.get(param, {})
            min_val = range_data.get('min', 0) if range_data else 0
            max_val = range_data.get('max', 0) if range_data else 0
            
            card.update_values(
                f"{avg_val:.1f}" if avg_val else "-",
                f"{min_val:.1f}" if min_val else "-",
                f"{max_val:.1f}" if max_val else "-"
            )
    
    def _update_charts(self, data: Dict[str, Any]) -> None:
        """Update charts with analytics data."""
        summary = data.get('summary', data) if isinstance(data, dict) else {}
        chart_data = data.get('chart_data', {}) if isinstance(data, dict) else {}
        
        # Pie chart - type distribution
        dist = summary.get('type_distribution', {}) if isinstance(summary, dict) else {}
        if dist:
            labels = list(dist.keys())
            values = list(dist.values())
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
            avgs = summary.get('averages', {}) if isinstance(summary, dict) else {}
            if avgs:
                params = [key.capitalize() for key in avgs.keys()]
                vals = [avgs.get(key, 0) or 0 for key in avgs.keys()]
                self.bar_chart.update_simple(params, vals)
            else:
                self.bar_chart.clear()
