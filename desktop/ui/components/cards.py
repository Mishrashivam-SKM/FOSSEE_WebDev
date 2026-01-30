"""
Cards Component Module - Card widgets matching React web UI.

This module provides card components for stats, charts, and summaries
that match the web application's styling exactly.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Optional, Any

from PyQt5.QtWidgets import (
    QWidget, QFrame, QVBoxLayout, QHBoxLayout, QLabel,
    QSizePolicy, QGridLayout
)
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS, FONT_SIZES, FONT_WEIGHTS, BORDER_RADIUS, SPACING, get_icon_style
from ui.components.constants import LAYOUT


class StatCard(QFrame):
    """
    Statistics card matching web UI .stat-card styling.
    
    Displays a metric with an icon, label, and value.
    Height: 86px, Icon: 48x48px, 4-column grid with 20px gap.
    
    Args:
        label: Metric label (e.g., "Total Datasets").
        value: Metric value (e.g., "15" or "123.45").
        icon: Icon type for background color (database, activity, trending, upload).
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        label: str,
        value: str = "-",
        icon: str = "database",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.label_text = label
        self.value_text = value
        self.icon_type = icon
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the stat card UI."""
        # Card styling - matching .stat-card
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: {BORDER_RADIUS['xl']}px;
            }}
            QFrame:hover {{
                border-color: {COLORS['gray_300']};
            }}
        """)
        
        # Fixed height matching web
        self.setFixedHeight(LAYOUT['stat_card_height'])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(20, 18, 20, 18)  # padding: 18px 20px
        layout.setSpacing(14)  # gap: 14px
        
        # Icon container - 48x48px
        icon_style = get_icon_style(self.icon_type)
        icon_container = QFrame()
        icon_container.setFixedSize(LAYOUT['stat_icon_size'], LAYOUT['stat_icon_size'])
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: {icon_style['bg']};
                border-radius: {BORDER_RADIUS['xl']}px;
                border: none;
            }}
        """)
        
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        # Icon label (using QtAwesome or emoji fallback)
        icon_label = QLabel()
        icon_label.setAlignment(Qt.AlignCenter)
        
        if HAS_QTAWESOME:
            icon_map = {
                'database': 'fa5s.database',
                'activity': 'fa5s.chart-line',
                'trending': 'fa5s.chart-line',
                'upload': 'fa5s.upload',
                'flowrate': 'fa5s.tint',
                'pressure': 'fa5s.tachometer-alt',
                'temperature': 'fa5s.thermometer-half',
                'thermometer': 'fa5s.thermometer-half',
                'droplet': 'fa5s.tint',
            }
            icon_name = icon_map.get(self.icon_type, 'fa5s.chart-bar')
            icon_widget = qta.IconWidget(icon_name, color=icon_style['fg'])
            icon_widget.setIconSize(22)
            icon_layout.addWidget(icon_widget)
        else:
            # Fallback to emoji
            emoji_map = {
                'database': '📊',
                'activity': '📈',
                'trending': '📈',
                'upload': '⬆️',
                'flowrate': '💧',
                'pressure': '🔧',
                'temperature': '🌡️',
            }
            icon_label.setText(emoji_map.get(self.icon_type, '📊'))
            icon_label.setStyleSheet(f"font-size: 20px; color: {icon_style['fg']};")
            icon_layout.addWidget(icon_label)
        
        layout.addWidget(icon_container)
        
        # Content container
        content = QWidget()
        content.setStyleSheet("background: transparent; border: none;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)
        content_layout.setSpacing(2)  # gap: 2px
        
        # Label - 13px, font-weight 500
        self.label_widget = QLabel(self.label_text)
        self.label_widget.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            font-weight: {FONT_WEIGHTS['medium']};
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(self.label_widget)
        
        # Value - 28px, font-weight 700
        self.value_widget = QLabel(self.value_text)
        self.value_widget.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 28px;
            font-weight: {FONT_WEIGHTS['bold']};
            background: transparent;
            border: none;
        """)
        content_layout.addWidget(self.value_widget)
        
        layout.addWidget(content, 1)
    
    def set_value(self, value: str) -> None:
        """Update the displayed value."""
        self.value_text = value
        self.value_widget.setText(value)
    
    def update_value(self, value: Any, small: bool = False) -> None:
        """Update the displayed value (alias for set_value with formatting)."""
        formatted = str(value) if not isinstance(value, str) else value
        self.value_text = formatted
        
        # Auto-adjust font size for long values
        if len(formatted) > 15:
            self._set_font_size(14)
        elif len(formatted) > 10:
            self._set_font_size(18)
        elif small:
            self.set_small_value(formatted)
            return
        else:
            self._set_font_size(28)
        
        self.value_widget.setText(formatted)
    
    def _set_font_size(self, size: int) -> None:
        """Set the value font size."""
        self.value_widget.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {size}px;
            font-weight: {FONT_WEIGHTS['bold']};
            background: transparent;
            border: none;
        """)
    
    def set_label(self, label: str) -> None:
        """Update the displayed label."""
        self.label_text = label
        self.label_widget.setText(label)
    
    def set_small_value(self, value: str) -> None:
        """Set a smaller font size for the value (for dates, etc.)."""
        self.value_widget.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: 14px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            border: none;
        """)
        self.value_widget.setText(value)


