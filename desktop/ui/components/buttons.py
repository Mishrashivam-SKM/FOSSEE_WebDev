"""
Buttons Component Module - Button widgets matching React web UI.

This module provides button components that match the web application's
button styling exactly.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations

from typing import List, Optional, Tuple, Callable

from PyQt5.QtWidgets import (
    QWidget, QPushButton, QHBoxLayout, QVBoxLayout,
    QFrame, QSizePolicy, QLabel
)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont, QCursor

try:
    import qtawesome as qta
    HAS_QTAWESOME = True
except ImportError:
    HAS_QTAWESOME = False

from ui.theme import COLORS, FONT_SIZES, FONT_WEIGHTS, BORDER_RADIUS, SPACING


class ActionButton(QPushButton):
    """
    Styled action button matching web UI button variants.
    
    Supports variants: primary, secondary, danger, success, ghost, view, download, delete
    
    Args:
        text: Button label text.
        icon: QtAwesome icon name (e.g., 'fa5s.upload').
        variant: Button style variant.
        size: Size variant ('sm', 'md', 'lg').
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        text: str,
        icon: Optional[str] = None,
        variant: str = 'primary',
        size: str = 'md',
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.variant = variant
        self.size = size
        self._icon_name = icon
        
        self._setup_button(text, icon)
        self._apply_style()
    
    def _setup_button(self, text: str, icon: Optional[str]) -> None:
        """Setup button text and icon."""
        self.setCursor(QCursor(Qt.PointingHandCursor))
        
        if icon:
            # Check if it's a qtawesome icon name (starts with fa, mdi, ph, ri, msc)
            is_qta_icon = HAS_QTAWESOME and icon.startswith(('fa', 'mdi', 'ph', 'ri', 'msc'))
            if is_qta_icon:
                color = self._get_icon_color()
                self.setIcon(qta.icon(icon, color=color))
                self.setText(text)
            else:
                # Use icon as text prefix (emoji or unicode)
                self.setText(f"{icon}  {text}")
        else:
            self.setText(text)
        
        # Size policy
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Fixed)
    
    def _get_icon_color(self) -> str:
        """Get icon color based on variant."""
        icon_colors = {
            'primary': COLORS['text_light'],
            'secondary': COLORS['text_primary'],
            'danger': COLORS['text_light'],
            'success': COLORS['text_light'],
            'ghost': COLORS['text_secondary'],
            'view': COLORS['primary'],
            'download': COLORS['secondary'],
            'delete': COLORS['danger'],
        }
        return icon_colors.get(self.variant, COLORS['text_light'])
    
    def _apply_style(self) -> None:
        """Apply stylesheet based on variant and size."""
        # Base padding by size
        paddings = {
            'sm': (8, 16),
            'md': (10, 18),
            'lg': (16, 32),
        }
        padding = paddings.get(self.size, paddings['md'])
        
        # Font size by size
        font_sizes = {
            'sm': FONT_SIZES['xs'],
            'md': FONT_SIZES['sm'],
            'lg': FONT_SIZES['md'],
        }
        font_size = font_sizes.get(self.size, FONT_SIZES['sm'])
        
        # Variant-specific styles
        variant_styles = {
            'primary': {
                'bg': COLORS['primary'],
                'bg_hover': COLORS['primary_dark'],
                'color': COLORS['text_light'],
                'border': 'none',
            },
            'secondary': {
                'bg': COLORS['bg_secondary'],
                'bg_hover': COLORS['gray_200'],
                'color': COLORS['text_primary'],
                'border': f"1px solid {COLORS['border']}",
            },
            'danger': {
                'bg': COLORS['danger'],
                'bg_hover': COLORS['danger_light'],
                'color': COLORS['text_light'],
                'border': 'none',
            },
            'success': {
                'bg': COLORS['success'],
                'bg_hover': COLORS['success_light'],
                'color': COLORS['text_light'],
                'border': 'none',
            },
            'ghost': {
                'bg': 'transparent',
                'bg_hover': COLORS['bg_secondary'],
                'color': COLORS['text_secondary'],
                'border': 'none',
            },
            # History page action buttons
            'view': {
                'bg': 'rgba(30, 64, 175, 0.04)',
                'bg_hover': COLORS['primary'],
                'color': COLORS['primary'],
                'color_hover': COLORS['text_light'],
                'border': f"2px solid rgba(30, 64, 175, 0.3)",
                'border_hover': COLORS['primary'],
            },
            'download': {
                'bg': 'rgba(5, 150, 105, 0.04)',
                'bg_hover': COLORS['secondary'],
                'color': COLORS['secondary'],
                'color_hover': COLORS['text_light'],
                'border': f"2px solid rgba(5, 150, 105, 0.3)",
                'border_hover': COLORS['secondary'],
            },
            'delete': {
                'bg': 'rgba(239, 68, 68, 0.04)',
                'bg_hover': COLORS['danger'],
                'color': COLORS['danger'],
                'color_hover': COLORS['text_light'],
                'border': f"2px solid rgba(239, 68, 68, 0.3)",
                'border_hover': COLORS['danger'],
            },
        }
        
        style = variant_styles.get(self.variant, variant_styles['primary'])
        
        # Handle action button variants with color change on hover
        if self.variant in ['view', 'download', 'delete']:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {style['bg']};
                    color: {style['color']};
                    border: {style['border']};
                    border-radius: {BORDER_RADIUS['md']}px;
                    padding: {padding[0]}px {padding[1]}px;
                    font-size: {font_size}px;
                    font-weight: {FONT_WEIGHTS['semibold']};
                }}
                QPushButton:hover {{
                    background: {style['bg_hover']};
                    color: {style.get('color_hover', style['color'])};
                    border: 2px solid {style.get('border_hover', style['bg_hover'])};
                }}
                QPushButton:pressed {{
                    background: {style['bg_hover']};
                }}
                QPushButton:disabled {{
                    opacity: 0.5;
                    background: {style['bg']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {style['bg']};
                    color: {style['color']};
                    border: {style['border']};
                    border-radius: {BORDER_RADIUS['md']}px;
                    padding: {padding[0]}px {padding[1]}px;
                    font-size: {font_size}px;
                    font-weight: {FONT_WEIGHTS['medium']};
                }}
                QPushButton:hover {{
                    background: {style['bg_hover']};
                }}
                QPushButton:pressed {{
                    background: {style['bg_hover']};
                }}
                QPushButton:disabled {{
                    opacity: 0.5;
                }}
            """)
    
    def set_loading(self, loading: bool) -> None:
        """Set loading state with spinner indicator."""
        self.setDisabled(loading)
        if loading:
            self.setText("Loading...")
        else:
            # Restore original text - caller should handle this
            pass


class ToggleButtonGroup(QWidget):
    """
    Toggle button group matching web UI view toggle.
    
    Used for switching between combined/specific dataset views on Dashboard.
    
    Signals:
        selection_changed: Emitted with index when selection changes.
    
    Args:
        options: List of (label, icon) tuples for each button.
        parent: Optional parent widget.
    """
    
    selection_changed = pyqtSignal(int)
    
    def __init__(
        self,
        options: List[Tuple[str, str]],
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.options = options
        self.buttons: List[QPushButton] = []
        self.selected_index = 0
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup the toggle button group UI."""
        self.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['border']};
                border-radius: 10px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(4, 4, 4, 4)
        layout.setSpacing(0)
        
        for i, (label, icon) in enumerate(self.options):
            btn = QPushButton(label)
            btn.setCursor(QCursor(Qt.PointingHandCursor))
            btn.clicked.connect(lambda checked, idx=i: self._on_button_clicked(idx))
            
            # Add icon if available
            if HAS_QTAWESOME and icon:
                btn.setIcon(qta.icon('fa5s.layer-group' if i == 0 else 'fa5s.database'))
            
            self.buttons.append(btn)
            layout.addWidget(btn)
        
        self._update_button_styles()
    
    def _on_button_clicked(self, index: int) -> None:
        """Handle button click."""
        if index != self.selected_index:
            self.selected_index = index
            self._update_button_styles()
            self.selection_changed.emit(index)
    
    def _update_button_styles(self) -> None:
        """Update button styles based on selection."""
        for i, btn in enumerate(self.buttons):
            # Update icon color based on selection
            if HAS_QTAWESOME:
                icon_name = 'fa5s.layer-group' if i == 0 else 'fa5s.database'
                icon_color = COLORS['text_light'] if i == self.selected_index else COLORS['text_secondary']
                btn.setIcon(qta.icon(icon_name, color=icon_color))
            
            if i == self.selected_index:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: {COLORS['primary']};
                        color: {COLORS['text_light']};
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 14px;
                        font-weight: {FONT_WEIGHTS['medium']};
                    }}
                """)
            else:
                btn.setStyleSheet(f"""
                    QPushButton {{
                        background: transparent;
                        color: {COLORS['text_secondary']};
                        border: none;
                        border-radius: 8px;
                        padding: 10px 20px;
                        font-size: 14px;
                        font-weight: {FONT_WEIGHTS['medium']};
                    }}
                    QPushButton:hover {{
                        color: {COLORS['text_primary']};
                    }}
                """)
    
    def set_selection(self, index: int) -> None:
        """Programmatically set the selected button."""
        if 0 <= index < len(self.buttons):
            self.selected_index = index
            self._update_button_styles()


class TabButton(QPushButton):
    """
    Tab button for Analysis page tabs matching web UI.
    
    Args:
        text: Tab label text.
        active: Whether this tab is active.
        parent: Optional parent widget.
    """
    
    def __init__(
        self,
        text: str,
        active: bool = False,
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(text, parent)
        self.active = active
        self.setCursor(QCursor(Qt.PointingHandCursor))
        self._apply_style()
    
    def set_active(self, active: bool) -> None:
        """Set active state and update styling."""
        self.active = active
        self._apply_style()
    
    def _apply_style(self) -> None:
        """Apply style based on active state."""
        if self.active:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: {COLORS['primary']};
                    color: {COLORS['text_light']};
                    border: none;
                    border-radius: {BORDER_RADIUS['lg']}px;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    font-size: {FONT_SIZES['md']}px;
                    font-weight: {FONT_WEIGHTS['semibold']};
                }}
            """)
        else:
            self.setStyleSheet(f"""
                QPushButton {{
                    background: transparent;
                    color: {COLORS['gray_500']};
                    border: none;
                    border-radius: {BORDER_RADIUS['lg']}px;
                    padding: {SPACING['md']}px {SPACING['lg']}px;
                    font-size: {FONT_SIZES['md']}px;
                    font-weight: {FONT_WEIGHTS['semibold']};
                }}
                QPushButton:hover {{
                    background: {COLORS['gray_50']};
                    color: {COLORS['gray_700']};
                }}
            """)


