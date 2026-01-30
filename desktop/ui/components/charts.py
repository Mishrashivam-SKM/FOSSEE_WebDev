"""
Charts Component Module - Matplotlib chart widgets matching React Chart.js UI.

This module provides chart widgets using Matplotlib that match the
web application's Chart.js styling.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import Dict, List, Optional, Any

from PyQt5.QtWidgets import QWidget, QVBoxLayout, QSizePolicy
from PyQt5.QtCore import Qt

import matplotlib
matplotlib.use('Qt5Agg')
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import matplotlib.pyplot as plt

from ui.theme import COLORS, CHART_COLORS, FONT_SIZES
from ui.components.constants import LAYOUT


class PieChartWidget(QWidget):
    """
    Pie chart widget matching web UI Chart.js pie chart.
    
    Displays equipment type distribution with legend on the right.
    
    Args:
        data: Dictionary with 'labels' and 'data' keys.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.chart_data = data
        self._setup_ui()
        
        if data:
            self.update_chart(data)
    
    def _setup_ui(self) -> None:
        """Setup the chart widget."""
        self.setMinimumHeight(LAYOUT['chart_height'])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: white;")
        
        layout.addWidget(self.canvas)
    
    def update_chart(self, data: Dict[str, Any]) -> None:
        """Update the chart with new data."""
        self.chart_data = data
        self.figure.clear()
        
        labels = data.get('labels', [])
        values = data.get('data', [])
        
        if not labels or not values:
            # Show empty state
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=12,
                   color=COLORS['text_muted'])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        # Create pie chart with space for legend
        ax = self.figure.add_subplot(121)  # Left subplot for pie
        
        # Colors for pie slices - match each label to its color
        colors = CHART_COLORS[:len(labels)]
        
        # Create pie
        wedges, texts, autotexts = ax.pie(
            values,
            labels=None,  # We'll use legend instead
            autopct='%1.1f%%',
            colors=colors,
            startangle=90,
            pctdistance=0.75,
            wedgeprops={'linewidth': 2, 'edgecolor': 'white'}
        )
        
        # Style autopct text
        for autotext in autotexts:
            autotext.set_color('white')
            autotext.set_fontsize(9)
            autotext.set_fontweight('bold')
        
        ax.set_title('Equipment Type Distribution', 
                    fontsize=12, fontweight='bold', 
                    color=COLORS['text_primary'], pad=10)
        
        # Create legend in separate area (right side)
        legend_ax = self.figure.add_subplot(122)
        legend_ax.axis('off')
        
        # Create custom legend handles with correct colors matching labels
        from matplotlib.patches import Patch
        legend_handles = [Patch(facecolor=colors[i], edgecolor='white', label=labels[i]) 
                          for i in range(len(labels))]
        
        # Add legend with proper sizing using custom handles
        legend = legend_ax.legend(
            handles=legend_handles,
            title="Equipment Types",
            loc="center",
            fontsize=9,
            title_fontsize=10,
            frameon=True,
            fancybox=True,
            shadow=False,
            borderpad=1
        )
        
        # Adjust layout
        self.figure.subplots_adjust(left=0.05, right=0.95, wspace=0.1)
        self.canvas.draw()
    
    def clear(self) -> None:
        """Clear the chart."""
        self.figure.clear()
        self.canvas.draw()
    
    def update_data(self, labels: List[str], values: List[float]) -> None:
        """
        Update pie chart with simple data format.
        
        Args:
            labels: List of category labels.
            values: List of corresponding values.
        """
        self.update_chart({'labels': labels, 'data': values})