class ChartCard(QFrame):
    """
    Chart container card matching web UI .chart-card styling.
    
    Provides a titled container for chart widgets with consistent styling.
    Height: 400px for charts.
    
    Args:
        title: Chart title.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        title: str,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.title_text = title
        self.chart_widget: Optional[QWidget] = None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the chart card UI."""
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: {BORDER_RADIUS['lg']}px;
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(SPACING['lg'], SPACING['lg'], SPACING['lg'], SPACING['lg'])
        self.layout.setSpacing(SPACING['md'])
        
        # Title
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {FONT_SIZES['lg']}px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            border: none;
            padding-bottom: 8px;
            border-bottom: 1px solid {COLORS['border']};
        """)
        self.layout.addWidget(title_label)
        
        # Chart container placeholder
        self.chart_container = QWidget()
        self.chart_container.setMinimumHeight(LAYOUT['chart_height'])
        self.chart_container.setStyleSheet("background: transparent; border: none;")
        self.chart_container_layout = QVBoxLayout(self.chart_container)
        self.chart_container_layout.setContentsMargins(0, 0, 0, 0)
        self.layout.addWidget(self.chart_container)
    
    def set_chart(self, chart_widget: QWidget) -> None:
        """Set the chart widget to display."""
        # Clear existing
        if self.chart_widget:
            self.chart_container_layout.removeWidget(self.chart_widget)
            self.chart_widget.deleteLater()
        
        self.chart_widget = chart_widget
        self.chart_container_layout.addWidget(chart_widget)


class SummaryCard(QFrame):
    """
    Summary card matching web UI .summary-card styling.
    
    Displays parameter summary with average and range values.
    Used in Dashboard for Flowrate/Pressure/Temperature summaries.
    
    Args:
        title: Parameter name (e.g., "Flowrate").
        average: Average value.
        min_val: Minimum value.
        max_val: Maximum value.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        title: str,
        average: str = "-",
        min_val: str = "-",
        max_val: str = "-",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.title_text = title
        self.average = average
        self.min_val = min_val
        self.max_val = max_val
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the summary card UI."""
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 12px;
            }}
            QFrame:hover {{
                border-color: {COLORS['gray_300']};
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)  # padding: 24px
        layout.setSpacing(16)
        
        # Initialize references BEFORE creating rows
        self._avg_value_label: Optional[QLabel] = None
        self._range_value_label: Optional[QLabel] = None
        
        # Title with bottom border
        title_label = QLabel(self.title_text)
        title_label.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {FONT_SIZES['lg']}px;
            font-weight: {FONT_WEIGHTS['bold']};
            background: transparent;
            border: none;
            padding-bottom: 12px;
            border-bottom: 1px solid {COLORS['border']};
        """)
        layout.addWidget(title_label)
        
        # Stats container
        stats_widget = QWidget()
        stats_widget.setStyleSheet("background: transparent; border: none;")
        stats_layout = QVBoxLayout(stats_widget)
        stats_layout.setContentsMargins(0, 0, 0, 0)
        stats_layout.setSpacing(12)
        
        # Average stat
        avg_row = self._create_stat_row("Average", self.average)
        stats_layout.addWidget(avg_row)
        
        # Range stat
        range_val = f"{self.min_val} - {self.max_val}"
        range_row = self._create_stat_row("Range", range_val)
        stats_layout.addWidget(range_row)
        
        layout.addWidget(stats_widget)
    
    def _create_stat_row(self, label: str, value: str) -> QWidget:
        """Create a stat row with label and value."""
        row = QWidget()
        row.setStyleSheet("background: transparent; border: none;")
        
        row_layout = QHBoxLayout(row)
        row_layout.setContentsMargins(0, 0, 0, 0)
        row_layout.setSpacing(8)
        
        label_widget = QLabel(label)
        label_widget.setStyleSheet(f"""
            color: {COLORS['text_secondary']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
            border: none;
        """)
        row_layout.addWidget(label_widget)
        
        row_layout.addStretch()
        
        value_widget = QLabel(value)
        value_widget.setStyleSheet(f"""
            color: {COLORS['text_primary']};
            font-size: {FONT_SIZES['md']}px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            border: none;
        """)
        row_layout.addWidget(value_widget)
        
        # Store reference
        if label == "Average":
            self._avg_value_label = value_widget
        else:
            self._range_value_label = value_widget
        
        return row
    
    def set_values(self, average: str, min_val: str, max_val: str) -> None:
        """Update all values."""
        self.average = average
        self.min_val = min_val
        self.max_val = max_val
        
        if self._avg_value_label:
            self._avg_value_label.setText(average)
        if self._range_value_label:
            self._range_value_label.setText(f"{min_val} - {max_val}")
    
    def update_values(self, average: str, min_val: str, max_val: str) -> None:
        """Update all values (alias for set_values)."""
        self.set_values(average, min_val, max_val)