class TabBar(QWidget):
    """
    Tab bar container matching Analysis page tabs.
    
    Signals:
        tab_changed: Emitted with tab id when tab changes.
    
    Args:
        tabs: List of tab dictionaries with 'id' and 'label'.
        parent: Optional parent widget.
    """
    
    tab_changed = pyqtSignal(str)
    
    def __init__(
        self,
        tabs: List[dict],
        parent: Optional[QWidget] = None
    ) -> None:
        super().__init__(parent)
        
        self.tabs = tabs
        self.buttons: dict = {}
        self.active_tab = tabs[0]['id'] if tabs else None
        
        self._setup_ui()
    
    def _setup_ui(self) -> None:
        """Setup tab bar UI matching web .tabs styling."""
        self.setStyleSheet(f"""
            QWidget {{
                background: {COLORS['bg_card']};
                border: 1px solid {COLORS['gray_100']};
                border-radius: {BORDER_RADIUS['xl']}px;
            }}
        """)
        
        layout = QHBoxLayout(self)
        layout.setContentsMargins(SPACING['sm'], SPACING['sm'], SPACING['sm'], SPACING['sm'])
        layout.setSpacing(SPACING['xs'])
        
        for tab in self.tabs:
            btn = TabButton(tab['label'], active=(tab['id'] == self.active_tab))
            btn.clicked.connect(lambda checked, tid=tab['id']: self._on_tab_clicked(tid))
            self.buttons[tab['id']] = btn
            layout.addWidget(btn, 1)  # Equal stretch
    
    def _on_tab_clicked(self, tab_id: str) -> None:
        """Handle tab click."""
        if tab_id != self.active_tab:
            # Deactivate previous
            if self.active_tab and self.active_tab in self.buttons:
                self.buttons[self.active_tab].set_active(False)
            
            # Activate new
            self.active_tab = tab_id
            self.buttons[tab_id].set_active(True)
            
            self.tab_changed.emit(tab_id)
    
    def set_active_tab(self, tab_id: str) -> None:
        """Programmatically set active tab."""
        if tab_id in self.buttons:
            self._on_tab_clicked(tab_id)
