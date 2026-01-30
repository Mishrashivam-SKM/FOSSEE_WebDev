"""
Theme Module - Color palette, typography, spacing matching React web UI.

This module provides all CSS variables from global.css as Python constants
for pixel-perfect matching between web and desktop UIs.

Author: FOSSEE Team
Version: 2.0.0
"""

from __future__ import annotations
from typing import Dict, Any

# =============================================================================
# COLORS - Matching global.css CSS variables exactly
# =============================================================================

COLORS = {
    # Primary - Professional Blue
    'primary': '#2563eb',
    'primary_dark': '#1d4ed8',
    'primary_light': '#3b82f6',
    'primary_bg': '#eff6ff',
    
    # Secondary - Teal
    'secondary': '#0f766e',
    'secondary_dark': '#115e59',
    'secondary_light': '#14b8a6',
    
    # Accent - Amber
    'accent': '#d97706',
    'accent_light': '#f59e0b',
    
    # Danger/Error
    'danger': '#dc2626',
    'danger_light': '#ef4444',
    
    # Success
    'success': '#16a34a',
    'success_light': '#22c55e',
    
    # Warning
    'warning': '#d97706',
    'warning_dark': '#b45309',
    
    # Neutrals - Slate
    'white': '#ffffff',
    'gray_50': '#f8fafc',
    'gray_100': '#f1f5f9',
    'gray_200': '#e2e8f0',
    'gray_300': '#cbd5e1',
    'gray_400': '#94a3b8',
    'gray_500': '#64748b',
    'gray_600': '#475569',
    'gray_700': '#334155',
    'gray_800': '#1e293b',
    'gray_900': '#0f172a',
    
    # Background
    'bg_primary': '#f8fafc',
    'bg_secondary': '#f1f5f9',
    'bg_card': '#ffffff',
    'bg_sidebar': '#1e293b',
    'bg_sidebar_hover': '#334155',
    'bg_sidebar_active': '#2563eb',
    
    # Text
    'text_primary': '#1e293b',
    'text_secondary': '#64748b',
    'text_muted': '#94a3b8',
    'text_light': '#ffffff',
    'text_sidebar': '#e2e8f0',
    
    # Borders
    'border': '#e2e8f0',
    'border_light': '#f1f5f9',
    'border_focus': '#2563eb',
}

# =============================================================================
# TYPOGRAPHY - Font sizes matching CSS variables
# =============================================================================

FONT_SIZES = {
    'xs': 12,      # 0.75rem
    'sm': 13,      # 0.8125rem
    'md': 14,      # 0.875rem
    'lg': 16,      # 1rem
    'xl': 18,      # 1.125rem
    '2xl': 22,     # 1.375rem
    '3xl': 26,     # 1.625rem
    '4xl': 32,     # 2rem
}

FONT_WEIGHTS = {
    'normal': 400,
    'medium': 500,
    'semibold': 600,
    'bold': 700,
}

# =============================================================================
# SPACING - Matching CSS spacing variables (in pixels)
# =============================================================================

SPACING = {
    'xs': 4,       # 0.25rem
    'sm': 8,       # 0.5rem
    'md': 16,      # 1rem
    'lg': 24,      # 1.5rem
    'xl': 28,      # 1.75rem
    '2xl': 40,     # 2.5rem
}

# =============================================================================
# BORDER RADIUS - Matching CSS border-radius variables (in pixels)
# =============================================================================

BORDER_RADIUS = {
    'sm': 3,
    'md': 4,
    'lg': 6,
    'xl': 8,
    'full': 9999,
}

# =============================================================================
# SHADOWS - Matching CSS shadow variables
# =============================================================================

SHADOWS = {
    'sm': '0 1px 2px 0 rgba(0, 0, 0, 0.04)',
    'md': '0 2px 4px -1px rgba(0, 0, 0, 0.06), 0 1px 2px -1px rgba(0, 0, 0, 0.04)',
    'lg': '0 4px 8px -2px rgba(0, 0, 0, 0.08), 0 2px 4px -2px rgba(0, 0, 0, 0.04)',
    'xl': '0 8px 16px -4px rgba(0, 0, 0, 0.1), 0 4px 8px -4px rgba(0, 0, 0, 0.06)',
}

# =============================================================================
# CHART COLORS - For Matplotlib charts
# =============================================================================

CHART_COLORS = [
    '#60a5fa',  # Light Blue
    '#34d399',  # Light Green/Emerald
    '#fbbf24',  # Light Amber/Yellow
    '#f87171',  # Light Red/Coral
    '#a78bfa',  # Light Purple
    '#f472b6',  # Light Pink
    '#2dd4bf',  # Light Teal
    '#fb923c',  # Light Orange
    '#38bdf8',  # Sky Blue
    '#4ade80',  # Light Green
]

CHART_COLORS_RGBA = [
    'rgba(59, 130, 246, 0.8)',   # Blue
    'rgba(16, 185, 129, 0.8)',   # Green
    'rgba(245, 158, 11, 0.8)',   # Amber
    'rgba(239, 68, 68, 0.8)',    # Red
    'rgba(139, 92, 246, 0.8)',   # Purple
    'rgba(236, 72, 153, 0.8)',   # Pink
    'rgba(20, 184, 166, 0.8)',   # Teal
    'rgba(251, 146, 60, 0.8)',   # Orange
]

# =============================================================================
# STAT ICON BACKGROUNDS - For StatCard icons
# =============================================================================