class DatasetCard(QFrame):
    """
    Dataset card for History page matching web UI .dataset-card styling.
    
    Displays dataset info with View, PDF, and Delete action buttons.
    
    Args:
        dataset: Dataset dictionary with id, name, row_count, uploaded_at.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        dataset: dict,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.dataset = dataset
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the dataset card UI."""
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: {BORDER_RADIUS['lg']}px;
            }}
            QFrame:hover {{
                border-color: {COLORS['gray_200']};
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING['lg'], SPACING['xl'], SPACING['xl'], SPACING['lg'])
        layout.setSpacing(SPACING['lg'])
        
        # Left side - Icon + Details
        info_widget = QWidget()
        info_widget.setStyleSheet("background: transparent; border: none;")
        info_layout = QHBoxLayout(info_widget)
        info_layout.setContentsMargins(0, 0, 0, 0)
        info_layout.setSpacing(SPACING['lg'])
        
        # Icon container - 48x48px
        icon_container = QFrame()
        icon_container.setFixedSize(48, 48)
        icon_container.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['primary_bg']};
                border-radius: {BORDER_RADIUS['md']}px;
                border: none;
            }}
        """)
        
        icon_layout = QHBoxLayout(icon_container)
        icon_layout.setContentsMargins(0, 0, 0, 0)
        icon_layout.setAlignment(Qt.AlignCenter)
        
        if HAS_QTAWESOME:
            icon_widget = qta.IconWidget('fa5s.database', color=COLORS['primary'])
            icon_widget.setIconSize(20)
            icon_layout.addWidget(icon_widget)
        else:
            icon_label = QLabel("📊")
            icon_label.setStyleSheet(f"font-size: 20px; color: {COLORS['primary']};")
            icon_layout.addWidget(icon_label)
        
        info_layout.addWidget(icon_container)
        
        # Details
        details_widget = QWidget()
        details_widget.setStyleSheet("background: transparent; border: none;")
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(0, 0, 0, 0)
        details_layout.setSpacing(SPACING['xs'])
        
        # Dataset name
        name_label = QLabel(self.dataset.get('name', 'Unnamed Dataset'))
        name_label.setStyleSheet(f"""
            color: {COLORS['gray_900']};
            font-size: {FONT_SIZES['lg']}px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            border: none;
        """)
        details_layout.addWidget(name_label)
        
        # Meta info
        row_count = self.dataset.get('row_count', 0)
        uploaded_at = self.dataset.get('uploaded_at', '')
        
        # Format date if needed
        if uploaded_at:
            try:
                from datetime import datetime
                if 'T' in uploaded_at:
                    dt = datetime.fromisoformat(uploaded_at.replace('Z', '+00:00'))
                    uploaded_at = dt.strftime('%b %d, %Y at %I:%M %p')
            except:
                pass
        
        meta_label = QLabel(f"{row_count} equipment records  •  Uploaded {uploaded_at}")
        meta_label.setStyleSheet(f"""
            color: {COLORS['gray_500']};
            font-size: {FONT_SIZES['sm']}px;
            background: transparent;
            border: none;
        """)
        details_layout.addWidget(meta_label)
        
        info_layout.addWidget(details_widget, 1)
        layout.addWidget(info_widget, 1)
        
        # Actions will be added by parent widget
        self.actions_layout = QHBoxLayout()
        self.actions_layout.setSpacing(SPACING['sm'])
        layout.addLayout(self.actions_layout)
    
    def add_action(self, button: 'ActionButton') -> None:
        """Add an action button to the card."""
        self.actions_layout.addWidget(button)


class DistributionItem(QFrame):
    """
    Distribution item card for Analysis page type distribution.
    
    Displays equipment type with count and percentage.
    
    Args:
        type_name: Equipment type name.
        count: Number of equipment of this type.
        total: Total equipment count for percentage calculation.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        type_name: str,
        count: int,
        total: int,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.type_name = type_name
        self.count = count
        self.percentage = (count / total * 100) if total > 0 else 0
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the distribution item UI."""
        self.setStyleSheet(f"""
            QFrame {{
                background: {COLORS['gray_50']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: {BORDER_RADIUS['md']}px;
            }}
            QFrame:hover {{
                border-color: {COLORS['gray_200']};
            }}
        """)
        
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(SPACING['md'], SPACING['md'], SPACING['md'], SPACING['md'])
        layout.setSpacing(4)
        
        # Type name
        type_label = QLabel(self.type_name)
        type_label.setStyleSheet(f"""
            color: {COLORS['gray_700']};
            font-size: {FONT_SIZES['sm']}px;
            font-weight: {FONT_WEIGHTS['medium']};
            background: transparent;
            border: none;
        """)
        layout.addWidget(type_label)
        
        # Count
        count_label = QLabel(str(self.count))
        count_label.setStyleSheet(f"""
            color: {COLORS['primary']};
            font-size: {FONT_SIZES['xl']}px;
            font-weight: {FONT_WEIGHTS['semibold']};
            background: transparent;
            border: none;
        """)
        layout.addWidget(count_label)
        
        # Percentage
        percent_label = QLabel(f"{self.percentage:.1f}%")
        percent_label.setStyleSheet(f"""
            color: {COLORS['gray_500']};
            font-size: {FONT_SIZES['xs']}px;
            background: transparent;
            border: none;
        """)
        layout.addWidget(percent_label)