class BarChartWidget(QWidget):
    """
    Bar chart widget matching web UI Chart.js bar chart.
    
    Displays average parameters by equipment type.
    
    Args:
        data: Dictionary with 'labels' and 'datasets' keys.
        x_label: X-axis label.
        y_label: Y-axis label.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        x_label: str = "Equipment Type",
        y_label: str = "Value",
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.chart_data = data
        self.x_label = x_label
        self.y_label = y_label
        
        self._setup_ui()
        
        if data:
            self.update_chart(data)
    
    def _setup_ui(self) -> None:
        """Setup the chart widget."""
        self.setMinimumHeight(LAYOUT['chart_height'])
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(6, 4), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        self.canvas.setStyleSheet("background: white;")
        
        layout.addWidget(self.canvas)
    
    def update_chart(self, data: Dict[str, Any]) -> None:
        """Update the chart with grouped bar data (equipment types on x-axis, parameters as datasets)."""
        self.chart_data = data
        self.figure.clear()
        
        labels = data.get('labels', [])  # Equipment types
        datasets = data.get('datasets', [])  # Parameter datasets (Flowrate, Pressure, Temperature)
        
        if not labels or not datasets:
            # Show empty state
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=12,
                   color=COLORS['text_muted'])
            ax.set_xlim(0, 1)
            ax.set_ylim(0, 1)
            ax.axis('off')
            self.canvas.draw()
            return
        
        import numpy as np
        from matplotlib.patches import Patch
        
        ax = self.figure.add_subplot(111)
        
        # Bar positioning
        x = np.arange(len(labels))
        num_datasets = len(datasets)
        bar_width = 0.8 / max(num_datasets, 1)
        
        # Each dataset (parameter) gets a unique color
        dataset_colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(num_datasets)]
        
        # Plot each dataset with its own consistent color
        for i, dataset in enumerate(datasets):
            offset = (i - num_datasets / 2 + 0.5) * bar_width
            data_values = dataset.get('data', [])
            
            bars = ax.bar(
                x + offset,
                data_values,
                bar_width,
                label=dataset.get('label', f'Dataset {i+1}'),
                color=dataset_colors[i],
                edgecolor='white',
                linewidth=1
            )
        
        # Styling
        ax.set_xlabel(self.x_label, fontsize=11, color=COLORS['text_secondary'])
        ax.set_ylabel(self.y_label, fontsize=11, color=COLORS['text_secondary'])
        ax.set_title('Average Parameters by Equipment Type', 
                    fontsize=12, fontweight='bold',
                    color=COLORS['text_primary'], pad=10)
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10, rotation=45, ha='right')
        
        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Create proper legend with dataset labels and their colors
        legend_handles = [Patch(facecolor=dataset_colors[i], edgecolor='white', 
                                label=datasets[i].get('label', f'Dataset {i+1}')) 
                          for i in range(num_datasets)]
        ax.legend(handles=legend_handles, loc='upper right', fontsize=9)
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['gray_200'])
        ax.spines['bottom'].set_color(COLORS['gray_200'])
        
        # Tick colors
        ax.tick_params(colors=COLORS['text_secondary'])
        
        self.figure.tight_layout()
        self.canvas.draw()
    
    def clear(self) -> None:
        """Clear the chart."""
        self.figure.clear()
        self.canvas.draw()
    
    def update_simple(self, labels: List[str], values: List[float]) -> None:
        """
        Update bar chart with simple data format (single dataset).
        Creates a bar chart where each bar has a different color with proper legend.
        
        Args:
            labels: List of category labels (x-axis).
            values: List of corresponding values (y-axis).
        """
        self.figure.clear()
        
        if not labels or not values:
            ax = self.figure.add_subplot(111)
            ax.text(0.5, 0.5, 'No data available', 
                   ha='center', va='center', fontsize=12,
                   color=COLORS['text_muted'])
            ax.axis('off')
            self.canvas.draw()
            return
        
        import numpy as np
        from matplotlib.patches import Patch
        
        ax = self.figure.add_subplot(111)
        x = np.arange(len(labels))
        
        # Each bar gets a unique color
        bar_colors = [CHART_COLORS[i % len(CHART_COLORS)] for i in range(len(labels))]
        
        # Create bars
        bars = ax.bar(x, values, color=bar_colors, edgecolor='white', linewidth=1)
        
        # Styling
        ax.set_xlabel(self.x_label, fontsize=11, color=COLORS['text_secondary'])
        ax.set_ylabel(self.y_label, fontsize=11, color=COLORS['text_secondary'])
        ax.set_title('Average Parameters', 
                    fontsize=12, fontweight='bold',
                    color=COLORS['text_primary'], pad=10)
        
        ax.set_xticks(x)
        ax.set_xticklabels(labels, fontsize=10, rotation=45, ha='right')
        
        # Grid
        ax.yaxis.grid(True, linestyle='--', alpha=0.3)
        ax.set_axisbelow(True)
        
        # Create legend with correct color-label mapping
        legend_handles = [Patch(facecolor=bar_colors[i], edgecolor='white', label=labels[i]) 
                          for i in range(len(labels))]
        ax.legend(handles=legend_handles, loc='upper right', fontsize=9)
        
        # Style spines
        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_color(COLORS['gray_200'])
        ax.spines['bottom'].set_color(COLORS['gray_200'])
        
        # Tick colors
        ax.tick_params(colors=COLORS['text_secondary'])
        
        self.figure.tight_layout()
        self.canvas.draw()


class MiniPieChart(QWidget):
    """
    Small pie chart for inline display (no legend).
    
    Args:
        data: Dictionary with 'labels' and 'data' keys.
        size: Chart size in pixels.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        data: Optional[Dict[str, Any]] = None,
        size: int = 150,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.chart_data = data
        self.chart_size = size
        
        self._setup_ui()
        
        if data:
            self.update_chart(data)
    
    def _setup_ui(self) -> None:
        """Setup the mini chart widget."""
        self.setFixedSize(self.chart_size, self.chart_size)
        
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        
        # Create matplotlib figure
        self.figure = Figure(figsize=(1.5, 1.5), dpi=100, facecolor='white')
        self.canvas = FigureCanvas(self.figure)
        
        layout.addWidget(self.canvas)
    
    def update_chart(self, data: Dict[str, Any]) -> None:
        """Update the chart with new data."""
        self.chart_data = data
        self.figure.clear()
        
        labels = data.get('labels', [])
        values = data.get('data', [])
        
        if not labels or not values:
            self.canvas.draw()
            return
        
        ax = self.figure.add_subplot(111)
        colors = CHART_COLORS[:len(labels)]
        
        ax.pie(
            values,
            colors=colors,
            startangle=90,
            wedgeprops={'linewidth': 1, 'edgecolor': 'white'}
        )
        
        self.figure.tight_layout(pad=0)
        self.canvas.draw()