STAT_ICON_COLORS = {
    'database': {
        'bg': 'rgba(59, 130, 246, 0.1)',
        'fg': '#2563eb',
    },
    'activity': {
        'bg': 'rgba(16, 185, 129, 0.1)',
        'fg': '#0f766e',
    },
    'trending': {
        'bg': 'rgba(245, 158, 11, 0.1)',
        'fg': '#d97706',
    },
    'upload': {
        'bg': 'rgba(139, 92, 246, 0.1)',
        'fg': '#8b5cf6',
    },
    'flowrate': {
        'bg': 'rgba(59, 130, 246, 0.1)',
        'fg': '#2563eb',
    },
    'pressure': {
        'bg': 'rgba(16, 185, 129, 0.1)',
        'fg': '#0f766e',
    },
    'temperature': {
        'bg': 'rgba(245, 158, 11, 0.1)',
        'fg': '#d97706',
    },
    'thermometer': {
        'bg': 'rgba(245, 158, 11, 0.1)',
        'fg': '#d97706',
    },
    'droplet': {
        'bg': 'rgba(59, 130, 246, 0.1)',
        'fg': '#2563eb',
    },
}


def get_metrics() -> Dict[str, Any]:
    """
    Get all theme metrics as a dictionary for easy access.
    
    Returns:
        Dictionary containing all theme values.
    """
    return {
        'colors': COLORS,
        'fonts': FONT_SIZES,
        'weights': FONT_WEIGHTS,
        'spacing': SPACING,
        'radius': BORDER_RADIUS,
        'shadows': SHADOWS,
        'chart_colors': CHART_COLORS,
        'stat_icons': STAT_ICON_COLORS,
    }


def get_icon_style(icon_type: str) -> Dict[str, str]:
    """
    Get icon background and foreground colors for a given icon type.
    
    Args:
        icon_type: Type of icon (database, activity, trending, upload, etc.)
        
    Returns:
        Dictionary with 'bg' and 'fg' color values.
    """
    return STAT_ICON_COLORS.get(icon_type, STAT_ICON_COLORS['database'])


# =============================================================================
# STYLESHEET TEMPLATES
# =============================================================================

def get_button_style(variant: str = 'primary') -> str:
    """
    Get button stylesheet for given variant.
    
    Args:
        variant: Button variant (primary, secondary, danger, ghost)
        
    Returns:
        Qt stylesheet string.
    """
    styles = {
        'primary': f"""
            QPushButton {{
                background: {COLORS['primary']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 10px 18px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['primary_dark']};
            }}
            QPushButton:pressed {{
                background: {COLORS['primary_dark']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
                background: {COLORS['gray_400']};
            }}
        """,
        'secondary': f"""
            QPushButton {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
                border: 1px solid {COLORS['border']};
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 10px 18px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['gray_200']};
            }}
            QPushButton:pressed {{
                background: {COLORS['gray_200']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """,
        'danger': f"""
            QPushButton {{
                background: {COLORS['danger']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 10px 18px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['danger_light']};
            }}
            QPushButton:pressed {{
                background: {COLORS['danger_light']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """,
        'success': f"""
            QPushButton {{
                background: {COLORS['success']};
                color: {COLORS['text_light']};
                border: none;
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 10px 18px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['success_light']};
            }}
            QPushButton:pressed {{
                background: {COLORS['success_light']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """,
        'ghost': f"""
            QPushButton {{
                background: transparent;
                color: {COLORS['text_secondary']};
                border: none;
                border-radius: {BORDER_RADIUS['md']}px;
                padding: 10px 18px;
                font-size: {FONT_SIZES['sm']}px;
                font-weight: {FONT_WEIGHTS['medium']};
            }}
            QPushButton:hover {{
                background: {COLORS['bg_secondary']};
                color: {COLORS['text_primary']};
            }}
            QPushButton:pressed {{
                background: {COLORS['bg_secondary']};
            }}
            QPushButton:disabled {{
                opacity: 0.5;
            }}
        """,
    }
    return styles.get(variant, styles['primary'])


def get_input_style() -> str:
    """Get input field stylesheet matching web UI."""
    return f"""
        QLineEdit {{
            width: 100%;
            padding: 12px 16px;
            font-size: {FONT_SIZES['md']}px;
            color: {COLORS['text_primary']};
            background-color: {COLORS['bg_card']};
            border: 2px solid {COLORS['border']};
            border-radius: {BORDER_RADIUS['lg']}px;
        }}
        QLineEdit:focus {{
            border-color: {COLORS['primary']};
        }}
        QLineEdit::placeholder {{
            color: {COLORS['text_muted']};
        }}
        QLineEdit:disabled {{
            background-color: {COLORS['bg_secondary']};
        }}
    """


def get_card_style() -> str:
    """Get card container stylesheet matching web UI."""
    return f"""
        QFrame {{
            background: {COLORS['bg_card']};
            border: 1px solid {COLORS['border']};
            border-radius: {BORDER_RADIUS['xl']}px;
        }}
    """


def get_table_header_style() -> str:
    """Get table header stylesheet matching web UI."""
    return f"""
        QHeaderView::section {{
            background: {COLORS['bg_secondary']};
            font-weight: {FONT_WEIGHTS['semibold']};
            font-size: {FONT_SIZES['sm']}px;
            color: {COLORS['text_secondary']};
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border-bottom: 2px solid {COLORS['border']};
            padding: 16px 20px;
        }}
    """
