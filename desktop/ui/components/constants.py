"""
Constants Module - Layout and grid settings matching React web UI.

Author: FOSSEE Team
Version: 2.0.0
"""

# =============================================================================
# LAYOUT DIMENSIONS - Matching Layout.css exactly
# =============================================================================

LAYOUT = {
    # Sidebar
    'sidebar_width': 220,
    'sidebar_collapsed_width': 64,
    
    # Content area
    'content_padding': 28,
    'max_width_default': 1400,
    'max_width_upload': 800,
    'max_width_history': 1000,
    
    # Page header
    'page_header_margin_bottom': 28,
    'page_header_title_size': 22,
    'page_header_subtitle_size': 13,
    
    # Cards
    'card_padding': 24,
    'card_padding_compact': 18,
    'stat_card_height': 86,
    'stat_icon_size': 48,
    
    # Charts
    'chart_height': 400,
    
    # Table
    'table_cell_padding': 16,
    'table_cell_padding_h': 20,
}

# =============================================================================
# GRID GAPS - Spacing between grid items (in pixels)
# =============================================================================

GRID_GAPS = {
    'stats': 20,       # Gap between stat cards (4 columns)
    'summary': 20,     # Gap between summary cards (3 columns)
    'charts': 24,      # Gap between chart cards (2 columns)
    'actions': 16,     # Gap between action buttons
    'form': 24,        # Gap between form sections
    'list': 16,        # Gap between list items
}

# =============================================================================
# GRID COLUMNS - Number of columns for various grids
# =============================================================================

GRID_COLUMNS = {
    'stats': 4,        # Dashboard stat cards
    'summary': 3,      # Dashboard summary cards
    'charts': 2,       # Chart grid
    'distribution': 6, # Type distribution items (auto-fill)
    'ranges': 4,       # Parameter ranges table columns
}

# =============================================================================
# NAVIGATION ITEMS - Matching Layout.jsx sidebar
# =============================================================================

NAV_ITEMS = [
    {
        'id': 'dashboard',
        'label': 'Dashboard',
        'icon': 'fa5s.home',
        'route': '/',
    },
    {
        'id': 'upload',
        'label': 'Upload Data',
        'icon': 'fa5s.upload',
        'route': '/upload',
    },
    {
        'id': 'history',
        'label': 'History',
        'icon': 'fa5s.clock',
        'route': '/history',
    },
]

# =============================================================================
# TAB DEFINITIONS - For Analysis page
# =============================================================================

ANALYSIS_TABS = [
    {'id': 'overview', 'label': 'Overview'},
    {'id': 'charts', 'label': 'Charts'},
    {'id': 'data', 'label': 'Data Table'},
]

# =============================================================================
# TABLE COLUMNS - Equipment table columns matching Analysis.jsx
# =============================================================================

EQUIPMENT_COLUMNS = [
    {'key': 'name', 'label': 'Equipment Name', 'width': 0.25},
    {'key': 'type', 'label': 'Type', 'width': 0.15},
    {'key': 'flowrate', 'label': 'Flowrate', 'width': 0.20, 'format': 'number'},
    {'key': 'pressure', 'label': 'Pressure', 'width': 0.20, 'format': 'number'},
    {'key': 'temperature', 'label': 'Temperature', 'width': 0.20, 'format': 'number'},
]

# =============================================================================
# ANIMATION DURATIONS (milliseconds) - Matching CSS transitions
# =============================================================================

TRANSITIONS = {
    'fast': 150,
    'normal': 250,
    'slow': 350,
}
